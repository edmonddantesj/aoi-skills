# ADP Restore Brief — 2026-03-12 v0.1

## Current state
- Current ADP UI repo exists at:
  - `/Users/silkroadcat/.openclaw/workspace/agents/maintainer/repos/aoineco-dataplane-ui`
  - GitHub: `edmonddantesj/aoineco-dataplane-ui`
- Current repo state is **skeleton/stub only**, not the previously richer internal server dashboard.
- Existing implemented page sections in current repo:
  - Overview (stub)
  - Recent Proof (GitHub API route wired)
  - Squad Status / Roster (stub text only)
  - Kanban (stub text only)
- From backup evidence, prior ADP had more than the current skeleton:
  - PixelOfficeMap.tsx (legacy isometric pixel office)
  - AgentRosterStrip.tsx (roster-first home UI)
  - `/legacy/pixel-office` route
  - status→zone movement MVP
  - ADP dev server on port 3010, exposed via Tailscale hostname

## Evidence sources used
1. Telegram ADP topic backup:
   - `/Users/silkroadcat/.openclaw/workspace/inbox/chatexport_2026-03-08_adp/ChatExport_2026-03-08 (11)/messages.html`
2. Current ADP UI repo:
   - `/Users/silkroadcat/.openclaw/workspace/agents/maintainer/repos/aoineco-dataplane-ui`
3. Reconstructed ADP SSOT/task docs already present locally:
   - `context/adp/ADP_AGENT_STATE_SCHEMA_V0_1.md`
   - `context/ops/items/TASK-20260304-ADP-*.md`

## Recovered prior-page structure/content from backup
### Home dashboard
- Archive-tone private internal dashboard
- Panels confirmed in backup:
  - Overview
  - Recent Proof
  - Squad Status (Roster-first)
  - Kanban (Ralph-loop)
- Home default was changed from isometric office to **12-agent roster view**.

### Legacy/experimental page
- Isometric Pixel Office was preserved as optional/experimental page:
  - `/legacy/pixel-office`

### Data/behavior confirmed in backup
- ADP agent state schema v0.1:
  - `agent_id, display_name, status, message, updated_at`
  - canonical statuses: `idle | writing | syncing | error`
- Pixel Office movement mapping:
  - idle → rest
  - writing → desk
  - syncing → server
  - error → bug
- Recent Proof was wired to GitHub-backed notion snapshot artifacts.

## Tailscale/internal serving history from backup
- Prior internal dev path existed with port 3010 and Tailscale exposure.
- Evidence in backup mentions:
  - `http://127.0.0.1:3010/`
  - `http://choi-macmini.tailc63c7c.ts.net/`
- This indicates the intended mode remains: internal/private dashboard reachable over Tailscale.

## Pixel asset recovery status
### Confirmed from backup evidence
- There previously existed 12 role sprite sets under:
  - `projects/adp/public/pixel/roles/<roleId>/idle.png`
  - `walk.png`
  - `work.png`
  - `error.png` (at least for some/all roles)
- Example roleIds explicitly mentioned in backup:
  - `aoineco`
  - `oracle`
  - `blue_sound`
  - `blue_eye`
  - `blue_maintainer`
  - `blue_gear`
  - `blue_brain`
- Backup also states user had produced 12 character profile/pixel images and could provide source files.

### Current local status
- Those sprite folders/files are **not currently present** in the current maintainer ADP UI repo.
- Therefore current status is:
  - evidence of prior existence: **yes**
  - current recoverable local asset files found: **no**
  - action needed: recover from backup source / Telegram ZIP / other repo / local archive if available

## Immediate execution plan
1. Reconstruct ADP page structure from backup into current `aoineco-dataplane-ui` repo.
2. Restore private/internal serving path for Tailscale-accessible ADP instance.
3. Build a pixel asset inventory document:
   - confirmed roleIds
   - found/missing files
   - required animations per role
4. Search broader workspace/backups for hidden asset archives or prior export bundles.
5. If local asset originals are not found, request/reingest the original ZIP from Telegram and normalize into:
   - `public/pixel/roles/<roleId>/{idle,walk,work,error}.png`

## Decision-ready summary
- There is **not yet** a restored full ADP site in the current active repo; only a skeleton exists.
- We **do have enough backup evidence** to restore the prior page structure and behavior.
- Pixel character/profile assets are evidenced in backup but **not currently recovered as files** in the workspace.
