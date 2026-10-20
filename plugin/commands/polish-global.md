---
description: Document-wide consistency scan (abbreviations, terminology, notation, identifiers, dashes, forbidden forms, cross-references, metric definitions). Read-only report; edits only when the user names items. Runs the thesis-polisher in global mode.
argument-hint: [optional chapter or topic scope]
---

Invoke the `thesis-polisher` subagent in **global mode** for `$ARGUMENTS` (no argument:
the whole document). If subagents are unavailable in this tool, read
`.claude/agents/thesis-polisher.md` (or the plugin's `agents/thesis-polisher.md`) and act
as that agent yourself.

Procedure:

1. Read `AGENTS.md`, `rules.md` from the writing-rules skill, and `reviewer.md` for the
   severity taxonomy.
2. Run the writing-rules linter over the scope to collect the mechanical findings.
3. Read every chapter file in scope (and the main `.tex` for macro and registry checks).
4. Check, document-wide: abbreviations defined before use and used consistently; one
   canonical term per concept; notation defined once; identifiers spelled as registered;
   dashes; forbidden forms; every figure and table referenced before it appears; every
   `\ref` and `\cite` resolves; metric definitions do not drift.
5. Return a numbered, severity-tagged report grouped by category, then a count by severity
   and a *canonical choices* block. **Do not edit.**

Then, only if the user replies naming items ("fix 3, 7, 12"), apply those as one focused
`Edit` each. Do not build unless asked.

Hard rules: read-only by default; never fill URL or link registries in the preamble
(report gaps); never invent or change numbers.
