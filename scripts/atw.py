#!/usr/bin/env python3
"""agentic-thesis-writing helper: install the kit into a repository and generate notes.

    python3 atw.py install   --target . [--thesis-dir thesis] [--agent claude] [--template tudelft]
                             [--with-presentation] [--update-kit] [--dry-run]
    python3 atw.py new-note    <chN.S> <slug> [--title "..."] [--target .]
    python3 atw.py new-handoff <slug>         [--title "..."] [--target .]
    python3 atw.py version

Standard library only. The installer never overwrites a user file: a conflicting file is
written as ``<file>.atw.new`` and the exit code is 1. ``--update-kit`` refreshes the files
the kit owns (agents, skills, commands, this script, the thesis scope files) and nothing
else.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

VERSION = "0.1.0"
START = "<!-- agentic-thesis-writing:start -->"
END = "<!-- agentic-thesis-writing:end -->"
GI_START = "# agentic-thesis-writing:start"
GI_END = "# agentic-thesis-writing:end"

SECTION_RE = re.compile(r"^ch\d+(?:\.\d+)?$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def kit_root() -> Path | None:
    """The kit checkout this script lives in, or None when running from an installed copy."""
    here = Path(__file__).resolve().parent.parent
    if (here / "plugin" / "agents").is_dir() and (here / "templates" / "thesis").is_dir():
        return here
    return None


# --------------------------------------------------------------------------------------
# Install
# --------------------------------------------------------------------------------------

@dataclass
class Report:
    created: list[str] = field(default_factory=list)
    identical: list[str] = field(default_factory=list)
    kept: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    merged: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)

    def print(self, dry: bool) -> None:
        tag = "[dry-run] " if dry else ""
        for name, items in (("created", self.created), ("updated (kit file)", self.updated),
                            ("merged", self.merged), ("kept (exists, not kit-owned)", self.kept),
                            ("identical", self.identical), ("CONFLICT (.atw.new written)", self.conflicts)):
            if items:
                print(f"{tag}{name}: {len(items)}")
                for it in items:
                    print(f"  {it}")


class Installer:
    def __init__(self, kit: Path, target: Path, thesis_dir: str, agent: str, template: str,
                 with_presentation: bool, update_kit: bool, dry: bool) -> None:
        self.kit = kit
        self.target = target
        self.thesis_dir = thesis_dir.strip("/").strip("\\")
        self.agent = agent
        self.template = template
        self.with_presentation = with_presentation
        self.update_kit = update_kit
        self.dry = dry
        self.report = Report()
        self.kit_owned: set[Path] = set()

    # -- primitives -----------------------------------------------------------------------

    def rel(self, p: Path) -> str:
        try:
            return p.relative_to(self.target).as_posix()
        except ValueError:
            return p.as_posix()

    def substitute(self, text: str) -> str:
        return text.replace("{{THESIS_DIR}}", self.thesis_dir)

    def copy_file(self, src: Path, dst: Path, *, owned: bool = False, subst: bool = False) -> None:
        if owned:
            self.kit_owned.add(dst)
        data = src.read_bytes()
        if subst:
            data = self.substitute(data.decode("utf-8")).encode("utf-8")
        if dst.exists():
            if dst.read_bytes() == data:
                self.report.identical.append(self.rel(dst))
                return
            if owned and self.update_kit:
                self.report.updated.append(self.rel(dst))
                if not self.dry:
                    dst.write_bytes(data)
                return
            if owned:
                new = dst.with_name(dst.name + ".atw.new")
                self.report.conflicts.append(self.rel(new))
                if not self.dry:
                    new.write_bytes(data)
                return
            self.report.kept.append(self.rel(dst))
            return
        self.report.created.append(self.rel(dst))
        if not self.dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
            if src.suffix in {".sh", ".py"}:
                try:
                    dst.chmod(src.stat().st_mode)
                except OSError:
                    pass

    def copy_tree(self, src_dir: Path, dst_dir: Path, *, owned: bool = False, subst: bool = False,
                  skip: set[str] | None = None) -> None:
        for src in sorted(src_dir.rglob("*")):
            if src.is_dir():
                continue
            relp = src.relative_to(src_dir)
            if skip and relp.as_posix() in skip:
                continue
            if any(part in {"__pycache__", ".pytest_cache"} for part in relp.parts):
                continue
            self.copy_file(src, dst_dir / relp, owned=owned, subst=subst)

    def ensure_dir(self, d: Path) -> None:
        if not d.exists():
            self.report.created.append(self.rel(d) + "/")
            if not self.dry:
                d.mkdir(parents=True, exist_ok=True)

    def merge_block(self, dst: Path, block: str, start: str, end: str, label: str) -> None:
        """Append a marked block to a file, once. Existing blocks are left alone."""
        if dst.exists():
            text = dst.read_text(encoding="utf-8")
            if start in text and end in text:
                self.report.identical.append(f"{self.rel(dst)} ({label} block present)")
                return
            sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
            self.report.merged.append(f"{self.rel(dst)} ({label} block appended)")
            if not self.dry:
                dst.write_text(text + sep + block, encoding="utf-8")
            return
        self.report.created.append(self.rel(dst))
        if not self.dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(block, encoding="utf-8")

    # -- steps ----------------------------------------------------------------------------

    def install_agents(self) -> None:
        plugin = self.kit / "plugin"
        if self.agent in {"claude", "both"}:
            self.copy_tree(plugin / "agents", self.target / ".claude" / "agents", owned=True)
            self.copy_tree(plugin / "skills", self.target / ".claude" / "skills", owned=True)
            self.copy_tree(plugin / "commands", self.target / ".claude" / "commands", owned=True)
        if self.agent in {"codex", "both"}:
            self.copy_tree(plugin / "skills", self.target / ".agents" / "skills", owned=True)
            # Codex has no agents folder; ship the agent definitions as a skill-like folder.
            self.copy_tree(plugin / "agents", self.target / ".agents" / "skills" / "thesis-agents", owned=True)

    def install_thesis(self) -> None:
        if self.template == "none":
            return
        src = self.kit / "templates" / "thesis"
        dst = self.target / self.thesis_dir
        scope_files = {"CLAUDE.md", ".latexmkrc", "figures/README.md"}
        if self.template == "tudelft" and not dst.exists():
            self.copy_tree(src, dst)
            for f in scope_files | {"build.sh", "fetch_assets.sh"}:
                self.kit_owned.add(dst / f)
            return
        if self.template == "tudelft" and dst.exists():
            print(f"note: {self.rel(dst)}/ exists; treating as --template existing")
        for f in sorted(scope_files):
            self.copy_file(src / f, dst / f, owned=True)

    def install_docs(self) -> None:
        self.copy_tree(self.kit / "templates" / "project" / "docs", self.target / "docs")
        self.ensure_dir(self.target / "docs" / "evidence_notes")
        self.ensure_dir(self.target / "docs" / "handoffs")
        self.ensure_dir(self.target / "docs" / "finalizer")

    def install_scripts(self) -> None:
        self.copy_file(self.kit / "scripts" / "atw.py", self.target / "scripts" / "atw.py", owned=True)

    def install_contract(self) -> None:
        block = self.substitute((self.kit / "templates" / "project" / "AGENTS.md").read_text(encoding="utf-8"))
        self.merge_block(self.target / "AGENTS.md", block, START, END, "AGENTS.md")
        if self.agent in {"claude", "both", "claude-plugin"}:
            claude = self.target / "CLAUDE.md"
            if claude.exists():
                text = claude.read_text(encoding="utf-8")
                if re.search(r"^@AGENTS\.md\s*$", text, flags=re.MULTILINE):
                    self.report.identical.append("CLAUDE.md (@AGENTS.md present)")
                else:
                    self.report.merged.append("CLAUDE.md (@AGENTS.md line appended)")
                    if not self.dry:
                        sep = "" if text.endswith("\n") else "\n"
                        claude.write_text(text + sep + "@AGENTS.md\n", encoding="utf-8")
            else:
                self.report.created.append("CLAUDE.md")
                if not self.dry:
                    claude.write_text("@AGENTS.md\n", encoding="utf-8")
        gi_block = self.substitute((self.kit / "templates" / "project" / "gitignore.snippet").read_text(encoding="utf-8"))
        self.merge_block(self.target / ".gitignore", gi_block, GI_START, GI_END, ".gitignore")

    def install_presentation(self) -> None:
        if not self.with_presentation:
            return
        dst = self.target / "presentation"
        self.copy_tree(self.kit / "templates" / "presentation", dst)
        self.kit_owned.add(dst / "CLAUDE.md")
        self.ensure_dir(dst / "storylines")
        self.ensure_dir(dst / "clips")

    def run(self) -> int:
        self.install_agents()
        self.install_thesis()
        self.install_docs()
        self.install_scripts()
        self.install_contract()
        self.install_presentation()
        self.report.print(self.dry)
        if self.report.conflicts:
            print("\nconflicts: merge each .atw.new into its original by hand, then delete it.")
            return 1
        print("\nnext: fill the Project map in AGENTS.md (search for <FILL>), then build the thesis.")
        return 0


# --------------------------------------------------------------------------------------
# Note generators
# --------------------------------------------------------------------------------------

FALLBACK_NOTE = """# Evidence note: {{SECTION}}: {{SLUG}} ({{TITLE}})

