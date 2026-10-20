# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-10-20

### Added

- Seven agents: `researcher`, `thesis-writer`, `reviewer`, `thesis-finalizer`,
  `thesis-polisher`, `writing-rules-checker`, `deck-planner`.
- Nine skills: `evidence-note`, `handoff-note`, `figure-import` (with `figure_import.py`),
  `data-inventory`, `trace-claim`, `latex-build`, `tudelft-writing-rules` (with
  `check_writing_rules.py`), `thesis-to-deck`, `thesis-setup`.
- Eleven commands: `/extract-evidence`, `/draft-section`, `/review-section`,
  `/finalize-section`, `/polish-global`, `/polish-write`, `/polish-plot`, `/build-thesis`,
  `/handoff`, `/check-writing`, `/deck-storyline`.
- Templates: the TU Delft thesis template with font and asset fallbacks, the project
  `AGENTS.md` contract, note folders, a presentation folder.
- `scripts/atw.py` installer and note generators; `scripts/hygiene.py`.
- Documentation: workflow, handoff notes, writing rules, LaTeX, plotting style,
  presentation, adapting; agent and human install guides; a worked example.
- CI: tests and hygiene, plugin validation, a LaTeX build of the template.
