---
name: figure-import
description: "Promote a figure from the research output area into the thesis figure tree at <thesis>/figures/ch<N>/<YYYYMMDD-HHMMSS>_<slug>/, additively, and record the source path and the active figure directory back into the evidence note. The only sanctioned way a figure enters the thesis directory. Use whenever a plot must land in LaTeX."
---

# figure-import

Figures cross the research/writing boundary only through this skill:

- `researcher` may copy a file into the thesis directory only this way (its write scope
  otherwise excludes the thesis).
- `thesis-writer` may invoke it to fetch a figure it has decided to include.
- `thesis-polisher` (plot mode) uses it after regenerating one figure.

The plotting style guide named in `AGENTS.md` decides *which* plots are eligible; this skill
enforces the destination mechanics.

## Destination

```
<thesis>/figures/ch<N>/<YYYYMMDD-HHMMSS>_<slug>/<file>.pdf
```

- `ch<N>`: the chapter.
- `<YYYYMMDD-HHMMSS>`: the timestamp of the plotting run that produced the figures; the
  same for every figure of that run. Reuse the timestamp already in the note's
  `Active figures:` field when one exists for this run.
- `<slug>`: a short kebab-case name for the topic (`tokenizer`, `data-treatment`).
- `<file>`: the plotting output filename, verbatim.

LaTeX references use the timestamped sub-path:

```latex
\includegraphics[width=\linewidth]{figures/ch4/20260519-114923_tokenizer/ch4_T1_roc_tokenizer.pdf}
```

Existing timestamped directories are **never** deleted or overwritten. They stay as
provenance; the note's `Active figures:` field says which one is current.

## Procedure

Run the script in this folder (standard library only):

```bash
python3 <skill dir>/figure_import.py \
    --src <output area>/report_x/figures/ch4_T1_roc_tokenizer.pdf \
    --chapter ch4 --slug tokenizer \
    --note docs/evidence_notes/ch4.2_tokenizer.md \
    [--thesis-dir thesis] [--timestamp 20260519-114923] [--dry-run]
```

It:

1. checks the source exists and the filename follows `ch<N>_*` (pass
   `--allow-any-name` to override, and say why in the note);
2. resolves the timestamp (`--timestamp`, else the note's current `Active figures:`
   directory if it belongs to this run, else now);
3. creates the destination directory if absent; refuses to overwrite an existing file;
4. copies the file (a copy, not a symlink: links across storage areas are fragile and do
   not commit);
5. sets the note's `Active figures:` line to the destination directory;
6. appends `- <destination> ← <source>` under the note's `Plot paths` section;
7. prints the destination directory.

If several notes share the section, run it once per note with the same `--timestamp`.

## Hard rules

- Never write a figure into the thesis tree without recording its source in a note.
- Never delete or overwrite an existing timestamped directory. Additive only.
- Never put a raw output-area path into a `.tex` file.
- Never invent or pad a timestamp.
- One conceptual figure per file. Composites are composed in LaTeX; a Python composite
  (agreed with the user) ships with its atomic plots in the same directory.
- Refuse the import if the source clearly violates the plotting style (a title inside the
  figure, a generic `figure-*.pdf` name). Surface the gap instead of importing.
