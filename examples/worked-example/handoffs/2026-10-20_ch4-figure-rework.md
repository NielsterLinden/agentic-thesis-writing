# Handoff: wire up the reworked Ch4 figures 4.1 and 4.2

> **Synthetic example** of a short handoff from `researcher` to `thesis-writer`.

- Status: done
- Date: 2026-10-20
- Agents: researcher → thesis-writer
- Files to edit: `thesis/mainmatter/04_input_representation.tex`

## TL;DR

The two tokenizer figures were re-plotted with the parameter count on a log x-axis. They
are re-imported; the evidence note `docs/evidence_notes/ch4.2_tokenizer.md` already has the
provenance and the new `Active figures:` directory. The writer updates two
`\includegraphics` paths and two captions. No prose claim depends on the old axis layout.

## How to resume

| You are starting at... | Do this |
|---|---|
| The chapter still references `20260519-114923_tokenizer` | do steps 1 to 3 below, then build |
| Paths updated, captions not yet | do step 2, then build |
| Build passes and both figures render from `20260601-161946_tokenizer` | set this note to `done` |

## 1. Update the two `\includegraphics` paths

New timestamped directory: `20260601-161946_tokenizer`.

- line 85: `figures/ch4/20260519-114923_tokenizer/ch4_T1_auroc_bar_tokenizer.pdf`
  → `figures/ch4/20260601-161946_tokenizer/ch4_T1_auroc_bar_tokenizer.pdf`
- line 101: `figures/ch4/20260519-114923_tokenizer/ch4_T1_roc_tokenizer.pdf`
  → `figures/ch4/20260601-161946_tokenizer/ch4_T1_roc_tokenizer.pdf`

## 2. What changed in the figures (so the captions match)

- The bar chart's x-axis is no longer categorical; bars sit at each tokenizer's parameter
  count on a log scale, so the gap between `binned` and `learned` is honest.
- The tokenizer name moved to an italic grey sub-tick under each parameter-count tick.
- The y-band stays at 0.800 to 0.850 (chapter band).

Caption for Figure 4.1 (replace lines 86 to 89):

> Test AUROC per tokenizer family, positioned at each family's parameter count on a log
> axis; the family name appears as a grey sub-tick. Bars are seed means, dots are the
> individual seeds (n=3), error bars are the seed spread. The y-axis is locked to the
> chapter band.

Caption for Figure 4.2: unchanged except "four curves" → "one curve per family".

## 3. Body-text check (verify, no change expected)

The body refers to families by name and quotes the deltas from the note. Nothing claims the
x-axis is categorical. Confirm by reading §4.2 Results once.

## Constraints

- Additive figure directories only; do not touch `20260519-114923_tokenizer`.
- No em or en dashes in captions.
- Build with `latexmk -pdfxe report.tex` and confirm both figures render from the new
  paths before reporting `Build OK.`.
- Do not commit.

## Changes

- 2026-10-20: created by researcher after re-import.
- 2026-10-20: writer updated paths and captions; `Build OK.`; status `done`.
