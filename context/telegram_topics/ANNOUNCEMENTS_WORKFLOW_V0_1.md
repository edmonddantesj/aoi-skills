# Announcements Workflow (Telegram) — SSOT (V0.1)

## Scope
Canonical rules for **the Telegram forum topic used to publish announcements**.

## Channel / Topic
- **Topic slug:** `announcements`
- **Forum topic_id (message_thread_id):** `32`
- **Role:** This topic **is the publishing surface** (not just a drafting room).

## Bot / Workspace Meaning
- `@Mercedes_cyrano1_bot` is not a separate third-party bot.
- It refers to the **Aoineco agent workspace**: **청묘 + squad agents** operating together.

## “Team members” default interpretation
When the user says “팀원(들)” **without explicitly stating they mean humans**, interpret it as:
- the **agent squad roster (12 agents)**.

If the user explicitly says “사람” or names a human, then interpret it as humans.

## Input → Output contract
### Acceptable input (from user)
Any of the following is sufficient:
- One-liner: `공지: ...`
- Draft paragraphs
- Links + bullet points

Optional fields if provided:
- `대상:` who should read/act
- `기한:` deadline
- `링크:` evidence/resources

### Default output format (assistant posts in topic 32)
1) **Title (1 line)**
2) **Key points (3 lines)**
3) **CTA (1 line)**
4) **Links / evidence**

## Decision record
- 2026-03-04: Instead of discovering a separate announcements topic id, we **confirmed topic_id=32 as the announcements work+publish thread**.
- 2026-03-06: Confirmed: publication target is **1.A = this topic (32)**, and “team members” implies **agents by default**.
