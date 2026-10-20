from __future__ import annotations

import json
import re
from pathlib import Path


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} has no frontmatter"
    head = text.split("\n---\n", 1)[0][4:]
    out: dict[str, str] = {}
    for line in head.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


YAML_UNSAFE_START = tuple("[{>|&*!%@`'\"")


def test_frontmatter_values_are_yaml_safe(root: Path):
    """Strict YAML rejects unquoted values with ': ' or ' #', or starting with flow/indicator
    characters. Newer Claude Code validators parse frontmatter strictly."""
    files = (list((root / "plugin" / "agents").glob("*.md"))
             + list((root / "plugin" / "commands").glob("*.md"))
             + list((root / "plugin" / "skills").glob("*/SKILL.md")))
    for f in files:
        text = f.read_text(encoding="utf-8")
        head = text.split("\n---\n", 1)[0][4:]
        for line in head.splitlines():
            m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
            assert m, f"{f}: unexpected frontmatter line {line!r}"
            key, val = m.group(1), m.group(2)
            if val.startswith('"') and val.endswith('"'):
                assert '"' not in val[1:-1].replace('\\"', ""), f"{f}: unescaped quote in {key}"
                continue
            assert ": " not in val and " #" not in val, f"{f}: unquoted {key} contains ': ' or ' #'"
            assert not val.startswith(YAML_UNSAFE_START), f"{f}: unquoted {key} starts with a YAML indicator"


def test_versions_agree(root: Path, atw):
    plugin = json.loads((root / "plugin" / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    citation = (root / "CITATION.cff").read_text(encoding="utf-8")
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    v = plugin["version"]
    assert atw.VERSION == v
    assert re.search(rf'^version = "{re.escape(v)}"', pyproject, flags=re.MULTILINE)
    assert re.search(rf"^version: {re.escape(v)}$", citation, flags=re.MULTILINE)
    assert f"## [{v}]" in changelog


def test_marketplace_points_at_plugin(root: Path):
    m = json.loads((root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert m["name"] == "agentic-thesis-writing"
    assert m["plugins"][0]["source"] == "./plugin"
    assert m["plugins"][0]["name"] == "agentic-thesis-writing"


def test_agents_have_frontmatter(root: Path):
    agents = sorted((root / "plugin" / "agents").glob("*.md"))
    assert len(agents) == 7
    for a in agents:
        fm = frontmatter(a)
        assert fm["name"] == a.stem, a
        assert fm["description"], a
        assert fm["tools"], a
        body = a.read_text(encoding="utf-8")
        assert "AGENTS.md" in body, f"{a} must tell the agent to read AGENTS.md"


def test_readonly_agents_have_no_write_tools(root: Path):
    for name in ("reviewer", "writing-rules-checker"):
        fm = frontmatter(root / "plugin" / "agents" / f"{name}.md")
        tools = {t.strip() for t in fm["tools"].split(",")}
        assert not tools & {"Edit", "Write"}, name


def test_skills_have_skill_md(root: Path):
    skills = sorted(p for p in (root / "plugin" / "skills").iterdir() if p.is_dir())
    assert len(skills) == 9
    for s in skills:
        fm = frontmatter(s / "SKILL.md")
        assert fm["name"] == s.name, s
        assert fm["description"], s


def test_commands_have_description(root: Path):
    commands = sorted((root / "plugin" / "commands").glob("*.md"))
    assert len(commands) == 11
    for c in commands:
        fm = frontmatter(c)
        assert fm["description"], c
        assert "$ARGUMENTS" in c.read_text(encoding="utf-8"), c


def test_readme_lists_every_component(root: Path):
    readme = (root / "README.md").read_text(encoding="utf-8")
    for a in (root / "plugin" / "agents").glob("*.md"):
        assert f"`{a.stem}`" in readme, a.stem
    for s in (root / "plugin" / "skills").iterdir():
        assert f"`{s.name}`" in readme, s.name
    for c in (root / "plugin" / "commands").glob("*.md"):
        assert f"`/{c.stem}`" in readme, c.stem


def test_no_unfilled_placeholders_outside_templates(root: Path):
    for p in root.rglob("*.md"):
        rel = p.relative_to(root).as_posix()
        if rel.startswith(("templates/", "plugin/skills/evidence-note/template", "plugin/skills/handoff-note/template",
                           "plugin/skills/thesis-to-deck/storyline_template")):
            continue
        if ".git/" in rel:
            continue
        assert "{{" not in p.read_text(encoding="utf-8"), rel


def test_template_thesis_files_present(root: Path):
    t = root / "templates" / "thesis"
    for f in ("report.tex", "report.bib", "tudelft-report.cls", ".latexmkrc", "build.sh", "fetch_assets.sh",
              "CLAUDE.md", "README.md", "LICENSE-TEMPLATE.md", "frontmatter/title-thesis.tex",
              "mainmatter/01_introduction.tex", "mainmatter/02_results_chapter_template.tex",
              "mainmatter/09_conclusion.tex", "appendix/appendix-a.tex", "figures/README.md"):
        assert (t / f).exists(), f
    cls = (t / "tudelft-report.cls").read_text(encoding="utf-8")
    assert "IfFontExistsTF" in cls and "IfFileExists" in cls
    for f in ("frontmatter/title-thesis.tex", "frontmatter/title-report.tex"):
        assert "IfFileExists{figures/logo-black.pdf}" in (t / f).read_text(encoding="utf-8"), f
