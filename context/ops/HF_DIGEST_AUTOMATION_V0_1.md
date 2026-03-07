# Automation (SSOT)

이 폴더는 반복업무를 자동화하기 위한 스크립트/설정(launchd 등)을 보관한다.

## HF ACTIVE Digest (file-only)
- Generator: `scripts/hf_digest.py`
- Output: `context/ops/digests/HF_ACTIVE_DIGEST_LATEST.md`
- launchd plist: `context/ops/launchd/com.aoineco.hf-digest.plist`

### 설치/활성화(수동 1회)
```bash
# 1) LaunchAgents로 복사
cp context/ops/launchd/com.aoineco.hf-digest.plist ~/Library/LaunchAgents/

# 2) 로드(활성화)
launchctl load -w ~/Library/LaunchAgents/com.aoineco.hf-digest.plist

# 3) 상태
launchctl list | grep com.aoineco.hf-digest
```

### 비활성화
```bash
launchctl unload -w ~/Library/LaunchAgents/com.aoineco.hf-digest.plist
```
