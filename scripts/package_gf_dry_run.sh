#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GF_REPO_PATH="${GF_REPO_PATH:-/Users/eli/GH/forks/fonts}"
METADATA_DRAFT="${PACKAGE_METADATA_PATH:-${METADATA_DRAFT_PATH:-$ROOT/documentation/google-fonts-downstream-metadata-draft.md}}"
PACKAGE_DIR="ofl/blocksync"
WORK_DIR="${PACKAGER_WORK_DIR:-$ROOT/out/google-fonts-packager}"
METADATA_PB="$WORK_DIR/METADATA.pb"
GFTOOLS_BIN="${GFTOOLS_BIN:-$ROOT/venv/bin/gftools}"
VENV_PYTHON="${VENV_PYTHON:-$ROOT/venv/bin/python}"
PACKAGER_RECORD_PATH="${PACKAGER_DRY_RUN_RECORD_PATH:-$ROOT/documentation/google-fonts-packager-dry-run-record.json}"
PACKAGER_RECORD_OUTPUT="${PACKAGER_DRY_RUN_RECORD_OUTPUT:-$ROOT/documentation/packager-dry-run-record.md}"

if [[ ! -d "$GF_REPO_PATH/.git" ]]; then
    echo "GF_REPO_PATH is not a git checkout: $GF_REPO_PATH" >&2
    exit 2
fi

if [[ "$(git -C "$GF_REPO_PATH" rev-parse --abbrev-ref HEAD)" != "main" ]]; then
    echo "GF_REPO_PATH must be on main before the no-PR Packager dry run." >&2
    exit 2
fi

dirty_outside="$(git -C "$GF_REPO_PATH" status --porcelain | grep -vE "^(.. )?${PACKAGE_DIR}/" || true)"
if [[ -n "$dirty_outside" ]]; then
    echo "google/fonts checkout has dirty paths outside $PACKAGE_DIR:" >&2
    echo "$dirty_outside" >&2
    exit 2
fi

if grep -q 'PENDING-YYYY-MM-DD\|PENDING_FINAL_40_CHARACTER_COMMIT' "$METADATA_DRAFT"; then
    echo "Refusing Packager dry run: metadata draft still has final-value placeholders." >&2
    echo "Run make final-readiness-check for the current blocker list." >&2
    exit 2
fi

mkdir -p "$WORK_DIR"
python3 - "$METADATA_DRAFT" "$METADATA_PB" <<'PY'
from pathlib import Path
import re
import sys

source = Path(sys.argv[1]).read_text(encoding="utf-8")
match = re.search(r"```textproto\n(.*?)\n```", source, flags=re.S)
if not match:
    raise SystemExit("metadata draft must contain a textproto fenced block")
Path(sys.argv[2]).write_text(match.group(1).strip() + "\n", encoding="utf-8")
PY

"$GFTOOLS_BIN" packager "$METADATA_PB" "$GF_REPO_PATH"
"$VENV_PYTHON" "$ROOT/scripts/report_packager_dry_run_record.py" \
    --record-success \
    --strict \
    --gf-repo-path "$GF_REPO_PATH" \
    --metadata "$METADATA_DRAFT" \
    --record-path "$PACKAGER_RECORD_PATH" \
    --output "$PACKAGER_RECORD_OUTPUT"

echo ""
echo "Packager dry run finished. Review $GF_REPO_PATH/$PACKAGE_DIR before any PR-mode run."
