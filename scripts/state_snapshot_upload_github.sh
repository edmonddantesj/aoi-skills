#!/usr/bin/env bash
set -euo pipefail

# Upload the newest state snapshot bundle to GitHub Releases (private repo).
#
# Repo: edmonddantesj/aoi-state-saves
# Assets:
# - state_snapshot__*.tar.gz
# - state_snapshot__*__manifest.txt
# - state_snapshot__*__sha256.txt
#
# Usage:
#   ./scripts/state_snapshot_upload_github.sh            # uploads latest
#   SNAP=state_snapshot__20260306_160843 ./scripts/state_snapshot_upload_github.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WS_DIR="${AOI_WORKSPACE_ROOT:-$HOME/.openclaw/workspace}"
if [[ -d "$WS_DIR/artifacts/state_saves" ]]; then
  STATE_DIR="$WS_DIR/artifacts/state_saves"
else
  STATE_DIR="$ROOT_DIR/artifacts/state_saves"
fi
REPO="edmonddantesj/aoi-state-saves"

if ! command -v gh >/dev/null 2>&1; then
  echo "WARN: gh CLI not found; local snapshot exists but GitHub upload skipped" >&2
  exit 3
fi

SNAP_BASENAME="${SNAP:-}"

if [[ -z "$SNAP_BASENAME" ]]; then
  SNAP_BASENAME="$(
    ls -1 "$STATE_DIR"/state_snapshot__*.tar.gz \
      | sed -E 's#.*/(state_snapshot__[^.]+)\.tar\.gz#\1#' \
      | sort \
      | tail -n 1
  )"
fi

TAR="$STATE_DIR/${SNAP_BASENAME}.tar.gz"
MAN="$STATE_DIR/${SNAP_BASENAME}__manifest.txt"
SHA="$STATE_DIR/${SNAP_BASENAME}__sha256.txt"

for f in "$TAR" "$MAN" "$SHA"; do
  if [[ ! -f "$f" ]]; then
    echo "ERROR: missing file: $f" >&2
    exit 2
  fi
done

tag="$SNAP_BASENAME"

tmp_notes="$ROOT_DIR/artifacts/state_saves/${SNAP_BASENAME}__release_notes.txt"
cat > "$tmp_notes" <<EOF
Workspace state snapshot uploaded from $ROOT_DIR

Assets:
- $(basename "$TAR")
- $(basename "$MAN")
- $(basename "$SHA")
EOF

# Important: unset GITHUB_TOKEN to avoid PAT 403 overriding keychain auth.
env -u GITHUB_TOKEN gh release view "$tag" --repo "$REPO" >/dev/null 2>&1 || \
  env -u GITHUB_TOKEN gh release create "$tag" \
    --repo "$REPO" \
    --title "$tag" \
    --notes-file "$tmp_notes" \
    --latest=false

# Upload assets (overwrite if already present)
env -u GITHUB_TOKEN gh release upload "$tag" \
  --repo "$REPO" \
  "$TAR" "$MAN" "$SHA" \
  --clobber

echo "STATUS: uploaded"
echo "PROOF: repo=https://github.com/$REPO/releases/tag/$tag"
