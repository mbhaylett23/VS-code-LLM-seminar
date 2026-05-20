---
name: how-to-write-a-skill
description: Compatibility pointer for users who ask how to write a skill. Use when a prompt says "how to write a skill"; follow create-new-skill instead so there is one public authoring workflow.
metadata:
  category: infrastructure
  tags: [skills, authoring, alias, redirect]
  created: 2026-05-20
  updated: 2026-05-20
---

# How To Write A Skill

## Status

This is a compatibility pointer, not a separate workflow.

The public skill-authoring procedure is:

```text
../create-new-skill/SKILL.md
```

That canonical procedure requires fail-fast dependency gates, explicit stop
statuses, tested failure paths, and public-safety checks for every new or
updated skill.

## Rule

Do not duplicate skill-authoring instructions here. If the public authoring
procedure needs to change, update `../create-new-skill/SKILL.md`.
