---
description: Check .tex prose against the writing rules: run the mechanical linter, then read for what it cannot judge, and return a numbered severity-tagged list. Read-only. Runs the writing-rules-checker agent.
argument-hint: <path-to-tex-file-or-directory> [--fail-on MINOR|MAJOR]
---

Invoke the `writing-rules-checker` subagent for `$ARGUMENTS`. If subagents are unavailable
in this tool, read `.claude/agents/writing-rules-checker.md` (or the plugin's
`agents/writing-rules-checker.md`) and act as that agent yourself, without editing.

Procedure:

1. Read `AGENTS.md` to find the thesis directory and the writing-rules skill in use.
2. Run the linter from that skill folder:

   ```bash
   python3 <skill dir>/check_writing_rules.py <paths>
   ```

3. Read the target for the rules the linter cannot judge: paragraph structure (topic,
   support, conclusion), old → new flow, specific reference words, hedging matched to the
   evidence, linking words used with intent, definitions on first use, figures referenced
   before they appear, domain and method reasoning kept apart, no known background.
4. Merge into one numbered list, `[SEVERITY] file:line: issue (rule N.N) → fix`, ordered by
   severity then line. End with the count by severity, the three most frequent rules, and
   the reminder that `/polish-write <chapter> "fix items ..."` applies fixes one edit at a
   time.

Do not edit files.
