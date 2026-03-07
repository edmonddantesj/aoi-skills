#!/usr/bin/env bash
set -euo pipefail

# x-post tick runner (SSOT-friendly, safe-by-default)
# - Does NOT auto-post to X.
# - Only prepares an output skeleton + logs so a human can copy/paste.

ROOT="/Users/silkroadcat/.openclaw/workspace"
TS="$(date +"%Y%m%d_%H%M%S")"
OUT_DIR="$ROOT/artifacts/x-post/$TS"
LOG_DIR="$ROOT/artifacts/x-post/_logs"

mkdir -p "$OUT_DIR" "$LOG_DIR"

cat > "$OUT_DIR/OUTPUT_TEMPLATE.md" <<'MD'
# x-post output (copy/paste bundle)

## 후보 3개
1) 링크: 
   지표(좋아요/RT): 
   왜 터질 각: 

2) 링크: 
   지표(좋아요/RT): 
   왜 터질 각: 

3) 링크: 
   지표(좋아요/RT): 
   왜 터질 각: 

---

## 선정 1개 — C톤(20~35줄) + AOI 증빙

(여기에 중장문 초안)

### AOI 증빙 (체크리스트 5개 또는 미니표 1개)
- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 

### 인용 복붙 박스
원문(1~3줄):

링크:

커뮤니티 반응/2차 인용(1줄):
MD

cat > "$OUT_DIR/RUN_NOTES.md" <<MD
# run notes

- timestamp: $TS
- playbook: $ROOT/context/topics/x-post_PLAYBOOK_V0_1.md
- guardrails: read-only / 1-tab / <=4min / captcha->stop
- discovery engine: (fill: relay | openchrome | manual)
- stopped_reason: (none | captcha | relogin | dom_fail | other)
MD

{
  echo "[$(date -Iseconds)] x-post tick created: $OUT_DIR"
  echo "- Next: fill OUTPUT_TEMPLATE.md (후보3 + 초안1)"
  echo "- Rules: $ROOT/context/topics/x-post_PLAYBOOK_V0_1.md"
} | tee -a "$LOG_DIR/xpost_tick.log"
