#!/usr/bin/env python3
"""
Free My TV for webOS - Build Script
Packages the webOS application into a distributable .ipk file
"""

import os
import sys
import json
import shutil
import subprocess

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(REPO_DIR, "app")
# Allow deployment to build into a temporary directory without modifying
# the repository's tracked dist/ IPK (important for scheduled git pulls).
DIST_DIR = os.environ.get("FMTV_DIST_DIR", os.path.join(REPO_DIR, "dist"))

def read_appinfo():
    with open(os.path.join(APP_DIR, "appinfo.json"), "r", encoding="utf-8") as f:
        info = json.load(f)
    return info["id"], info["version"]

def ipk_filename(app_id, version):
    return f"{app_id}_{version}_all.ipk"

def _fix_ipk_timestamps(ipk_path):
    """Rewrite epoch-zero mtimes inside control.tar.gz/data.tar.gz.

    ares-package (current @webosose/ares-cli lineage, including the 2.4.0
    used here) bakes 1970-01-01 mtimes into every tar entry it writes.
    webOS 5.x's on-device pkgverifier shells out to tar to extract those
    archives, and treats GNU tar's "implausibly old time stamp" warning on
    epoch-zero entries as a fatal error ("-5: ipk verified failed"), even
    though older webOS versions installed the exact same package fine.
    Rewriting every entry's mtime to the build time avoids the warning
    without depending on ares-package (or any other tool) fixing it upstream.
    """
    import tarfile
    import io
    import time

    with open(ipk_path, "rb") as f:
        raw = f.read()
    if raw[:8] != b"!<arch>\n":
        return  # Not a standard ar archive; leave untouched.

    now = int(time.time())
    offset = 8
    entries = []
    while offset < len(raw):
        header = raw[offset:offset + 60]
        if len(header) < 60:
            break
        name = header[0:16].decode("ascii").strip()
        size = int(header[48:58].decode("ascii").strip())
        content_start = offset + 60
        content = raw[content_start:content_start + size]
        entries.append((name, content))
        offset = content_start + size
        if offset % 2 == 1:
            offset += 1

    def retar(gz_bytes):
        src = tarfile.open(fileobj=io.BytesIO(gz_bytes), mode="r:gz")
        out_buf = io.BytesIO()
        with tarfile.open(fileobj=out_buf, mode="w:gz") as dst:
            for member in src.getmembers():
                member.mtime = now
                if member.isfile():
                    dst.addfile(member, src.extractfile(member))
                else:
                    dst.addfile(member)
        return out_buf.getvalue()

    with open(ipk_path, "wb") as f:
        f.write(b"!<arch>\n")
        for name, content in entries:
            if name in ("control.tar.gz", "data.tar.gz"):
                content = retar(content)
            hdr = f"{name:<16}{now:<12}{'0':<6}{'0':<6}{'100644':<8}{len(content):<10}`\n".encode("latin1")
            f.write(hdr)
            f.write(content)
            if len(content) % 2 != 0:
                f.write(b"\n")

def build():
    os.makedirs(DIST_DIR, exist_ok=True)
    app_id, version = read_appinfo()
    print(f"[*] Packaging Free My TV from {APP_DIR}...")
    ipk_path = os.path.join(DIST_DIR, ipk_filename(app_id, version))

    # Check if ares-package is available
    has_ares = shutil.which("ares-package") is not None
    built = False
    if has_ares:
        cmd = f'ares-package "{APP_DIR}" -o "{DIST_DIR}"'
        print(f"[*] Running: {cmd}")
        res = subprocess.run(cmd, shell=True)
        if res.returncode == 0:
            built = True
        else:
            print("[!] ares-package failed, trying fallback packager...")

    if built:
        print("[*] Fixing epoch-zero tar timestamps (webOS 5.x install fix)...")
        _fix_ipk_timestamps(ipk_path)
        print(f"[+] Successfully built package in {DIST_DIR}!")
        return True

    # Fallback pure-python packager if ares-package is missing
    print("[*] Using built-in Python IPK packager...")
    import tarfile
    import io

    # Installed-Size (bytes of app files) is required by the webosbrew apps-repo tooling.
    installed_size = sum(os.path.getsize(os.path.join(root, f))
                         for root, _, files in os.walk(APP_DIR) for f in files)
    control_content = f"""Package: {app_id}
Version: {version}
Section: misc
Priority: optional
Installed-Size: {installed_size}
Architecture: all
Maintainer: FreeMyTV
Description: A fast, ad-free 60fps home screen for LG webOS TVs.
"""
    # 1. control.tar.gz
    control_buf = io.BytesIO()
    with tarfile.open(fileobj=control_buf, mode="w:gz") as tar:
        ti = tarfile.TarInfo(name="control")
        ti.size = len(control_content)
        tar.addfile(ti, io.BytesIO(control_content.encode("utf-8")))
    control_bytes = control_buf.getvalue()

    # 2. data.tar.gz
    data_buf = io.BytesIO()
    with tarfile.open(fileobj=data_buf, mode="w:gz") as tar:
        for root, _, files in os.walk(APP_DIR):
            for file in files:
                full_p = os.path.join(root, file)
                rel_p = os.path.relpath(full_p, APP_DIR)
                dest_p = f"/usr/palm/applications/{app_id}/{rel_p.replace(os.sep, '/')}"
                tar.add(full_p, arcname=dest_p)
    data_bytes = data_buf.getvalue()

    # 3. debian-binary
    debian_binary = b"2.0\n"

    # 4. Standard ar archive
    ipk_path = os.path.join(DIST_DIR, ipk_filename(app_id, version))
    with open(ipk_path, "wb") as f:
        f.write(b"!<arch>\n")
        def write_ar_entry(name, data):
            hdr = f"{name:<16}{'0':<12}{'0':<6}{'0':<6}{'100644':<8}{len(data):<10}`\n".encode("latin1")
            f.write(hdr)
            f.write(data)
            if len(data) % 2 != 0:
                f.write(b"\n")
        write_ar_entry("debian-binary", debian_binary)
        write_ar_entry("control.tar.gz", control_bytes)
        write_ar_entry("data.tar.gz", data_bytes)

    _fix_ipk_timestamps(ipk_path)
    print(f"[+] Successfully built fallback IPK: {ipk_path}")
    return True

if __name__ == "__main__":
    build()
