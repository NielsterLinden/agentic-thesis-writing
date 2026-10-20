# Handoff: {{TITLE}}

- Status: open
- Date: {{DATE}}
- Agents: <researcher | thesis-writer | reviewer | thesis-finalizer | thesis-polisher | user>
- Files to edit: <paths>

> Read this file end-to-end before doing anything. The companion plan (if any) is
> `<path>`; read it when you need detail.

## TL;DR

<Three to six lines: what is being done, why, and what the target state is.>

## How to resume

| You are starting at... | Do this |
|---|---|
| Fresh session, nothing executed | Read this file. Run the invocation in *Agent invocations §1*. |
| `<observable state, e.g. docs/evidence_notes/<note>.md has Status: run-complete>` | <next action> |
| `<observable state>` | <next action> |
| You want to change a decision | Edit *Locked decisions* first, then update this file, then continue. |

## The roadmap

| # | Owner | Action | Inputs | Outputs | Gate / risk |
|---|---|---|---|---|---|
| 1 | researcher | <...> | <...> | <...> | <...> |
| **1.5** | **USER** | <checkpoint: review X> | <...> | verbal go-ahead | agent STOPS here |
| 2 | thesis-writer | <...> | <...> | <...> | build must pass |
| 3 | reviewer | <...> | <...> | review | read-only |

## Locked decisions

| D# | Topic | Choice |
|---|---|---|
| D1 | <...> | <...> |

## Agent invocations

### §1. researcher (steps 1 to N)

```
Read docs/handoffs/{{DATE}}_{{SLUG}}.md end-to-end before doing anything.

START AT STEP 1: <...>.
If <failure condition>: STOP and escalate.
If clean: continue through steps 2 to N in strict sequence.
At step <k>: <dry run only>. STOP and wait for the user.

Constraints:
- DO NOT touch the thesis directory.
- DO NOT commit anything.
- All generated outputs land under the data root; use figure-import to promote figures.

When done, send one summary under 300 words: artefacts produced, paths, evidence-note
status, files modified.
```

### §2. thesis-writer (steps N+1 ...)

**Only after the user checkpoint at step <k>.**

```
Read docs/handoffs/{{DATE}}_{{SLUG}}.md end-to-end before doing anything.
<instructions>
Constraints:
- DO NOT edit code, configs or scripts.
- DO NOT commit anything.
- Build with the project build command before finishing.
```

## If something breaks

<Known failure mode> → options:

- **A.** <...> (pro / con)
- **B.** <...> (pro / con), *recommended*
- **C.** <...> (pro / con)

## Files of interest

| File | Role |
|---|---|
| `docs/handoffs/{{DATE}}_{{SLUG}}.md` | this file (orchestration) |
| <plan> | full specification |
| <evidence notes> | provenance |

## FAQ

**Q:** <...>
**A:** <...>

## Changes

- {{DATE}}: created.
