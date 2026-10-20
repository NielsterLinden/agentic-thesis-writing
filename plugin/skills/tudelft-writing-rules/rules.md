# Writing rules

A condensed set of academic-writing conventions in the TU Delft tradition, as used for an
MSc thesis in experimental physics and machine learning. They are numbered so that reviews
can cite them. They are a personal condensation, not an official document: check the
current guidelines of your faculty and edit this file where they differ.

The reader is a specialist in your field who has not followed your project. Write for that
person.

---

## 1. Core principles

**Do**

- 1.1 Write one section per topic.
- 1.2 Keep sentences short and direct.
- 1.3 Prefer clarity over sophistication.
- 1.4 Use informative headers and subheaders.
- 1.5 Use bold or italics sparingly, to mark a key concept on first use.
- 1.6 Use illustrations, diagrams, tables and plots whenever they improve understanding.
- 1.7 Explain symbols, abbreviations and notation on first use.
- 1.8 Keep a clear logical structure: paragraph → section → chapter.
- 1.9 Use precise, concise academic language with an objective, formal tone.
- 1.10 Prefer active voice with impersonal subjects: "The model learns pairwise
  correlations", not "It is learned by the model that".
- 1.11 Hedge claims that are not established: "These results suggest", "The architecture
  appears to benefit from".
- 1.12 Keep terminology consistent throughout the thesis: one term per concept.

**Do not**

- 1.13 Do not write long, overloaded sentences.
- 1.14 Do not overuse "I", "we" or "you". First-person singular is avoided; "we" is
  acceptable for choices the author made.
- 1.15 Do not use unnecessarily complex vocabulary or legalistic language.
- 1.16 Do not use colloquial language, slang, idioms or clichés.
- 1.17 Do not make absolute claims without evidence.
- 1.18 Do not use vague quantifiers without supporting numbers ("works very well",
  "significant improvement").

---

## 2. Scientific style

- 2.1 Separate domain-motivated reasoning from method-motivated reasoning. One paragraph
  argues from the physics (or the application); another argues from the model or the
  statistics. Do not interleave them sentence by sentence.
- 2.2 Quantify claims: the metric, the baseline, the uncertainty, the number of seeds or
  samples, the cost (parameters, FLOPs, wall-clock) when it matters.
- 2.3 Frame every experiment as a controlled comparison: what changed, what was held fixed,
  which metric was evaluated, how seeds were treated.
- 2.4 State confounders and limitations explicitly, once, in the place the reader expects
  them (the chapter-level *Limitations* paragraph).
- 2.5 Never invent a number. A value that is not yet in an evidence note is written as
  `\todo{value pending}`.
- 2.6 Do not make absolute claims ("proves", "always", "never", "clearly", "obviously").
  Evidence supports; it does not prove.
