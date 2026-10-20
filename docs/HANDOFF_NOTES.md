# Handoff notes

The notes are the product. The agents are replaceable; the notes are what makes a
months-long, multi-agent thesis auditable and resumable.

## Why notes

Three facts about agentic work shape the design:

1. **Context windows end.** Anything that lives only in a conversation is lost. A note
   written for a reader with no memory of the conversation is the only durable state.
2. **Scopes are disjoint on purpose.** The researcher cannot write prose; the writer cannot
   run analyses. Work therefore has to cross the boundary as a file, not as an instruction
   in chat.
3. **Numbers must be traceable.** A thesis committee asks "where does this number come
   from?". The answer has to be a path, not a recollection.

## The four kinds

### 1. Evidence note (researcher → writer)

One per thesis section and topic. The researcher fills everything; the writer reads, lifts
the *Thesis-safe interpretation* paragraph, and flips the status. Its load-bearing parts:

- **`Status`**, a state machine with forward-only transitions. The writer may not draft
  results below `run-complete`.
- **Entry point and inventory**: what existed, what was chosen, why the costlier options
  were not needed.
- **Full output path, exact command**: reproducibility.
- **Metrics from the canonical table only**; `<TBD>` until then.
- **Confounders**: never empty.
- **Thesis-safe interpretation**: a hedged paragraph the writer can edit into the chapter's
  voice without inventing.
- **`Active figures:`**: the timestamped directory set by `figure-import`; the `Plot paths`
  list carries `destination ← source` pairs.

Skill: `evidence-note`. Generator: `python3 scripts/atw.py new-note ch4.2 tokenizer`.

### 2. Task handoff (anyone → anyone)

Work in progress, written so that a cold reader can continue. Its load-bearing parts:

- **How to resume**: a table keyed on *observable* states ("the note has
  `Status: run-complete`", "`_pre_label.csv` exists"), each with the exact next action.
- **The roadmap**: numbered steps, one owner each, inputs, outputs, gate; **user
  checkpoints** in bold where the agent must stop.
- **Locked decisions**: a table; change the table first, then continue.
- **Agent invocations**: copy-paste blocks that are self-contained ("Read this file
  end-to-end before doing anything. START AT STEP 3 ... At step 6 run the dry run only.
  STOP and wait.").
- **If something breaks**: options A/B/C with a recommendation.

Skill: `handoff-note`. Command: `/handoff <slug>`. Generator:
`python3 scripts/atw.py new-handoff <slug>`.

### 3. Critique and proposed rewrite (finalizer → you)

A staged pair under `docs/finalizer/ch<N>.<Y>/<timestamp>/`. The critique is a list of
`[SEVERITY/ACTION]` entries against a canonical section template; the rewrite is a drop-in
`.tex` block with every label, citation and figure path preserved. Nothing touches the
chapter until you type `apply`; the old chapter is archived first. The staging directory
is the record of the pass.

### 4. Review (reviewer → writer)

Chat output by default: `[BLOCK] [MAJOR] [MINOR] [NOTE]` findings with location and
suggestion, a *Cuts and condensations* block, a six-axis grade. Ask for it to be saved
under `docs/reviews/` when you want a record.

## Anatomy of a good resume matrix

| Bad row | Good row |
|---|---|
| "Step 3 done → do step 4" | "`docs/evidence_notes/ch8_data_provenance.md` exists with `Status: run-complete` → run the writer invocation in §2" |
| "Figures updated" | "`thesis/figures/ch7/20260601-161946_scaling/` contains two PDFs and the note's `Active figures:` points at it → update the two `\includegraphics` paths at lines 85 and 101 of `07_scaling.tex`" |
| "Ask the user" | "**USER checkpoint 6b:** review the printed dry-run diff; say `go` to execute the push" |

The test: could a different agent, with a fresh context, start from the row without
asking you anything?

## Anti-patterns

- **Results in the handoff.** A number in a handoff goes stale and has no provenance. Point
  at the note.
- **Vague stop conditions.** "Ask before doing anything risky" is not a checkpoint. Name
  the step.
- **Two owners per step.** Split it.
- **Rewriting the plan in chat.** Edit the note first; the chat is not durable.
- **Deleting superseded notes.** Supersede with `-v2`, link the old one. The trail is the
  point.

## Worked example

`examples/worked-example/` holds a complete, synthetic cycle: an evidence note at
`interpreted`, the short handoff that wired two reworked figures into a chapter, and the
review that followed. The numbers are invented and labelled as such; the shapes are real.
