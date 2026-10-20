# Working on agentic-thesis-writing (rules for coding agents)

This repository is agentic-thesis-writing: agents, skills, commands, notes and a LaTeX
template for writing a thesis with research agents and writing agents. It is **not** a
thesis; it is the kit that gets installed into one. Three layers ship together:

| Layer | Where | What |
|---|---|---|
| Agent layer | `plugin/` | 7 agents, 9 skills (two carry a script), 11 commands; the root `.claude-plugin/marketplace.json` lists it |
| Templates | `templates/` | the TU Delft thesis template, the project `AGENTS.md` contract, note folders, a presentation folder |
| Tools and docs | `scripts/`, `docs/`, `examples/`, `tests/` | the installer, hygiene check, documentation, a worked example, tests |

The design is in `docs/design/2026-10-20-agentic-thesis-writing-design.md`.

## How to work

These four principles are adapted from Jiayuan Zhang's
[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills).

1. **Think before coding.** State your assumptions. If a requirement is unclear, ask; never
   guess.
2. **Simplicity first.** Write the smallest change that does the job. No new agent, skill or
   option that nothing needs yet.
3. **Surgical changes.** Touch only what the task needs. Do not reformat or restructure
   neighbouring files.
4. **Goal-driven execution.** Define the check that proves the change works, run it, and
   report it.

## Repository rules

- **Generic, not project-specific.** Agent and skill files must not contain paths,
  hostnames, usernames, project identifiers or numbers from any particular thesis. Anything
  a project must supply goes into the *Project map* of `templates/project/AGENTS.md`, and
  the agents read it from there.
- **Tool-agnostic where possible.** Commands are written so that pasting the body into any
  agent works. Agent frontmatter follows the Claude Code format (`name`, `description`,
  `tools`); the body must make sense without it.
- **Write scopes are explicit.** Every agent states what it may edit, what it must not edit,
  and what it may run. The boundary is the product; do not soften it for convenience.
- **Notes are the interface.** A change to the evidence-note or handoff-note template
  updates the skill, the docs, the example and the generator in `scripts/atw.py` in the
  same change.
- **Scripts are standard library only** (Python 3.10+), so they run inside any thesis
  repository without an install step.
- **Template changes stay minimal.** `templates/thesis/` tracks the upstream TU Delft
  template; each deviation is marked with a `%% agentic-thesis-writing:` comment and listed
  in `templates/thesis/README.md`.
- **No dashes in prose.** The docs follow the writing rules they ship: no em or en dashes;
  use a colon, a semicolon, or two sentences.

## Checks to run before you say "done"

```bash
python -m pytest                                   # unit tests for the scripts and manifests
python scripts/hygiene.py                          # no private paths, hosts, names, media, large files
claude plugin validate --strict plugin/            # Claude Code plugin manifest, agents, skills, commands
claude plugin validate --strict .                  # the marketplace manifest
cd templates/thesis && latexmk -pdfxe report.tex   # the template compiles (XeLaTeX + biber)
```

## Publication safety (enforced by `scripts/hygiene.py` and CI)

- **Private details:** no private paths (AFS or EOS mounts, project or data mounts of a
  cluster, home folders), no cluster host names, no usernames or personal names other than
  the credited authors.
- **Results:** no numbers from an unpublished thesis. The worked example uses synthetic
  numbers and says so.
- **Logos:** no university or collaboration logos. The template fetches them at install time
  from upstream, and compiles without them.
- **Files:** no committed media (PDF, MP4, PNG larger than a thumbnail) and no file over
  1 MB.
- **Licences:** MIT for everything except `templates/thesis/` (CC BY-NC 4.0, attributed).
- **Git:** never push, tag, publish or create GitHub issues or repositories without the
  owner's explicit go-ahead.
