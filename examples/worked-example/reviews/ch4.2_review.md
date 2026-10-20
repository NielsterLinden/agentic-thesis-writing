# Review: §4.2 Tokenizer family (`thesis/mainmatter/04_input_representation.tex`)

> **Synthetic example** of `reviewer` output, saved at the user's request.

[MAJOR] Location: 04_input_representation.tex: §4.2 Setup, `\paragraph{Lens.}`
Issue: Two lenses are declared (performance, efficiency) but the Discussion gives a verdict only for performance.
Suggestion: Add one sentence on the efficiency lens (parameter count versus AUROC) or drop the lens from Setup (rule 5.5; scaffold check 5).

[MAJOR] Location: 04_input_representation.tex: §4.2 Discussion, second paragraph
Issue: "Binning removes the information the classifier needs" states a cause; the design only varies the tokenizer and cannot separate information loss from under-training.
Suggestion: Hedge to "suggests that discretising ... removes information" as in the evidence note, and name the epoch-budget confounder (rule 2.8).

[MINOR] Location: 04_input_representation.tex: §4.2 Results, first sentence
Issue: Sentence starts with "But".
Suggestion: Join to the previous sentence with "whereas" (rule 3.5).

[MINOR] Location: 04_input_representation.tex: §4.2 Results, Figure 4.1 caption
Issue: Caption says "see text" instead of describing the error bars.
Suggestion: State "error bars are the seed spread (n=3)" in the caption (rule 7.2).

[MINOR] Location: 04_input_representation.tex: §4.2 Setup, `\paragraph{Factors.}`
Issue: Identifier written as `T01`.
Suggestion: Use the registered compact form `T1` (rule 8.1).

[NOTE] Location: 04_input_representation.tex: §4.2 intro, last sentence
Issue: "A number of runs" where the count is known.
Suggestion: "Twelve runs" (rule 3.4).

Counts: BLOCK 0, MAJOR 2, MINOR 3, NOTE 1.

### Cuts and condensations

- §4.2 Results, paragraph 2: the three sentences restating the bar heights duplicate Table 4.2 (≈ 4 lines saved).
- Figures 4.1 and 4.2 could share one float with `subfigure` (≈ half a page saved).

### Section grade

1. Writing style: 4. Clean apart from one FANBOYS start and one wordy phrase.
2. Figure quality and consistency: 4. Chapter band and seed dots present; caption incomplete.
3. Domain depth: 3. The physics reason why binning hurts is asserted, not argued.
4. Method depth: 4. Factors and options introduced clearly; efficiency lens left dangling.
5. Brevity: 3. Results restate the table; the two floats could merge.
6. Citations: 4. The learned-tokenizer reference is present; the binning convention needs one.

Total: 22 / 30: sound section; fix the dangling lens and the causal sentence, then merge the floats.
