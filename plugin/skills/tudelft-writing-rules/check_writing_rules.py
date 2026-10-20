#!/usr/bin/env python3
"""Check LaTeX prose against the writing rules (see rules.md next to this file).

Standard library only. Usage:

    python3 check_writing_rules.py PATH [PATH ...] [--json] [--fail-on MINOR|MAJOR|BLOCK]
                                   [--figure-pattern REGEX] [--max-words N]

PATH is a .tex file or a directory (searched recursively for .tex files). Each finding is
printed as ``[SEVERITY] file:line: message (rule N.N) -> fix``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

# --------------------------------------------------------------------------------------
# Word lists (edit these when adapting the rules)
# --------------------------------------------------------------------------------------

CONTRACTIONS = [
    "don't", "doesn't", "didn't", "can't", "won't", "isn't", "aren't", "wasn't", "weren't",
    "hasn't", "haven't", "hadn't", "couldn't", "shouldn't", "wouldn't", "mustn't", "it's",
    "that's", "there's", "here's", "what's", "who's", "where's", "we're", "they're",
    "you're", "i'm", "i've", "we've", "they've", "you've", "i'd", "we'd", "they'd", "i'll",
    "we'll", "they'll", "it'll", "let's",
]

FANBOYS = ["For", "And", "Nor", "But", "Or", "Yet", "So"]
FANBOYS_EXCEPTIONS = {"For": ["example", "instance", "each", "every", "all", "any", "a", "an",
                              "the", "this", "these", "those", "both", "clarity", "brevity",
                              "completeness", "comparison", "reference", "simplicity"],
                      "So": ["far", "called", "that"]}

PHRASAL_VERBS = [
    ("set", "up"), ("look", "into"), ("carry", "out"), ("find", "out"), ("figure", "out"),
    ("point", "out"), ("make", "up"), ("bring", "about"), ("come", "up with"), ("deal", "with"),
    ("end", "up"), ("go", "through"), ("rule", "out"), ("sort", "out"), ("turn", "out"),
    ("work", "out"), ("pick", "up"), ("build", "up"), ("break", "down"), ("put", "forward"),
    ("look", "for"), ("get", "rid of"), ("cut", "down"), ("make", "sure"), ("keep", "track of"),
    ("come", "across"), ("take", "away"), ("back", "up"), ("sum", "up"),
]

INTENSIFIERS_MINOR = ["very", "extremely", "greatly", "really", "hugely", "massively",
                      "incredibly", "a lot", "lots of"]
INTENSIFIERS_NOTE = ["significantly", "dramatically", "remarkably", "substantially",
                     "considerably", "drastically"]

LEGALISTIC_MINOR = ["forthwith", "henceforth", "hereof", "thereof", "herein", "therein",
                    "hereby", "heretofore", "aforementioned", "hereinafter"]
LEGALISTIC_NOTE = {"utilize": "use", "utilise": "use", "utilization": "use",
                   "utilisation": "use", "whilst": "while", "amongst": "among"}

ANTHRO_SUBJECTS = r"(?:model|models|network|networks|classifier|classifiers|transformer|" \
                  r"transformers|architecture|architectures|algorithm|algorithms|method|" \
                  r"methods|system|systems|encoder|decoder|attention|head|heads|layer|layers|" \
                  r"it|they)"
ANTHRO_VERBS_MAJOR = r"(?:understands?|understood|knows?|knew|believes?|believed|thinks?|" \
                     r"thought|wants?|wanted|realis(?:es?|ed)|realiz(?:es?|ed)|feels?|felt|" \
                     r"is aware|are aware|intends?|intended|tries to|try to|likes?|prefers?)"
ANTHRO_VERBS_NOTE = r"(?:decides?|decided|sees?|saw|looks? at|looked at|focus(?:es)? on|" \
                    r"pays? attention|paid attention|chooses?|chose|notices?|noticed)"

ABSOLUTES = ["proves", "prove", "proved", "proven", "always", "never", "clearly",
             "obviously", "undoubtedly", "certainly", "definitely", "guarantees",
             "guarantee", "guaranteed"]

WORDY = {
    "in order to": "to", "the majority of": "most", "a number of": "several",
    "due to the fact that": "because", "in spite of the fact that": "although",
    "at this point in time": "now", "it should be noted that": "(delete)",
    "it is important to note that": "(delete)", "in the event that": "if",
    "with regard to": "about", "in terms of": "(recast)", "the fact that": "that",
    "as a matter of fact": "(delete)", "for the purpose of": "to",
}

VAGUE_THIS = r"^This (?:is|was|means|shows|suggests|indicates|implies|results|leads|causes|" \
             r"allows|makes|has|had|can|could|may|might|will|would|does|did|gives|explains)\b"

ABBREVIATIONS = ["e.g.", "i.e.", "et al.", "cf.", "vs.", "fig.", "figs.", "eq.", "eqs.",
                 "sec.", "ref.", "refs.", "approx.", "no.", "dr.", "prof.", "ir.", "mr.",
                 "ms.", "ch.", "tab.", "etc.", "resp.", "incl.", "viz."]

SKIP_ENVS = {"figure", "figure*", "table", "table*", "tabular", "tabularx", "tabulary",
             "longtable", "equation", "equation*", "align", "align*", "gather", "gather*",
             "multline", "multline*", "eqnarray", "lstlisting", "verbatim", "comment",
             "tikzpicture", "minted", "algorithm", "algorithmic", "thebibliography",
             "titlepage", "subfigure", "wrapfigure", "sidewaysfigure", "sidewaystable"}

MASK_MACROS = ["cite", "citep", "citet", "parencite", "textcite", "autocite", "ref", "cref",
               "Cref", "eqref", "pageref", "label", "url", "includegraphics", "texttt",
               "lstinline", "path", "nameref", "input", "include", "todo"]

SEVERITY_RANK = {"BLOCK": 0, "MAJOR": 1, "MINOR": 2, "NOTE": 3}

DEFAULT_FIGURE_PATTERN = r"figures/ch\d+/\d{8}-\d{6}_[^/]+/"


@dataclass
class Finding:
    severity: str
    file: str
    line: int
    rule: str
    message: str
    fix: str

    def text(self) -> str:
        return f"[{self.severity}] {self.file}:{self.line}: {self.message} (rule {self.rule}) -> {self.fix}"


# --------------------------------------------------------------------------------------
# Preprocessing
# --------------------------------------------------------------------------------------

_COMMENT_RE = re.compile(r"(?<!\\)%.*$")
_BEGIN_RE = re.compile(r"\\begin\{([^}]*)\}")
_END_RE = re.compile(r"\\end\{([^}]*)\}")
_INLINE_MATH_RE = re.compile(r"(?<!\\)\$(?:[^$\\]|\\.)*\$|\\\((?:.|\n)*?\\\)")
_DISPLAY_MATH_RE = re.compile(r"\\\[(?:.|\n)*?\\\]")
_VERB_RE = re.compile(r"\\verb(\S)(.*?)\1")


def strip_comment(line: str) -> str:
    return _COMMENT_RE.sub("", line)


def mask_macro_args(text: str) -> str:
    """Replace the braced arguments of reference-like macros with a placeholder."""
    for name in MASK_MACROS:
        pattern = re.compile(r"\\" + name + r"\*?(?:\[[^\]]*\])?\{")
        pos = 0
        while True:
            m = pattern.search(text, pos)
            if not m:
                break
            depth = 1
            i = m.end()
            while i < len(text) and depth:
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                i += 1
            text = text[: m.start()] + f"\\{name}{{X}}" + text[i:]
            pos = m.start() + len(name) + 4
    text = _VERB_RE.sub("X", text)
    return text


def prose_lines(path: Path) -> list[str]:
    """Return the file's lines with comments stripped and non-prose environments blanked.

    Line count is preserved so findings carry real line numbers."""
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    out: list[str] = []
    stack: list[str] = []
    for line in raw:
        line = strip_comment(line)
        if stack:
            for m in _END_RE.finditer(line):
                if stack and m.group(1) == stack[-1]:
                    stack.pop()
            out.append("")
            for m in _BEGIN_RE.finditer(line):
                if m.group(1) in SKIP_ENVS:
                    stack.append(m.group(1))
            continue
        begins = [m for m in _BEGIN_RE.finditer(line) if m.group(1) in SKIP_ENVS]
        if begins:
            first = begins[0]
            out.append(line[: first.start()])
            for m in begins:
                stack.append(m.group(1))
            for m in _END_RE.finditer(line):
                if stack and m.group(1) == stack[-1]:
                    stack.pop()
            continue
        out.append(line)
    return out


def mask_math(text: str) -> str:
    text = _DISPLAY_MATH_RE.sub(" MATH ", text)
    text = _INLINE_MATH_RE.sub(" MATH ", text)
    return text


# --------------------------------------------------------------------------------------
# Paragraphs and sentences
# --------------------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^\s*\\(chapter|section|subsection|subsubsection|paragraph)\*?(\[[^\]]*\])?\{")
_COMMAND_ONLY_RE = re.compile(r"^\s*\\[A-Za-z@]+\*?(\[[^\]]*\])?(\{[^{}]*\})*\s*$")


@dataclass
class Paragraph:
    start_line: int
    lines: list[str]

    @property
    def text(self) -> str:
        return " ".join(l.strip() for l in self.lines)


def paragraphs(lines: list[str]) -> list[Paragraph]:
    """Split prose lines into paragraphs; headings and command-only lines break paragraphs."""
    paras: list[Paragraph] = []
    cur: list[str] = []
    start = 0
    for i, line in enumerate(lines, start=1):
        is_blank = line.strip() == ""
        is_heading = bool(_HEADING_RE.match(line))
        is_cmd = bool(_COMMAND_ONLY_RE.match(line)) and not line.strip().startswith("\\caption")
        if is_blank or is_heading or is_cmd:
            if cur:
                paras.append(Paragraph(start, cur))
                cur = []
            if is_heading:
                # The \paragraph{...} anchor may carry prose on the same line.
                rest = re.sub(r"^\s*\\paragraph\*?\{[^}]*\}", "", line)
                if line.strip().startswith("\\paragraph") and rest.strip():
                    cur = [rest]
                    start = i
            continue
        if not cur:
            start = i
        cur.append(line)
    if cur:
        paras.append(Paragraph(start, cur))
    return paras


def protect_abbreviations(text: str) -> str:
    for abbr in ABBREVIATIONS:
        text = re.sub(re.escape(abbr), abbr.replace(".", "\u2024"), text, flags=re.IGNORECASE)
    text = re.sub(r"(\d)\.(\d)", "\\1\u2024\\2", text)          # decimals
    text = re.sub(r"\b([A-Z])\.\s", "\\1\u2024 ", text)        # initials
    return text


_SENT_END_RE = re.compile(r"[.!?]+(?=\s|$)")


def sentences(text: str) -> list[str]:
    """Split paragraph text into sentences (after abbreviation protection)."""
    protected = protect_abbreviations(text)
    parts = _SENT_END_RE.split(protected)
    ends = _SENT_END_RE.findall(protected)
    out = []
    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue
        end = ends[i] if i < len(ends) else ""
        out.append((part + end).replace("\u2024", "."))
    return out


def line_of(para: Paragraph, needle_offset: int) -> int:
    """Map a character offset in para.text to a file line number."""
    pos = 0
    for k, line in enumerate(para.lines):
        seg = line.strip()
        if needle_offset <= pos + len(seg):
            return para.start_line + k
        pos += len(seg) + 1
    return para.start_line + len(para.lines) - 1


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------

def check_file(path: Path, figure_pattern: str, max_words: int) -> list[Finding]:
    findings: list[Finding] = []
    rel = path.as_posix()
    lines = prose_lines(path)

    def add(sev: str, line: int, rule: str, msg: str, fix: str) -> None:
        findings.append(Finding(sev, rel, line, rule, msg, fix))

    # ---- structural checks on the raw (comment-stripped) lines --------------------------
    raw_for_structure = [strip_comment(l) for l in path.read_text(encoding="utf-8", errors="replace").splitlines()]
    section_children: list[tuple[int, int]] = []   # (section line, subsection count)
    subsection_children: list[tuple[int, int]] = []
    fig_re = re.compile(figure_pattern)
    for i, line in enumerate(raw_for_structure, start=1):
        if re.match(r"\s*\\subsubsection\b", line):
            add("MINOR", i, "5.1", "\\subsubsection exceeds the chapter → section → subsection depth",
                "promote to a \\subsection or demote to a \\paragraph{} anchor")
        if re.match(r"\s*\\(chapter|section)\b", line):
            section_children.append((i, 0))
            subsection_children.append((i, -1))
        elif re.match(r"\s*\\subsection\b", line):
            if section_children:
                ln, n = section_children[-1]
                section_children[-1] = (ln, n + 1)
            subsection_children.append((i, 0))
        elif re.match(r"\s*\\subsubsection\b", line) and subsection_children:
            ln, n = subsection_children[-1]
            if n >= 0:
                subsection_children[-1] = (ln, n + 1)
        for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", line):
            if not fig_re.search(m.group(1)):
                add("NOTE", i, "7.6", f"figure path is not timestamped: {m.group(1)}",
                    "import the figure with figure-import into figures/ch<N>/<timestamp>_<slug>/")
        for _ in re.finditer(r"\\todo\{", line):
            add("NOTE", i, "2.5", "pending \\todo{} marker", "resolve before submission")
    for ln, n in section_children:
        if n == 1 and re.match(r"\s*\\section\b", raw_for_structure[ln - 1]):
            add("MINOR", ln, "5.3", "section has exactly one subsection",
                "merge the subsection into the section or add a sibling")
    for ln, n in subsection_children:
        if n == 1:
            add("MINOR", ln, "5.3", "subsection has exactly one subsubsection",
                "merge or add a sibling")

    # ---- prose checks ---------------------------------------------------------------------
    for para in paragraphs(lines):
        text = mask_math(mask_macro_args(para.text))
        if not re.search(r"[A-Za-z]{3,}", text):
            continue
        pline = para.start_line

        # 3.9 dashes
        for m in re.finditer(r"\u2014|\u2013|(?<!-)---?(?!-)", text):
            add("MINOR", line_of(para, m.start()), "3.9", "em or en dash in prose",
                "recast with a colon, a comma, a semicolon, or two sentences")

        # 3.10 contractions
        for c in CONTRACTIONS:
            for m in re.finditer(r"(?<![A-Za-z])" + re.escape(c) + r"(?![A-Za-z])", text, flags=re.IGNORECASE):
                add("MINOR", line_of(para, m.start()), "3.10", f"contraction {m.group(0)!r}",
                    "write the full form")

        # 3.8 phrasal verbs
        for verb, particle in PHRASAL_VERBS:
            forms = {verb, verb + "s", verb + "ed", verb + "ing", verb + "d"}
            if verb.endswith("e"):
                forms.add(verb[:-1] + "ing")
            if verb == "set":
                forms.add("setting")
            if verb in {"cut", "put"}:
                forms.add(verb + "ting")
            if verb == "come":
                forms |= {"came", "comes", "coming"}
            if verb == "go":
                forms |= {"goes", "went", "going", "gone"}
            if verb == "find":
                forms |= {"found", "finds", "finding"}
            if verb == "bring":
                forms |= {"brought", "brings", "bringing"}
            if verb == "break":
                forms |= {"broke", "broken", "breaks", "breaking"}
            if verb == "get":
                forms |= {"got", "gets", "getting", "gotten"}
            if verb == "keep":
                forms |= {"kept", "keeps", "keeping"}
            if verb == "take":
                forms |= {"took", "takes", "taking", "taken"}
            if verb == "make":
                forms |= {"made", "makes", "making"}
            if verb == "deal":
                forms |= {"dealt", "deals", "dealing"}
            pat = r"\b(?:" + "|".join(sorted(map(re.escape, forms))) + r")\s+" + re.escape(particle) + r"\b"
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                add("MINOR", line_of(para, m.start()), "3.8", f"phrasal verb {m.group(0)!r}",
                    "use a single verb (investigate, perform, determine, ...)")

        # 3.6 intensifiers
        for w in INTENSIFIERS_MINOR:
            for m in re.finditer(r"\b" + re.escape(w) + r"\b", text, flags=re.IGNORECASE):
                add("MINOR", line_of(para, m.start()), "3.6", f"vague intensifier {m.group(0)!r}",
                    "give the number, or delete")
        for w in INTENSIFIERS_NOTE:
            for m in re.finditer(r"\b" + re.escape(w) + r"\b", text, flags=re.IGNORECASE):
                add("NOTE", line_of(para, m.start()), "3.6", f"{m.group(0)!r} needs a number next to it",
                    "quantify the effect, or delete the adverb")

        # 3.12 legalistic
        for w in LEGALISTIC_MINOR:
            for m in re.finditer(r"\b" + re.escape(w) + r"\b", text, flags=re.IGNORECASE):
                add("MINOR", line_of(para, m.start()), "3.12", f"legalistic word {m.group(0)!r}",
                    "use plain wording")
        for w, repl in LEGALISTIC_NOTE.items():
            for m in re.finditer(r"\b" + re.escape(w) + r"\b", text, flags=re.IGNORECASE):
                add("NOTE", line_of(para, m.start()), "3.12", f"prefer {repl!r} to {m.group(0)!r}",
                    f"replace with {repl!r}")

        # 3.4 wordy phrases
        for phrase, repl in WORDY.items():
            for m in re.finditer(r"\b" + re.escape(phrase) + r"\b", text, flags=re.IGNORECASE):
                add("NOTE", line_of(para, m.start()), "3.4", f"wordy phrase {m.group(0)!r}",
                    f"use {repl}")

        # 2.7 anthropomorphism
        for m in re.finditer(r"\b(?:the|a|an|our|this|each|every)\s+" + ANTHRO_SUBJECTS + r"\s+" + ANTHRO_VERBS_MAJOR + r"\b",
                             text, flags=re.IGNORECASE):
            add("MAJOR", line_of(para, m.start()), "2.7", f"anthropomorphism {m.group(0)!r}",
                "describe what the model computes, fits, assigns or weights")
        for m in re.finditer(r"\b(?:the|a|an|our|this|each|every)\s+" + ANTHRO_SUBJECTS + r"\s+" + ANTHRO_VERBS_NOTE + r"\b",
                             text, flags=re.IGNORECASE):
            add("NOTE", line_of(para, m.start()), "2.7", f"possible anthropomorphism {m.group(0)!r}",
                "prefer a mechanistic verb if one fits")

        # 2.6 absolutes
        for w in ABSOLUTES:
            for m in re.finditer(r"\b" + re.escape(w) + r"\b", text, flags=re.IGNORECASE):
                add("NOTE", line_of(para, m.start()), "2.6", f"absolute claim word {m.group(0)!r}",
                    "hedge, or make sure the evidence is controlled")

        # 1.14 first person singular
        for m in re.finditer(r"(?<![A-Za-z])I(?=\s+(?:[a-z]|am\b|was\b|have\b|will\b))", text):
            before = text[max(0, m.start() - 12): m.start()]
            if re.search(r"(Part|Chapter|Section|Phase|Type|Table|Figure|Appendix|class|Class)\s*$", before):
                continue
            add("MINOR", line_of(para, m.start()), "1.14", "first-person singular",
                "use an impersonal subject or 'we'")
        for m in re.finditer(r"\b(?:my|mine|myself)\b", text):
            add("MINOR", line_of(para, m.start()), "1.14", f"first-person singular {m.group(0)!r}",
                "use 'the' or 'our'")

        sents = sentences(text)

        # 4.5 one-sentence paragraphs (skip very short lead-ins such as list introductions)
        if len(sents) == 1 and len(text.split()) >= 8 and not text.rstrip().endswith(":"):
            add("MINOR", pline, "4.5", "one-sentence paragraph",
                "merge with a neighbour or develop the idea")

        for s in sents:
            s_stripped = s.strip()
            # locate sentence start in the paragraph text for line mapping
            idx = text.find(s_stripped[: min(30, len(s_stripped))])
            ln = line_of(para, idx if idx >= 0 else 0)
            first = re.match(r"^[\(\[\"'“‘]*([A-Za-z]+)\b\s*([A-Za-z]*)", s_stripped)
            if first:
                w1, w2 = first.group(1), first.group(2)
                # 3.5 FANBOYS
                if w1 in FANBOYS and w2.lower() not in [x.lower() for x in FANBOYS_EXCEPTIONS.get(w1, [])]:
                    add("MINOR", ln, "3.5", f"sentence starts with {w1!r}",
                        "join to the previous sentence or use a linking adverb")
                # 3.7 There is/are
                if w1 == "There" and w2.lower() in {"is", "are", "was", "were", "exists", "exist"}:
                    add("MINOR", ln, "3.7", "sentence starts with 'There is / There are'",
                        "make the real subject the grammatical subject")
            # 3.11 questions
            if s_stripped.endswith("?"):
                add("MINOR", ln, "3.11", "question in body prose", "state the point instead")
            # 4.4 vague this
            if re.match(VAGUE_THIS, s_stripped):
                add("NOTE", ln, "4.4", "sentence opens with a bare 'This'",
                    "name the referent: 'This mechanism ...'")
            # 3.1 long sentences
            n_words = len(re.findall(r"[A-Za-z0-9\\]+", s_stripped))
            if n_words > max_words:
                add("NOTE", ln, "3.1", f"sentence of {n_words} words",
                    "split into two sentences")

    findings.sort(key=lambda f: (SEVERITY_RANK[f.severity], f.file, f.line, f.rule))
    return findings


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def collect(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            out.extend(sorted(pp.rglob("*.tex")))
        elif pp.is_file():
            out.append(pp)
        else:
            sys.exit(f"error: not found: {p}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--fail-on", choices=["BLOCK", "MAJOR", "MINOR", "NOTE"],
                    help="exit 1 if any finding at this severity or worse")
    ap.add_argument("--figure-pattern", default=DEFAULT_FIGURE_PATTERN,
                    help="regex an \\includegraphics path must match (rule 7.6)")
    ap.add_argument("--max-words", type=int, default=40, help="sentence length threshold (rule 3.1)")
    args = ap.parse_args(argv)

    files = collect(args.paths)
    findings: list[Finding] = []
    for f in files:
        findings.extend(check_file(f, args.figure_pattern, args.max_words))

    counts = {k: 0 for k in SEVERITY_RANK}
    for f in findings:
        counts[f.severity] += 1

    if args.json:
        print(json.dumps({"files": [f.as_posix() for f in files],
                          "counts": counts,
                          "findings": [asdict(f) for f in findings]}, indent=2, ensure_ascii=False))
    else:
        for f in findings:
            print(f.text())
        print(f"\n{len(files)} file(s), {len(findings)} finding(s): "
              + ", ".join(f"{k} {v}" for k, v in counts.items()))
        by_rule: dict[str, int] = {}
        for f in findings:
            by_rule[f.rule] = by_rule.get(f.rule, 0) + 1
        if by_rule:
            top = sorted(by_rule.items(), key=lambda kv: -kv[1])[:3]
            print("most frequent rules: " + ", ".join(f"{r} ({n})" for r, n in top))

    if args.fail_on:
        threshold = SEVERITY_RANK[args.fail_on]
        if any(SEVERITY_RANK[f.severity] <= threshold for f in findings):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
