# BLACKCAT REMOTE DEPLOY HANDOFF V0.1

## Objective
Deploy **흑묘/strategist** on a **different server** from 청묘 so `@Mercedes_cyrano_3_bot` speaks from its own host in topic 6062.

## Already done locally
- strategist workspace files created and allowlisted
- cat-strategic router/runtime files created
- distributed migration plan documented
- temporary local heukmyo Telegram attach tested, then removed to avoid DM/token conflict

## What must happen on remote host
1. OpenClaw gateway must be healthy
2. `@Mercedes_cyrano_3_bot` token must be configured there only
3. strategist workspace files from migration bundle must be copied there
4. Binding must route `telegram:-1003732040608:topic:6062` to strategist on that host
5. No simultaneous polling of the same token on this host

## Acceptance test
1. DM to `@Mercedes_cyrano_3_bot` still works
2. In topic 6062 send: `흑묘, 한 줄로 살아있다고만 답해봐.`
3. Response must come from remote-host blackcat bot
4. Then test: `둘이 논의해...` and confirm 청묘/흑묘 alternating behavior

## Remaining blocker
Remote host access / deployment path is not yet available in this session.
This is the only hard blocker left for full cutover.
