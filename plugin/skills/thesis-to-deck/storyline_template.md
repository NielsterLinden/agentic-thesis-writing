# Clip brief: {{CLIP_NAME}}

Compatible with the manim-hep `hep-storyline` format. One file per clip.

- Slide(s): <numbers from SLIDELIST.md>
- Act and beat: <Why | How | So what> / <beat>
- Draws on: <chapter and section>; evidence note(s): <docs/evidence_notes/...>
- Kind: <schematic | recreated plot | imported figure with callouts>
- Duration target: <seconds>
- Chained with: <previous clip> → this → <next clip> (or "standalone")

## Beats

| t (s) | What appears or moves | Why (the spoken point) |
|---|---|---|
| 0.0 | <...> | <...> |
| 2.5 | <...> | <...> |
| end | held final state | <...> |

## On-screen text whitelist

Only these strings may appear in the clip (symbols, units, tick labels, identifiers).
Everything else is added in the slide tool.

- <e.g. `p_T`, `η`, `AUROC`, `n = 3`>

## Numbers

Every number shown traces to an evidence note. Schematic values are marked as such.

| Value | Shown as | Source | Note status |
|---|---|---|---|
| <0.84> | <bar height> | <docs/evidence_notes/ch4.2_tokenizer.md §5> | interpreted |
| <schematic> | <curve shape> | seeded synthetic, declared schematic | n/a |

## Data (recreated plots only)

- File: <frozen extract, e.g. presentation/data/ch4_tokenizer.json>
- Filter: <rows selected from the canonical table>
- Aggregation across seeds: <median | mean ± std>, per the thesis chapter
- Anchor values the recreation must reproduce: <list>

## Final-frame checklist

- [ ] title band (top of frame) clear
- [ ] clip rests on a clean held state
- [ ] colours and font from the presentation style module
- [ ] no narrative text
- [ ] numbers match the table above
