# PATHS: provenance manifest

Every number and every figure that appears on a slide, with where it comes from. A number
without an evidence note is `[BLOCK]`: the slide is not built until the note exists.

- Repository root: `<path>`
- Thesis directory: `<thesis>/`
- Evidence notes: `docs/evidence_notes/`
- Last verified: <date>

## Numbers on slides

| Slide | Value | Shown as | Source (note § or table) | Note status | Check |
|---|---|---|---|---|---|
| 12 | <0.84 ± 0.01, n=3> | bar height | `docs/evidence_notes/<note>.md §5` | interpreted | ok |
| 14 | <...> | callout | `docs/evidence_notes/<note>.md §5` | run-complete | `[BLOCK]`: note not interpreted |

## Figures on slides

| Slide | File | Directory | Recreate or import | Why |
|---|---|---|---|---|
| 10 | `ch4_T1_roc.pdf` | `<thesis>/figures/ch4/<ts>_tokenizer/` | recreate | three curves; animates well |
| 15 | `ch7_pareto.pdf` | `<thesis>/figures/ch7/<ts>_scaling/` | import | dense log-log; callouts only |

## Anchors for recreated plots

Values a recreation must reproduce before the clip is delivered.

| Clip | Quantity | Anchor | Source |
|---|---|---|---|
| `<name>` | <baseline metric> | <0.8063> | `docs/evidence_notes/<note>.md §5` |
