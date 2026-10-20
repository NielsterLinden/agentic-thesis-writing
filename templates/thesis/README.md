# Thesis template (TU Delft house style)

This folder is the [unofficial TU Delft report/thesis template](https://github.com/dzwaneveld/tudelft-report-thesis-template)
by Daan Zwaneveld, licensed [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
(see [LICENSE-TEMPLATE.md](LICENSE-TEMPLATE.md)), set up for the agentic-thesis-writing
workflow. Full documentation of the template itself: https://dzwaneveld.github.io/report/.

## Build

```bash
latexmk -pdfxe report.tex      # XeLaTeX + biber, driven by .latexmkrc
./build.sh                     # the same, with -gg (full rebuild), -pdf (pdfLaTeX), -C (clean)
```

Requirements: a TeX distribution with `latexmk`, `xelatex`, `biber`, `biblatex`,
`fontspec`, `siunitx`, `tikz` and the usual packages (TeX Live `scheme-medium` or
MiKTeX with on-the-fly installation). See `docs/LATEX.md` in the kit for per-platform
install notes.

## Fonts and assets

- The house style uses **Arial** and **Roboto Slab**. When they are not installed the
  class falls back to TeX Gyre Heros and TeX Gyre Pagella (free, shipped with TeX) and
  prints a warning. Roboto Slab is also found by file name in the TeX tree (`roboto`
  package).
- The TU Delft logos and the sample cover image are **not** included here. Run
  `./fetch_assets.sh` to download them from upstream into `figures/`; the document builds
  without them (plain cover, no logo).

## Changes relative to upstream

Each change is marked `%% agentic-thesis-writing:` in the source.

| File | Change |
|---|---|
| `tudelft-report.cls` | font fallbacks (`\IfFontExistsTF`); optional cover image and logo (`\IfFileExists`) |
| `frontmatter/title-thesis.tex`, `title-report.tex` | optional logo |
| `report.tex` | `\todo{}` macro; chapter files renamed to `<NN>_<slug>.tex`; `style=numeric-comp,sorting=none` for biblatex |
| `mainmatter/` | `01_introduction.tex`, `02_results_chapter_template.tex` (the mini-thesis scaffold) and `09_conclusion.tex` replace the upstream sample chapters |
| `.latexmkrc`, `build.sh`, `fetch_assets.sh`, `CLAUDE.md`, `figures/README.md` | added |

## Layout

```
report.tex                  main file
report.bib                  bibliography
tudelft-report.cls          class file (do not edit from a writing context)
frontmatter/                title pages, preface, summary, nomenclature
mainmatter/                 one file per chapter; _archive/ for finalizer backups
appendix/                   appendices
figures/ch<N>/<ts>_<slug>/  figures, one timestamped directory per plotting run
```
