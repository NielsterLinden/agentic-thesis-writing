---
name: thesis-setup
description: Install or update agentic-thesis-writing in the current repository: fetch the kit, run the installer, fill the Project map in AGENTS.md, check the TeX toolchain, build the template once, and run the writing-rules linter. Use when the user asks to set up, install, update or configure the thesis-writing agents.
---

# thesis-setup

The full procedure, with gates and the questions to ask, is
`docs/install/AGENT_INSTALL.md` in the kit:
https://github.com/NielsterLinden/agentic-thesis-writing/blob/main/docs/install/AGENT_INSTALL.md

Follow it phase by phase. The short form:

1. **Ask first** (one message): thesis directory, template, research directories, data
   root, canonical results table, long-job policy, agent tool, presentation, commit
   permission, files not to touch.
2. **Fetch and install:**

   ```bash
   git clone --depth 1 https://github.com/NielsterLinden/agentic-thesis-writing /tmp/atw
   python3 /tmp/atw/scripts/atw.py install --target . --agent claude   # or codex | both | claude-plugin | none
   ```

   The installer copies agents, skills and commands, scaffolds `thesis/` (TU Delft template),
   `docs/evidence_notes/`, `docs/handoffs/`, `docs/finalizer/`, and merges an `AGENTS.md`
   block, a `CLAUDE.md` line and a `.gitignore` block. It never overwrites: conflicts are
   written as `<file>.atw.new` for you to merge by hand.
3. **Fill the Project map** in `AGENTS.md` with the answers from step 1. Search for
   `<FILL>` placeholders; none may remain.
4. **TeX check and first build:** `latexmk --version`, `xelatex --version`,
   `biber --version`; then `cd thesis && latexmk -pdfxe report.tex`. If XeLaTeX is missing,
   `latexmk -pdf report.tex` builds with free fonts. Print install commands for the user
   rather than running long installs.
5. **Lint the scaffold:** `python3 .claude/skills/tudelft-writing-rules/check_writing_rules.py thesis/mainmatter` (or the plugin path) runs clean.
6. **Report:** done, could not do, next step.

Updating later: run the same `install` with `--update-kit` to refresh the kit's own files
(agents, skills, commands, templates' `CLAUDE.md`); your `AGENTS.md`, notes and thesis
content are never touched.
