# PUBLIC REPO INTERNAL INFO NO-LEAK POLICY V0.1

## Non-negotiable rule
Public repositories must never receive Aoineco internal operating information, private SSOT, internal routing rules, internal topic policy, private backup details, private workspace state, or confidential company context.

## Effective rule
Before any external git push, verify all of the following:
1. repo root
2. remote URL
3. branch
4. whether the target repo is public or private
5. whether every staged change is public-safe

If any doubt remains, do **not** push.

## Public repo forbidden content
Never push these to a public repo:
- internal SSOT / operating policy
- topic-state / topic routing / summon policy
- private workspace structure
- backup paths / restore paths / recovery notes
- internal team routing / role policies
- company-internal strategy / ops / handoff context
- AOI PRO internal-only policy or company-specific private configuration
- any secret / token / credential / local path disclosure

## Required handling when public/private is mixed
If a working tree contains both public-safe and internal-only changes:
- do not push from the mixed root blindly
- split changes by correct repo/root first
- keep internal changes local or move them to a private repo
- push only the public-safe subset

## Incident response rule
If internal information is pushed to a public repo by mistake:
1. revert public commit immediately
2. push the revert immediately
3. record the incident in local audit notes
4. publish an internal warning so all topic owners avoid repeating it
5. tighten SSOT / workflow so the same mistake is less likely

## Operating interpretation
- Public OSS repo = code/artifacts/docs that are explicitly safe for public distribution
- Workspace/internal repo = company operating memory and private execution layer
- Never assume the current git remote is safe just because the local files look familiar

## One-line rule
When in doubt: **public push stops first, verification comes before convenience.**
