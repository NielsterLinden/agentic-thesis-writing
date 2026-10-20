# Plotting style

Figures are where the research/writing boundary is crossed most often and where
inconsistency shows first. The kit ships one plotting style guide that `researcher` reads
before writing plot code, `thesis-writer` and `reviewer` check figures against, and
`figure-import` enforces at the destination.

The guide itself is installed into your repository as
**`docs/thesis_style/PLOTTING_STYLE.md`** (source:
[`templates/project/docs/thesis_style/PLOTTING_STYLE.md`](../templates/project/docs/thesis_style/PLOTTING_STYLE.md)).
Edit it there; the agents read the installed copy, named in the Project map.

## The ideas behind it

- **One style module, applied at import time.** Fonts, sizes and rc parameters come from
  one place; no `fontsize=` and no `figsize=` tuples in analysis scripts. Figures are saved
  at the width they will be printed, so point sizes are physical.
- **Titles live in captions.** A title inside a plot duplicates the caption and cannot be
  edited by the writer.
- **A chapter has an identity colour**, and within a chapter the same value of a factor is
  always the same colour. Register the mapping before plotting; never improvise a hex.
- **One metric band per chapter**, round ticks, no broken-axis glyphs. The reader learns the
  band once.
- **Composites in LaTeX.** One conceptual figure per file; a Python composite needs the
  user's agreement and ships its atoms.
- **Seeds are visible**: dots on bars, faint traces under means, `n=` in the figure.
- **Timestamped, additive output.** Every plotting run lands in its own directory; the
  evidence note says which one is current; nothing is overwritten.

## How it is enforced

| Where | What |
|---|---|
| `researcher` | reads the guide; repeats the most-violated rules in its own definition |
| `figure-import` | refuses generic filenames and flat paths; records provenance |
| `reviewer` §7a | the visual-consistency checklist with severities |
| `thesis-polisher` plot mode | changes go through the style helpers, never around them |
| `thesis-writer` | sets `Figure compliance: needs-replot` and hands off instead of patching |
