# OpenClaw Telegram Topics Router

One-click-ish setup for splitting a Telegram **Forum** group into topics (threads) and maintaining a `thread_id → topic_slug` routing map for OpenClaw.

## What you get
- A portable OpenClaw skill folder: `openclaw-telegram-topics-router/`
- Scripts to initialize SSOT and update mappings

## Install (as a skill)

### Option A) One-liner install (macOS/Linux)
```bash
set -euo pipefail
URL="https://github.com/edmonddantesj/openclaw-telegram-topics-router/releases/latest/download/openclaw-telegram-topics-router.skill"
mkdir -p skills/public/openclaw-telegram-topics-router
curl -fsSL "$URL" -o /tmp/openclaw-telegram-topics-router.skill
unzip -o /tmp/openclaw-telegram-topics-router.skill -d skills/public/openclaw-telegram-topics-router
```

### Option A-2) One-liner install (Windows)

#### Windows (WSL Ubuntu) — recommended
Run in **PowerShell**:
```powershell
wsl.exe bash -lc 'set -euo pipefail; URL="https://github.com/edmonddantesj/openclaw-telegram-topics-router/releases/latest/download/openclaw-telegram-topics-router.skill"; mkdir -p skills/public/openclaw-telegram-topics-router; curl -fsSL "$URL" -o /tmp/openclaw-telegram-topics-router.skill; unzip -o /tmp/openclaw-telegram-topics-router.skill -d skills/public/openclaw-telegram-topics-router'
```

#### Windows (Git Bash)
Run in **Git Bash**:
```bash
set -euo pipefail
URL="https://github.com/edmonddantesj/openclaw-telegram-topics-router/releases/latest/download/openclaw-telegram-topics-router.skill"
mkdir -p skills/public/openclaw-telegram-topics-router
curl -fsSL "$URL" -o /tmp/openclaw-telegram-topics-router.skill
unzip -o /tmp/openclaw-telegram-topics-router.skill -d skills/public/openclaw-telegram-topics-router
```

### Option B) Download the `.skill` (recommended)
1) Download from Releases:
- <https://github.com/edmonddantesj/openclaw-telegram-topics-router/releases>

2) Unzip it into your workspace:
```bash
mkdir -p skills/public/openclaw-telegram-topics-router
unzip -o openclaw-telegram-topics-router.skill -d skills/public/openclaw-telegram-topics-router
```

### Option B) Git clone
```bash
git clone https://github.com/edmonddantesj/openclaw-telegram-topics-router
cd openclaw-telegram-topics-router
mkdir -p ../skills/public
cp -R openclaw-telegram-topics-router ../skills/public/
```

## Quick start
```bash
python3 skills/public/openclaw-telegram-topics-router/scripts/init_topics_ssot.py
python3 skills/public/openclaw-telegram-topics-router/scripts/add_mapping.py --slug ops --thread-id 38
python3 skills/public/openclaw-telegram-topics-router/scripts/audit_map.py
```

## Notes
- Creating Telegram topics is typically done in the Telegram UI.
- Calibration: send a ping message inside each topic/thread, then record its `message_thread_id`.

## License
MIT
