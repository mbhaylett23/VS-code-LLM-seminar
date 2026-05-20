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

## Fail-Fast Gate

Before following this skill, identify the required inputs, tools, services,
accounts, environment variables, and permissions. Run the dependency or preflight
checks named in this skill before doing substantive work.

If a required item is missing or a check fails, stop with an explicit status such
as `dependency_missing`, `input_missing`, `permission_blocked`, or
`verification_failed`. Do not continue in best-effort mode, do not silently skip
the unavailable step, and do not claim success until the required verification
has passed.

Public skills must not assume the user has conda. If Python packages are needed,
provide a standard `venv`/`pip` route and keep conda as an optional route. If a
non-Python tool is required, provide a clear install instruction or ask the user
to install it before continuing.

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