- Status: triaged
- Entry point: <D | C | E | B | A>
- Inventory snapshot:
    - <run group>: checkpoint <✓/✗>, results <✓/✗>, figures <✓/✗>
- Identifiers covered: <IDs from the registry, or "none">
- Config keys: <...>
- Tracker keys: <...>
- Run group(s): <...>
- Output path: <full path under the data root>
- Action staged:
    - Batch:  <submit command the user runs>
    - Local:  <exact local command>
- Metrics tracked: <...>
- Result summary:
    - <TBD>
- Plot paths:
    - <none yet>
- Active figures: <none yet>
- Figure compliance: <TBD>
- Reused vs new code:
    - Reused: <...>
    - New:    <...>
- Confounders / limitations:
    - <...>
- Thesis-safe interpretation:
    > <TBD: one hedged paragraph, no speculative numbers>

## Log

- {{DATE}}: created ({{SECTION}}, {{SLUG}}).
"""

FALLBACK_HANDOFF = """# Handoff: {{TITLE}}

- Status: open
- Date: {{DATE}}
- Agents: <researcher | thesis-writer | reviewer | thesis-finalizer | thesis-polisher | user>
- Files to edit: <paths>

## TL;DR

<Three to six lines: what is being done, why, and what the target state is.>

## How to resume

