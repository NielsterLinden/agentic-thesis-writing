# Writing rules

The full rule set is one file, numbered so that reviews can cite it:

**[`plugin/skills/tudelft-writing-rules/rules.md`](../plugin/skills/tudelft-writing-rules/rules.md)**

The installer places it under `.claude/skills/tudelft-writing-rules/` (or
`.agents/skills/`), where `thesis-writer` reads it before drafting, `reviewer` grades
against it, `thesis-finalizer` and `thesis-polisher` inherit it, and
`writing-rules-checker` applies it.

## What the rules say, in one screen

| Area | Rule |
|---|---|
| Sentences | short; subject near verb; active voice with impersonal subjects; linking words on purpose; single verbs instead of phrasal ones; no contractions; no sentence-initial FANBOYS; no "There is"; no intensifiers; no em or en dashes; no rhetorical questions |
| Paragraphs | topic sentence, support, concluding sentence; one idea; old → new flow; specific reference words; no one-sentence paragraphs |
| Science | quantify (metric, baseline, uncertainty, seeds); controlled-comparison framing; domain and method reasoning kept apart; confounders stated once; hedge to the evidence; no anthropomorphism; no absolutes; no overselling; never invent a number |
| Structure | chapter → section → subsection, no deeper; every chapter opens with what, how, which question; results chapters are mini-theses; introduction in a fixed order |
| Figures | referenced before they appear; self-contained captions; interpreted in text; notation matches; timestamped paths; titles in captions, not in plots |
| Vocabulary | one term per concept; abbreviations defined once; registered identifiers spelled exactly |
| Tone | a careful experimentalist explaining controlled experiments to a peer |

## The hedge ladder

| Evidence | Verb |
|---|---|
| established | is, has |
| this thesis, several seeds, controlled | shows, demonstrates |
| few seeds, or a control missing | suggests, indicates, is consistent with |
| at the resolution limit | appears to, tends to, may |
| speculation | could, might, one possible explanation is |

## The linter

```bash
python3 plugin/skills/tudelft-writing-rules/check_writing_rules.py thesis/mainmatter/ [--json] [--fail-on MINOR]
```

It catches the mechanical rules (dashes, contractions, FANBOYS, phrasal verbs,
intensifiers, legalisms, questions, anthropomorphism, absolutes, first person, one-sentence
paragraphs, heading depth, single-child sections, long sentences, wordy phrases, flat
figure paths, pending `\todo{}`), with the rule number and a one-line fix. It skips
comments, math and non-prose environments. A clean run is necessary, not sufficient: the
rules that matter most need a reader, which is what `/check-writing` and `/review-section`
are for.

## Provenance and adaptation

The rules condense the academic-writing conventions taught in the TU Delft tradition and
the house conventions of one thesis. They are not an official TU Delft document; your
faculty's current guidelines take precedence. To adapt: copy the skill folder to a
sibling, edit `rules.md`, adjust the word lists at the top of the linter, and point the
Project map's *Writing rules skill* at it. Contributions of other rule sets are welcome
(see `CONTRIBUTING.md`).
