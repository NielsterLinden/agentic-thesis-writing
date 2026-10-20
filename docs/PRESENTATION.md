# Presentations

A defence talk follows the thesis. The same evidence that grounded the chapters grounds
the slides, and the same boundary applies: the plan is written from the thesis, the
animations are built from the plan, and nobody edits the thesis to make a slide easier.

## Pieces

| Piece | Where | Who |
|---|---|---|
| the plan: storyline, slide list, provenance manifest, clip briefs | `presentation/` | `deck-planner` (`/deck-storyline`), the `thesis-to-deck` skill |
| the animations | scenes and clips, rendered in an isolated environment | [manim-hep](https://github.com/NielsterLinden/manim-hep): `scene-builder`, `plot-recreator`, `render-verifier`, `physics-checker` |
| the deck | your slide tool | you |

manim-hep is a separate kit: high-energy-physics building blocks for Manim Community
Edition plus agents and skills that plan a clip, build it on tested components, render it,
inspect the frames and deliver an MP4. Its storyline format is what the briefs here follow,
so a brief written by `deck-planner` is a valid input to manim-hep's `scene-builder`.
Install it with its one-sentence quick install:

> Set up manim-hep in this repository: follow https://github.com/NielsterLinden/manim-hep/blob/main/docs/install/AGENT_INSTALL.md, and ask me the setup questions first.

## Rules carried over from the thesis

- **Animation only.** Clips contain no narrative text (titles, captions, bullets, labels).
  You add text in the slide tool, where you control wording and font. Symbols, units, tick
  labels, numbers on data plots and a registered identifier labelling a mechanism are
  exempt.
- **Numbers from evidence notes.** `PATHS.md` lists every on-slide number and figure with
  its note or figure directory. A number without a note is `[BLOCK]`.
- **Recreate or import, logged.** Simple bars, curves, points: recreate natively so the
  clip can animate them, and assert the recreation against the anchor values in `PATHS.md`.
  Dense plots and large tables: import the thesis PDF and animate callouts.
- **One style module**, ported once from the thesis plotting style; never a hardcoded hex
  in a scene.
- **Clips end on a held state** and keep the top band clear for the title.

## Two practical notes from the original project

- When a clip's final frame is rebuilt as editable shapes in the slide tool, sample the
  colour from the decoded video frame rather than the source hex: video compression shifts
  colours by a few units, and the shapes should match what the viewer saw a second earlier.
- Render the animation tool in its own environment. Adding it to the research environment
  has broken more than one training setup.

## Flow

1. Thesis chapters reach `interpreted` evidence notes.
2. `/deck-storyline 25` writes the storyline, slide list, manifest and briefs.
3. You adjust the title-band wording and the beat order.
4. manim-hep's `scene-builder` or `plot-recreator` builds each clip from its brief;
   `render-verifier` and `physics-checker` close the loop.
5. You assemble the deck; the clips rest on their last frame.