| You are starting at... | Do this |
|---|---|
| Fresh session, nothing executed | Read this file. Run the invocation in *Agent invocations §1*. |
| <observable state> | <next action> |

## The roadmap

| # | Owner | Action | Inputs | Outputs | Gate / risk |
|---|---|---|---|---|---|
| 1 | <agent> | <...> | <...> | <...> | <...> |

## Locked decisions

| D# | Topic | Choice |
|---|---|---|
| D1 | <...> | <...> |

## Agent invocations

### §1. <agent>

```
Read docs/handoffs/{{DATE}}_{{SLUG}}.md end-to-end before doing anything.
START AT STEP 1: <...>. STOP at <...>.
Constraints: scope boundaries per AGENTS.md; no commits.
```

## If something breaks

- **A.** <...>
- **B.** <...> (recommended)

## Files of interest

| File | Role |
|---|---|
| `docs/handoffs/{{DATE}}_{{SLUG}}.md` | this file |

## Changes

- {{DATE}}: created.
"""


def find_template(target: Path, skill: str, name: str) -> str | None:
    candidates = [
        target / ".claude" / "skills" / skill / name,
        target / ".agents" / "skills" / skill / name,
    ]
    kit = kit_root()
    if kit:
        candidates.append(kit / "plugin" / "skills" / skill / name)
    for c in candidates:
        if c.is_file():
            return c.read_text(encoding="utf-8")
    return None


def fill(text: str, **values: str) -> str:
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def cmd_new_note(args: argparse.Namespace) -> int:
    if not SECTION_RE.match(args.section):
        sys.exit(f"error: section must look like ch4 or ch4.2, got {args.section!r}")
    if not SLUG_RE.match(args.slug):
        sys.exit(f"error: slug must be kebab-case, got {args.slug!r}")
    target = Path(args.target).resolve()
    dst = target / "docs" / "evidence_notes" / f"{args.section}_{args.slug}.md"
    if dst.exists():
        sys.exit(f"error: {dst.relative_to(target).as_posix()} exists; supersede with -v2 instead of overwriting")
    template = find_template(target, "evidence-note", "template.md") or FALLBACK_NOTE
    title = args.title or args.slug.replace("-", " ")
    text = fill(template, SECTION=args.section, SLUG=args.slug, TITLE=title,
                DATE=date.today().isoformat())
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    print(dst.relative_to(target).as_posix())
    return 0


def cmd_new_handoff(args: argparse.Namespace) -> int:
    if not SLUG_RE.match(args.slug):
        sys.exit(f"error: slug must be kebab-case, got {args.slug!r}")
    target = Path(args.target).resolve()
    today = date.today().isoformat()
    dst = target / "docs" / "handoffs" / f"{today}_{args.slug}.md"
    if dst.exists():
        sys.exit(f"error: {dst.relative_to(target).as_posix()} exists; update it in place")
    template = find_template(target, "handoff-note", "template.md") or FALLBACK_HANDOFF
    title = args.title or args.slug.replace("-", " ")
    text = fill(template, SLUG=args.slug, TITLE=title, DATE=today)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    print(dst.relative_to(target).as_posix())
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    kit = kit_root()
    if kit is None:
        sys.exit("error: run install from a checkout of the kit "
                 "(git clone --depth 1 https://github.com/NielsterLinden/agentic-thesis-writing)")
    target = Path(args.target).resolve()
    if not target.is_dir():
        sys.exit(f"error: target is not a directory: {target}")
    inst = Installer(kit, target, args.thesis_dir, args.agent, args.template,
                     args.with_presentation, args.update_kit, args.dry_run)
    return inst.run()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("install", help="install the kit into a repository")
    p.add_argument("--target", default=".", help="repository to install into (default: .)")
    p.add_argument("--thesis-dir", default="thesis", help="thesis directory name (default: thesis)")
    p.add_argument("--agent", default="claude",
                   choices=["claude", "claude-plugin", "codex", "both", "none"],
                   help="where the agent files go (default: claude)")
    p.add_argument("--template", default="tudelft", choices=["tudelft", "existing", "none"],
                   help="scaffold the TU Delft template, keep an existing LaTeX project, or none")
    p.add_argument("--with-presentation", action="store_true", help="also create presentation/")
    p.add_argument("--update-kit", action="store_true",
                   help="overwrite kit-owned files (agents, skills, commands, scripts/atw.py, scope files)")
    p.add_argument("--dry-run", action="store_true", help="print the plan; write nothing")
    p.set_defaults(func=cmd_install)

    p = sub.add_parser("new-note", help="create docs/evidence_notes/<chN.S>_<slug>.md")
    p.add_argument("section")
    p.add_argument("slug")
    p.add_argument("--title")
    p.add_argument("--target", default=".")
    p.set_defaults(func=cmd_new_note)

    p = sub.add_parser("new-handoff", help="create docs/handoffs/<date>_<slug>.md")
    p.add_argument("slug")
    p.add_argument("--title")
    p.add_argument("--target", default=".")
    p.set_defaults(func=cmd_new_handoff)

    p = sub.add_parser("version", help="print the kit version")
    p.set_defaults(func=lambda a: print(VERSION) or 0)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
