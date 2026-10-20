# Quick install

Open your coding agent (Claude Code, Codex, Cursor, ...) **in the repository that holds, or
will hold, your thesis**, and paste this sentence:

> Set up agentic-thesis-writing in this repository: follow https://github.com/NielsterLinden/agentic-thesis-writing/blob/main/docs/install/AGENT_INSTALL.md and ask me the setup questions first.

The agent then:

1. asks a few setup questions (where the thesis lives, which directories are research-only,
   where large outputs go, how long jobs are submitted, which agent tool you use);
2. fetches this repository and runs `scripts/atw.py install`, which copies the agents,
   skills and commands, scaffolds `thesis/`, `docs/evidence_notes/` and `docs/handoffs/`,
   and merges an `AGENTS.md` block, a `CLAUDE.md` line and a `.gitignore` block without
   overwriting anything;
3. checks your TeX installation and builds the thesis template once;
4. runs the writing-rules linter on the scaffold;
5. reports what it did, and anything it could not do.

It never overwrites your files and never pushes.

**Claude Code plugin route.** If you prefer the agents to load from the plugin cache instead
of living in your repository:

```
/plugin marketplace add NielsterLinden/agentic-thesis-writing
/plugin install agentic-thesis-writing@agentic-thesis-writing
```

then run the installer with `--agent claude-plugin` so it scaffolds the project files only.

Rather do it yourself? Read [docs/install/HUMAN_GUIDE.md](docs/install/HUMAN_GUIDE.md).
