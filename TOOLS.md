# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## OpenClaw Browser Relay

### Known-good port mapping
- **Gateway / Control UI port:** `18789`
- **Chrome Browser Relay extension Options → Port:** `18792`

### Troubleshooting order
1. Check Chrome extension Options port is **18792** (not 18789).
2. Re-save the token in the extension.
3. If auth errors persist, compare:
   - `~/.openclaw/openclaw.json` → `gateway.auth.token`
   - `~/Library/LaunchAgents/ai.openclaw.gateway.plist` → `EnvironmentVariables.OPENCLAW_GATEWAY_TOKEN`
4. If needed, fully quit Chrome (`⌘Q`) and retry attach.

### Useful token lookup commands
```bash
# openclaw.json token
python3 - <<'PY'
import json, os
p=os.path.expanduser("~/.openclaw/openclaw.json")
print(json.load(open(p))["gateway"]["auth"]["token"])
PY

# launchd service token
python3 - <<'PY'
import plistlib, pathlib
p = pathlib.Path.home() / "Library/LaunchAgents/ai.openclaw.gateway.plist"
pl = plistlib.loads(p.read_bytes())
print(pl["EnvironmentVariables"]["OPENCLAW_GATEWAY_TOKEN"])
PY
```

### Symptom notes
- `Gateway token rejected` = token mismatch / wrong token for current relay path.
- Relay settings can look healthy while attach still fails if the port is wrong.
- “Connected/연결됨” after using `18792` is the reliable success signal.
