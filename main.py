#!/usr/bin/env python3
"""news-image-20261121 entry program.

Copies the shipped entry.png into the output directory, byte-identically,
on every run. No network, no randomness, no timestamps (standard library only).

Output dir: $MAKEFUN_OUTPUT_DIR (default /output, as the gate expects).
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print(f"copied {SRC} -> {dst}")


if __name__ == "__main__":
    main()
