#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMPDIR="$(mktemp -d "${TMPDIR:-/tmp}/blocksync-packager-gates.XXXXXX")"
trap 'rm -rf "$TMPDIR"' EXIT

FINAL_METADATA="$TMPDIR/final-metadata.md"
"$ROOT/.venv/bin/python" "$ROOT/scripts/test_packager_dry_run_record.py" --write-fixture "$FINAL_METADATA"
PENDING_METADATA="$TMPDIR/pending-metadata.md"
sed -e 's/date_added: "[^"]*"/date_added: "PENDING-YYYY-MM-DD"/' \
    -e 's/commit: "[^"]*"/commit: "PENDING_FINAL_40_CHARACTER_COMMIT"/' \
    "$FINAL_METADATA" > "$PENDING_METADATA"
export PACKAGE_METADATA_PATH="$PENDING_METADATA"
export PACKAGER_WORK_DIR="$TMPDIR/packager-work"
export PACKAGER_DRY_RUN_RECORD_PATH="$TMPDIR/packager-record.json"
export PACKAGER_DRY_RUN_RECORD_OUTPUT="$TMPDIR/packager-record.md"
export GFTOOLS_BIN=false

expect_blocked() {
    local label="$1"
    local expected="$2"
    shift 2
    local output

    if output="$("$@" 2>&1)"; then
        echo "Expected Packager wrapper to block: $label"
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

assert_contains() {
    local label="$1"
    local expected="$2"
    local file="$3"

    if ! grep -Fq -- "$expected" "$file"; then
        echo "Expected report text not found for: $label"
        echo "Expected: $expected"
        cat "$file"
        exit 1
    fi
}

assert_not_contains() {
    local label="$1"
    local unexpected="$2"
    local file="$3"

    if grep -Fq -- "$unexpected" "$file"; then
        echo "Unexpected report text found for: $label"
        echo "Unexpected: $unexpected"
        cat "$file"
        exit 1
    fi
}

expect_blocked "missing google/fonts checkout" "GF_REPO_PATH is not a git checkout" \
    env GF_REPO_PATH="$TMPDIR/missing" bash "$ROOT/scripts/package_gf_dry_run.sh"

GF_REPO="$TMPDIR/fonts"
git init -q -b main "$GF_REPO"
git -C "$GF_REPO" remote add origin git@github.com:eliheuer/fonts.git
git -C "$GF_REPO" remote add upstream https://github.com/google/fonts.git
mkdir -p "$GF_REPO/ofl/blocksync"
touch "$GF_REPO/ofl/blocksync/.keep"
git -C "$GF_REPO" add ofl/blocksync/.keep
git -C "$GF_REPO" -c user.name="Blocksync Test" -c user.email="blocksync-test@example.com" commit -q -m "initial"

git -C "$GF_REPO" checkout -q -b not-main
expect_blocked "non-main checkout" "GF_REPO_PATH must be on main" \
    env GF_REPO_PATH="$GF_REPO" bash "$ROOT/scripts/package_gf_dry_run.sh"

git -C "$GF_REPO" checkout -q main
mkdir -p "$GF_REPO/ofl/virtuagrotesk"
printf 'dirty\n' >"$GF_REPO/ofl/virtuagrotesk/METADATA.pb"
expect_blocked "dirty outside package" "dirty paths outside ofl/blocksync" \
    env GF_REPO_PATH="$GF_REPO" bash "$ROOT/scripts/package_gf_dry_run.sh"

CLEAN_REPO="$TMPDIR/clean-fonts"
git init -q -b main "$CLEAN_REPO"
git -C "$CLEAN_REPO" remote add origin git@github.com:eliheuer/fonts.git
git -C "$CLEAN_REPO" remote add upstream https://github.com/google/fonts.git
mkdir -p "$CLEAN_REPO/ofl/blocksync"
touch "$CLEAN_REPO/ofl/blocksync/.keep"
git -C "$CLEAN_REPO" add ofl/blocksync/.keep
git -C "$CLEAN_REPO" -c user.name="Blocksync Test" -c user.email="blocksync-test@example.com" commit -q -m "initial"
git -C "$CLEAN_REPO" update-ref refs/remotes/origin/main HEAD
git -C "$CLEAN_REPO" update-ref refs/remotes/upstream/main HEAD
CLEAN_REPO_DISPLAY="$(cd "$CLEAN_REPO" && pwd)"

PACKAGE_REPORT="$TMPDIR/package-readiness.md"
env \
    GF_REPO_PATH="$GF_REPO" \
    GF_CLEAN_REPO_PATH="$CLEAN_REPO" \
    PACKAGE_DRY_RUN_READINESS_OUTPUT="$PACKAGE_REPORT" \
    "$ROOT/.venv/bin/python" "$ROOT/scripts/report_package_dry_run_readiness.py" >/dev/null
assert_contains "package report clean checkout" "Clean checkout avoids shared dirty paths: yes" "$PACKAGE_REPORT"
assert_contains "package report effective checkout" "Effective checkout path for final dry run: \`$CLEAN_REPO_DISPLAY\`" "$PACKAGE_REPORT"
assert_not_contains "package report dirty outside blocker" "- google/fonts checkout has dirty paths outside ofl/blocksync" "$PACKAGE_REPORT"

FINAL_ARCHIVE="$TMPDIR/final-archive.md"
FINAL_FONT="$TMPDIR/Blocksync[wdth,wght].ttf"
FINAL_PACKAGE_REPORT="$TMPDIR/final-package-readiness.md"
printf 'Local release archive hashes match source files: yes\n' >"$FINAL_ARCHIVE"
touch "$FINAL_FONT"
env \
    GF_REPO_PATH="$GF_REPO" \
    GF_CLEAN_REPO_PATH="$CLEAN_REPO" \
    PACKAGE_METADATA_PATH="$FINAL_METADATA" \
    RELEASE_ARCHIVE_MANIFEST_PATH="$FINAL_ARCHIVE" \
    BUILT_VARIABLE_FONT_PATH="$FINAL_FONT" \
    PACKAGE_DRY_RUN_READINESS_OUTPUT="$FINAL_PACKAGE_REPORT" \
    "$ROOT/.venv/bin/python" "$ROOT/scripts/report_package_dry_run_readiness.py" >/dev/null
assert_contains "final package report ready" "Ready to run final no-PR Packager dry run: yes" "$FINAL_PACKAGE_REPORT"
assert_contains "final package report clean checkout" "Clean checkout avoids shared dirty paths: yes" "$FINAL_PACKAGE_REPORT"
assert_contains "final package report effective checkout" "Effective checkout path for final dry run: \`$CLEAN_REPO_DISPLAY\`" "$FINAL_PACKAGE_REPORT"
assert_not_contains "final package report date placeholder" "- metadata date_added is still a placeholder" "$FINAL_PACKAGE_REPORT"
assert_not_contains "final package report commit placeholder" "- metadata source.commit is still a placeholder" "$FINAL_PACKAGE_REPORT"

DOWNSTREAM_REPORT="$TMPDIR/downstream-readiness.md"
env \
    GF_REPO_PATH="$GF_REPO" \
    GF_CLEAN_REPO_PATH="$CLEAN_REPO" \
    DOWNSTREAM_METADATA_PATH="$FINAL_METADATA" \
    DOWNSTREAM_PR_READINESS_OUTPUT="$DOWNSTREAM_REPORT" \
    "$ROOT/.venv/bin/python" "$ROOT/scripts/report_downstream_pr_readiness.py" >/dev/null
assert_contains "downstream report clean base" "Suggested clean checkout base ready: yes" "$DOWNSTREAM_REPORT"
assert_contains "downstream report effective base" "Effective clean fork base ready for branch: yes" "$DOWNSTREAM_REPORT"
assert_contains "downstream report clean dry-run command" "GF_REPO_PATH=$CLEAN_REPO_DISPLAY make package-dry-run" "$DOWNSTREAM_REPORT"
assert_not_contains "downstream report dirty outside blocker" "- google/fonts checkout has dirty paths outside ofl/blocksync" "$DOWNSTREAM_REPORT"

rm -rf "$GF_REPO/ofl/virtuagrotesk"
FAKE_GFTOOLS="$TMPDIR/fake-gftools"
{
    printf '#!/usr/bin/env bash\n'
    printf 'set -euo pipefail\n'
    printf 'if [[ "${1:-}" != "packager" ]]; then exit 99; fi\n'
    printf '[[ "$#" -eq 4 && "$4" == "--build-from-source" ]]\n'
    printf 'mkdir -p "$3/ofl/blocksync"\n'
    printf 'cp "$2" "$3/ofl/blocksync/METADATA.pb"\n'
} >"$FAKE_GFTOOLS"
chmod +x "$FAKE_GFTOOLS"
env \
    GF_REPO_PATH="$GF_REPO" \
    PACKAGE_METADATA_PATH="$FINAL_METADATA" \
    GFTOOLS_BIN="$FAKE_GFTOOLS" \
    bash "$ROOT/scripts/package_gf_dry_run.sh" >/dev/null
assert_contains "wrapper records final dry run" "Final no-PR Packager dry run recorded: yes" "$PACKAGER_DRY_RUN_RECORD_OUTPUT"
assert_contains "wrapper passes metadata override" '"metadata_date_added": "2026-05-30"' "$PACKAGER_DRY_RUN_RECORD_PATH"

mkdir -p "$GF_REPO/ofl/blocksync"
printf 'allowed dirty\n' >"$GF_REPO/ofl/blocksync/METADATA.pb"
expect_blocked "metadata placeholders" "metadata draft still has final-value placeholders" \
    env GF_REPO_PATH="$GF_REPO" bash "$ROOT/scripts/package_gf_dry_run.sh"

echo "Package dry-run gate tests passed."
