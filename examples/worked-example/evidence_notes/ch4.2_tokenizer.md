# Evidence note: ch4.2: tokenizer (Tokenizer family)

> **Synthetic example.** All numbers below are invented to illustrate the note's shape.

- Status: interpreted
- Entry point: C
- Inventory snapshot:
    - `exp_20260510-091200_ch4_tokenizer`: checkpoint ✓ (12/12), results ✓ (12/12 rows in the canonical table), figures ✗
- Identifiers covered: T1 (tokenizer family), R5 (seed)
- Config keys: `model.tokenizer.name` ∈ {`raw`, `binned`, `learned`, `identity`}; `trainer.seed` ∈ {42, 123, 314}
- Tracker keys: `axes/tokenizer_name`, `axes/seed`
- Run group(s): `exp_20260510-091200_ch4_tokenizer` (tracker group and directory name)
- Output path: `<data root>/reports/report_20260519-114923_ch4_tokenizer/`
- Action staged:
    - Local:  `python -m pkg.reports.compare --group exp_20260510-091200_ch4_tokenizer --metric test_auroc --out <data root>/reports/report_20260519-114923_ch4_tokenizer/`
- Metrics tracked: test AUROC (primary); parameter count (secondary)
- Result summary:
    - `identity` 0.841 ± 0.001 (n=3); `raw` 0.839 ± 0.002 (n=3); `binned` 0.826 ± 0.002 (n=3); `learned` 0.831 ± 0.003 (n=3)
    - `identity` and `raw` are indistinguishable at this seed budget (delta 0.002, seed spread 0.001 to 0.002)
    - `binned` sits 0.015 below `identity`, about seven seed spreads
- Plot paths:
    - thesis/figures/ch4/20260519-114923_tokenizer/ch4_T1_auroc_bar_tokenizer.pdf ← <data root>/reports/report_20260519-114923_ch4_tokenizer/ch4_T1_auroc_bar_tokenizer.pdf
    - thesis/figures/ch4/20260519-114923_tokenizer/ch4_T1_roc_tokenizer.pdf ← <data root>/reports/report_20260519-114923_ch4_tokenizer/ch4_T1_roc_tokenizer.pdf
    - thesis/figures/ch4/20260601-161946_tokenizer/ch4_T1_auroc_bar_tokenizer.pdf ← <data root>/reports/report_20260601-161946_ch4_tokenizer/ch4_T1_auroc_bar_tokenizer.pdf
    - thesis/figures/ch4/20260601-161946_tokenizer/ch4_T1_roc_tokenizer.pdf ← <data root>/reports/report_20260601-161946_ch4_tokenizer/ch4_T1_roc_tokenizer.pdf
- Active figures: thesis/figures/ch4/20260601-161946_tokenizer/
- Figure compliance: PLOTTING_STYLE.md OK (chapter band 0.800 to 0.850; seed dots; `n=` inside bars)
- Reused vs new code:
    - Reused: `pkg/reports/compare.py` (bar and ROC plots), `pkg/reports/style.py`
    - New:    none
- Confounders / limitations:
    - n=3 seeds per cell; deltas below 0.003 are at the noise floor.
    - The `learned` tokenizer was trained with the same epoch budget as the others; it may be under-trained relative to its parameter count.
    - All cells share the data treatment fixed in ch4.1; interactions with that factor are not tested here.
- Thesis-safe interpretation:
    > The tokenizer family has a small but resolvable effect on test AUROC at this seed budget. The `identity` and `raw` tokenizers are indistinguishable (0.841 versus 0.839, within the seed spread), whereas the `binned` tokenizer lies 0.015 below them, about seven seed spreads, which suggests that discretising the continuous features removes information the classifier uses. The `learned` tokenizer recovers part of that gap (0.831) but not all of it under the shared epoch budget; whether a longer schedule would close the gap is open.

## Log

- 2026-05-19: created at `triaged`; `data-inventory` found 12 checkpoints and 12 result rows; entry point C (D rejected: no existing comparison figure; E, B, A not needed).
- 2026-05-19: local run complete; two figures imported; `run-complete`.
- 2026-05-20: `thesis-writer` drafted §4.2; `interpreted`.
- 2026-06-01: figures reworked (parameter count on the x-axis, log scale); re-imported into a new timestamped directory; `Active figures` updated; handoff to the writer for the path and caption changes (`docs/handoffs/2026-10-20_ch4-figure-rework.md` in this example).
