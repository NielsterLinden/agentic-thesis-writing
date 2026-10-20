# Worked example

One complete cycle through the handoff notes, for a fictional thesis section on a
"tokenizer family" factor of a classifier. **Every number here is synthetic** and marked as
such; the shapes of the notes are the real ones.

| File | Kind | Who wrote it | Status |
|---|---|---|---|
| `evidence_notes/ch4.2_tokenizer.md` | evidence note | `researcher`, then `thesis-writer` flipped the status | `interpreted` |
| `handoffs/2026-10-20_ch4-figure-rework.md` | short task handoff | `researcher` → `thesis-writer` | `done` |
| `reviews/ch4.2_review.md` | review | `reviewer` | saved at the user's request |

Read them in that order. Things to notice:

- The evidence note records the entry point and why the costlier ones were rejected, the
  exact command, the full output path, metrics *with* seed counts and spreads, confounders,
  and a hedged interpretation paragraph the writer lifted almost verbatim.
- The `Active figures:` field and the `Plot paths` list were written by `figure-import`;
  the old timestamped directory is still on disk.
- The handoff tells the writer exactly which two lines to change, what changed in the
  figures so the captions can follow, and the constraints; it does not restate the
  results.
- The review cites rule numbers, grades six axes, and ends with a cuts block even though
  the section was short.
