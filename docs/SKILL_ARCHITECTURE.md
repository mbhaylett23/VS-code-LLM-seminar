# Skill Architecture

This repository uses a simple skill-bundle layout that participants can inspect and adapt.

## Bundle Layout

Each skill is a directory under `skills/`:

```text
skills/
  <skill-name>/
    SKILL.md          # required: frontmatter + instructions
    scripts/          # optional: deterministic helper scripts
    references/       # optional: extra docs loaded only when needed
    assets/           # optional: templates or files used by the skill
```

The directory name should match the `name` field in `SKILL.md`.

## Required Frontmatter

Every `SKILL.md` needs YAML frontmatter:

```yaml
---
name: skill-name
description: Use when the user asks to do a specific recurring workflow.
---
```

YAML is a simple human-readable way to write structured settings as `key: value` pairs. In a skill file, the YAML frontmatter is the small metadata block between the two `---` lines at the top.

The agent reads this block before it reads the whole skill. That is why `name` and `description` matter:

- `name` is the skill's identifier.
- `description` tells the agent when the skill should be used.

Good descriptions are specific. They should say when the skill should be used.

## Fail Fast Dependency Rule

Every public skill must define what counts as a hard requirement before it
starts work. Silent failure is a skill bug.

- List required packages, command-line tools, services, accounts, environment
  variables, permissions, and source files.
- Add a dependency gate that proves required tools are installed and usable.
- If a required dependency is missing and can be safely installed, install it
  and rerun the gate.
- If it cannot be installed, stop and give the user the exact install command or
  manual action.
- Public skills must not assume conda. If Python packages are required, include
  a standard `venv`/`pip` route and keep conda as an optional route.
- Optional dependencies become required when the user's requested outcome
  depends on them. OCR is optional for a text-layer PDF, but required for a
  scanned PDF or explicit OCR request.
- Scripts should exit nonzero on missing required dependencies, unsupported
  inputs, failed external commands, failed verification gates, or incomplete
  required outputs.
- Skills should use explicit statuses such as `ok`, `ok_with_warnings`,
  `dependency_missing`, `needs_password`, `ocr_required`, or
  `verification_failed`.
- Test both happy paths and failure paths.

## What Belongs In A Skill

Put stable, reusable procedure into a skill:

- what to read first
- what questions to ask
- what commands or checks prove the work
- what failure modes to avoid
- what privacy or safety boundaries apply
- what the final answer should include

Do not turn a skill into a long manual. Keep `SKILL.md` concise. Move detailed examples into `references/` only if they are genuinely useful.

## Progressive Disclosure

Skills work best when they load context in layers:

1. **Metadata**: `name` and `description` tell the agent when to use the skill.
2. **SKILL.md**: the main procedure is read when the skill is relevant.
3. **Support files**: `scripts/`, `references/`, and `assets/` are read or run only when needed.

This keeps the agent focused and avoids filling the context window with irrelevant details.

## Public Repo Copy Boundary

The skills in this GitHub repository are public, copied starter versions.

They are not symlinks, submodules, or live mirrors of any private local skill library. Editing a skill here changes only this public repository.

Seminar participants do not need access to any private skill library.

## Updating Skills Safely

Use this rule:

```text
private source -> copy -> sanitize -> GitHub
```

Do not sync changes automatically in either direction.

If a public skill improves during the seminar, review it manually before deciding whether to port the idea back into a private local skill library.

If a private skill improves, copy it manually into this repo only after removing private paths, internal names, secrets, emails, student details, and machine-specific workflow assumptions.

## Good Starter Skills

This repo intentionally keeps the starter set small:

- `create-new-skill`
- `how-to-write-a-skill`
- `publish-skills-to-github`
- `create-agents-md`
- `setup-python-environment`
- `systematic-debugging`
- `code-review-quality`
- `dont-write-like-ai`
- `simple-wiki-memory`
- `search-outlook-email`
- `search-gmail-email`
- `extract-grant-call-pdf`

These are broad enough for participants to reuse without exposing private infrastructure.
