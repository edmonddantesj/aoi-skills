# AOI Skills

Public-safe OpenClaw skills published by **Aoineco & Co.**

## Support / Issues
- Please file bugs and requests in **GitHub Issues** for this repo.
- Include the **skill slug** (e.g., `aoi-demo-clip-maker`) in the issue title.

## Skills
- aoi-demo-clip-maker — https://clawhub.com/skills/aoi-demo-clip-maker
- aoi-hackathon-scout-lite — https://clawhub.com/skills/aoi-hackathon-scout-lite
- aoi-council — https://clawhub.com/skills/aoi-council
- aoi-triple-memory-lite — https://clawhub.com/skills/aoi-triple-memory-lite
- aoi-prompt-injection-sentinel — https://clawhub.com/skills/aoi-prompt-injection-sentinel
- aoi-sandbox-shield-lite — https://clawhub.com/skills/aoi-sandbox-shield-lite
- aoi-upbit-market-data-remaster — https://clawhub.com/skills/aoi-upbit-market-data-remaster

## Policy
- No secrets in issues (keys/tokens/private URLs/internal paths).
- Public-safe scope for free releases.

---

## AOI Guard Cheat Sheet (When commits are blocked)

This repo uses **AOI Guard** (default-deny). If a commit/push is blocked:

1) See what you staged:
```bash
git status
```

2) If you added a new file/folder intentionally, allow it (with Edmond approval):
```bash
# edit allowlist
nano .aoi-allowlist

# then
git add .aoi-allowlist
```

3) Re-stage only what you want, then commit:
```bash
git add <files>
git commit -m "..."
```

Rule of thumb: **new paths must be added to `.aoi-allowlist` first**, otherwise commits will be blocked.
