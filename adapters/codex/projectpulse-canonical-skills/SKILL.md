---
name: projectpulse-canonical-skills
description: Example adapter showing how Codex can point to a separate canonical skill library. Use only in Mike's private ProjectPulse environment; seminar participants should use the public skills in this repository instead.
metadata:
  category: infrastructure
  tags: [skills, adapter, codex, claude, gemini, canonical, cross-agent]
  created: 2026-05-04
  updated: 2026-05-04
---

# ProjectPulse Canonical Skills

This is an adapter example, not a seminar skill.

`G:/My Drive/PythonCode/ProjectPulse/pulse_memory/skills/` is the canonical skills repository for Claude, Codex, Gemini, and future agents.

That path only exists in Mike's private ProjectPulse setup. In this public seminar repo, use the copied skills under:

```text
skills/
```

For the public skill-bundle architecture, read:

```text
docs/SKILL_ARCHITECTURE.md
docs/PUBLIC_COPY_BOUNDARY.md
```

Agent-specific skill folders should contain only discovery adapters that point here. Do not mirror full `SKILL.md` bodies, scripts, references, or assets into agent-specific folders.

## Workflow

1. Use `MEMORY.md` as the skill index.
2. If the right skill is not obvious, search `SKILL.md` descriptions under the canonical root.
3. Read the selected canonical `SKILL.md`.
4. Follow that skill exactly.
5. Resolve `scripts/`, `references/`, and `assets/` relative to the selected canonical skill folder.
6. If instructions need to change, edit the canonical ProjectPulse bundle first, then update adapters only if their pointer or trigger description is stale.

Useful search command:

```powershell
rg -n "description:|Use when|<keyword>" "G:\My Drive\PythonCode\ProjectPulse\pulse_memory\skills" -g "SKILL.md"
```

Architecture docs:

- `G:/My Drive/PythonCode/ProjectPulse/pulse_memory/skills/MEMORY.md`
- `G:/My Drive/PythonCode/ProjectPulse/pulse_memory/skills/SKILL_ARCHITECTURE.md`

Public seminar equivalent:

- `docs/SKILL_ARCHITECTURE.md`
- `docs/PUBLIC_COPY_BOUNDARY.md`
