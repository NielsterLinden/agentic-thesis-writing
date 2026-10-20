---
description: Plan the defence talk from the thesis: three-act storyline, slide list, a provenance manifest for every number and figure on a slide, and per-clip briefs for manim-hep. Runs the deck-planner agent; never edits the thesis.
argument-hint: [talk length in minutes] [chapters to cover]
---

Invoke the `deck-planner` subagent for `$ARGUMENTS` (default: a 25-minute talk covering
every chapter). If subagents are unavailable in this tool, read
`.claude/agents/deck-planner.md` (or the plugin's `agents/deck-planner.md`) and act as that
agent yourself.

Procedure (the `thesis-to-deck` skill):

1. Read `AGENTS.md`; confirm `presentation/` exists (the installer creates it with
   `--with-presentation`; otherwise create `presentation/` with the kit's
   `templates/presentation/` files first).
2. Read every chapter intro and chapter-level Discussion, the conclusion, and the
   *Thesis-safe interpretation* of every `interpreted` evidence note.
3. Write `presentation/STORYLINE.md` (Why / How / So what; beats tagged
   `clip | plot | figure | spoken`), `presentation/SLIDELIST.md`, and
   `presentation/PATHS.md` (every on-slide number and figure with its source and status;
   a number without an evidence note is `[BLOCK]`).
4. Write one brief per clip under `presentation/storylines/`, from the skill's
   `storyline_template.md`.
5. Check whether manim-hep is installed (`manim-hep doctor`). If so, name the brief to hand
   to `scene-builder` or `plot-recreator`; if not, print the manim-hep install sentence.

Rules: animation only, no narrative text in clips; numbers from evidence notes only;
recreate or import, logged; never edit the thesis to make a slide easier.

End with the files written, the clip count, the number of `[BLOCK]` rows, and the next
manim-hep invocation.
