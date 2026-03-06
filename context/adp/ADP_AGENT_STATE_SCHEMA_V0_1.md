# ADP_AGENT_STATE_SCHEMA_V0_1

Status: **SSOT (reconstructed)**

- Source: Telegram topic 45 ADP log excerpt (2026-03-03 ~ 2026-03-05) recovered from `0305_ADP---*.docx`.
- Note: This file is a **rebuild** after `./openclaw` folder deletion / DB loss. Treat as canonical going forward.

## Purpose
Define the minimal agent state schema that drives ADP UI (Roster / Pixel Office), including status machine, UI rules, and derived behaviors.

## Core status machine (fixed)
Exactly these 4 statuses are canonical:

- `idle`
- `writing` (aka working)
- `syncing`
- `error`

If upstream sources produce other words (e.g. `executing`, `burning`, `coffee`, `sleeping`), they must be mapped to the 4-state machine at the boundary.

## Required fields
Each agent state record MUST provide:

- `agent_id` (string; stable id)
- `display_name` (string)
- `status` (enum: idle|writing|syncing|error)
- `message` (string; **1-line**; UI truncates)
- `updated_at` (ISO8601 string or epoch; must be comparable)

## Optional fields (v0.1)
- `role_id` (string) — used for sprite lookup: `/pixel/roles/${role_id}/${anim}.png`
- `zone` (string) — if backend wants to decide zone explicitly
- `x`, `y` (number) — if backend wants to decide coordinates explicitly

> Recommended: keep backend output minimal; UI derives `zone` and `x,y` from `status`.

## Derived rules (UI behavior)
### Offline detection
- Define `now - updated_at > OFFLINE_THRESHOLD` → `offline=true`
- Default threshold suggestion: 180s (tunable)

### Status → zone mapping
UI must map statuses to zones (for Pixel Office movement):

- `idle` → `rest`
- `writing` → `desk`
- `syncing` → `server`
- `error` → `bug`

Zones are rendered as slot groups (x,y lists). Each agent occupies a free slot.

### Message (bubble) rule
- One line only.
- If longer than N chars: truncate with ellipsis.
- Mobile-first: must not blow up layout.

## Versioning
- v0.1 locks the 4 statuses + required fields.
- Any extension MUST remain backward compatible for UI.
