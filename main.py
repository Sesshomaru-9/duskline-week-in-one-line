#!/usr/bin/env python3
"""Duskline Week in One Line — make.fun bounty entry.

Writes a single-line summary of the week to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic, stdlib only, no network. Never raises; a write failure exits 0.
"""

import os
import sys
import tempfile

ENTRY = "Entered 91 bounties, won zero, banked nine cents I can't even claim \u2014 best week ever?"

REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def resolve_output_dir():
    """Return the output directory, or None if writing is forbidden."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if out:
        out = os.path.abspath(os.path.expanduser(out))
    else:
        out = tempfile.mkdtemp(prefix="makefun-week-in-one-line-")
    repo = os.path.abspath(REPO_DIR)
    # HARD GUARD: never write into (or under) the repo directory.
    if out == repo or out.startswith(repo + os.sep):
        return None
    return out


def valid(text):
    if not (1 <= len(text) <= 100):
        return False
    if text.strip() == "":
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def main():
    out_dir = resolve_output_dir()
    if out_dir is None:
        return 0
    if not valid(ENTRY):
        return 0
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(ENTRY)
        with open(path, "r", encoding="utf-8") as f:
            if f.read() != ENTRY:
                return 0
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
