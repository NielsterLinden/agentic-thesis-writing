# agentic-thesis-writing: design

Date: 2026-10-20. Status: implemented in v0.1.0.

## Intent

Turn the agent setup of one MSc thesis (a research agent and a writing agent with disjoint
scopes, connected by evidence notes and handoff notes; LaTeX in the repository; TU Delft
writing rules; late-stage finalize and polish agents; a Manim-based defence deck) into a
public kit that another person installs by giving their coding agent one sentence.

## Goals

- An agent can install the kit into an arbitrary thesis repository, non-destructively,
  following a phased procedure with gates.
- The research/writing boundary and the handoff notes are the centre of the design; the
  docs explain why, not only how.
- The TeX lives in the repository, builds anywhere (font and asset fallbacks), and the
  agents compile it and read the log.
- The writing rules ship as a numbered file plus a linter for the mechanical rules.
- The presentation path links to manim-hep rather than duplicating its agents.
- Nothing project-specific remains: no paths, hosts, usernames, identifiers or numbers
  from the original thesis.

## Non-goals

- A pip package or a service. Standard-library scripts copied into the target repository
  are enough.
- Replacing manim-hep's animation agents.
- Supporting every agent tool natively. Claude Code is first-class; others get
  `AGENTS.md`, the skills folder and paste-able commands.

## Anti-goals

- An agent that can both run analyses and write prose. The split is the product.
- Silent overwrites during install.
- A kit that only compiles with proprietary fonts or with the TU Delft logos present.

## Constraints

- The LaTeX template is CC BY-NC 4.0; it stays in one folder with its own licence, and the
  logos and cover are fetched, not stored.
- Publication safety as in manim-hep: no private paths, hosts, names, media or files over
  1 MB; a hygiene script enforces it in CI.
- No dashes in the kit's own prose, since the kit preaches that rule.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Project configuration | a *Project map* table in the installed `AGENTS.md` | readable by every agent tool; one place; no new file format |
| Agent names | `researcher`, `thesis-writer`, `reviewer`, `thesis-finalizer`, `thesis-polisher`, `writing-rules-checker`, `deck-planner` | the original `experiment-coder` was too specific; `researcher` names the role |
| Identifiers | optional registry; `trace-claim` skill | the original axis system was essential there and absent elsewhere |
| Scaffold anchors | `Lens.`, `Factors.`, `Hypothesis.`; `Domain conclusion.`, `Method conclusion.`, `Limitations.`, `Bridge.` | generic names for the physics/ML pair; mandatory set unchanged |
| Entry-point letters | kept (D, C, E, B, A) with names | continuity with the origin; names carry the meaning |
| Linter | regex over comment-stripped, environment-filtered, macro-masked text | catches the mechanical rules with line numbers; no dependency |
| Figure import | a script, not prose | deterministic destination and provenance |
| Install | `scripts/atw.py install` with `.atw.new` conflicts | mirrors manim-hep's `init`; never overwrites |
| Plugin | marketplace at the root, plugin in `plugin/` | the same layout as manim-hep; `claude plugin validate --strict` passes |
| Presentation | `deck-planner` plus templates; animation by manim-hep | one owner for the animation toolchain |

## Left to the builder (and done)

- The exact word lists in the linter.
- The wording of the docs.
- The worked example (synthetic).
- CI: tests and hygiene, plugin validation, a LaTeX build of the template.
