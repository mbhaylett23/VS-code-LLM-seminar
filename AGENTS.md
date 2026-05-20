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
- `skills/create-new-skill/SKILL.md` - public skill-authoring workflow with fail-fast dependency gates.
- `skills/how-to-write-a-skill/SKILL.md` - compatibility pointer to `create-new-skill`.
- `skills/create-agents-md/SKILL.md` - creates workspace-specific `AGENTS.md`.
- `skills/setup-python-environment/SKILL.md` - chooses and verifies a Python setup.
- `skills/systematic-debugging/SKILL.md` - debugging loop.
- `skills/code-review-quality/SKILL.md` - review checklist.
- `skills/dont-write-like-ai/SKILL.md` - removes generic AI style from serious prose.
- `skills/simple-wiki-memory/SKILL.md` - Markdown wiki memory workflow.
- `skills/search-outlook-email/SKILL.md` - public-safe Classic Outlook COM search workflow.
- `skills/search-gmail-email/SKILL.md` - public-safe Gmail IMAP search workflow.
- `skills/extract-grant-call-pdf/SKILL.md` - public-safe grant-call PDF extraction with mandatory OCR/dependency preflight.
- `skills/grant-ground-truth-ledger/SKILL.md` - public-safe separated grant fact ledgers.
- `skills/bibliography-ground-truth/SKILL.md` - public-safe bibliography/citation audit workflow.
- `skills/grant-definite-language/SKILL.md` - public-safe external grant language cleanup workflow.
- `docs/SKILL_ARCHITECTURE.md` - public skill bundle architecture.
- `docs/PUBLIC_COPY_BOUNDARY.md` - explains that GitHub skills are detached public copies, not live private files.
- `docs/MEMORY_HUB_ARCHITECTURE.md` - sanitized public blueprint for multi-machine LLM memory.
- `memory/wiki/index.md` - wiki page index.
- `memory/wiki/log.md` - memory activity log.

## Operating Rules

- Keep this repository public-safe.
- Treat all skills here as public copies. Do not assume edits here should be ported back to any private local skill library.
- Do not replace public skills with symlinks, adapters, or live references to private skills.
- Do not add private hostnames, local drive paths, API tokens, passwords, endpoint URLs, or machine-specific names to public memory architecture docs.
- Do not add real private emails, student data, credentials, API keys, or unpublished sensitive material.
- Prefer concise Markdown over heavy tooling.
- If editing skills, keep `SKILL.md` self-contained unless a support file is clearly useful.
- Any skill with dependencies must fail fast: check required tools before work starts, stop on missing requirements, and give exact install/recovery instructions.
- Public skills must not assume conda. Include standard Python `venv`/`pip` instructions when packages are needed, with conda only as an optional route.
- GitHub skill copies must never overwrite private/local skills unless the user explicitly asks for that reverse import.
- Do not invent verification results. Run commands before claiming they passed.

## Verification

No build step is required. Before finishing edits:

```powershell
Get-ChildItem -Recurse -Filter SKILL.md
```

Check that every skill has YAML frontmatter with `name` and `description`.

## End Of Session

If meaningful changes were made, update `README.md` when the public instructions have changed.
