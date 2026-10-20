# presentation/ scope rules

Defence-talk visuals. This directory holds the **plan** (storyline, slide list, provenance
manifest, clip briefs) and the **clips**. It does not hold a self-contained slideshow.

## Assembly model (read first)

- **The deck is built in the slide tool by the user** (PowerPoint, Keynote, Google Slides,
  Beamer). Agents produce **animation clips** (MP4, 16:9, white background) that the user
  inserts, plus the plan files.
- When a clip's final state is reusable, also hand over its **final frame** (PNG) and,
  if the toolchain supports it, the final shot as editable shapes.
- No `next_slide()` boundaries, no speaker notes, no HTML or PDF deck from the animation
  tool. Clips are continuous videos from plain scenes.

## Animation-only rule (important)

**Limit scenes and clips to animation. Do not add text unless the user explicitly asks.**
The user adds all narrative text (titles, headings, captions, bullets, section labels) in
the slide tool, where they control wording and font.

Exempt, because the symbol *is* the content: physics or domain symbols and variables,
units, axis tick labels and numeric values on data plots, and a registered identifier
labelling a depicted mechanism. When in doubt, leave the text out.

## Handoff folder

Deliver per clip to `presentation/clips/`:

- `<name>.mp4`: 1920×1080, white background;
- `<name>_last.png`: the final frame.

**Colour match:** when rebuilding a clip's final state as shapes, sample the colour from the
decoded video frame, not the source hex; video compression shifts colours slightly.

## Who does what

- `deck-planner` (this kit) writes `STORYLINE.md`, `SLIDELIST.md`, `PATHS.md` and the
  briefs in `storylines/`.
- manim-hep's agents build and check the clips from the briefs: `scene-builder`,
  `plot-recreator`, `render-verifier`, `physics-checker`. Install:
  https://github.com/NielsterLinden/manim-hep (`QUICKINSTALL.md`).
- Rendering happens in an isolated environment for the animation tool; never add it to
  the research environment.

## Data fidelity (recreated plots)

- Every number on a slide traces to an evidence note (`PATHS.md`). No numbers from memory
  or from run directories.
- Aggregation across seeds follows the thesis chapter (median or mean ± std); say which.
- Recreated values are asserted against the anchors in `PATHS.md` before a clip is
  delivered.
- Data-plot tick labels, units and values are part of the data and exempt from the
  animation-only rule; narrative titles and captions are not.

## Style

White background, 16:9. Colours and font from one presentation style module, ported once
from the thesis plotting style; never hardcoded in a scene. The top band of the frame stays
clear for the user's title. Clips end on a clean held state.

## Orientation

`STORYLINE.md` (three acts) · `SLIDELIST.md` · `PATHS.md` (provenance) · `storylines/`
(one brief per clip). The cross-tool contract is in the repository root `AGENTS.md`.
