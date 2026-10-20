# Thesis directory: scope rules

This directory holds the LaTeX thesis. Research code, configs, data and job files live
elsewhere (see the Project map in the repository's `AGENTS.md`).

## Boundary

- Edits from a writing context stay inside this directory.
- Do **not** edit research directories from a writing context. If a claim needs new code or
  a new experiment, hand off with `/extract-evidence`.
- Figures under `figures/` enter only through the `figure-import` skill, which records
  provenance back into the evidence note in `docs/evidence_notes/`.
- `tudelft-report.cls` is the template class file. Do not modify it from a writing context.

## Structure

- `report.tex`: the main file; preamble, metadata, the list of `\input`s.
- `report.bib`: the bibliography (append-only from a polish context).
- `frontmatter/`: title pages, preface, summary, nomenclature.
- `mainmatter/<NN>_<slug>.tex`: one file per chapter, numbered.
- `mainmatter/_archive/`: copies made by `thesis-finalizer` before an `apply`.
- `appendix/`: appendices.
- `figures/ch<N>/<YYYYMMDD-HHMMSS>_<slug>/`: figures, one timestamped directory per
  plotting run; never overwritten.

## Build

```bash
latexmk -pdfxe report.tex        # minimum passes; biber only when the .bcf changed
latexmk -C                       # wipe generated files
latexmk -pdfxe -gg report.tex    # force a full rebuild
latexmk -pdf report.tex          # pdfLaTeX fallback, free fonts
```

Do not hand-roll `xelatex && biber && xelatex && xelatex`. On failure read `report.log`
and act on the first line starting with `!` (see the `latex-build` skill).

## Writing rules

The rules live in the writing-rules skill (`rules.md`). The boundary-relevant ones:

- Every result claim comes from an evidence note with `Status: run-complete` or higher.
- Never invent a number. Write `\todo{value pending}` when a value is pending.
- Figure paths are timestamped sub-paths under `figures/`.
- No em or en dashes in prose.
