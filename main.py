#!/usr/bin/env python3
"""Entry point for the news-image-20261124 bounty.

Copies the bundled front-page image (entry.png, drawn by draw.py)
to /output/entry.png. Standard library only, no network, and fully
deterministic: the same input bytes always produce the same output.

Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(HERE, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
