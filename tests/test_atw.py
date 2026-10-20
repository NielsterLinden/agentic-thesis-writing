from __future__ import annotations

from pathlib import Path

import pytest


def install(atw, target: Path, *extra: str) -> int:
    return atw.main(["install", "--target", str(target), *extra])


def test_fresh_install_claude(atw, tmp_path: Path):
    assert install(atw, tmp_path) == 0
    assert (tmp_path / ".claude" / "agents" / "researcher.md").exists()
    assert (tmp_path / ".claude" / "skills" / "evidence-note" / "SKILL.md").exists()
    assert (tmp_path / ".claude" / "skills" / "tudelft-writing-rules" / "check_writing_rules.py").exists()
    assert (tmp_path / ".claude" / "commands" / "draft-section.md").exists()
    assert (tmp_path / "thesis" / "report.tex").exists()
    assert (tmp_path / "thesis" / "tudelft-report.cls").exists()
    assert (tmp_path / "thesis" / "LICENSE-TEMPLATE.md").exists()
    assert (tmp_path / "thesis" / "CLAUDE.md").exists()
    assert (tmp_path / "docs" / "evidence_notes" / "README.md").exists()
    assert (tmp_path / "docs" / "handoffs" / "README.md").exists()
    assert (tmp_path / "docs" / "finalizer").is_dir()
    assert (tmp_path / "docs" / "thesis_style" / "PLOTTING_STYLE.md").exists()
    assert (tmp_path / "scripts" / "atw.py").exists()
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "<!-- agentic-thesis-writing:start -->" in agents
    assert "`thesis/`" in agents and "{{THESIS_DIR}}" not in agents
    assert "<FILL" in agents
    assert (tmp_path / "CLAUDE.md").read_text(encoding="utf-8").strip() == "@AGENTS.md"
    gi = (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert "# agentic-thesis-writing:start" in gi and "thesis/**/*.aux" in gi
    assert not (tmp_path / "presentation").exists()


def test_reinstall_is_idempotent(atw, tmp_path: Path):
    assert install(atw, tmp_path) == 0
    assert install(atw, tmp_path) == 0
    assert not list(tmp_path.rglob("*.atw.new"))
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert agents.count("<!-- agentic-thesis-writing:start -->") == 1
    assert (tmp_path / "CLAUDE.md").read_text(encoding="utf-8").count("@AGENTS.md") == 1


def test_conflict_writes_atw_new_and_update_kit_overwrites(atw, tmp_path: Path, root: Path):
    assert install(atw, tmp_path) == 0
    agent = tmp_path / ".claude" / "agents" / "researcher.md"
    agent.write_text("local edits\n", encoding="utf-8")
    assert install(atw, tmp_path) == 1
    new = agent.with_name("researcher.md.atw.new")
    assert new.exists()
    assert agent.read_text(encoding="utf-8") == "local edits\n"
    new.unlink()
    assert install(atw, tmp_path, "--update-kit") == 0
    assert agent.read_bytes() == (root / "plugin" / "agents" / "researcher.md").read_bytes()


def test_update_kit_never_touches_user_content(atw, tmp_path: Path):
    assert install(atw, tmp_path) == 0
    agents = tmp_path / "AGENTS.md"
    agents.write_text(agents.read_text(encoding="utf-8").replace("<FILL: e.g. src/, configs/, scripts/, jobs/>", "src/"),
                      encoding="utf-8")
    chapter = tmp_path / "thesis" / "mainmatter" / "01_introduction.tex"
    chapter.write_text("my chapter\n", encoding="utf-8")
    assert install(atw, tmp_path, "--update-kit") == 0
    assert "src/" in agents.read_text(encoding="utf-8")
    assert chapter.read_text(encoding="utf-8") == "my chapter\n"


def test_existing_files_are_merged_not_overwritten(atw, tmp_path: Path):
    (tmp_path / "AGENTS.md").write_text("# My rules\n\nKeep these.\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("# Notes\n", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("*.pyc\n", encoding="utf-8")
    assert install(atw, tmp_path) == 0
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert agents.startswith("# My rules") and "<!-- agentic-thesis-writing:start -->" in agents
    claude = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert claude.startswith("# Notes") and "@AGENTS.md" in claude
    gi = (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert gi.startswith("*.pyc") and "# agentic-thesis-writing:start" in gi


def test_existing_thesis_gets_scope_files_only(atw, tmp_path: Path):
    thesis = tmp_path / "doc"
    thesis.mkdir()
    (thesis / "main.tex").write_text("\\documentclass{article}\n", encoding="utf-8")
    assert install(atw, tmp_path, "--thesis-dir", "doc", "--template", "existing") == 0
    assert (thesis / "CLAUDE.md").exists()
    assert (thesis / ".latexmkrc").exists()
    assert (thesis / "figures" / "README.md").exists()
    assert not (thesis / "report.tex").exists()
    assert "`doc/`" in (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "doc/**/*.aux" in (tmp_path / ".gitignore").read_text(encoding="utf-8")


def test_codex_and_plugin_and_none_agents(atw, tmp_path: Path):
    codex = tmp_path / "codex"
    codex.mkdir()
    assert install(atw, codex, "--agent", "codex") == 0
    assert (codex / ".agents" / "skills" / "evidence-note" / "SKILL.md").exists()
    assert (codex / ".agents" / "skills" / "thesis-agents" / "researcher.md").exists()
    assert not (codex / ".claude").exists()
    assert not (codex / "CLAUDE.md").exists()

    plugin = tmp_path / "plugin"
    plugin.mkdir()
    assert install(atw, plugin, "--agent", "claude-plugin") == 0
    assert not (plugin / ".claude").exists()
    assert (plugin / "CLAUDE.md").exists()
    assert (plugin / "AGENTS.md").exists()

    none = tmp_path / "none"
    none.mkdir()
    assert install(atw, none, "--agent", "none", "--template", "none") == 0
    assert not (none / "thesis").exists()
    assert (none / "AGENTS.md").exists()


def test_presentation_and_dry_run(atw, tmp_path: Path):
    assert install(atw, tmp_path, "--dry-run", "--with-presentation") == 0
    assert not (tmp_path / "AGENTS.md").exists()
    assert install(atw, tmp_path, "--with-presentation") == 0
    assert (tmp_path / "presentation" / "CLAUDE.md").exists()
    assert (tmp_path / "presentation" / "STORYLINE.md").exists()
    assert (tmp_path / "presentation" / "storylines").is_dir()
    assert (tmp_path / "presentation" / "clips").is_dir()


def test_new_note_and_handoff(atw, tmp_path: Path, capsys):
    assert install(atw, tmp_path) == 0
    assert atw.main(["new-note", "ch4.2", "tokenizer", "--title", "Tokenizer family", "--target", str(tmp_path)]) == 0
    note = tmp_path / "docs" / "evidence_notes" / "ch4.2_tokenizer.md"
    text = note.read_text(encoding="utf-8")
    assert text.startswith("# Evidence note: ch4.2: tokenizer (Tokenizer family)")
    assert "- Status: triaged" in text and "{{" not in text
    with pytest.raises(SystemExit):
        atw.main(["new-note", "ch4.2", "tokenizer", "--target", str(tmp_path)])
    with pytest.raises(SystemExit):
        atw.main(["new-note", "chapter4", "tokenizer", "--target", str(tmp_path)])

    assert atw.main(["new-handoff", "ch4-figures", "--title", "Rework Ch4 figures", "--target", str(tmp_path)]) == 0
    handoffs = list((tmp_path / "docs" / "handoffs").glob("*_ch4-figures.md"))
    assert len(handoffs) == 1
    text = handoffs[0].read_text(encoding="utf-8")
    assert text.startswith("# Handoff: Rework Ch4 figures") and "{{" not in text
    assert "- Status: open" in text
    with pytest.raises(SystemExit):
        atw.main(["new-handoff", "Bad Slug", "--target", str(tmp_path)])


def test_version(atw, capsys, root: Path):
    assert atw.main(["version"]) == 0
    assert capsys.readouterr().out.strip() == atw.VERSION
