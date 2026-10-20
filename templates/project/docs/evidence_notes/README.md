# docs/evidence_notes/

Structured hand-off artefacts from `researcher` (author) to `thesis-writer` (reader). One
markdown file per (thesis section, topic). The template and the status state machine live in
the `evidence-note` skill.

## Naming

```
<chN.S>_<slug>.md
# e.g. ch4.2_tokenizer.md, ch6.3_attention-type.md
```

If a section needs a regenerated run, version the file as `<chN.S>_<slug>-v2.md` rather
than overwriting.

## Lifecycle

```
triaged  →  run-pending  →  run-complete  →  interpreted
```

- `researcher` creates the file at `triaged` after `data-inventory`, advances it through
  `run-pending` and `run-complete`.
- `thesis-writer` flips it to `interpreted` once the corresponding `.tex` is updated.

## Rules

- Do not invent metrics. Leave `<TBD>` until a run produces the number.
- Record *Reused vs new code* so bespoke analyses can be audited.
- Do not delete a note. Supersede with `-vN` and link the old one.
- New note: `python3 scripts/atw.py new-note <chN.S> <slug> --title "<title>"` (if the kit's
  scripts are installed) or copy the skill's `template.md`.
