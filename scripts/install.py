#!/usr/bin/env python3
"""
Free My TV for webOS - One-Command Installer
Automates discovery, pairing, and installation onto your LG Smart TV
"""

import os
import sys
import json
import socket
import urllib.request
import subprocess
import shutil
import getpass

# Windows' default console codepage can't encode the emoji in the success
# message below; UTF-8 output works on every platform this script runs on.
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(REPO_DIR, "app", "appinfo.json"), "r", encoding="utf-8") as _f:
    _appinfo = json.load(_f)
APP_ID = _appinfo["id"]
DIST_IPK = os.path.join(REPO_DIR, "dist", f"{APP_ID}_{_appinfo['version']}_all.ipk")

def discover_lg_tv():
    print("[*] Scanning local network for LG webOS TV...")
    msg = (
        'M-SEARCH * HTTP/1.1\r\n'
        'HOST: 239.255.255.250:1900\r\n'
        'MAN: "ssdp:discover"\r\n'
        'MX: 2\r\n'
        'ST: urn:schemas-upnp-org:device:MediaRenderer:1\r\n\r\n'
    ).encode('utf-8')
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(2.5)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    try:
        sock.sendto(msg, ('239.255.255.250', 1900))
        while True:
            data, addr = sock.recvfrom(4096)
            ip = addr[0]
            # Probe dev port 9922
            s = socket.socket()
            s.settimeout(0.3)
            if s.connect_ex((ip, 9922)) == 0:
                s.close()
                sock.close()
                return ip
            s.close()
    except Exception:
        pass
    sock.close()
    return None

