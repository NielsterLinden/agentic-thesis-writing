# Adapting the kit to your project

Everything project-specific lives in the **Project map** of your repository's `AGENTS.md`.
The agents read it first. Most adaptations are a row in that table; the rest are listed
here.

## The Project map

| Row | What it controls |
|---|---|
| Thesis directory, main file, build command | where the writer works and how everything builds |
| Research directories | what the researcher may edit |
| Data root, run layout, canonical results table | where the researcher looks, and the only source of metric values |
| Long-job policy | the command every agent prints and never runs |
| Environment activation | the line to source before any command |
| Figure staging, plotting style guide, plotting modules | where plots are produced, the rules they follow, and what the polisher may touch in plot mode |
| Identifier registry | the compact IDs the prose must use (optional) |
| Writing rules skill | which `rules.md` applies |
| Page budget | the results-chapter target and ceiling |
| Reference papers | a gitignored folder of PDFs the finalizer may read |
| Presentation directory | whether `/deck-storyline` has a home |

## Another LaTeX template

The agents assume a main file, a `latexmk` build and a `figures/` tree; nothing else. To
use your faculty's template:

1. Install with `--template existing` into the directory that holds it (or `--template
   none` and create the directory yourself).
2. Copy `templates/thesis/.latexmkrc`, adjust the engine if needed, and define a
   `\todo{}` macro in your preamble.
3. Adjust the *Main file and build command* row.
4. Keep the `figures/ch<N>/<timestamp>_<slug>/` convention; `figure-import` depends on it.

The results-chapter scaffold (`02_results_chapter_template.tex`) is plain LaTeX and works
in any class.

## Other writing rules

Copy `plugin/skills/tudelft-writing-rules/` to a sibling folder, edit `rules.md` (keep the
numbering scheme so findings can cite rules), adjust the word lists at the top of
`check_writing_rules.py`, and set the *Writing rules skill* row. Pull requests with other
institutions' rule sets are welcome.

## An identifier registry

If the thesis names more than a handful of recurring factors (architecture choices,
dataset variants, protocol options), give each a compact ID in a markdown table:

```
| ID | Name | Config key | Options | Implementation |
|---|---|---|---|---|
| T1 | tokenizer family | model.tokenizer.name | raw, binned, learned | src/pkg/tokenizer.py |
```

Point the *Identifier registry* row at it. `trace-claim` then checks every ID in prose,
and renames happen in one place.

## Batch systems

The long-job policy is one line: the submit command and the words "print, never run".
Examples: `sbatch jobs/train.sbatch`; `condor_submit jobs/train.sub`; `qsub jobs/train.pbs`;
`none; everything runs locally`. The researcher fills the job file and prints the
command; you run it.

## Other agent tools

- **Claude Code:** agents, skills and slash commands as written, either in `.claude/`
  (`--agent claude`) or as the plugin (`--agent claude-plugin`).
- **Codex:** `--agent codex` installs the skills under `.agents/skills/`; the `AGENTS.md`
  contract is read natively; commands are pasted as prompts (each is written to work as
  one).
- **Cursor and others:** read `AGENTS.md`; add a rule file that points at the agent
  definitions; paste commands as prompts.
- **No subagents:** every command says "if subagents are unavailable, read the agent
  definition and act as that agent". The scope rules then rely on the single agent's
  discipline, which is weaker; keep sessions single-role (a research session, then a
  writing session) to compensate.

## Trimming

Projects without a late-stage phase can drop `thesis-finalizer` and `thesis-polisher`;
projects without a talk can drop `deck-planner` and the presentation folder. Delete the
agent file and its commands; nothing else references them except the docs.

## Renaming

The thesis directory name is substituted at install time (the `THESIS_DIR` placeholder in
the project templates). The note
directories (`docs/evidence_notes/`, `docs/handoffs/`, `docs/finalizer/`) are fixed in the
skills; renaming them means editing the skills and `scripts/atw.py`.
