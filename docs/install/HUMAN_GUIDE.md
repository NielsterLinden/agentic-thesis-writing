# Installing by hand

The same steps the agent follows in [AGENT_INSTALL.md](AGENT_INSTALL.md), for a person.

## 1. Fetch and install

```bash
git clone --depth 1 https://github.com/NielsterLinden/agentic-thesis-writing /tmp/atw
cd <your thesis repository>
python3 /tmp/atw/scripts/atw.py install --target . --thesis-dir thesis --agent claude
```

Options:

| Flag | Meaning |
|---|---|
| `--thesis-dir <dir>` | where the LaTeX lives or should be created (default `thesis`) |
| `--agent claude \| claude-plugin \| codex \| both \| none` | where the agent files go (`.claude/`, nothing, `.agents/skills/`, both, nothing) |
| `--template tudelft \| existing \| none` | scaffold the TU Delft template, keep an existing LaTeX project and add only the scope files, or create no thesis directory |
| `--with-presentation` | also create `presentation/` |
| `--update-kit` | refresh the kit's own files (agents, skills, commands, `scripts/atw.py`, template `CLAUDE.md`), never your content |
| `--dry-run` | print what would be written |

The installer never overwrites. A conflicting file is written as `<file>.atw.new`; merge
by hand and delete it. Exit code 1 means there is at least one `.atw.new` to look at.

## 2. Fill the Project map

Open `AGENTS.md`, find the *Project map* table, replace every `<FILL: ...>`. `none` is a
valid answer. The agents read this table before acting.

## 3. TeX

You need `latexmk`, `xelatex` (or `pdflatex`), `biber` and the usual packages.
[docs/LATEX.md](../LATEX.md) has install notes per platform. Then:

```bash
cd thesis
latexmk -pdfxe report.tex       # or: latexmk -pdf report.tex  (free fonts)
./fetch_assets.sh               # optional: TU Delft logos and the sample cover
```

## 4. Lint

```bash
python3 .claude/skills/tudelft-writing-rules/check_writing_rules.py thesis/mainmatter
```

## 5. Use it

| You want to | Say to your agent |
|---|---|
| gather evidence for a section | `/extract-evidence ch4.1 tokenizer` |
| draft that section | `/draft-section ch4.1 tokenizer` |
| get a critique | `/review-section thesis/mainmatter/04_tokenizer.tex` |
| restructure a section late | `/finalize-section ch4.2` and then `apply` |
| small fixes | `/polish-write ch4 "split the second sentence of 4.2"` |
| a figure tweak | `/polish-plot fig:ch4-roc "larger y label"` |
| a whole-document consistency scan | `/polish-global` |
| a writing-rules check | `/check-writing thesis/mainmatter/04_tokenizer.tex` |
| compile | `/build-thesis` |
| write down where you are | `/handoff ch4-figures "Rework Ch4 figures"` |
| plan the talk | `/deck-storyline 25` |

Without slash commands (Codex, Cursor, others), paste the body of the corresponding file in
`plugin/commands/` (installed under `.agents/skills/` or readable from the clone); each one
is written to work as a plain prompt.
