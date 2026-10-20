from __future__ import annotations

from pathlib import Path

import pytest

GOOD_PARAGRAPH = (
    "The model assigns a score to each event. The score separates the two classes "
    "with a margin that grows with the training set size.\n"
)


def run(linter, tmp_path: Path, text: str, **kw):
    f = tmp_path / "s.tex"
    f.write_text(text, encoding="utf-8")
    return linter.check_file(f, kw.get("figure_pattern", linter.DEFAULT_FIGURE_PATTERN), kw.get("max_words", 40))


def rules(findings) -> set[str]:
    return {f.rule for f in findings}


def test_clean_paragraph_has_no_findings(linter, tmp_path):
    assert run(linter, tmp_path, GOOD_PARAGRAPH) == []


@pytest.mark.parametrize("text, rule", [
    ("The model scores events --- one per row. The margin grows with size.\n", "3.9"),
    ("The model scores events \u2014 one per row. The margin grows with size.\n", "3.9"),
    ("The model scores events; it doesn't fail. The margin grows with size.\n", "3.10"),
    ("The score is high. But the margin is small for small sets.\n", "3.5"),
    ("There are two classes in the data. The score separates them.\n", "3.7"),
    ("We set up the experiment with care. The score separates the classes.\n", "3.8"),
    ("The score is very high for the baseline. The margin grows with size.\n", "3.6"),
    ("The score is henceforth called the margin. The margin grows with size.\n", "3.12"),
    ("The score is high. Why does the margin grow with size?\n", "3.11"),
    ("The model understands the event topology. The margin grows with size.\n", "2.7"),
    ("The result proves that the score is robust. The margin grows with size.\n", "2.6"),
    ("I trained the model on the full set. The margin grows with size.\n", "1.14"),
    ("In order to score events, the model reads each row. The margin grows with size.\n", "3.4"),
    ("The score is high. This shows that the margin grows with size.\n", "4.4"),
])
def test_rule_triggers(linter, tmp_path, text, rule):
    assert rule in rules(run(linter, tmp_path, text))


def test_for_example_is_not_a_fanboys_start(linter, tmp_path):
    text = "The score is high. For example, the margin grows with size for every seed.\n"
    assert "3.5" not in rules(run(linter, tmp_path, text))


def test_roman_numeral_is_not_first_person(linter, tmp_path):
    text = "Part I covers the data. Part II covers the model and its score.\n"
    assert "1.14" not in rules(run(linter, tmp_path, text))


def test_one_sentence_paragraph(linter, tmp_path):
    text = "The model assigns a score to each event in the held-out set of the study.\n"
    assert "4.5" in rules(run(linter, tmp_path, text))
    assert "4.5" not in rules(run(linter, tmp_path, GOOD_PARAGRAPH))


def test_short_lead_in_is_not_flagged(linter, tmp_path):
    assert "4.5" not in rules(run(linter, tmp_path, "The steps are:\n"))


def test_long_sentence(linter, tmp_path):
    words = " ".join(["word"] * 45)
    text = f"The model {words} ends here. The margin grows with size.\n"
    assert "3.1" in rules(run(linter, tmp_path, text))


def test_structure_rules(linter, tmp_path):
    text = (
        "\\section{Setup}\n\\subsection{Only child}\n" + GOOD_PARAGRAPH +
        "\\subsubsection{Too deep}\n" + GOOD_PARAGRAPH
    )
    found = rules(run(linter, tmp_path, text))
    assert "5.1" in found
    assert "5.3" in found


def test_two_subsections_are_fine(linter, tmp_path):
    text = ("\\section{Setup}\n\\subsection{A}\n" + GOOD_PARAGRAPH +
            "\\subsection{B}\n" + GOOD_PARAGRAPH)
    assert "5.3" not in rules(run(linter, tmp_path, text))


def test_figure_paths(linter, tmp_path):
    flat = "\\includegraphics{figures/ch4/figure-roc.pdf}\n" + GOOD_PARAGRAPH
    good = "\\includegraphics[width=\\linewidth]{figures/ch4/20260519-114923_tokenizer/ch4_T1_roc.pdf}\n" + GOOD_PARAGRAPH
    assert "7.6" in rules(run(linter, tmp_path, flat))
    assert "7.6" not in rules(run(linter, tmp_path, good))


def test_todo_is_a_note(linter, tmp_path):
    text = "The score is \\todo{value pending} for the baseline. The margin grows with size.\n"
    f = [x for x in run(linter, tmp_path, text) if x.rule == "2.5"]
    assert f and f[0].severity == "NOTE"


def test_comments_math_and_masked_macros_are_ignored(linter, tmp_path):
    text = (
        "% don't flag this --- it's a comment\n"
        "The model scores $a -- b$ events with \\texttt{--multirun}. "
        "The margin grows with size, see \\cite{smith--2020} and \\ref{fig:a--b}.\n"
    )
    found = rules(run(linter, tmp_path, text))
    assert "3.9" not in found
    assert "3.10" not in found


def test_skipped_environments(linter, tmp_path):
    text = (
        "\\begin{tabular}{ll}\n a -- b & don't \\\\\n\\end{tabular}\n"
        "\\begin{figure}\n\\caption{The model understands --- no.}\n\\end{figure}\n"
        + GOOD_PARAGRAPH
    )
    assert run(linter, tmp_path, text) == []


def test_caption_outside_figure_is_prose(linter, tmp_path):
    text = "\\caption{The model doesn't fail. The margin grows with size.}\n"
    assert "3.10" in rules(run(linter, tmp_path, text))


def test_line_numbers(linter, tmp_path):
    text = GOOD_PARAGRAPH + "\n" + "The score is high. But the margin is small for small sets.\n"
    found = [f for f in run(linter, tmp_path, text) if f.rule == "3.5"]
    assert found and found[0].line == 3


def test_cli_fail_on_and_json(linter, tmp_path, capsys):
    f = tmp_path / "s.tex"
    f.write_text("The score is high. But the margin is small for small sets.\n", encoding="utf-8")
    assert linter.main([str(f), "--fail-on", "MINOR"]) == 1
    assert linter.main([str(f), "--fail-on", "MAJOR"]) == 0
    assert linter.main([str(f), "--json"]) == 0
    out = capsys.readouterr().out
    assert '"rule": "3.5"' in out


def test_template_scaffold_is_clean(linter, root):
    mainmatter = root / "templates" / "thesis" / "mainmatter"
    assert linter.main([str(mainmatter), "--fail-on", "MINOR"]) == 0
