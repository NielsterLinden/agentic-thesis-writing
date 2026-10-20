#!/usr/bin/env bash
# Fetch the optional template assets (TU Delft logos and the sample cover image) from the
# upstream template repository into figures/. The document builds without them; with them
# the cover and title page look like the original template.
#
# The logos are TU Delft's; the sample cover is "Canadarm 2 Robotic Arm Grapples SpaceX
# Dragon" by NASA (CC BY-NC 2.0, modified), as credited in the template. Replace the cover
# with your own image and update the attribution in frontmatter/title-thesis.tex.
set -euo pipefail
cd "$(dirname "$0")"

base="https://raw.githubusercontent.com/dzwaneveld/tudelft-report-thesis-template/master/figures"
mkdir -p figures

fetch() {
    local name="$1"
    if [[ -f "figures/$name" ]]; then
        echo "exists: figures/$name"
        return
    fi
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$base/$name" -o "figures/$name"
    elif command -v wget >/dev/null 2>&1; then
        wget -q "$base/$name" -O "figures/$name"
    else
        echo "error: need curl or wget" >&2
        exit 1
    fi
    echo "fetched: figures/$name"
}

fetch logo-black.pdf
fetch logo-white.pdf
fetch cover.jpg