- 2.7 Do not anthropomorphize models ("the model understands", "the network knows", "the
  attention learns to focus"). Models compute, fit, assign, weight, reduce.
- 2.8 Do not imply causation without a controlled comparison. "X improves Y" needs the
  comparison where only X changed.
- 2.9 Do not oversell ("state of the art", "dramatically", "remarkable").
- 2.10 Prefer noun-form titles: "Physics-Informed Attention Biases", not "Investigating
  Biases".

---

## 3. Sentence level

- 3.1 Keep subject and verb close together. A sentence over about 40 words is usually two
  sentences.
- 3.2 Use linking words deliberately, and only when the logical relation is real:

  | Relation | Linking words |
  |---|---|
  | addition | furthermore, moreover, additionally, in addition |
  | cause and effect | therefore, consequently, thus, hence |
  | reason | because, since, owing to |
  | contrast | however, although, whereas, in contrast |
  | comparison | similarly, likewise |
  | example | for example, such as |

- 3.3 Replace multi-word verbs with single verbs: "investigate" not "look into";
  "demonstrate" not "show up as"; "perform" not "carry out".
- 3.4 Prefer concise phrasing: "most" not "the majority of"; "to" not "in order to";
  "several" not "a number of"; "because" not "due to the fact that".
- 3.5 Do not start a sentence with a coordinating conjunction (FANBOYS: for, and, nor, but,
  or, yet, so).
- 3.6 Do not use vague intensifiers ("very", "extremely", "greatly", "really", "a lot").
  Give the number instead.
- 3.7 Do not start a sentence with "There is" or "There are" unless unavoidable.
- 3.8 Do not use phrasal verbs ("set up", "look into", "carry out", "find out", "point
  out", "end up", "turn out").
- 3.9 Do not use em dashes or en dashes in prose. Recast the sentence: a colon, a comma, a
  semicolon, or two sentences. (Hyphens in compound words and in identifiers are fine.)
- 3.10 Do not use contractions.
- 3.11 Do not use rhetorical or direct questions in body prose.
- 3.12 Do not use legalistic vocabulary ("forthwith", "henceforth", "hereof", "thereof",
  "herein", "aforementioned").

---

## 4. Paragraph structure

Every paragraph contains:

- 4.1 a **topic sentence**: one clear idea;
- 4.2 **supporting sentences**: each explains, defines, justifies, contrasts, exemplifies or
  extends the topic sentence directly;
- 4.3 a **concluding sentence**: summarises the paragraph and, optionally, transitions to
  the next.

Further:

- 4.4 Maintain old → new information flow: a sentence starts from what the reader already
  has and ends with what is new. Use specific reference words ("this mechanism", "this
  procedure") instead of a bare "this" or "it".
- 4.5 Start a new paragraph when the topic changes. Do not mix unrelated ideas in one
  paragraph. Do not write one-sentence paragraphs unless intentional.
- 4.6 Do not pad. A paragraph that restates the chapter intro, or a caption that repeats the
  surrounding prose, is cut.

---

## 5. Document structure

- 5.1 Hierarchy depth: chapter → section → subsection. No deeper. (`\paragraph{}` anchors
  such as *Hypothesis.* or *Limitations.* are labels inside a subsection, not a level.)
- 5.2 Every chapter opens with a short introduction stating what the chapter covers, how it
  is structured, and which question it answers.
- 5.3 Do not create a subsection hierarchy with a single child.
- 5.4 Global structure: front matter (preface, summary, contents, lists), body
  (introduction, chapters, conclusion), back matter (references, appendices).
- 5.5 Each results chapter maps to one question, one set of factors, one evaluation lens,
  and is itself a mini-thesis: framing, shared setup, focused experiments, synthesis.
- 5.6 Do not introduce a concept without contextual framing; do not re-explain a concept
  already introduced in an earlier chapter.

---

## 6. The introduction

In this order:

1. 6.1 General domain and method context.
2. 6.2 Current state of the field.
3. 6.3 The research gap.
4. 6.4 Thesis statement and deliverables.
5. 6.5 Reader's guide.

The introduction motivates the problem in the domain, motivates the method challenge
structurally, and explains why the thesis' framework matters. It is not a textbook review.

---

## 7. Figures, tables and references

- 7.1 Use figures whenever they improve comprehension; prefer schematics over dense prose.
- 7.2 Write self-contained captions: a reader who sees only the figure and its caption
  understands what is plotted, for which configuration, with what uncertainty.
- 7.3 Reference every figure and table in the text before it appears.
- 7.4 Interpret every figure in the text. No decorative figures.
- 7.5 Keep notation identical between figures and text.
- 7.6 Figures enter the document through the project's figure-import procedure; paths are
  of the form `figures/ch<N>/<YYYYMMDD-HHMMSS>_<slug>/<file>.pdf`. Titles live in captions,
  never inside the plot.
- 7.7 Cite with the project's citation style (IEEE numeric by default) consistently.
  Introduce a cited work on first mention ("Vaswani et al. introduced ..."); reuse the key
  thereafter.
- 7.8 Define every symbol on first use, in the text and in the nomenclature.

---

## 8. Thesis-specific discipline

- 8.1 If the project keeps an identifier registry, name every studied factor by its
  registered compact ID in `\texttt{}` on every mention, spelled exactly as registered.
- 8.2 Mention a configuration key only when it is the sole unambiguous identifier of a
  choice.
- 8.3 Distinguish design, training protocol and evaluation protocol. Do not mix training
  hyperparameters with design conclusions.
- 8.4 Treat tracked results as experimental evidence, not anecdotes: every result claim
  traces to an evidence note with status `run-complete` or `interpreted`.
- 8.5 Do not discuss a result without specifying task, baseline, metric and seed treatment.
- 8.6 Write with reproducibility in mind: run identifiers and configuration names belong in
  evidence notes and, where the reader needs them, in the text.
- 8.7 Do not write generic background the specialist reader already has.

---

## 9. Tone

Write as a careful experimentalist explaining controlled experiments to a peer: technical,
precise, restrained, analytical, readable, oriented to the domain.

---

## 10. The hedge ladder

Match the verb to the evidence.

| Evidence | Verb or phrase |
|---|---|
| established, textbook | is, has, does |
| this thesis, several seeds, controlled | shows, demonstrates, reduces by |
| this thesis, few seeds, or one control missing | suggests, indicates, is consistent with |
| a trend at the resolution limit | appears to, tends to, may |
| speculation | could, might, one possible explanation is |

A result within the seed spread is "indistinguishable from the baseline at this seed
budget", not "slightly better".

---

## 11. Vocabulary discipline

- 11.1 One canonical term per recurring concept; record the choices in a glossary (the
  nomenclature, or a *Vocabulary* section in `AGENTS.md`). Typical pairs to fix early:
  "seed spread" versus "variance across seeds"; "baseline" versus "reference"; "metric
  delta" versus "metric range".
- 11.2 Abbreviations: spell out on first use in the body, then abbreviate. Do not define
  twice. Do not abbreviate in headings.
- 11.3 Numbers: digits with units; thin space or `\,` before units; consistent decimals per
  metric across chapters.
