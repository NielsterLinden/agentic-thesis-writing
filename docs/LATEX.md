# TeX inside the repository

The thesis source lives in the repository, next to the code and the notes, and the agents
compile it. This page covers the template, the build, fonts, installing TeX (including on a
cluster without root), CI, and troubleshooting.

## The template

`templates/thesis/` is the [unofficial TU Delft report/thesis template](https://github.com/dzwaneveld/tudelft-report-thesis-template)
by Daan Zwaneveld (CC BY-NC 4.0), installed as `<thesis dir>/` by the installer. Three
changes, each marked in the source:

1. **Font fallbacks.** The house style wants Arial and Roboto Slab. The class file now
   checks for them and falls back to TeX Gyre Heros and TeX Gyre Pagella (free, in every
   TeX distribution) with a warning, so the document builds anywhere.
2. **Optional assets.** The TU Delft logos and the sample cover are not in the kit; the
   cover and title page compile without them, and `fetch_assets.sh` downloads them from
   upstream when you want them.
3. **A `\todo{}` macro** and chapter scaffolds: `01_introduction.tex`,
   `02_results_chapter_template.tex` (the mini-thesis shape with its anchors),
   `09_conclusion.tex`.

Using another template: see `docs/ADAPTING.md`. The agents only assume a main file, a
`latexmk`-driven build, and a `figures/` tree.

## Build

```bash
cd thesis
latexmk -pdfxe report.tex        # XeLaTeX + biber; minimum passes
latexmk -pdfxe -gg report.tex    # full rebuild
latexmk -C                       # clean
latexmk -pdf report.tex          # pdfLaTeX, free fonts
./build.sh [-gg|-pdf|-C]         # the same, wrapped
```

`.latexmkrc` sets `$pdf_mode = 5` (XeLaTeX), biber, `-interaction=batchmode` (warnings go
to `report.log`) and `-halt-on-error` (fail fast). Agents use the `latex-build` skill,
which tells them to act on the **first** `!` line of the log and which failures are theirs
to fix.

## Fonts

| Font | Role | Where to get it |
|---|---|---|
| Arial | body (XeLaTeX) | Windows and macOS have it; on Linux install `ttf-mscorefonts-installer` or copy licensed TTFs into `~/.local/share/fonts/` and run `fc-cache -fv`; or accept the TeX Gyre Heros fallback |
| Roboto Slab (Light, Thin) | titles (XeLaTeX) | the `roboto` CTAN package ships the OTFs and the class finds them by file name; or install from Google Fonts system-wide |
| TeX Gyre Heros, TeX Gyre Pagella | fallbacks | in every TeX distribution |
| Palatino (newpx), Roboto Slab TLF | pdfLaTeX path | `newpx`, `roboto` packages |

## Installing TeX

| Platform | Command |
|---|---|
| Debian / Ubuntu | `sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-extra texlive-bibtex-extra biber latexmk` |
| Fedora | `sudo dnf install texlive-scheme-medium texlive-biber latexmk` |
| macOS | `brew install --cask mactex-no-gui` (or BasicTeX plus `tlmgr install` of the packages below) |
| Windows | [MiKTeX](https://miktex.org) with "install missing packages on the fly" enabled; or TeX Live |
| Any | TeX Live `install-tl` with `scheme-medium` |

Packages the template needs beyond a basic scheme: `biblatex`, `biber`, `fontspec`,
`siunitx`, `tikz` (`pgf`), `titlesec`, `titletoc`, `fancyhdr`, `enumitem`, `etoolbox`,
`cleveref`, `subcaption`, `pdfpages`, `datetime` (`fmtcount`), `microtype`, `listings`,
`newpx` and `roboto` (pdfLaTeX path), `tex-gyre` (fallbacks), `latexmk`.

### On a cluster without root

Install TeX Live into user space with a profile file:

```bash
wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
tar xzf install-tl-unx.tar.gz && cd install-tl-*/
cat > texlive.profile <<'EOF'
selected_scheme scheme-medium
TEXDIR /path/to/texlive/2026
TEXMFLOCAL /path/to/texlive/texmf-local
TEXMFSYSCONFIG /path/to/texlive/2026/texmf-config
TEXMFSYSVAR /path/to/texlive/2026/texmf-var
TEXMFHOME ~/texmf
tlpdbopt_install_docfiles 0
tlpdbopt_install_srcfiles 0
EOF
./install-tl -profile texlive.profile
export PATH="/path/to/texlive/2026/bin/x86_64-linux:$PATH"
tlmgr install biblatex biber fontspec siunitx cleveref titlesec titletoc fancyhdr enumitem \
              subcaption pdfpages datetime fmtcount microtype listings newpx roboto tex-gyre latexmk
```

Put the `export PATH` line (and, if you installed fonts under a custom fontconfig file,
`export FONTCONFIG_FILE=...`) in a small `env.sh` the agents source before building; name
it in the Project map's *Environment activation*. Home-directory quotas are often tight on
clusters: install on the project or scratch filesystem.

## CI

`.github/workflows/latex.yml` builds `templates/thesis/report.tex` with XeLaTeX on every
push (the fallback fonts make this work without Arial) and uploads the PDF as an artifact.
Copy the workflow into your thesis repository and point it at your thesis directory to get
the same check on every commit.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `! Extra }` while reading `report.aux`; `malformed bcf` | corrupted generated state | `latexmk -C`, rebuild |
| `! LaTeX Error: File 'figures/...' not found` | wrong or stale `\includegraphics` path | check the note's `Active figures:`; never copy a figure in by hand |
| `fontspec error: "font-not-found"` | a font named in the preamble is missing | the class falls back for Arial and Roboto Slab; for others, install or build with `-pdf` |
| build takes minutes per pass | over-resolution rasters | keep embedded images at ≤ 600 DPI at display size; prefer PDF figures |
| the `?` prompt hangs | an engine run without `-interaction` | always build through `latexmk` and the `.latexmkrc` |
| biber errors on a pasted entry | encoding or smart quotes in the `.bib` | the polisher cleans pasted BibTeX before appending |
