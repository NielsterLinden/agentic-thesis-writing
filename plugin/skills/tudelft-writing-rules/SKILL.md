---
name: tudelft-writing-rules
description: The writing rules for thesis prose (TU Delft academic-writing conventions, condensed), a linter that catches the mechanical ones, and the procedure for applying them. Load before drafting, reviewing or polishing any .tex prose.
---

# tudelft-writing-rules

The rules live in `rules.md` next to this file; read it in full before drafting. They are
numbered so that findings can cite them (`rule 3.9`). This skill tells you how to apply
them.

## When drafting (`thesis-writer`, `thesis-finalizer`)

1. Read `rules.md`.
2. Write the paragraph with the rules in mind: topic sentence, one idea, concluding
   sentence; short sentences; subject near verb; hedged claims; no forbidden forms.
3. Before the build, run the linter on the file you edited and fix every `[MINOR]` it
   reports that you introduced:

   ```bash
   python3 <this folder>/check_writing_rules.py thesis/mainmatter/04_chapter.tex
   ```

## When reviewing (`reviewer`, `writing-rules-checker`, `thesis-polisher` global mode)

1. Run the linter over the target; it produces the mechanical findings with line numbers.
2. Read for the rules the linter cannot judge (section 4 paragraph structure, section 10
   hedging, information flow, definitions on first use, figure placement).
3. Cite the rule in every finding.

## The linter

`check_writing_rules.py` is standard-library Python. It strips comments, skips math and
non-prose environments (figures, tables, equations, listings), masks the arguments of
`\cite`, `\ref`, `\label`, `\url`, `\includegraphics`, `\texttt` and `\verb`, and then
checks each paragraph. Rules it covers, with the severity it assigns:

| Rule | Check | Severity |
|---|---|---|
| 3.9 | em or en dashes (`---`, `--`, U+2014, U+2013) | MINOR |
| 3.10 | contractions | MINOR |
| 3.5 | sentence-initial FANBOYS (For, And, Nor, But, Or, Yet, So) | MINOR |
| 3.7 | sentence-initial "There is / There are" | MINOR |
| 3.8 | phrasal verbs (set up, look into, carry out, ...) | MINOR |
| 3.6 | vague intensifiers (very, extremely, greatly, ...) | MINOR / NOTE |
| 3.12 | legalistic vocabulary (forthwith, henceforth, hereof, ...) | MINOR |
| 3.11 | a question mark ending a sentence of body text | MINOR |
| 2.7 | anthropomorphism (the model understands / knows / believes ...) | MAJOR |
| 2.6 | absolute claims (proves, always, clearly, obviously, ...) | NOTE |
| 1.14 | first-person singular | MINOR |
| 4.5 | one-sentence paragraphs | MINOR |
| 5.1 | `\subsubsection` (depth beyond subsection) | MINOR |
| 5.3 | a section with exactly one subsection | MINOR |
| 3.4 | wordy phrases (in order to, the majority of, a number of, ...) | NOTE |
| 4.4 | sentence-initial vague "This is / This shows ..." | NOTE |
| 3.1 | sentences over 40 words | NOTE |
| 7.6 | `\includegraphics` paths that are not timestamped | NOTE |
| 2.5 | pending `\todo{}` markers | NOTE |

Options: `--json` for machine-readable output; `--fail-on MINOR|MAJOR|BLOCK` to set the exit
code for CI; `--figure-pattern <regex>` to change the accepted figure path;
`--max-words <n>` for rule 3.1.

A clean linter run is necessary, not sufficient. The rules that matter most (one idea per
paragraph, hedging matched to evidence, no background the reader knows) need a reader.

## Adapting

Projects with other conventions copy this folder to a sibling (`<institution>-writing-rules`),
edit `rules.md`, adjust the word lists at the top of the linter, and point `AGENTS.md`
(*Project map › Writing rules skill*) at the new folder.
