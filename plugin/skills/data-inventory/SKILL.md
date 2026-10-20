---
name: data-inventory
description: "Inspect what already exists for a set of runs (checkpoints, results, figures) under the data root and recommend the cheapest entry point (D reuse > C recompute > E bespoke > B re-derive > A new run) before any code or job work begins. Always the researcher's first step."
---

# data-inventory

Triage every `/extract-evidence` request by finding out what already exists on disk for the
relevant runs. The cost order is **D > C > E > B > A** (cheapest first); pick the lowest
entry point that answers the question.

## Inputs

- a section identifier (`ch4.2`) and a topic slug (`tokenizer`);
- optionally an explicit run group, tracker group, or directory pattern. If absent, infer it
  from the experiment configs and the identifier registry named in `AGENTS.md`.

## Procedure

1. Resolve the target run directories under the data root (see the Project map for the
   layout: runs, sweeps, reports).
2. For each run, check the existence of:
   - the checkpoint (name from the Project map);
   - the results (the canonical table rows, or per-run result files);
   - a report bundle or already-rendered figures.
3. Build the inventory snapshot and recommend:

| Code | Recommend when |
|---|---|
| **D** reuse | existing figures or tables already answer the question |
| **C** recompute | results exist and a local analysis module covers the metric |
| **E** bespoke | a new analysis is needed on existing artefacts (checkpoints, raw outputs) |
| **B** re-derive | artefacts exist but the derived outputs (inference, post-processing) are missing |
| **A** new run | no artefact exists for the comparison |

## Output

A block to paste into the evidence note's *Inventory snapshot* and *Entry point* fields:

```
Inventory snapshot:
  - <run group>: checkpoint ✓, results ✓, figures ✗
  - <run group>: checkpoint ✓, results ✗
Recommended entry point: C (checkpoints and results exist; needs the comparison plot only)
Rejected: D (no existing figure covers this comparison); E, B, A (not needed)
```

## Hard rules

- Read-only on the data root. Never delete, rename or move.
- Several run groups (a sweep): report each; do not paper over partial coverage.
- If you recommend A, justify why D, C, E and B are insufficient, and name the thesis
  section and argument that needs the run.
- When several directories share a base name and differ only by timestamp, inventory the
  latest and say so.
