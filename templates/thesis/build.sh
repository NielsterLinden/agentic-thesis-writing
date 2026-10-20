#!/usr/bin/env bash
# Build report.pdf with latexmk (XeLaTeX + biber per .latexmkrc).
#
#   ./build.sh          minimum passes
#   ./build.sh -gg      force a full rebuild
#   ./build.sh -pdf     pdfLaTeX fallback (free fonts)
#   ./build.sh -C       clean generated files and exit
set -euo pipefail
cd "$(dirname "$0")"

engine="-pdfxe"
extra=()
for a in "$@"; do
    case "$a" in
        -C)   latexmk -C; exit 0 ;;
        -pdf) engine="-pdf" ;;
        *)    extra+=("$a") ;;
    esac
done

latexmk "$engine" ${extra[@]+"${extra[@]}"} report.tex
echo "Built: $(pwd)/report.pdf"
