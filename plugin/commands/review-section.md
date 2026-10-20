---
description: Read-only critique of a thesis section or an evidence note against the grounding, framing, writing and figure checklists. Runs the reviewer agent; edits nothing.
argument-hint: <path-to-tex-section-or-evidence-note> [chapter kind: framing|results|synthesis]
---

Invoke the `reviewer` subagent for `$ARGUMENTS`. If subagents are unavailable in this tool,
read `.claude/agents/reviewer.md` (or the plugin's `agents/reviewer.md`) and act as that
agent yourself, without editing any file.

Procedure:

1. Read `AGENTS.md` (Project map), `rules.md` from the writing-rules skill, and the plotting
   style guide.
2. Read the target (`.tex` section, or `docs/evidence_notes/*.md`). For a `.tex` target,
   also read the evidence note(s) it draws on and the chapter intro.
3. Walk the checklist in the reviewer definition, in order, citing the rule for each
   finding.
4. Return chat-only commentary in the `[SEVERITY] Location / Issue / Suggestion` format,
   then the count by severity, then the two mandatory closing blocks:
   *Cuts and condensations* and the six-axis *Section grade*.

The reviewer must not call `Edit`, `Write` or `Bash`. If the user wants the review kept,
they ask for it to be saved under `docs/reviews/`; that save is the user's call.
