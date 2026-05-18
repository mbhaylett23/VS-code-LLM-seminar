---
name: projectpulse-canonical-skills
description: Locate and use the shared ProjectPulse canonical skills repository from any LLM agent. Use when an agent needs a skill-backed workflow, shared skill lookup, Outlook email/calendar action, PDF processing, ground-truth checking, grant writing, write-as-Mike drafting, paper ingestion, document conversion, package installation, memory-hub work, or skill creation/update.
metadata:
  category: infrastructure
  tags: [skills, adapter, codex, claude, gemini, canonical, cross-agent]
  created: 2026-05-04
  updated: 2026-05-04
---

# ProjectPulse Canonical Skills

`G:/My Drive/PythonCode/ProjectPulse/pulse_memory/skills/` is the canonical skills repository for Claude, Codex, Gemini, and future agents.

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

