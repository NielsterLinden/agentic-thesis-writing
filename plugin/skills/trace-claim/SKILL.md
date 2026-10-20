---
name: trace-claim
description: "Verify that a thesis claim traces through identifier → configuration → implementation → run or result → metric → interpretation → limitation, and return a status table. Use before writing any design claim (thesis-writer) and before adding or changing a config or analysis (researcher)."
---

# trace-claim

A claim in the thesis is only as good as its chain. This skill forces the chain to be
written down before the claim is.

```
claim → identifier → config key → implementation → run group / result → metric → interpretation → limitation
```

## Inputs

One of: a compact identifier from the registry (if the project keeps one), a thesis section
path, a config-key fragment, or a sentence from the draft.

## Procedure

1. **Identifier.** If the project has an identifier registry (named in `AGENTS.md`), look
   the identifier up. An ID that is not in the registry does not go into prose; flag it.
2. **Config key.** Find the configuration key that selects the option. Confirm the spelling
   against the registry.
3. **Implementation.** Find the code that consumes the key. Confirm that what the code does
   matches what the registry and the claim say it does. Do not paper over a mismatch.
4. **Result.** Find the evidence note (and through it the run group and the canonical table
   rows) that carries the number or the figure. Check the note's `Status`.
5. **Metric and interpretation.** Confirm that the metric named in the claim is the metric
   in the note, with the same seed treatment, and that the interpretation is within what
   the note's *Thesis-safe interpretation* supports.
6. **Limitation.** Name the confounder from the note that bounds the claim.

## Output

```
| Claim | ID | Config key | Implementation | Evidence note (status) | Metric | Status |
|---|---|---|---|---|---|---|
| "<claim>" | T1 | model.tokenizer.name | src/.../tokenizer.py | ch4.2_tokenizer.md (run-complete) | AUROC, n=3 | supported |
```

`Status` is one of `supported`, `partially supported`, `unsupported`, `unclear`. Anything
other than `supported` goes back to the user (writer) or into the evidence note's
*Confounders* (researcher) before the claim is written.

## Without a registry

Projects without a registry skip step 1; the chain then starts at the config key or the
analysis script. The output table drops the `ID` column. Consider adding a registry once the
thesis names more than a handful of recurring factors: a markdown table of
`ID | name | config key | options | implementation path` is enough, and it is the single
place where renames happen.
