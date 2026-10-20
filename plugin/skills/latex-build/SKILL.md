---
name: latex-build
description: "Build the thesis PDF with latexmk (XeLaTeX + biber by default), read the log correctly when it fails, and decide what is yours to fix. Use after every edit to a .tex file and whenever the rendered PDF is needed."
---

# latex-build

The thesis is built with `latexmk`, driven by the `.latexmkrc` in the thesis directory. The
rc file selects the engine (XeLaTeX for the TU Delft house style, with biber for the
bibliography) and sends the warning firehose to the log instead of the terminal.

## Commands

From the thesis directory (path in `AGENTS.md`; default `thesis/`):

```bash
latexmk -pdfxe report.tex       # minimum passes; runs biber only when the .bcf changed
latexmk -C                      # wipe generated files (aux, bbl, bcf, toc, fdb, ...)
latexmk -pdfxe -gg report.tex   # force a full rebuild from scratch
latexmk -pdf report.tex         # pdfLaTeX fallback (free fonts; use when XeLaTeX is unavailable)
```

Give the build a generous timeout (a cold build with many figures can take minutes). Do not
hand-roll `xelatex && biber && xelatex && xelatex`: it runs three unconditional passes
every time and a bare engine without `-interaction=nonstopmode` hangs at the `?` prompt on
any error. `latexmk` content-hashes the sources and runs only the passes needed.

## Reading the result

| Outcome | What you see | Action |
|---|---|---|
| Success | exit 0; `All targets (report.pdf) are up-to-date` or the passes complete | proceed |
| An error you introduced | exit non-zero; the log has a line starting with `!` | open `report.log`, find the **first** `!` line and the `l.<n>` line after it, fix the source, rebuild |
| Corrupted generated state | `! Extra }` while reading the `.aux`, `malformed bcf`, biber stack traces | `latexmk -C`, then rebuild once |
| Missing figure | `! LaTeX Error: File 'figures/...' not found` | check the `\includegraphics` path against the timestamped directory; never "fix" by copying a figure in by hand; use `figure-import` |
| Undefined reference or citation | `LaTeX Warning: Reference 'x' undefined` after the final pass | fix the key; a key you cannot resolve is a `\todo{}` and a note to the user |
| Font not found (XeLaTeX) | `! fontspec error: "font-not-found"` | the template falls back to free fonts; if the error persists, install the fonts named in `docs/LATEX.md` or build with `-pdf` |

Only the first error matters; later ones are usually consequences.

## What is yours to fix

- unbalanced braces, an undefined macro you typed, a bad path, a mistyped `\ref` or `\cite`:
  yours;
- the preamble, the class file, the bibliography style, a missing package: **not yours**
  from a writing context. Report it.
- a figure that will not import: hand off to `researcher`.

## Reporting

End the turn with one line, `Build OK.` or `Build FAILED: <first error line, trimmed>`, and
the list of `.tex` files touched. Attach the page count when the chapter has a page budget
(`pdfinfo report.pdf | grep Pages`, or the last page number in the log).

## Keeping builds fast

- keep embedded rasters at print resolution (≤ 600 DPI at display size) and without
  unnecessary alpha channels; over-resolution images dominate per-pass time;
- prefer PDF figures;
- do not commit build artefacts (the template's `.gitignore` covers them).
