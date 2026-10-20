---
description: "Write a task handoff note in docs/handoffs/ so that another agent, another session or your future self can resume the current work cold. Uses the handoff-note skill."
argument-hint: "<slug> [\"quoted title\"]"
---

Write a handoff note for the work in progress, using the `handoff-note` skill, for
`$ARGUMENTS` (a kebab-case slug and an optional title).

1. Generate the skeleton: `python3 scripts/atw.py new-handoff <slug> --title "<title>"`
   (or copy `template.md` from the skill folder) into `docs/handoffs/<YYYY-MM-DD>_<slug>.md`.
2. Fill it from the conversation and the files, not from memory of intent:
   - **TL;DR**: what is being done, why, the target state;
   - **How to resume**: a table keyed on *observable* states (a file exists, a note has a
     given `Status`, a staged command has or has not been run) with the exact next action;
   - **The roadmap**: numbered steps, one owner each, inputs, outputs, gate; **user
     checkpoints** in bold where the agent must stop;
   - **Locked decisions**: what was decided, one line each;
   - **Agent invocations**: copy-paste blocks per agent, self-contained, with start step,
     stop conditions, constraints (no commits; scope boundaries) and the shape of the final
     summary;
   - **If something breaks**: known failure modes with options and a recommendation;
   - **Files of interest** and a short **FAQ**.
3. No results in the handoff: point at evidence notes.
4. Set `Status: open` (or `in-progress` if steps already ran) and print the path.

If a handoff for this slug already exists, update it in place and add a line under
*Changes* rather than creating a second file.
