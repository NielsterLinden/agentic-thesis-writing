from __future__ import annotations

from pathlib import Path

import pytest

NOTE = """# Evidence note: ch4.2: tokenizer (Tokenizer family)

- Status: run-complete
- Plot paths:
    - <none yet>
- Active figures: <none yet>
- Figure compliance: <TBD>
"""


@pytest.fixture
def ws(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docs" / "evidence_notes").mkdir(parents=True)
    note = tmp_path / "docs" / "evidence_notes" / "ch4.2_tokenizer.md"
    note.write_text(NOTE, encoding="utf-8")
    src = tmp_path / "out" / "ch4_T1_roc.pdf"
    src.parent.mkdir()
    src.write_bytes(b"%PDF-1.4 fake")
    return tmp_path, note, src


def test_import_creates_dir_and_updates_note(figure_import, ws):
    tmp, note, src = ws
    rc = figure_import.main(["--src", str(src), "--chapter", "ch4", "--slug", "tokenizer",
                             "--note", str(note), "--timestamp", "20260519-114923"])
    assert rc == 0
    dest = tmp / "thesis" / "figures" / "ch4" / "20260519-114923_tokenizer" / "ch4_T1_roc.pdf"
    assert dest.read_bytes() == b"%PDF-1.4 fake"
    text = note.read_text(encoding="utf-8")
    assert "- Active figures: thesis/figures/ch4/20260519-114923_tokenizer/" in text
    assert "- thesis/figures/ch4/20260519-114923_tokenizer/ch4_T1_roc.pdf ← out/ch4_T1_roc.pdf" in text
    assert "<none yet>" not in text.split("Plot paths:")[1].split("Active figures")[0]


def test_timestamp_is_reused_from_note(figure_import, ws):
    tmp, note, src = ws
    figure_import.main(["--src", str(src), "--chapter", "ch4", "--slug", "tokenizer",
                        "--note", str(note), "--timestamp", "20260519-114923"])
    second = src.with_name("ch4_T1_bars.pdf")
    second.write_bytes(b"%PDF second")
    figure_import.main(["--src", str(second), "--chapter", "ch4", "--slug", "tokenizer", "--note", str(note)])
    assert (tmp / "thesis" / "figures" / "ch4" / "20260519-114923_tokenizer" / "ch4_T1_bars.pdf").exists()
    text = note.read_text(encoding="utf-8")
    assert text.count("Active figures:") == 1
    assert text.count("←") == 2


def test_refuses_overwrite(figure_import, ws):
    tmp, note, src = ws
    args = ["--src", str(src), "--chapter", "ch4", "--slug", "tokenizer", "--note", str(note),
            "--timestamp", "20260519-114923"]
    figure_import.main(args)
    with pytest.raises(SystemExit):
        figure_import.main(args)


def test_refuses_generic_filename_unless_allowed(figure_import, ws):
    tmp, note, src = ws
    bad = src.with_name("figure-roc.pdf")
    bad.write_bytes(b"x")
    with pytest.raises(SystemExit):
        figure_import.main(["--src", str(bad), "--chapter", "ch4", "--slug", "tokenizer", "--note", str(note)])
    assert figure_import.main(["--src", str(bad), "--chapter", "ch4", "--slug", "tokenizer",
                               "--note", str(note), "--allow-any-name"]) == 0


def test_dry_run_writes_nothing(figure_import, ws):
    tmp, note, src = ws
    before = note.read_text(encoding="utf-8")
    assert figure_import.main(["--src", str(src), "--chapter", "ch4", "--slug", "tokenizer",
                               "--note", str(note), "--dry-run"]) == 0
    assert note.read_text(encoding="utf-8") == before
    assert not (tmp / "thesis").exists()


def test_bad_arguments(figure_import, ws):
    tmp, note, src = ws
    with pytest.raises(SystemExit):
        figure_import.main(["--src", str(src), "--chapter", "chapter4", "--slug", "tokenizer", "--note", str(note)])
    with pytest.raises(SystemExit):
        figure_import.main(["--src", str(src), "--chapter", "ch4", "--slug", "Tokenizer_Family", "--note", str(note)])


def test_note_without_plot_paths_section_gets_one(figure_import, ws):
    tmp, note, src = ws
    note.write_text("# Evidence note\n\n- Status: run-complete\n", encoding="utf-8")
    figure_import.main(["--src", str(src), "--chapter", "ch4", "--slug", "tokenizer", "--note", str(note),
                        "--timestamp", "20260519-114923"])
    text = note.read_text(encoding="utf-8")
    assert "## Plot paths" in text
    assert "- Active figures: thesis/figures/ch4/20260519-114923_tokenizer/" in text
