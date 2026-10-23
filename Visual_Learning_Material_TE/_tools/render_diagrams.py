#!/usr/bin/env python3
"""
Render every ```mermaid block found in the Visual_Learning_Material_TE guides
to PNG + SVG, so learners can view the diagrams offline / in print.

Usage:
    python3 render_diagrams.py                     # render all
    python3 render_diagrams.py --check             # validate only, no output files

Requires: npx @mermaid-js/mermaid-cli (invoked via `npx --yes`).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDE_DIR = os.path.dirname(HERE)
IMAGE_DIR = os.path.join(GUIDE_DIR, "images")
BLOCK_RE = re.compile(r"^```mermaid\n(.*?)^```", re.S | re.M)


def extract_blocks():
    files = sorted(
        f for f in os.listdir(GUIDE_DIR) if f.endswith(".md") and f[:1].isdigit()
    )
    blocks = []
    for fn in files:
        base = os.path.splitext(fn)[0]
        text = open(os.path.join(GUIDE_DIR, fn), encoding="utf-8").read()
        for i, body in enumerate(BLOCK_RE.findall(text), 1):
            blocks.append({"md": fn, "name": f"{base}_{i}", "source": body})
    return blocks


def render(mmd_path, out_stem):
    cmd = [
        "npx", "--yes", "@mermaid-js/mermaid-cli@11",
        "-i", mmd_path,
        "-o", out_stem + ".png",
        "-b", "white",
        "-s", "2",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        return False, (proc.stderr or proc.stdout or "unknown error").strip()

    # PNG succeeded -> also emit SVG
    svg = subprocess.run(
        ["npx", "--yes", "@mermaid-js/mermaid-cli@11",
         "-i", mmd_path, "-o", out_stem + ".svg", "-b", "white"],
        capture_output=True, text=True, timeout=300,
    )
    return True, (svg.stderr or "").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate only")
    args = ap.parse_args()

    blocks = extract_blocks()
    print(f"Found {len(blocks)} mermaid blocks\n")

    if not args.check:
        os.makedirs(IMAGE_DIR, exist_ok=True)

    failures = []
    for b in blocks:
        tmpdir = tempfile.mkdtemp(prefix="mmd_")
        mmd_path = os.path.join(tmpdir, b["name"] + ".mmd")
        with open(mmd_path, "w", encoding="utf-8") as fh:
            fh.write(b["source"])

        if args.check:
            cmd = ["npx", "--yes", "@mermaid-js/mermaid-cli@11",
                   "-i", mmd_path, "-o", os.path.join(tmpdir, "out.svg")]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            ok = proc.returncode == 0
            err = "" if ok else (proc.stderr or proc.stdout).strip()
        else:
            ok, err = render(mmd_path, os.path.join(IMAGE_DIR, b["name"]))

        shutil.rmtree(tmpdir, ignore_errors=True)

        status = "OK  " if ok else "FAIL"
        print(f"  [{status}] {b['md']} -> {b['name']}")
        if not ok:
            failures.append((b, err))
            print("        " + err.replace("\n", "\n        ")[:1200])

    print()
    if failures:
        print(f"{len(failures)} block(s) FAILED to render.")
        return 1
    print("All mermaid blocks render cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
