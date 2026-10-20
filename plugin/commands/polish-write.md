---
description: Sentence- and paragraph-level prose or caption polish; reads the whole chapter, proposes one focused edit at a time. Runs the thesis-polisher in write mode.
argument-hint: <chN | chN.S | path-to-tex> ["quoted instruction, e.g. split the second sentence of 4.2"]
---

Invoke the `thesis-polisher` subagent in **write mode** for `$ARGUMENTS`. If subagents are
unavailable in this tool, read `.claude/agents/thesis-polisher.md` (or the plugin's
`agents/thesis-polisher.md`) and act as that agent yourself.

Procedure:

1. Read `AGENTS.md` and `rules.md` from the writing-rules skill.
2. Read the **entire** target chapter, plus any figure or table the target sentence depends
   on.
3. Make the requested fix (split a sentence, add an explainer, reword, tighten, fix a
   forbidden form) as one focused `Edit` per logical change, so each diff is reviewable on
   its own. Pause after a non-trivial edit.
4. Run the writing-rules linter on the file; fix anything you introduced.
5. Do not build unless asked. End with the files touched and a note on anything that only
   appears after a rebuild.

Hard rules: polish, not restructure (recommend `/finalize-section` for structure);
preserve `\label`, `\cite`, `\ref`, `\includegraphics` verbatim; no dashes, contractions,
sentence-initial FANBOYS; never invent a number; never edit research directories or the
preamble.
