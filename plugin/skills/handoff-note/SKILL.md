---
name: handoff-note
description: Write or read a task handoff note in docs/handoffs/ so that another agent, another session, or your future self can resume multi-step work without re-deriving it. Use at the end of a session, when work crosses an agent boundary, or before any step that needs the user's decision.
---

# handoff-note

An evidence note carries *results* from research to writing. A handoff note carries *work in
progress* across any boundary: between agents, between sessions, or past a point where the
user must decide. It is written for a reader with no memory of the conversation.

## When to write one

- the end of a session with unfinished multi-step work;
- work that the next step hands to a different agent (researcher → writer, writer →
  reviewer, anyone → user);
- before a user checkpoint (a submit command, a destructive step, a decision between
  options);
- a plan long enough that it will outlive one context window.

## File path

```
docs/handoffs/<YYYY-MM-DD>_<slug>.md
# e.g. docs/handoffs/2026-10-20_ch7-figure-rework.md
```

Generate the skeleton:

```bash
python3 scripts/atw.py new-handoff ch7-figure-rework --title "Rework Ch7 figures 7.1 and 7.2"
```

## Structure (see `template.md`)

1. **Header:** title, `Status: open | in-progress | blocked | done`, date, the agent(s)
   involved, the files to edit.
2. **TL;DR:** three to six lines. What is being done and why; the target state.
3. **How to resume:** a table keyed on "you are starting at...". Each row names the state
   you can observe (a file exists, a status is set, a step number) and the exact action to
   take. This is the part a cold reader uses.
4. **The roadmap:** a numbered table: owner, action, inputs, outputs, gate or risk. Mark
   **user checkpoints** in bold; they are the rows where the agent must stop.
5. **Locked decisions:** a table of decisions already taken, with one line each. Decisions
   are revisable; change the table first, then continue.
6. **Agent invocations:** copy-paste blocks, one per agent, self-contained (the agent reads
   this note and the referenced plan; the block does not recap them). State the start step,
   the stop conditions, the constraints (what not to touch, no commits), and the shape of
   the final summary.
7. **If something breaks:** the known failure modes and the options (A/B/C) with a
   recommendation.
8. **Files of interest:** tables of the plan, the inputs, the outputs, the references.
9. **FAQ:** the questions the next reader will ask.

Short handoffs (a single change to wire up) keep sections 1 to 3 and a *Constraints* list;
see `examples/worked-example/handoffs/` in the kit.

## Rules

- **Observable states only** in the resume matrix. "Step 3 complete" is not observable;
  "`docs/evidence_notes/ch7_scaling.md` has `Status: run-complete`" is.
- **Exact paths, exact commands, exact line numbers** where they matter. Line numbers go
  stale; pair them with the text they point at.
- **One owner per step.** A step with two owners is two steps.
- **User checkpoints are explicit** and the agent instructions say "STOP and wait" at
  each.
- **No results in a handoff.** Numbers live in evidence notes; the handoff points at them.
- **Update, do not fork.** When the plan changes, edit the handoff in place and bump the
  date in the header; keep a short *Changes* log at the bottom.
- Set `Status: done` when the work lands; do not delete the note.
