# The workflow

How research agents and writing agents share one thesis without stepping on each other,
and how the work survives the end of a context window.

## Two roles, one channel

```
research directories ──researcher──▶ docs/evidence_notes/<chN.S>_<slug>.md ──thesis-writer──▶ thesis/
        ▲                                   │  Status: triaged → run-pending → run-complete → interpreted
        │                                   ▼
   data root (outside the repo)        figure-import → thesis/figures/ch<N>/<ts>_<slug>/
```

- **`researcher`** may edit code, configs, scripts, job files and evidence notes. It may
  not edit the thesis. It stages long jobs and prints the submit command; it never runs it.
- **`thesis-writer`** may edit the thesis and, in a note, only the `interpreted` flip and
  the figure-path confirmation. It may not edit research directories. It never invents a
  number.
- **`reviewer`** edits nothing.

Why so strict: a single agent with both scopes drifts into "fixing" a number by editing
the plot, or "clarifying" the code by editing the prose, and the trail is lost. With
disjoint scopes every number in the thesis has a note, every note has a run, and every
figure has a source path.

## The loop, step by step

1. **`/extract-evidence ch4.2 tokenizer`.** The researcher reads `AGENTS.md`, runs
   `data-inventory` (what exists for these runs?), `trace-claim` (does the factor map
   cleanly to config and code?), creates the note at `triaged`, picks the cheapest entry
   point, stages the action and sets `run-pending`. If the action is cheap and local, it
   runs it, verifies the artefacts, imports the figures and sets `run-complete`.
2. **You** run the submit command, if there was one.
3. **`/extract-evidence ch4.2 tokenizer`** again. The researcher verifies the artefacts
   (expected count, latest timestamped directory), fills in the metrics from the canonical
   table, imports the figures, writes the confounders and the thesis-safe interpretation,
   sets `run-complete`.
4. **`/draft-section ch4.2 tokenizer`.** The writer refuses if the note is below
   `run-complete`. Otherwise it reads the note, the whole chapter and the registry, drafts
   into the results-chapter scaffold, runs the linter, builds, reports `Build OK.`, flips
   the note to `interpreted`.
5. **`/review-section thesis/mainmatter/04_tokenizer.tex`** (optional). Severity-tagged
   findings, a cuts block, a six-axis grade. You decide what to act on.
6. **`/handoff ch4-tokenizer`** at the end of the session, or before any step that needs
   your decision.

## Entry points: cheapest first

| Code | Name | When |
|---|---|---|
| D | reuse | existing figures or tables answer the question |
| C | recompute | results exist and an analysis module covers the metric |
| E | bespoke | a new analysis on existing artefacts |
| B | re-derive | artefacts exist, derived outputs are missing |
| A | new run | nothing exists; only with a named thesis argument |

The default expectation late in a thesis is C, not A. The researcher must justify A with
the section and the argument that cannot be made otherwise.

## Source of truth

1. the implementation and configuration that actually ran;
2. the canonical results table;
3. tracker exports (cross-reference);
4. the identifier registry;
5. thesis prose: never.

## Late stage

Once chapters exist, three agents work at decreasing amplitude:

| Agent | Amplitude | How it lands |
|---|---|---|
| `thesis-finalizer` | structural, one section at a time | staged `critique.md` + `proposed_rewrite.tex`; spliced only on the literal `apply`, with the old chapter archived |
| `thesis-polisher` | sentence, caption, one figure | one reviewable edit at a time; plot mode may touch plotting code cosmetically and regenerate one figure |
| `writing-rules-checker` | none (report) | numbered findings you hand to `/polish-write` |

`/polish-global` is the whole-document consistency scan: abbreviations, terminology,
notation, identifiers, dashes, cross-references, metric definitions.

## Session hygiene

- Start a session by reading the open handoff notes (`docs/handoffs/*.md` with
  `Status: open | in-progress`).
- End a session with `/handoff`. The resume matrix is keyed on observable states, so the
  next session (or agent) can pick up without the conversation.
- Agents never commit unless you say so for a named change. You own the history.

## A day in the life

> Morning: `/extract-evidence ch6.1 attention-type`. The researcher finds 12 runs with
> checkpoints and results, picks C, runs the comparison plot locally, imports two figures,
> writes the note at `run-complete`.
>
> `/draft-section ch6.1 attention-type`. The writer drafts Setup, Results and Discussion
> into the scaffold, builds, reports `Build OK.`, flips the note.
>
> `/review-section thesis/mainmatter/06_attention.tex`. Two `[MAJOR]` (a lens declared
> without a verdict; an uncontrolled causal sentence), five `[MINOR]`, one `[CUT]`.
>
> `/polish-write ch6 "address review items 1 and 2"`. Two edits, each shown as a diff.
>
> Evening: `/handoff ch6-attention "Ch6 §6.1 drafted; §6.2 needs the entropy figure"`.
