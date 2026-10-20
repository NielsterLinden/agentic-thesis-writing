# agentic-thesis-writing plugin

The agent layer of [agentic-thesis-writing](https://github.com/NielsterLinden/agentic-thesis-writing),
packaged for Claude Code. The same files are copied into `.claude/` by the installer when
you prefer to version them with your thesis repository.

```
/plugin marketplace add NielsterLinden/agentic-thesis-writing
/plugin install agentic-thesis-writing@agentic-thesis-writing
```

| Folder | Contents |
|---|---|
| `agents/` | `researcher`, `thesis-writer`, `reviewer`, `thesis-finalizer`, `thesis-polisher`, `writing-rules-checker`, `deck-planner` |
| `skills/` | `evidence-note`, `handoff-note`, `figure-import` (+ `figure_import.py`), `data-inventory`, `trace-claim`, `latex-build`, `tudelft-writing-rules` (+ `rules.md`, `check_writing_rules.py`), `thesis-to-deck` (+ `storyline_template.md`), `thesis-setup` |
| `commands/` | `/extract-evidence`, `/draft-section`, `/review-section`, `/finalize-section`, `/polish-global`, `/polish-write`, `/polish-plot`, `/build-thesis`, `/handoff`, `/check-writing`, `/deck-storyline` |

Every agent reads the **Project map** in your repository's `AGENTS.md` first. Install that
file with `python3 scripts/atw.py install --agent claude-plugin` from a checkout of the
repository, or by following `docs/install/AGENT_INSTALL.md`.
