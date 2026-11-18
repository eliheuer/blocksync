#!/bin/bash

# Build script for Blocksync fonts.
# The Google Fonts-ready path is sources/config.yaml -> Blocksync.designspace
# -> UFO masters.

set -euo pipefail

if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "Building Blocksync fonts..."

rm -rf build build.ninja .ninja_log fonts sources/build.ninja sources/.ninja_log sources/instance_ufos
mkdir -p fonts/variable fonts/ttf

if command -v gftools >/dev/null 2>&1; then
    echo ""
    echo "Building with gftools builder..."
    gftools builder sources/config.yaml
    built_fonts=()
    while IFS= read -r font_path; do
        built_fonts+=("$font_path")
    done < <(find fonts/variable fonts/ttf -type f -name "*.ttf" 2>/dev/null)
    if [ "${#built_fonts[@]}" -gt 0 ]; then
        python scripts/fix_gf_metadata.py "${built_fonts[@]}"
    fi
    echo ""
    echo "Build complete. Fonts are in fonts/:"
    find fonts -type f -name "*.ttf" -print
    exit 0
fi

if command -v fontmake >/dev/null 2>&1; then
    echo ""
    echo "gftools is not installed; using fontmake fallback."
    fontmake -m sources/Blocksync.designspace -o variable --output-dir fonts/variable
    fontmake -m sources/Blocksync.designspace -i -o ttf --output-dir fonts/ttf
    fallback_fonts=()
    while IFS= read -r font_path; do
        fallback_fonts+=("$font_path")
    done < <(find fonts/variable fonts/ttf -type f -name "*.ttf" 2>/dev/null)
    if [ "${#fallback_fonts[@]}" -gt 0 ]; then
        python scripts/fix_gf_metadata.py "${fallback_fonts[@]}"
    fi
    echo ""
    echo "Build complete. Fonts are in fonts/:"
    find fonts -type f -name "*.ttf" -print
    exit 0
fi

echo "Neither gftools nor fontmake is available. Install requirements.txt first." >&2
exit 1
