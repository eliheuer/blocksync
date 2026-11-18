#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-$ROOT/venv/bin/python}"
if [[ ! -x "$PYTHON" ]]; then
    PYTHON="python3"
fi
TMPDIR="$(mktemp -d "${TMPDIR:-/tmp}/blocksync-release-archive-gates.XXXXXX")"
trap 'rm -rf "$TMPDIR"' EXIT

write_metadata() {
    local path="$1"
    shift
    {
        printf '```textproto\n'
        printf 'source {\n'
        for source_file in "$@"; do
            printf '  files {\n'
            printf '    source_file: "%s"\n' "$source_file"
            printf '    dest_file: "%s"\n' "$(basename "$source_file")"
            printf '  }\n'
        done
        printf '}\n'
        printf '```\n'
    } >"$path"
}

write_metadata_pair() {
    local path="$1"
    local source_file="$2"
    local dest_file="$3"
    {
        printf '```textproto\n'
        printf 'source {\n'
        printf '  files {\n'
        printf '    source_file: "%s"\n' "$source_file"
        printf '    dest_file: "%s"\n' "$dest_file"
        printf '  }\n'
        printf '}\n'
        printf '```\n'
    } >"$path"
}

expect_blocked() {
    local label="$1"
    local expected="$2"
    shift 2
    local output

    if output="$("$@" 2>&1)"; then
        echo "Expected release archive gate to block: $label"
        echo "$output"
        exit 1
    fi
    if [[ "$output" != *"$expected"* ]]; then
        echo "Expected message not found for: $label"
        echo "Expected: $expected"
        echo "$output"
        exit 1
    fi
}

SAFE_METADATA="$TMPDIR/safe.md"
EMPTY_METADATA="$TMPDIR/empty.md"
UNSAFE_METADATA="$TMPDIR/unsafe.md"
DUPLICATE_METADATA="$TMPDIR/duplicate.md"
UNSAFE_DEST_METADATA="$TMPDIR/unsafe-dest.md"
DUPLICATE_DEST_METADATA="$TMPDIR/duplicate-dest.md"
MISSING_METADATA="$TMPDIR/missing.md"

write_metadata "$SAFE_METADATA" "OFL.txt" "documentation/DESCRIPTION.en_us.html"
printf '```textproto\nsource {\n}\n```\n' >"$EMPTY_METADATA"
write_metadata "$UNSAFE_METADATA" "../evil.txt"
write_metadata "$DUPLICATE_METADATA" "OFL.txt" "OFL.txt"
write_metadata_pair "$UNSAFE_DEST_METADATA" "OFL.txt" "../evil.txt"
{
    printf '```textproto\nsource {\n'
    printf '  files { source_file: "OFL.txt" dest_file: "duplicate.txt" }\n'
    printf '  files { source_file: "documentation/DESCRIPTION.en_us.html" dest_file: "duplicate.txt" }\n'
    printf '}\n```\n'
} >"$DUPLICATE_DEST_METADATA"
write_metadata "$MISSING_METADATA" "documentation/does-not-exist.txt"

"$PYTHON" "$ROOT/scripts/build_release_archive.py" \
    --metadata "$SAFE_METADATA" \
    --output "$TMPDIR/safe.zip" \
    --manifest "$TMPDIR/safe-manifest.md" >/dev/null

expect_blocked "missing source_file entries" "no source.files entries found" \
    "$PYTHON" "$ROOT/scripts/build_release_archive.py" --metadata "$EMPTY_METADATA" --output "$TMPDIR/out.zip" --manifest "$TMPDIR/out.md"
expect_blocked "unsafe source_file paths" "unsafe source_file paths" \
    "$PYTHON" "$ROOT/scripts/build_release_archive.py" --metadata "$UNSAFE_METADATA" --output "$TMPDIR/out.zip" --manifest "$TMPDIR/out.md"
expect_blocked "duplicate source_file paths" "duplicate source_file paths" \
    "$PYTHON" "$ROOT/scripts/build_release_archive.py" --metadata "$DUPLICATE_METADATA" --output "$TMPDIR/out.zip" --manifest "$TMPDIR/out.md"
expect_blocked "unsafe dest_file paths" "unsafe dest_file paths" \
    "$PYTHON" "$ROOT/scripts/build_release_archive.py" --metadata "$UNSAFE_DEST_METADATA" --output "$TMPDIR/out.zip" --manifest "$TMPDIR/out.md"
expect_blocked "duplicate dest_file paths" "duplicate dest_file paths" \
    "$PYTHON" "$ROOT/scripts/build_release_archive.py" --metadata "$DUPLICATE_DEST_METADATA" --output "$TMPDIR/out.zip" --manifest "$TMPDIR/out.md"
expect_blocked "missing source file" "missing source files" \
    "$PYTHON" "$ROOT/scripts/build_release_archive.py" --metadata "$MISSING_METADATA" --output "$TMPDIR/out.zip" --manifest "$TMPDIR/out.md"

echo "Release archive gate tests passed."
