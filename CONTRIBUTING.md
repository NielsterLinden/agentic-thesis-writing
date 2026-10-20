# Contributing

Thanks for helping. This repository is a kit that other people install into their thesis
repositories, so the bar is: generic, small, tested, and safe to publish.

## What is welcome

- **Writing-rule sets** for other universities or fields, as a sibling of
  `plugin/skills/tudelft-writing-rules/` (one `SKILL.md`, one `rules.md`, and linter
  patterns if they differ).
- **LaTeX templates** for other institutions, as a sibling of `templates/thesis/`, with a
  licence file and a working `.latexmkrc`.
- **Agent-tool adapters** (Codex, Cursor, Gemini CLI, ...): an install path in
  `scripts/atw.py` and a section in `docs/ADAPTING.md`.
- **Better checks** in `check_writing_rules.py`, with a test per rule.
- **Fixes to the agents** that make a boundary clearer or a procedure shorter.

## What is not

- Anything that only works for one project (paths, identifiers, cluster commands).
- A new agent when an existing one can take the task with one more paragraph.
- Dependencies for the scripts: they stay standard library.
- Media files, logos, or results from a real thesis.

## Workflow

1. Open an issue or a short discussion first for anything larger than a fix.
2. Branch from `main`. Keep the change surgical.
3. Run the checks listed in `AGENTS.md` ("Checks to run before you say done").
4. Add a line to `CHANGELOG.md` under *Unreleased*.
5. Open a pull request. Describe the check you ran.

By contributing you agree that your contribution is licensed under the MIT licence of this
repository (except for template files, which keep their own licence).
