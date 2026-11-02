#!/usr/bin/env python3
"""
Free My TV for webOS - keep the docs/ live preview in sync with app/.

docs/index.html is a verbatim copy of app/index.html (served by GitHub Pages),
and docs/assets/brands mirrors app/assets/brands. Run this after editing the
app; `python scripts/sync_docs.py --check` exits non-zero if they differ (CI).
"""

import filecmp
import os
import shutil
import sys

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(REPO_DIR, "app")
DOCS = os.path.join(REPO_DIR, "docs")


def mirrored_files():
    """Yield (src, dst) pairs that docs/ must mirror from app/."""
    yield os.path.join(APP, "index.html"), os.path.join(DOCS, "index.html")
    # User-supplied artwork is optional; when present it must be mirrored into
    # docs/ so the GitHub Pages preview can display exactly the packaged image.
    for name in ("background.jpg", "background-2.jpg", "background-3.jpg"):
        src = os.path.join(APP, "assets", name)
        if os.path.isfile(src):
            yield src, os.path.join(DOCS, "assets", name)
    brands = os.path.join(APP, "assets", "brands")
    for name in sorted(os.listdir(brands)):
        yield os.path.join(brands, name), os.path.join(DOCS, "assets", "brands", name)


def main(check=False):
    stale = [dst for src, dst in mirrored_files()
             if not os.path.exists(dst) or not filecmp.cmp(src, dst, shallow=False)]
    if check:
        for dst in stale:
            print(f"[!] out of sync: {os.path.relpath(dst, REPO_DIR)}")
        if stale:
            print("    Run: python scripts/sync_docs.py")
        return 1 if stale else 0
    for src, dst in mirrored_files():
        if dst in stale:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            print(f"[+] updated {os.path.relpath(dst, REPO_DIR)}")
    if not stale:
        print("[*] docs/ already in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main(check="--check" in sys.argv[1:]))
