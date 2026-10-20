#!/usr/bin/env python3
"""Publication-safety check for this repository (see AGENTS.md, "Publication safety").

Fails (exit 1) on: private paths, cluster host names, usernames other than the credited
author, experiment-tracker URLs, committed media, files over 1 MB, and em or en dashes in
prose files. Standard library only.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_TEXT = [
    (re.compile(r"/afs/|/eos/|/project/atlas|/data/atlas|/user/[a-z]{3,}"), "private path"),
    (re.compile(r"(?<![\w.])/home/[a-z][a-z0-9_-]+(?:/|\b)"), "home-directory path"),
    (re.compile(r"[A-Za-z]:\\Users\\[A-Za-z]"), "Windows user path"),
    (re.compile(r"(?<![\w.])/Users/[a-z][a-z0-9_-]+/"), "macOS user path"),
    (re.compile(r"nikhef|stbc-|stoomboot|lxplus|cern\.ch", re.IGNORECASE), "cluster or host name"),
    (re.compile(r"nterlind", re.IGNORECASE), "username"),
    (re.compile(r"wandb\.ai/|VmlldzoxN"), "experiment-tracker URL"),
]
# The first name may appear only in the credit line or the citation file.
NAME_RE = re.compile(r"\bniels\b", re.IGNORECASE)
NAME_OK = ("Niels ter Linden", "NielsterLinden", 'given-names: "Niels"')

# This script holds the forbidden patterns themselves.
SELF = Path(__file__).resolve()

DASH_RE = re.compile("[–—]")
PROSE_SUFFIXES = {".md", ".tex", ".cls"}
DASH_EXEMPT = set()  # relative posix paths allowed to contain dashes (none at the moment)

MEDIA_FORBIDDEN = {".mp4", ".mov", ".gif", ".pdf", ".avi", ".mkv", ".webm"}
IMAGE_LIMIT = 200 * 1024
SIZE_LIMIT = 1024 * 1024

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", "build", ".venv"}


def tracked_files() -> list[Path]:
    try:
        out = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                             cwd=ROOT, capture_output=True, check=True).stdout
        names = [n for n in out.decode("utf-8").split("\0") if n]
        return [ROOT / n for n in names if (ROOT / n).is_file()]
    except (OSError, subprocess.CalledProcessError):
        files = []
        for p in ROOT.rglob("*"):
            if p.is_file() and not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
                files.append(p)
        return files


def main() -> int:
    problems: list[str] = []
    for path in tracked_files():
        rel = path.relative_to(ROOT).as_posix()
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.resolve() == SELF:
            continue
        size = path.stat().st_size
        if size > SIZE_LIMIT:
            problems.append(f"{rel}: {size / 1024 / 1024:.1f} MB exceeds 1 MB")
        suffix = path.suffix.lower()
        if suffix in MEDIA_FORBIDDEN:
            problems.append(f"{rel}: committed media ({suffix})")
        if suffix in {".png", ".jpg", ".jpeg"} and size > IMAGE_LIMIT:
            problems.append(f"{rel}: image larger than {IMAGE_LIMIT // 1024} KB")
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            for rx, label in FORBIDDEN_TEXT:
                if rx.search(line):
                    problems.append(f"{rel}:{i}: {label}: {line.strip()[:100]}")
            if NAME_RE.search(line) and not any(ok in line for ok in NAME_OK):
                problems.append(f"{rel}:{i}: personal name outside the credit line: {line.strip()[:100]}")
            if suffix in PROSE_SUFFIXES and rel not in DASH_EXEMPT and DASH_RE.search(line):
                problems.append(f"{rel}:{i}: em or en dash in prose: {line.strip()[:100]}")
    if problems:
        print("hygiene: FAIL")
        for p in problems:
            print("  " + p)
        return 1
    print("hygiene: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
