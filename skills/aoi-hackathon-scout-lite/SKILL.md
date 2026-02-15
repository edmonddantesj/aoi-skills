---
name: aoi-hackathon-scout-lite
version: 0.1.0
description: Public-safe hackathon source registry + filtering output (no crawling, no submissions).
author: Aoineco & Co.
license: MIT
---

# AOI Hackathon Scout (Lite)

S-DNA: `AOI-2026-0215-SDNA-HACK01`

## Scope (public-safe)
- ✅ Outputs curated **source list** for hackathons / builder programs / grants
- ✅ Provides a filtering view: online-only preference, type tags
- ✅ Provides a paste-ready summary template for the user
- ❌ No crawling, no login, no form-fill, no submission automation
- ❌ No Notion API usage in the public skill (paste template only)

## Data source
- Uses the local registry file:
  - `context/HACKATHON_SOURCES_REGISTRY.md`

## Commands
### Show sources
```bash
aoi-hackathon sources
```

### Filter (best-effort)
```bash
# show only likely-online sources
# (filters Online-only fit = ✅ or ⚠️)
aoi-hackathon sources --online ok

# show only web3 sources
aoi-hackathon sources --type web3
```

### Recommend from shortlist (best-effort)
```bash
# reads context/HACKATHON_SHORTLIST.md and prints top N online-eligible items
# (excludes rejected; prioritizes 🔥 markers and 'applying/watching')
aoi-hackathon recommend --n 5
```

### Print Notion paste template (text only)
```bash
aoi-hackathon template
```

## Support
- Issues / bugs / requests: https://github.com/edmonddantesj/aoi-skills/issues
- Please include the skill slug: `aoi-hackathon-scout-lite`

## Provenance / originality
- AOI implementation is original code.
- Registry content is a curated link list.