def install_app(tv_ip, passphrase=None):
    if not os.path.exists(DIST_IPK):
        print("[!] Package not found. Building first...")
        build_script = os.path.join(REPO_DIR, "scripts", "build.py")
        res = subprocess.run([sys.executable, build_script])
        if res.returncode != 0:
            print("[!] Package build failed.")
            return False

    # Check for OpenSSH client tools
    if not shutil.which("ssh") or not shutil.which("scp"):
        print("[!] Missing required dependency: OpenSSH (ssh / scp)")
        print("    Please install OpenSSH:")
        print("    - On Windows: Settings -> System -> Optional Features -> OpenSSH Client")
        print("    - On macOS: Built-in or 'brew install openssh'")
        print("    - On Linux: sudo apt install openssh-client (or distro equivalent)")
        print("    - On Android (Termux): pkg install openssh")
        return False

    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, exist_ok=True)
    raw_key = os.path.join(ssh_dir, "webos_tv_rsa")
    dec_key = os.path.join(ssh_dir, "webos_tv_rsa_decrypted")

    # Download key from TV if not present
    if not os.path.exists(dec_key):
        if not passphrase:
            passphrase = getpass.getpass(f"Enter the 6-character Passphrase shown in Developer Mode on TV ({tv_ip}): ").strip()

        print(f"[*] Downloading authentication key from http://{tv_ip}:9991/webos_rsa ...")
        try:
            with urllib.request.urlopen(f"http://{tv_ip}:9991/webos_rsa", timeout=5) as resp:
                key_data = resp.read()
                fd = os.open(raw_key, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
                with os.fdopen(fd, "wb") as f:
                    f.write(key_data)
                os.chmod(raw_key, 0o600)
        except Exception as e:
            print(f"[!] Failed to fetch key: {e}")
            print("[!] Make sure 'Key Server' is toggled ON in the Developer Mode app on the TV.")
            return False

        # Decrypt key
        try:
            from cryptography.hazmat.primitives import serialization
        except ImportError:
            print("[!] Missing required dependency: cryptography")
            print("    Please install it using:")
            print("    - On PC/Mac/Linux: pip install cryptography")
            print("    - On Android (Termux): pkg install python-cryptography")
            return False

        key = serialization.load_pem_private_key(key_data, password=passphrase.encode())
        unenc = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        # Private keys must be owner-only: other local users could otherwise read
        # them, and OpenSSH refuses to use a key with group/other permissions.
        fd = os.open(dec_key, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(unenc)
        os.chmod(dec_key, 0o600)
        print("[+] SSH Key saved & decrypted successfully.")

    print(f"[*] Uploading Free My TV to TV ({tv_ip})...")
    # List-form args (no shell=True) throughout: on Windows, shell=True runs
    # the command through cmd.exe regardless of which shell launched Python,
    # and cmd.exe mangles the embedded double quotes in the JSON payloads
    # below before ssh.exe ever sees them. Passing argv as a list sidesteps
    # every local shell's quoting rules; the single remote command string
    # still reaches the TV's real POSIX shell exactly as written.
    # Trust-on-first-use: the TV's host key is recorded on the first connection
    # and a later mismatch at the same IP aborts instead of being ignored.
    known_hosts = os.path.join(ssh_dir, "webos_tv_known_hosts")
    ssh_opts = ["-o", "StrictHostKeyChecking=accept-new", "-o", f"UserKnownHostsFile={known_hosts}", "-o", "HostKeyAlgorithms=+ssh-rsa", "-o", "PubkeyAcceptedKeyTypes=+ssh-rsa"]
    scp_args = ["scp", *ssh_opts, "-P", "9922", "-i", dec_key, DIST_IPK, f"prisoner@{tv_ip}:/media/developer/temp/app.ipk"]
    res = subprocess.run(scp_args)
    if res.returncode != 0:
        print("[!] SCP upload failed.")
        return False

    # Older TVs may require a PTY for luna-send-pub to produce output; other
    # TVs (including some C5 units) explicitly reject forced PTY allocation.
    # Cache the detected capability per TV IP to avoid rejected attempts on
    # subsequent installs. Delete ~/.ssh/webos_tv_pty_support.json to retest.
    pty_cache_file = os.path.join(ssh_dir, "webos_tv_pty_support.json")
    try:
        with open(pty_cache_file, "r", encoding="utf-8") as f:
            pty_support = json.load(f)
        if not isinstance(pty_support, dict):
            pty_support = {}
    except (OSError, ValueError):
        pty_support = {}

    def run_luna(remote_cmd):
        force_pty = pty_support.get(tv_ip, True)
        tty_flags = ["-tt"] if force_pty else ["-T"]
        args = ["ssh", *tty_flags, *ssh_opts, "-p", "9922", "-i", dec_key, f"prisoner@{tv_ip}", remote_cmd]
        res = subprocess.run(args, capture_output=True, text=True)
        if force_pty and "PTY allocation request failed" in (res.stderr or ""):
            pty_support[tv_ip] = False
            try:
                with open(pty_cache_file, "w", encoding="utf-8") as f:
                    json.dump(pty_support, f, indent=2)
            except OSError:
                pass  # Detection still applies to both commands in this run.
            print("[*] TV does not support SSH PTY; using non-interactive commands from now on.")
            res = subprocess.run(["ssh", "-T", *ssh_opts, "-p", "9922", "-i", dec_key, f"prisoner@{tv_ip}", remote_cmd], capture_output=True, text=True)
        return res

    def run_luna_timed(seconds, inner_cmd):
        # BusyBox's timeout only learned the coreutils "timeout DURATION CMD" spelling
        # in 1.30; before that it wanted "-t SECS", and older webOS builds ship the
        # older applet, which tries to execute the duration as a program instead.
        # Try the modern form first, then fall back on that complaint.
        res = run_luna(f"timeout {seconds} {inner_cmd}")
        blob = (res.stdout or "") + (res.stderr or "")
        if "can't execute" in blob or "Unknown option" in blob or "invalid option" in blob:
            print("[*] TV's timeout wants the older -t form; retrying...")
            res = run_luna(f"timeout -t {seconds} {inner_cmd}")
        return res

    print("[*] Installing package on TV...")
    install_payload = json.dumps({"id": APP_ID, "ipkUrl": "/media/developer/temp/app.ipk", "subscribe": True})
    install_res = run_luna_timed(45, f"luna-send-pub -n 30 luna://com.webos.appInstallService/dev/install '{install_payload}'")
    install_out = install_res.stdout
    if '"state":"installed"' not in install_out:
        print("[!] Install did not reach the 'installed' state. Raw output:")
        print(install_out or "(empty)")
        if install_res.stderr:
            print(install_res.stderr)
        return False

    print("[*] Launching Free My TV...")
    launch_payload = json.dumps({"id": APP_ID})
    launch_remote_cmd = f"luna-send-pub -n 1 luna://com.webos.applicationManager/launch '{launch_payload}'"
    launch_res = run_luna(launch_remote_cmd)
    if '"returnValue":true' not in launch_res.stdout:
        print("[!] Install succeeded but launch failed. Raw output:")
        print(launch_res.stdout or "(empty)")
        return False

    print("\n[+] SUCCESS! Free My TV is installed and running on your LG TV! Enjoy! 🎉")
    return True

def confirm(question):
    try:
        return input(f"{question} [y/N]: ").strip().lower() in ("y", "yes")
    except EOFError:
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Install Free My TV on an LG webOS TV.")
    parser.add_argument("ip", nargs="?", help="TV IP address (skips network discovery)")
    parser.add_argument("legacy_passphrase", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("--passphrase-stdin", action="store_true",
                        help="read the Developer Mode passphrase from stdin")
    parser.add_argument("-y", "--yes", action="store_true",
                        help="don't ask to confirm a TV found by network discovery")
    args = parser.parse_args()

    # The passphrase never needs to be on the command line (where `ps` and shell
    # history would expose it): use FMTV_PASSPHRASE, --passphrase-stdin, or the prompt.
    passphrase = os.environ.get("FMTV_PASSPHRASE")
    if args.passphrase_stdin:
        passphrase = sys.stdin.readline().strip()
    elif args.legacy_passphrase:
        print("[!] Passing the passphrase as an argument is deprecated (visible in `ps` and shell history).")
        print("    Use the interactive prompt, FMTV_PASSPHRASE, or --passphrase-stdin instead.")
        passphrase = args.legacy_passphrase

    ip = args.ip
    if not ip:
        ip = discover_lg_tv()
        if ip and not args.yes and not confirm(f"[?] Found a device at {ip}. Install Free My TV on it?"):
            print("[!] Aborted. Re-run with the TV's IP address to choose a device explicitly.")
            sys.exit(1)
        if not ip:
            print("[!] TV not found automatically via SSDP network scan.")
            print("    Make sure your device and TV are on the same Wi-Fi network (not a guest network),")
            print("    and that Developer Mode & Key Server are turned ON.")
            ip = input("Enter TV IP Address (shown in Developer Mode app): ").strip()

    if not ip:
        print("[!] No IP address provided. Aborting.")
        sys.exit(1)

    sys.exit(0 if install_app(ip, passphrase) else 1)
