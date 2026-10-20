# Installing agentic-thesis-writing: procedure for coding agents

You are a coding agent setting up agentic-thesis-writing in the user's current repository.
Follow the phases in order. Each phase ends in a **gate** with a known result; do not start
the next phase until the gate passes, or until the user decides how to proceed.

**Ground rules**

- Never overwrite or delete a user file. The installer writes `<file>.atw.new` on conflict.
- Never push. Commit only if the user allowed it in Phase 0.
- Do not start long installs (a TeX distribution, system fonts) unless the user tells you
  to: print the commands for them instead.

## Phase 0: ask first

Ask these in **one** message, each with the default in brackets, and wait for the answers.
Detect what you can first (an existing LaTeX folder, `src/` and `configs/` directories, the
agent tool you are running in) and say what you found.

1. Where does the thesis live, or where should it be created? [`thesis/`]. If a LaTeX
   project already exists there, say so: the installer then keeps it and only adds the
   scope rules, `.latexmkrc` and `figures/README.md` where absent.
2. Which directories are research-only (code, configs, scripts, job files)? [what you
   detected]
3. Where do large outputs live, outside the repository (the data root)? [`none`]
4. Is there a canonical results table (one CSV or similar from which every metric is
   read)? [`none yet`]
5. How are long jobs submitted (the batch command the agents must print but never run)?
   [`none; everything runs locally`]
6. Is there an identifier registry for the factors the thesis studies? [`none`]
7. Which agent tool? `claude` (copy into `.claude/`), `claude-plugin` (plugin installed
   via the marketplace; scaffold only), `codex` (`.agents/skills/`), `both`, or `none`
   [detect]
8. Set up the presentation folder now? [`no`]
9. Files or folders I must not touch? [`none`]
10. May I commit the setup when it is done? [`no`]

**Gate:** you have an answer, or the default was accepted, for all ten.

## Phase 1: fetch and install

```bash
git clone --depth 1 https://github.com/NielsterLinden/agentic-thesis-writing "$TMPDIR/atw"
python3 "$TMPDIR/atw/scripts/atw.py" install \
    --target . \
    --thesis-dir <answer 1> \
    --agent <answer 7> \
    [--template existing]        # when a LaTeX project already exists at the thesis dir
    [--with-presentation]        # answer 8
```

(On Windows use `%TEMP%` or any scratch folder for the clone.)

What `install` does, without overwriting:

- copies the agents, skills and commands into `.claude/` (or `.agents/skills/` for codex);
  with `--agent claude-plugin` it skips this step;
- scaffolds `<thesis dir>/` from the TU Delft template (or adds the three files to an
  existing project), `docs/evidence_notes/`, `docs/handoffs/`, `docs/finalizer/`,
  `docs/thesis_style/PLOTTING_STYLE.md`, and `presentation/` if requested;
- copies `scripts/atw.py` to `scripts/atw.py` in the target so the note generators work
  without the clone;
- merges an `AGENTS.md` block (between `<!-- agentic-thesis-writing:start/end -->`
  markers), an `@AGENTS.md` line in `CLAUDE.md`, and a `.gitignore` block.

**Gate:**

1. `install` exits 0, and `find . -name "*.atw.new"` finds nothing. If it exits 1, show
   each `.atw.new` next to the original and merge by hand with the user; delete the `.new`
   file afterwards.
2. `AGENTS.md` contains the Project map table.

## Phase 2: fill the Project map

Open `AGENTS.md` and replace every `<FILL: ...>` in the Project map with the Phase 0
answers. Use `none` where the project has no such thing; do not leave a placeholder.

**Gate:** `grep -n "<FILL" AGENTS.md` prints nothing.

## Phase 3: TeX check and first build

```bash
latexmk --version && xelatex --version | head -1 && biber --version
cd <thesis dir> && latexmk -pdfxe report.tex
```

- If `xelatex` is missing but `pdflatex` exists: `latexmk -pdf report.tex` builds with free
  fonts; say so.
- If TeX is missing entirely, print the install command for the user's platform (see
  `docs/LATEX.md`: TeX Live `scheme-medium` on Linux, including a user-space install for
  clusters without root; MiKTeX on Windows; MacTeX on macOS) and continue without the
  build.
- Font warnings about Arial or Roboto Slab are expected without the house fonts; the
  fallback fonts are used.
- Optional: `./fetch_assets.sh` in the thesis directory downloads the logos and the sample
  cover; ask before downloading.

**Gate:** `<thesis dir>/report.pdf` exists, or the user chose to continue without TeX.
Report which.

## Phase 4: lint the scaffold

```bash
python3 .claude/skills/tudelft-writing-rules/check_writing_rules.py <thesis dir>/mainmatter --fail-on MINOR
```

(For the plugin route, the script lives in the plugin's `skills/tudelft-writing-rules/`
folder; for codex in `.agents/skills/tudelft-writing-rules/`.)

**Gate:** exit 0. `[NOTE]` findings for `\todo{}` markers are expected on a fresh
scaffold.

## Phase 5: hand back

Report to the user:

- **Done:** what you installed, the files created or merged, the Project map values.
- **Could not do:** anything that failed or was skipped, with the reason and the fix
  command.
- **Next:** "Ask me for the first evidence note, for example:
  `/extract-evidence ch4.1 <slug>`. When the note reaches `run-complete`, ask for
  `/draft-section ch4.1 <slug>`." For Claude Code, mention that collaborators who trust the
  folder get the same agents.

If the user allowed it in Phase 0, commit the setup (`AGENTS.md`, `CLAUDE.md`,
`.gitignore`, `.claude/` or `.agents/`, `<thesis dir>/`, `docs/`, `scripts/atw.py`,
`presentation/` if created). Build artefacts are ignored. Never push.
