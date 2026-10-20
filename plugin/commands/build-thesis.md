---
description: Build the thesis PDF with latexmk, read the log on failure, and report a one-line verdict plus the page count. Uses the latex-build skill.
argument-hint: [-gg | -C | -pdf]
---

Build the thesis using the `latex-build` skill, with the option in `$ARGUMENTS` if any:

- no argument: `latexmk -pdfxe report.tex` in the thesis directory named in `AGENTS.md`
  (minimum passes);
- `-gg`: force a full rebuild;
- `-C`: clean generated files, then stop;
- `-pdf`: build with pdfLaTeX and free fonts (use when XeLaTeX or the house fonts are
  unavailable).

Use a generous timeout. On failure, open the log, quote the **first** line starting with
`!` and the `l.<n>` line after it, and say whether the fix is within a writing scope
(unbalanced braces, bad path, mistyped key) or outside it (preamble, class file, missing
package, missing figure). Do not edit the preamble or the class file from this command.

Report: `Build OK. <N> pages.` or `Build FAILED: <first error line>`, and the path of the
PDF.
