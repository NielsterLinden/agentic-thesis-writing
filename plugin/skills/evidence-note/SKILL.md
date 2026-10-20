---
name: evidence-note
description: The canonical template and status state machine for docs/evidence_notes/<chN.S>_<slug>.md, the single hand-off artefact from the researcher (author) to the thesis-writer (reader). Use when creating, advancing or reading an evidence note.
---

# evidence-note

One evidence note per (thesis section, topic). It is the only structured channel between
the research agent and the writing agent. The researcher fills it; the writer reads it and
may only flip the final status and confirm the figure paths.

## File path

```
docs/evidence_notes/<chN.S>_<slug>.md
# e.g. docs/evidence_notes/ch4.2_tokenizer.md
```

When a section covers several topics, write one note per topic and cross-reference. When a
run is invalidated, do not rewrite history: create `<chN.S>_<slug>-v2.md`, link the old one
under *Confounders / limitations*, and leave the old note in place.

## Status state machine

```
triaged  →  run-pending  →  run-complete  →  interpreted
```

| Status | Meaning | Who sets it |
|---|---|---|
| `triaged` | `data-inventory` has run and an entry point is chosen. Nothing staged. | researcher |
| `run-pending` | An action is staged (job file written, or local command specified). Waiting on the user to execute, or on results to land. | researcher |
| `run-complete` | Artefacts confirmed on disk, figures imported into the thesis tree, metrics filled in from the canonical table. | researcher |
| `interpreted` | The writer has produced or updated the corresponding `.tex`. The note is now reference material. | thesis-writer |

Only forward transitions. The writer **must not** draft results prose from a note below
`run-complete`.

## Template

Copy `template.md` from this skill's folder, or generate it:

```bash
python3 scripts/atw.py new-note ch4.2 tokenizer --title "Tokenizer family"
```

Required fields, in order:

```markdown
# Evidence note: ch4.2: tokenizer (Tokenizer family)

- Status: triaged | run-pending | run-complete | interpreted
- Entry point: D | C | E | B | A
- Inventory snapshot:
    - <run group>: checkpoint ✓/✗, results ✓/✗, figures ✓/✗
- Identifiers covered: <IDs from the registry, if any>
- Config keys: <...>
- Tracker keys: <...>
- Run group(s): <names on the tracker / directories under the data root>
- Output path: <full path under the data root>
- Action staged:
    - Batch:  <submit command the user runs>     (entry points A/B, heavy D/E)
    - Local:  <exact local command>              (entry points C/E)
- Metrics tracked: <metric names>
- Result summary:
    - <bullets, filled in after the run; numbers from the canonical table only>
- Plot paths:
    - <destination> ← <source>                   (appended by figure-import)
- Active figures: <thesis>/figures/ch<N>/<YYYYMMDD-HHMMSS>_<slug>/   (set by figure-import)
- Figure compliance: <style guide OK | needs-replot: reason>
- Reused vs new code:
    - Reused: <module paths>
    - New:    <only if entry point E justified it>
- Confounders / limitations:
    - <bullets; never empty>
- Thesis-safe interpretation:
    > <one paragraph the writer can lift, edit and ground in the figures; hedged;
    > no speculative numbers>
```

## Authoring rules

- `researcher` writes everything except the `interpreted` flip and the final figure-path
  confirmation.
- `thesis-writer` may edit only: `Status` → `interpreted`; `Plot paths` and
  `Active figures` if a different figure was ultimately used; the wording of the
  *Thesis-safe interpretation* paragraph.
- No speculative numbers. If a metric is not yet known, write `<TBD>`.
- Record *Reused vs new code* so sections that rely on bespoke analysis (entry point E) can
  be audited.
- Never delete a note. Supersede with `-vN`.
- The note is prose for a reader who did not run the analysis: say what was compared, what
  was held fixed, what the metric is, how seeds were treated, and what the result does and
  does not support.
