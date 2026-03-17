# Watcher — Setup & Triage Rules

## Purpose

`scripts/watcher.py` scans canonical support request paths for OPEN/WORKING requests
and reports them. Use manually or via cron to ensure no request is missed.

## Usage

```bash
# Scan one lane
python3 scripts/watcher.py --lane inbox-dev --root /path/to/context

# Scan all known lanes
python3 scripts/watcher.py --all --root /path/to/context

# Quiet mode (only output if OPEN requests exist — for cron)
python3 scripts/watcher.py --all --root /path/to/context --quiet
```

## Output

```
⚠️  1 OPEN request(s) found:

  🟢 [P2] 📥 OPEN  TASK-20260317-INBOXDEV-STITCH-MCP-POC-01
     Lane: inbox-dev | From: topic-60 | Date: 2026-03-17
     File: context/inbox-dev/support/requests/TASK-20260317-INBOXDEV-STITCH-MCP-POC-01.md
```

Exit code `0` = nothing to do. Exit code `1` = OPEN requests exist.

## Scan Cadence

| Mode | When |
|---|---|
| Manual | On-demand, when picking up work |
| Cron (every 30 min) | During active work hours |
| Cron (daily digest) | End of day summary across all lanes |

Example crontab (every 30 min, 9–18 KST):
```cron
*/30 9-18 * * 1-5 python3 /path/to/watcher.py --all --root /path/to/context --quiet
```

## Triage Rules (v0.2)

When watcher detects an OPEN request, executor applies these checks before starting:

### 1. Required fields check
All of these must be present:
- `request_id`, `state`, `requester`, `priority`
- Body: `Current state`, `Goal`, `Needed support`, `Constraints / human gate`, `Reference paths`

If missing → return `MISSING_FIELDS`, do not start.

### 2. Human gate scan
Does `Constraints / human gate` contain any of:
- submit / publish / deploy / production / policy change / org change / billing / auth / credential

If yes → flag as `NEEDS_HUMAN_REVIEW` for those items, proceed only on non-gated parts.

### 3. Scope check
Is the request within L1/L2 bounded support?
- ✅ Allowed: research memo / checklist / draft / implementation plan / review / structured notes / SSOT draft / PoC (isolated)
- ❌ Blocked: production deploy, live trading, org-wide policy change, external publish

### 4. Reference path check
Do the listed `Reference paths` exist locally or on canonical GitHub?
If not → note as `REFERENCE_MISSING` in result, proceed with available context.

### Triage verdict

| Verdict | Action |
|---|---|
| `AUTO_EXECUTABLE` | All checks pass → proceed |
| `NEEDS_HUMAN_REVIEW` | Human gate items found → partial proceed or hold |
| `MISSING_FIELDS` | Return to requester |
| `OUT_OF_SCOPE` | Block + explain |
| `REFERENCE_MISSING` | Proceed with note |

## Canonical Path Structure

```
context/<lane>/support/
  requests/    ← REQUEST files (state: OPEN / WORKING)
  results/     ← RESULT + FEEDBACK files
  closed/      ← CLOSE files
```

Watcher scans both `support/requests/` (v0.2) and `requests/` (legacy flat).

## Updating Request State

When executor picks up a request, update `state: WORKING` in the REQUEST file:

```yaml
---
request_id: TASK-...
state: WORKING   # ← change from OPEN
...
---
```

This signals to other watchers that the request is in progress.
