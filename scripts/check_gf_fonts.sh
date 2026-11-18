#!/bin/bash

set -euo pipefail

FONT_PATHS=(
    'fonts/variable/Blocksync[wdth,wght].ttf'
)

if [ "${CHECK_STATIC:-0}" = "1" ]; then
    while IFS= read -r font_path; do
        FONT_PATHS+=("$font_path")
    done < <(find fonts/ttf -maxdepth 1 -type f -name '*.ttf' | sort)
fi

if ! command -v fontspector >/dev/null 2>&1; then
    echo "Missing fontspector. Install it from https://github.com/fonttools/fontspector/releases or with cargo-binstall."
    exit 1
fi

for font_path in "${FONT_PATHS[@]}"; do
    if [ ! -f "$font_path" ]; then
        echo "Missing $font_path. Run 'make build' before running Google Fonts QA."
        exit 1
    fi
done

if [ "${CHECK_STATIC:-0}" = "1" ]; then
    REPORT_HTML="out/fontspector/fontspector-static-report.html"
    REPORT_MD="out/fontspector/fontspector-static-report.md"
    BADGE_DIR="out/badges-static"
    echo "Running Fontspector on variable and static TTFs."
else
    REPORT_HTML="out/fontspector/fontspector-report.html"
    REPORT_MD="out/fontspector/fontspector-report.md"
    BADGE_DIR="out/badges"
    echo "Running Fontspector on the release variable font. Use CHECK_STATIC=1 $0 to include static TTF proofing outputs."
fi

mkdir -p out/fontspector "$BADGE_DIR" "$HOME/.fontspector"

fontspector \
    -p googlefonts \
    "${FONT_PATHS[@]}" \
    --exclude-checkid googlefonts/repo/dirname_matches_nameid_1 \
    --succinct \
    --loglevel warn \
    --skip-network \
    --full-lists \
    --badges "$BADGE_DIR" \
    --html "$REPORT_HTML" \
    --ghmarkdown "$REPORT_MD"
