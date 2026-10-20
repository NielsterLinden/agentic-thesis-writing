---
description: "Draft or revise a thesis section from its evidence note, following the writing rules, and compile. Runs the thesis-writer agent; never edits code, configs or data."
argument-hint: "<chN.S> <slug>"
---

Invoke the `thesis-writer` subagent for `$ARGUMENTS` (section identifier and topic slug).
If subagents are unavailable in this tool, read `.claude/agents/thesis-writer.md` (or the
plugin's `agents/thesis-writer.md`) and act as that agent yourself.

Procedure, in order:

1. Read `AGENTS.md` (Project map) and `rules.md` from the writing-rules skill.
2. Read `docs/evidence_notes/<chN.S>_<slug>.md`. If the note is missing, or its `Status` is
   `triaged` or `run-pending`, **stop** and tell the user to run
   `/extract-evidence <chN.S> <slug>` first.
3. Read the whole chapter file in the thesis directory, plus the chapter intro and the
   previous section.
4. Run `trace-claim` for any design claim; every identifier must exist in the registry.
5. Draft or revise the section into the results-chapter scaffold (Setup with `Lens.`,
   `Factors.`, `Hypothesis.`; Results; Discussion per hypothesis) unless the chapter has an
   established structure. Lift the note's *Thesis-safe interpretation* as the starting
   point; keep its hedges.
6. If a figure is added or replaced, bring it in with `figure-import` and use the
   timestamped path.
7. Run the writing-rules linter on the file; fix the `[MINOR]` items you introduced.
8. Build with the `latex-build` skill and act on the result.
9. Flip the note's `Status` to `interpreted` and confirm the final figure path(s).

Hard rules:

- never edit research directories;
- never invent a number: `<TBD>` in the note becomes `\todo{value pending}` in the text;
- no dashes, contractions, sentence-initial FANBOYS, phrasal verbs, rhetorical questions;
- end with `Build OK.` or `Build FAILED: <cause>` and the list of `.tex` files touched.
