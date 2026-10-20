---
description: "Light figure polish. Either a caption-only fix, or a single surgical change to the plotting code followed by regeneration of that one figure and re-import into a new timestamped directory. Runs the thesis-polisher in plot mode."
argument-hint: "<fig-label | figure-path> [\"quoted instruction, e.g. make the y-axis label larger\"]"
---

Invoke the `thesis-polisher` subagent in **plot mode** for `$ARGUMENTS`. If subagents are
unavailable in this tool, read `.claude/agents/thesis-polisher.md` (or the plugin's
`agents/thesis-polisher.md`) and act as that agent yourself.

First classify the request and tell the user which sub-case applies and what it costs.

**A. Caption-only (instant).** Wording, symbol, or self-containment → edit the `\caption`.
No regeneration. Preferred whenever it suffices.

**B. Plot-code fix (needs regeneration).** Axis range, ticks, label position, size, legend,
palette:

1. `grep` the figure's filename stem under the plotting modules and figure scripts named in
   `AGENTS.md` to find the producing function.
2. Read the plotting style guide; make the change *through* its helpers.
3. Make the single surgical edit (no refactor, no change to what is computed).
4. Show the exact local regeneration command and **confirm before running it**.
5. Re-import with `figure-import` into a **new** timestamped directory; update the
   `\includegraphics` path. Do not auto-build.

Hard rules: never train, never run heavy inference, never submit jobs; additive only under
the data root and in the figure tree; do not edit shared style constants that change other
chapters (hand off to `researcher`); a code fix is incomplete until the figure is
regenerated, re-imported and the path updated.
