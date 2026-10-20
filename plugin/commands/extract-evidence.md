---
description: Triage and stage (or run) the analysis behind a thesis section, and record it in an evidence note. Runs the researcher agent; never edits the thesis directory.
argument-hint: <chN.S> <slug>
---

Invoke the `researcher` subagent for `$ARGUMENTS` (section identifier and topic slug). If
subagents are unavailable in this tool, read `.claude/agents/researcher.md` (or the plugin's
`agents/researcher.md`) and act as that agent yourself.

Procedure, in order:

1. Read `AGENTS.md` (Project map).
2. Run the `data-inventory` skill against the relevant run group(s) or output directories.
3. Run the `trace-claim` skill for the factor(s) under study.
4. Open or create `docs/evidence_notes/<chN.S>_<slug>.md` from the `evidence-note` skill
   template (`python3 scripts/atw.py new-note <chN.S> <slug>` if the kit's scripts are
   installed).
5. Pick the lowest-cost entry point (D reuse > C recompute > E bespoke > B re-derive > A new
   run) that answers the question.
6. Stage the action **without executing the long-running step**:
   - A, B, and heavy D or E: fill in the job file and print the submit command for the user;
   - C and cheap E: print the exact local command; run it only if it is quick.
7. Update the note's `Status`: `triaged` after step 5; `run-pending` after step 6 if the user
   must execute; `run-complete` only if step 6 already produced the artefacts and
   `data-inventory` confirms them (then import figures with `figure-import`).

Hard rules:

- never edit the thesis directory;
- never run the batch-submit command; print it;
- never run long training or inference on an interactive node;
- never invent a number; metrics come from the canonical results table;
- reuse existing analysis modules before writing new code.

End with: entry point, note path and status, output path, the exact command staged or run,
and the active figure directory if any.
