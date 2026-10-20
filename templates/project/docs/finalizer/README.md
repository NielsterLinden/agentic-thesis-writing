# docs/finalizer/

Staging area for `thesis-finalizer` (`/finalize-section ch<N>.<Y>`):

```
docs/finalizer/ch<N>.<Y>/<YYYYMMDD-HHMMSS>/critique.md
docs/finalizer/ch<N>.<Y>/<YYYYMMDD-HHMMSS>/proposed_rewrite.tex
```

The critique lists `[SEVERITY/ACTION]` findings against the canonical section templates;
the proposed rewrite is a drop-in block for the section. Nothing here touches the thesis
until the user types the literal word `apply`, at which point the current chapter is
copied to `<thesis>/mainmatter/_archive/` and the block is spliced in.

Old staging directories are kept as a record of the passes.
