<!-- agentic-thesis-writing:start -->
# Agent operating manual (thesis workflow)

Cross-tool contract for the thesis work in this repository. Two domains, two agent roles,
one channel between them. This file is the human-readable summary; the enforced rules live
in the agent and skill definitions (`.claude/agents/*.md`, `.claude/skills/*/SKILL.md`, or
the `agentic-thesis-writing` plugin). Every agent reads this file first, in particular the
**Project map** at the end.

## Domains

1. **Research**: code, configurations, scripts, job files, data and run outputs. Owned by
   `researcher`.
2. **Thesis**: the LaTeX document in `{{THESIS_DIR}}/`. Owned by `thesis-writer` and the
   late-stage agents.
3. **Presentation** (optional): `presentation/`, the defence-talk plan and clip briefs.
   Owned by `deck-planner`; animations by manim-hep's agents.

## Agents

| Agent | May edit | May not edit | Bash |
|---|---|---|---|
| `researcher` | research directories; `docs/evidence_notes/**` (primary author) | `{{THESIS_DIR}}/**` | inspection, quick local runs; **never the batch-submit command** |
| `thesis-writer` | `{{THESIS_DIR}}/**`; in evidence notes only the `interpreted` flip and figure-path confirmation | research directories | LaTeX build only |
| `reviewer` | nothing | everything | none |
| `thesis-finalizer` | `docs/finalizer/**`; one chapter file at `apply` time; `{{THESIS_DIR}}/mainmatter/_archive/**` | research directories, evidence notes, other thesis files | build, `cp` for archive, a Python splice |
| `thesis-polisher` | `{{THESIS_DIR}}/**`; `.bib` append-only; **plot mode only:** cosmetic edits to plotting code | model code, configs, job files, preamble macros, class file, evidence-note content | build; fast single-figure regeneration |
| `writing-rules-checker` | nothing | everything | the linter only |
| `deck-planner` | `presentation/**` (plan files) | thesis, research directories, evidence notes | inspection |

The boundary is enforced by the allowlists in each agent's definition, not by prose alone.

## Hand-off

The only structured channel between research and writing is an evidence note:

```
docs/evidence_notes/<chN.S>_<slug>.md
```

Status state machine: `triaged → run-pending → run-complete → interpreted`. The researcher
writes everything except the final `interpreted` flip, which the writer owns. The writer
does not draft results prose from a note below `run-complete` and never states a number
that is not in a note.

Work in progress crosses sessions and agents through a handoff note in `docs/handoffs/`
(`/handoff <slug>`), with a resume matrix and copy-paste invocations.

## Workflow

Triage first; never assume a new run is needed.

1. `/extract-evidence <chN.S> <slug>`: `researcher` runs `data-inventory`, picks an entry
   point, stages the action, writes the note.
2. The user executes the staged action (submit command or local command).
3. `/extract-evidence ...` again: `researcher` ingests results, imports figures
   (`figure-import`), fills in the note → `run-complete`.
4. `/draft-section <chN.S> <slug>`: `thesis-writer` drafts or revises the `.tex`, builds,
   flips the note → `interpreted`.
5. `/review-section <path>`: `reviewer` comments (optional, read-only).
6. Late stage: `/finalize-section`, `/polish-write`, `/polish-plot`, `/polish-global`,
   `/check-writing`.
7. `/handoff <slug>` at the end of a session or before a user checkpoint.

## Entry points (cheapest first)

| Code | When | Action |
|---|---|---|
| D reuse | existing figures or tables answer the question | collect and import |
| C recompute | results exist and an analysis module covers the metric | run locally |
| E bespoke | a new analysis on existing artefacts | new script or module; run or stage |
| B re-derive | artefacts exist, derived outputs missing | stage the derivation |
| A new run | nothing exists for the comparison | stage the run; only with a named thesis argument |

## Source-of-truth hierarchy

1. The implementation and configuration that actually ran.
2. The canonical results table (Project map).
3. Tracker exports: cross-reference only.
4. The identifier registry (Project map), if any.
5. Thesis prose: never a source of truth for code or numbers.

## Forbidden habits

- No invented numbers in `.tex`; `\todo{...}` when pending.
- No renaming of identifiers, config keys, figure paths or labels without a deliberate
  cross-cutting pass.
- No background the reader already knows.
- No batch-submit command from any agent; no long jobs on an interactive node.
- No writes outside the per-agent allowlists, even when convenient.
- No deletes or overwrites under the data root. Additive only.
- No figures written directly into `{{THESIS_DIR}}/figures/`; all figures land in a
  timestamped directory via `figure-import`.
- No commits or pushes by agents unless the user says so for a named change.

## Project map

Fill every `<FILL>` once; the agents read this table before acting.

| Key | Value |
|---|---|
| Thesis directory | `{{THESIS_DIR}}/` |
| Main file and build command | `report.tex`; `latexmk -pdfxe report.tex` (run in the thesis directory) |
| Evidence notes | `docs/evidence_notes/` |
| Handoff notes | `docs/handoffs/` |
| Finalizer staging | `docs/finalizer/` |
| Research directories (researcher may edit) | `<FILL: e.g. src/, configs/, scripts/, jobs/>` |
| Data root (outside the repo; additive only) | `<FILL: e.g. /scratch/<user>/project or "none">` |
| Run directory layout | `<FILL: e.g. <data root>/runs/run_<ts>_<name>/ with checkpoint model.pt>` |
| Canonical results table | `<FILL: e.g. results/analysis_ready.csv or "none yet">` |
| Long-job policy | `<FILL: e.g. "sbatch jobs/train.sbatch" (print, never run) or "none; everything runs locally">` |
| Environment activation | `<FILL: e.g. "conda activate thesis" or "none">` |
| Figure staging (where plots are produced) | `<FILL: e.g. <data root>/reports/<run>/figures/>` |
| Plotting style guide | `docs/thesis_style/PLOTTING_STYLE.md` |
| Plotting modules (polisher plot mode may edit) | `<FILL: e.g. src/<pkg>/plots/ or "none">` |
| Identifier registry | `<FILL: e.g. docs/REGISTRY.md or "none">` |
| Writing rules skill | `tudelft-writing-rules` |
| Results-chapter page budget (target / ceiling) | `8 / 12` |
| Reference papers for agents (gitignored) | `<FILL: e.g. agent_reference/ or "none">` |
| Presentation directory | `<FILL: presentation/ or "not installed">` |

## Vocabulary

One canonical term per recurring concept. Add rows as the thesis settles them.

| Concept | Use | Do not use |
|---|---|---|
| spread of a metric across seeds | seed spread | variance, marginal sensitivity |
| difference to the baseline | <metric> delta | <metric> range |
<!-- agentic-thesis-writing:end -->
