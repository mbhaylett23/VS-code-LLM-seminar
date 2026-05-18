# VS Code LLM Seminar

This repository is a public starter pack for a seminar on using LLM agents inside VS Code.

## Purpose

Help participants move from one-off prompting to reusable project infrastructure:

- project instructions with `AGENTS.md`
- reusable skills in `skills/`
- evidence-driven debugging and review
- simple Markdown wiki memory

## Important Files

- `README.md` - participant-facing overview and copy-paste prompts.
- `skills/create-agents-md/SKILL.md` - creates workspace-specific `AGENTS.md`.
- `skills/setup-python-environment/SKILL.md` - chooses and verifies a Python setup.
- `skills/systematic-debugging/SKILL.md` - debugging loop.
- `skills/code-review-quality/SKILL.md` - review checklist.
- `skills/simple-wiki-memory/SKILL.md` - Markdown wiki memory workflow.
- `docs/SKILL_ARCHITECTURE.md` - public skill bundle architecture.
- `docs/PUBLIC_COPY_BOUNDARY.md` - explains that GitHub skills are detached copies, not live ProjectPulse files.
- `memory/wiki/index.md` - wiki page index.
- `memory/wiki/log.md` - memory activity log.

## Operating Rules

- Keep this repository public-safe.
- Treat all skills here as public copies. Do not assume edits here should be ported back to ProjectPulse.
- Do not add real private emails, student data, credentials, API keys, or unpublished sensitive material.
- Prefer concise Markdown over heavy tooling.
- If editing skills, keep `SKILL.md` self-contained unless a support file is clearly useful.
- Do not invent verification results. Run commands before claiming they passed.

## Verification

No build step is required. Before finishing edits:

```powershell
Get-ChildItem -Recurse -Filter SKILL.md
```

Check that every skill has YAML frontmatter with `name` and `description`.

## End Of Session

If meaningful changes were made, update `README.md` when the public instructions have changed.
