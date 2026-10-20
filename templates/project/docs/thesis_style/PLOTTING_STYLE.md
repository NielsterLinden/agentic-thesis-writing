# Plotting style guide

The cross-chapter rules for every figure that enters the thesis. `researcher` reads this
before writing plot code; `thesis-writer` and `reviewer` check figures against it;
`figure-import` enforces the destination mechanics. Adapt the helper names to your own
style module; keep the rules.

> **Authority order** when sources disagree: (1) the project's style module (the code
> that defines palette, sizes and rc parameters); (2) this document; (3) any narrative
> colour-language note.

---

## 1. Output workflow and timestamped folders

1. **Generate** figures in the research output area (Project map › *Figure staging*);
   never write into the repository from a plotting script.
2. **Promote** into the thesis via the `figure-import` skill:
   `<thesis>/figures/ch<N>/<YYYYMMDD-HHMMSS>_<slug>/<file>.pdf`. Existing directories are
   never overwritten.
3. **Reference** in LaTeX with the timestamped sub-path.

Flat paths like `figures/ch6/figure-foo.pdf` are forbidden for new work.

## 2. One style module, applied at module level

Every plotting module calls the project's `apply_style()` (or equivalent) at import time.
No `fontsize=` on labels, ticks or legends; no `ax.set_title` or `plt.suptitle` (titles
live in captions); figure sizes only through `figure_size(width, aspect)` at the final
printed width (`full`, `two_thirds`, `half`, `third`), so font sizes stay physical.

## 3. Chapter identity colour

Each chapter picks one colour from the project palette as its identity. The recommended or
winning configuration wears it in every plot of the chapter; the baseline wears mid-grey
(`#666666`). Declare it at the top of the chapter's analysis script.

## 4. Intra-chapter value colours

For each factor whose values appear in a chapter's plots, register a fixed `{value → hex}`
mapping in the style module (`CHAPTER_VALUE_COLORS[chN][factor]`) before writing the
script. Every plot in the chapter draws that value in that colour. No per-script
overrides, no improvised hex strings. Lightened shades come from a single helper
(`lighten(hex, amount)` or `chapter_palette(hex, n)`), never typed in.

## 5. Colormaps and heatmaps

| Content | Colormap |
|---|---|
| chapter-internal sequential | a sequential map anchored at the chapter colour |
| diverging, signed (delta from baseline) | `RdBu_r` centred on zero |
| confusion matrices | `Blues`, normalised to [0, 1] |
| cross-chapter non-negative magnitudes | `viridis` |

Always set explicit `vmin`/`vmax` (clamp metric heatmaps to the chapter band). Annotate
cells when the grid is at most 15 × 15. `row_order` and `col_order` are module-level
constants; never rely on `groupby()` order.

## 6. Metric axis: per-chapter band, no break mark, round ticks

- One y-band per chapter for the headline metric, registered in the style module and
  identical for every plot in the chapter (bars, curves, colour bars).
- No broken-axis glyphs. The axis simply starts at the band's lower bound.
- Ticks end in 0 or 5 at the last significant decimal; a helper enforces it and raises
  when the band cannot produce a clean tick set.
- All panels of a multi-panel figure share `ylim` and tick count.

## 7. Composites: LaTeX by default

Each plotting function produces one conceptual figure. Multi-panel composites are built in
LaTeX (`subfigure`). A Python composite is allowed only when (a) the user agreed
beforehand, (b) all panels share one quantity and one story, and (c) the atomic plots are
saved beside it in the same timestamped directory.

## 8. Filenames

- Atomic: `ch<N>_<FACTOR>_<metric>_<variant>.pdf` (metric lowercase).
- Composite: `ch<N>_F<n>_combined_<description>.pdf`.
- Never a generic `figure-*.pdf` prefix.

## 9. Seed encoding

- **Bars:** bar = seed mean; black jittered dots (`s=20`, `alpha=0.5`, on top); error bar =
  std; `n=<int>` inside the bar.
- **Curves:** per-seed traces first (`alpha=0.2`, thin, behind); mean curve on top
  (`linewidth ≥ 1.4`); std band `alpha=0.15`.
- Captions state the number of seeds.

## 10. Diagnostic and one-off plots

Attention maps, gates, scaling overheads, latency scatters, distributions: always in colour,
drawn from the palette (no `tab10`); greyscale only for low-saliency references. Numeric
ranges are free; tick rounding still applies.

## 11. Plot-type quick reference

| Plot | Reference | Mean / individual | Save |
|---|---|---|---|
| ROC | diagonal, grey dashed, thin | mean `lw=2.5`; individual `alpha=0.2` | PDF |
| metric bars | none (axis zoomed to band) | seed mean, dots, `n=` inside | PDF |
| training curves | none | mean `lw≥1.4`; individual thin and faint | PDF |
| scatter (embeddings) | none | `s=15`, `alpha=0.6`, `rasterized=True` above 5k points | PDF |
| heatmap | none | per section 5 | PDF |

## 12. Reviewer checklist

- `[BLOCK]` style applied at module level; no in-figure titles; timestamped paths; one
  metric band per chapter; composites ship their atoms.
- `[MAJOR]` filename convention; shared band and ticks across panels; explicit orderings;
  consistent value colours; no hardcoded font sizes; sizes via the helper; palette colours
  only; no ad-hoc hex.
- `[MINOR]` colormap choices; diagnostic plots in palette colours; ROC conventions; seed
  encoding; top and right spines absent.
- `[NOTE]` rasterized dense scatters; PDF format (or the note explains why not).

## 13. Forbidden practices

`ax.set_title`; `plt.suptitle`; hardcoded `fontsize=`; bare `figsize=` tuples; `tab10`
for factor comparisons; flat figure paths; implicit categorical order; generic filenames;
broken-axis glyphs; silent composites; ad-hoc lightened hex constants; auto-scaled
`vmin`/`vmax` on metric heatmaps.
