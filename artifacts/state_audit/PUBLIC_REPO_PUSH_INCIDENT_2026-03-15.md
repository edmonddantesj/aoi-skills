# Public Repo Push Incident — 2026-03-15

## Summary
A workspace commit containing internal operating-policy changes was mistakenly pushed to the public repository `edmonddantesj/openclaw-telegram-topics-router`.

## What happened
- Workspace root remote was pointing to the public OSS repo.
- Internal SSOT / policy-style changes were pushed as commit `b4357bd`.
- User correctly flagged that the target repository is public and should never receive company internal information.

## Immediate containment
- Revert commit created: `1a8ac3a`
- Revert pushed to public remote immediately.

## Containment status
- Public rollback completed.
- Follow-up action: local no-leak policy SSOT created and topic-wide warning to be published.

## Lesson
Never treat the workspace root as safe for public push without checking repo root, remote URL, visibility, and staged change class first.
