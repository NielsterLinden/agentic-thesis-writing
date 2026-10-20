---
name: thesis-to-deck
description: "Turn finished thesis chapters and evidence notes into a defence-talk plan (three-act storyline, slide list, provenance manifest) and per-clip briefs in the manim-hep storyline format, so manim-hep's agents can build the animations. Use when planning slides, recreating a thesis figure as an animation, or checking that a number on a slide traces to an evidence note."
---

# thesis-to-deck

The talk is the thesis told in 25 minutes. The same evidence that grounded the chapters
grounds the slides; the handoff is a set of files under `presentation/` that the animation
agents of [manim-hep](https://github.com/NielsterLinden/manim-hep) can work from.

## Files

| File | What it holds |
|---|---|
| `presentation/STORYLINE.md` | three acts (Why / How / So what), the beats, which chapter each beat draws on, which beats become clips |
| `presentation/SLIDELIST.md` | one row per slide: title-band text, visual, source, spoken point |
| `presentation/PATHS.md` | the manifest: every number and figure on a slide → its evidence note or thesis figure directory, with status |
| `presentation/storylines/<clip>.md` | one brief per clip in the manim-hep storyline format (see `storyline_template.md` here) |
| `presentation/CLAUDE.md` | the assembly contract for the presentation directory (installed from the kit's template) |

## Procedure

1. **Read for the story**: chapter intros, chapter-level Discussions, the conclusion; the
   *Thesis-safe interpretation* of every `interpreted` evidence note.
2. **Storyline**: three acts, beats as one-liners, each tagged `clip | plot | figure | spoken`.
3. **Slide list**: the user writes the title-band text; you propose it, they own it.
4. **Manifest**: a row per on-slide number and figure. A number without an evidence note is
   `[BLOCK]`; the slide does not get built until the note exists.
5. **Briefs**: one per clip, from `storyline_template.md`. For a recreated thesis figure:
   the data file and filter, the aggregation across seeds (the thesis convention, usually
   the median or the mean ± std; check the chapter), and the anchor values the recreation
   must reproduce. For a schematic: say "schematic, seeded synthetic values".
6. **Hand off** to manim-hep: `scene-builder` for schematics, `plot-recreator` for
   recreated figures, `render-verifier` and `physics-checker` afterwards. If manim-hep is
   not installed, print its install sentence.

## Rules carried over from the thesis

- **Animation only.** No narrative text in clips (titles, captions, bullets, labels); the
  user adds it in the slide tool. Symbols, units, tick labels, numeric values on data plots
  and a registered identifier labelling a depicted mechanism are exempt.
- **Numbers from evidence notes**, never from memory or a run directory.
- **Recreate or import, logged.** Simple bars, curves, points: recreate (it can animate).
  Dense log-log plots, large tables: import the PDF, animate callouts.
- **Palette and font** ported once from the thesis plotting style into the presentation
  style module; never hardcoded in a scene.
- **Clips end on a held final state** and keep the title band clear.
- **Never edit the thesis** to make a slide easier.
