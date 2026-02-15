# Security

## AOI Guard (Repo Upload Safety)

This repository is protected by **AOI Guard**:
- Commits are blocked by default unless a `.aoi-allowlist` exists.
- Only paths in `.aoi-allowlist` are allowed without explicitly updating the allowlist.
- CI enforces the same allowlist + a lightweight secret scan.

Goal: prevent accidental inclusion of unrelated project data, keys, or private materials.
