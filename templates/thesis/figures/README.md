# figures/

One timestamped directory per plotting run, per chapter:

```
figures/ch<N>/<YYYYMMDD-HHMMSS>_<slug>/<file>.pdf
```

Figures land here only through the `figure-import` skill, which records the source path
and the active directory in the matching evidence note under `docs/evidence_notes/`.
Existing directories are never deleted or overwritten; the evidence note's
`Active figures:` field says which directory is current.

`logo-black.pdf`, `logo-white.pdf` and `cover.jpg` are fetched by `../fetch_assets.sh`
and are ignored by git.
