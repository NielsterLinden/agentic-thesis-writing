#!/usr/bin/env python3
"""Promote a figure into the thesis figure tree and record provenance in an evidence note.

Standard library only. Destination layout:

    <thesis>/figures/<chapter>/<YYYYMMDD-HHMMSS>_<slug>/<file>

Existing timestamped directories are never overwritten. The evidence note's
``Active figures:`` line is set to the destination directory and a
``- <destination> ← <source>`` line is appended under its ``Plot paths`` section.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

TIMESTAMP_RE = re.compile(r"^\d{8}-\d{6}$")
CHAPTER_RE = re.compile(r"^ch\d+$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FILENAME_RE = re.compile(r"^ch\d+_")
ACTIVE_RE = re.compile(r"^(\s*-?\s*)Active figures:\s*(.*)$")
PLOT_PATHS_RE = re.compile(r"^(\s*-?\s*)Plot paths:\s*$")
PLOT_PATHS_HEADING_RE = re.compile(r"^#+\s*Plot paths\s*$", re.IGNORECASE)


def posix(p: Path) -> str:
    """Display a path relative to the working directory when it lies inside it."""
    try:
        return p.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return p.as_posix()


def resolve_timestamp(explicit: str | None, note_text: str, chapter: str, slug: str) -> str:
    """Explicit timestamp wins; else reuse the note's active directory for this chapter/slug;
    else now."""
    if explicit:
        if not TIMESTAMP_RE.match(explicit):
            sys.exit(f"error: --timestamp must be YYYYMMDD-HHMMSS, got {explicit!r}")
        return explicit
    for line in note_text.splitlines():
        m = ACTIVE_RE.match(line)
        if not m:
            continue
        value = m.group(2).strip().rstrip("/")
        tail = value.split("/")[-1] if value else ""
        if tail.endswith(f"_{slug}") and f"/{chapter}/" in value + "/":
            ts = tail[: -len(f"_{slug}")]
            if TIMESTAMP_RE.match(ts):
                return ts
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def update_note(note_text: str, dest_dir: str, dest_file: str, src: str) -> str:
    lines = note_text.splitlines()
    out: list[str] = []
    active_done = False
    plot_idx = -1
    for i, line in enumerate(lines):
        m = ACTIVE_RE.match(line)
        if m and not active_done:
            out.append(f"{m.group(1)}Active figures: {dest_dir}/")
            active_done = True
            continue
        out.append(line)
        if PLOT_PATHS_RE.match(line) or PLOT_PATHS_HEADING_RE.match(line):
            plot_idx = len(out) - 1
    if not active_done:
        out.append(f"- Active figures: {dest_dir}/")

    entry = f"- {dest_file} ← {src}"
    if plot_idx == -1:
        out.extend(["", "## Plot paths", "", entry])
        return "\n".join(out) + "\n"

    # Insert after the last existing entry of the Plot paths block.
    insert_at = plot_idx + 1
    indent = "    "
    while insert_at < len(out):
        cand = out[insert_at]
        stripped = cand.strip()
        if stripped.startswith("- ") and (cand.startswith(" ") or cand.startswith("\t") or
                                           PLOT_PATHS_HEADING_RE.match(out[plot_idx])):
            indent = cand[: len(cand) - len(cand.lstrip())]
            insert_at += 1
            continue
        if stripped == "" and insert_at + 1 < len(out) and out[insert_at + 1].strip().startswith("- ") \
                and PLOT_PATHS_HEADING_RE.match(out[plot_idx]):
            insert_at += 1
            continue
        break
    if PLOT_PATHS_HEADING_RE.match(out[plot_idx]):
        indent = ""
    # Drop a "<none yet>" placeholder if it is the only entry.
    block = out[plot_idx + 1 : insert_at]
    if len(block) == 1 and "none yet" in block[0]:
        out[plot_idx + 1] = f"{indent}{entry}"
    else:
        out.insert(insert_at, f"{indent}{entry}")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", nargs="+", required=True, help="source figure file(s)")
    ap.add_argument("--chapter", required=True, help="chapter directory name, e.g. ch4")
    ap.add_argument("--slug", required=True, help="kebab-case topic slug, e.g. tokenizer")
    ap.add_argument("--note", required=True, help="evidence note to update")
    ap.add_argument("--thesis-dir", default="thesis", help="thesis directory (default: thesis)")
    ap.add_argument("--timestamp", help="YYYYMMDD-HHMMSS of the plotting run (default: reuse or now)")
    ap.add_argument("--allow-any-name", action="store_true",
                    help="accept filenames that do not start with ch<N>_")
    ap.add_argument("--dry-run", action="store_true", help="print what would happen; write nothing")
    args = ap.parse_args(argv)

    if not CHAPTER_RE.match(args.chapter):
        sys.exit(f"error: --chapter must look like ch4, got {args.chapter!r}")
    if not SLUG_RE.match(args.slug):
        sys.exit(f"error: --slug must be kebab-case, got {args.slug!r}")

    note_path = Path(args.note)
    if not note_path.is_file():
        sys.exit(f"error: evidence note not found: {note_path}")
    note_text = note_path.read_text(encoding="utf-8")

    sources = [Path(s) for s in args.src]
    for s in sources:
        if not s.is_file():
            sys.exit(f"error: source not found: {s}")
        if not args.allow_any_name and not FILENAME_RE.match(s.name):
            sys.exit(f"error: {s.name!r} does not follow the ch<N>_* naming rule "
                     f"(pass --allow-any-name to override and explain why in the note)")

    ts = resolve_timestamp(args.timestamp, note_text, args.chapter, args.slug)
    dest_dir = Path(args.thesis_dir) / "figures" / args.chapter / f"{ts}_{args.slug}"

    for s in sources:
        dest = dest_dir / s.name
        if dest.exists():
            sys.exit(f"error: refusing to overwrite existing {posix(dest)}; "
                     f"use a new --timestamp for a new run")

    if args.dry_run:
        print(f"[dry-run] would create {posix(dest_dir)}/")
        for s in sources:
            print(f"[dry-run] would copy {posix(s)} -> {posix(dest_dir / s.name)}")
        print(f"[dry-run] would set Active figures: {posix(dest_dir)}/ in {posix(note_path)}")
        return 0

    dest_dir.mkdir(parents=True, exist_ok=True)
    for s in sources:
        shutil.copy2(s, dest_dir / s.name)
        note_text = update_note(note_text, posix(dest_dir), posix(dest_dir / s.name), posix(s))
    note_path.write_text(note_text, encoding="utf-8")

    print(f"Active figures: {posix(dest_dir)}/")
    for s in sources:
        print(f"imported {posix(dest_dir / s.name)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
