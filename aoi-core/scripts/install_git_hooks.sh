#!/bin/sh
set -e

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [ -z "$REPO_ROOT" ]; then
  echo "Not inside a git repo. cd into the repo and re-run." >&2
  exit 1
fi

HOOKS_DIR="$REPO_ROOT/.git/hooks"
SRC="$REPO_ROOT/scripts/git-hooks/pre-push"
DST="$HOOKS_DIR/pre-push"

if [ ! -f "$SRC" ]; then
  echo "Missing hook source: $SRC" >&2
  exit 1
fi

mkdir -p "$HOOKS_DIR"
cp "$SRC" "$DST"
chmod +x "$DST"

echo "✅ Installed pre-push hook"
echo "- $DST"
