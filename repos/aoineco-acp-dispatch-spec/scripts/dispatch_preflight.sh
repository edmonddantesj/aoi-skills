#!/usr/bin/env bash
set -euo pipefail

DIR="${1:-}"
if [[ -z "$DIR" || ! -d "$DIR" ]]; then
  echo "Usage: $0 <dispatch_dir>" >&2
  exit 2
fi

# required files
req=("README.md" "agent-manifest.json")
for f in "${req[@]}"; do
  [[ -f "$DIR/$f" ]] || { echo "MISSING: $f"; exit 3; }
done

# required deliverables
ls "$DIR"/ACP_DISPATCH_002__onepager__bought_and_analyzed__AOINECO_\$NECO.md >/dev/null 2>&1 || { echo "MISSING onepager EN"; exit 4; }
ls "$DIR"/ACP_DISPATCH_002__onepager__bought_and_analyzed__AOINECO_\$NECO_KR.md >/dev/null 2>&1 || { echo "MISSING onepager KR"; exit 4; }
ls "$DIR"/ACP_DISPATCH_002__preface__AOINECO_\$NECO.md >/dev/null 2>&1 || { echo "MISSING preface"; exit 4; }

# forbidden terms scan
forbidden=(
  "청묘"
  "TOP SECRET"
  "STEALTH"
  "PRIVATE_KEY"
  "SECRET_"
  "sb_secret_"
  "ntn_"
  "ghp_"
  "github_pat_"
)

hit=0
while IFS= read -r -d '' file; do
  for term in "${forbidden[@]}"; do
    if rg -n --fixed-strings "$term" "$file" >/dev/null 2>&1; then
      echo "FORBIDDEN HIT: $term in $file"
      rg -n --fixed-strings "$term" "$file" | head -n 3 || true
      hit=1
    fi
  done

done < <(find "$DIR" -type f \( -name '*.md' -o -name '*.json' \) -print0)

if [[ "$hit" -eq 1 ]]; then
  echo "FAIL: forbidden terms" >&2
  exit 5
fi

echo "PASS preflight: $DIR"
