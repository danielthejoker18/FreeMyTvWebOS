#!/usr/bin/env python3
"""One-command build and deployment to a rooted TV via webOS CLI.

One-time setup (on your Windows PC):
    npm install -g @webos-tools/cli
    ares-setup-device --add lg-c5 --info "host=YOUR_TV_IP" \
        --info "username=root" --info "port=22" \
        --info "privatekey=PATH_TO_YOUR_SSH_PRIVATE_KEY"

Use:
    py scripts/deploy_rooted.py --device lg-c5 --launch
    py scripts/deploy_rooted.py --device lg-c5 --pull --only-if-changed

With --pull the checkout must be on Custom and clean. SSH keys live on
the PC; this script never sends them to GitHub or stores TV credentials.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(args):
    print("[*] " + " ".join(str(x) for x in args), flush=True)
    subprocess.run([str(x) for x in args], cwd=str(ROOT), check=True)


def capture(args):
    return subprocess.check_output([str(x) for x in args], cwd=str(ROOT), text=True).strip()


def main():
    parser = argparse.ArgumentParser(description="Build and deploy to a rooted webOS TV")
    parser.add_argument("--device", required=True, help="Registered ares device name (e.g. lg-c5)")
    parser.add_argument("--launch", action="store_true", help="Open the launcher after installation (interrupts TV)")
    parser.add_argument("--pull", action="store_true", help="Fast-forward the clean Custom branch before deploying")
    parser.add_argument("--only-if-changed", action="store_true", help="Skip when this Git commit was successfully deployed")
    args = parser.parse_args()

    if args.pull:
        if capture(["git", "branch", "--show-current"]) != "Custom":
            parser.error("--pull requires the Custom branch")
        if capture(["git", "status", "--porcelain"]):
            parser.error("--pull requires a clean checkout; commit any background image first")
        run(["git", "fetch", "origin", "Custom"])
        run(["git", "merge", "--ff-only", "origin/Custom"])

    if not shutil.which("ares-install"):
        parser.error("ares-install not found. Install @webos-tools/cli and register your rooted TV first")

    stamp_name = re.sub(r"[^a-zA-Z0-9_-]", "_", args.device)
    git_dir = Path(capture(["git", "rev-parse", "--git-dir"]))
    if not git_dir.is_absolute():
        git_dir = ROOT / git_dir
    stamp = git_dir / ("freemytv-last-deployed-" + stamp_name)
    sha = capture(["git", "rev-parse", "HEAD"])

    if args.only_if_changed and stamp.exists() and stamp.read_text(encoding="utf-8").strip() == sha:
        print("[+] Already deployed this commit to " + args.device + "; no update necessary")
        return 0

    info = json.loads((ROOT / "app" / "appinfo.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="freemytv-deploy-") as staging:
        # A temporary build avoids changing tracked dist/ and breaking --pull.
        env = os.environ.copy()
        env["FMTV_DIST_DIR"] = staging
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py")],
                       cwd=str(ROOT), env=env, check=True)
        ipk = Path(staging) / (info["id"] + "_" + info["version"] + "_all.ipk")
        if not ipk.is_file():
            raise RuntimeError("Build did not produce " + str(ipk))

        run(["ares-install", "--device", args.device, ipk])
        if args.launch:
            if not shutil.which("ares-launch"):
                raise RuntimeError("ares-launch not found")
            run(["ares-launch", "--device", args.device, info["id"]])
    stamp.write_text(sha + "\n", encoding="utf-8")
    print("[+] Deployed " + info["id"] + " to " + args.device)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (subprocess.CalledProcessError, RuntimeError) as exc:
        print("[!] Deployment failed: " + str(exc), file=sys.stderr)
        sys.exit(1)
