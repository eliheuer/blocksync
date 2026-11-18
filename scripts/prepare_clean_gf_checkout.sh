#!/usr/bin/env bash
set -euo pipefail

SOURCE_REPO="${GF_REPO_SOURCE:-/Users/eli/GH/forks/fonts}"
DEST_REPO="${GF_CLEAN_REPO_PATH:-/private/tmp/blocksync-google-fonts}"

if [[ ! -d "$SOURCE_REPO/.git" ]]; then
    echo "GF_REPO_SOURCE is not a git checkout: $SOURCE_REPO" >&2
    exit 2
fi

origin_url="$(git -C "$SOURCE_REPO" remote get-url origin 2>/dev/null || true)"
upstream_url="$(git -C "$SOURCE_REPO" remote get-url upstream 2>/dev/null || true)"

if [[ -d "$DEST_REPO/.git" ]]; then
    if [[ -n "$(git -C "$DEST_REPO" status --porcelain)" ]]; then
        echo "Clean checkout already exists but is dirty: $DEST_REPO" >&2
        git -C "$DEST_REPO" status --short >&2
        exit 2
    fi
else
    mkdir -p "$(dirname "$DEST_REPO")"
    git clone --shared "$SOURCE_REPO" "$DEST_REPO"
fi

git -C "$DEST_REPO" checkout main

if [[ -n "$origin_url" ]]; then
    git -C "$DEST_REPO" remote set-url origin "$origin_url"
fi

if [[ -n "$upstream_url" ]]; then
    if git -C "$DEST_REPO" remote get-url upstream >/dev/null 2>&1; then
        git -C "$DEST_REPO" remote set-url upstream "$upstream_url"
    else
        git -C "$DEST_REPO" remote add upstream "$upstream_url"
    fi
fi

for ref in refs/remotes/origin/main refs/remotes/upstream/main; do
    if source_sha="$(git -C "$SOURCE_REPO" rev-parse --verify "$ref" 2>/dev/null)"; then
        git -C "$DEST_REPO" update-ref "$ref" "$source_sha"
    fi
done

echo "Prepared clean google/fonts checkout: $DEST_REPO"
echo "Use: GF_REPO_PATH=\"$DEST_REPO\" make package-dry-run-readiness"
