# TASK-20260304-ADP-PIXEL-MOVE-01

labels: adp, pixel-office, ui, ralph-loop, move, rebuild
priority: P0
status: TODO

## Goal
Implement "status → zone → (x,y)" movement for pixel agents.

## Depends on
- `context/adp/ADP_AGENT_STATE_SCHEMA_V0_1.md`

## Spec
- Zones: `desk | rest | server | bug`
- Status→zone mapping:
  - idle→rest
  - writing→desk
  - syncing→server
  - error→bug
- Each zone has multiple slots; agents occupy free slots.
- Movement uses CSS transition (or canvas tween) to visibly move between slots.

## Acceptance
- Changing an agent's status moves their sprite to the correct zone slot.
- Movement is smooth (transition) and does not overlap too badly.

## Notes
Originally implemented in PixelOfficeMap.tsx in the lost workspace; now tracked for rebuild.
