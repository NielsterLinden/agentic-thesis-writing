---
description: "Structural last-pass rewrite of one section, staged as a critique plus a proposed rewrite under docs/finalizer/; applied to the chapter only when the user types the literal word \"apply\". Runs the thesis-finalizer agent."
argument-hint: "<chN.Y> [setup|discussion]"
---

Invoke the `thesis-finalizer` subagent for `$ARGUMENTS` (chapter and section number, with an
optional disambiguator). If subagents are unavailable in this tool, read
`.claude/agents/thesis-finalizer.md` (or the plugin's `agents/thesis-finalizer.md`) and act
as that agent yourself.

Procedure:

1. Read `AGENTS.md`, `rules.md` from the writing-rules skill, `thesis-writer.md` and
   `reviewer.md`. Stop if any is missing.
2. Resolve the section's role (Template A per-experiment, B chapter setup, C chapter
   discussion) from its position, or from the disambiguator.
3. Read the whole chapter, the cited figures (as PDFs), the cited tables, and the rendered
   PDF over the section's pages (build first if the PDF is stale).
4. Write `docs/finalizer/ch<N>.<Y>/<YYYYMMDD-HHMMSS>/critique.md` and
   `proposed_rewrite.tex`. Preserve every `\label`, `\cite`, `\ref` and `\includegraphics`
   verbatim. Never invent or change a number; flag disagreements with figures for
   `researcher`.
5. Iterate in chat, overwriting the two staged files in place.
6. On the user's literal `apply`: archive the chapter to `mainmatter/_archive/`, splice the
   rewrite, build, run the dash audit, report the word-count delta. Do not roll back on a
   failed build; report and wait. Apply at most once per conversation.

Hard rules: never read evidence notes; never touch research directories, other chapters,
the preamble, front matter, the class file or the `.bib`.
