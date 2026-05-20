# Public Copy Boundary

This repository is a public teaching artifact. It is not a live mirror of any private local skills repository.

## What Is Safe To Edit Here

Safe:

- `README.md`
- `AGENTS.md`
- `skills/*/SKILL.md`
- `skills/*/references/*`
- `skills/*/assets/*`
- `memory/wiki/*`
- `docs/*`

Edits here affect only this local checkout and
`https://github.com/mbhaylett23/VS-code-LLM-seminar`.

They do not modify private local skills.

## What Not To Do

- Do not replace this repo with symlinks to a private skill library.
- Do not create automatic sync from GitHub back to a private skill library.
- Do not tell participants to use private local paths.
- Do not publish internal-only skills without manual sanitization.

## Why This Boundary Exists

Private skills are often curated for specific machines, email tools, research corpora, memory systems, and private workflows.

The GitHub repo is for a general audience. It should be simpler, safer, and easier to understand.

The two can share ideas, but they should not share live files.

## Current Grant Skills

The public grant-related skills in this repo are detached teaching versions:

- `skills/grant-ground-truth-ledger/`
- `skills/extract-grant-call-pdf/`
- `skills/bibliography-ground-truth/`
- `skills/grant-definite-language/`

They should not import, symlink, auto-sync, or depend on private grant-writing skills.

## Current Skill-Authoring Skills

The public skill-authoring skills are detached teaching versions:

- `skills/create-new-skill/`
- `skills/how-to-write-a-skill/`
- `skills/publish-skills-to-github/`

They should not expose private paths or private memory-system implementation
details. They should teach the general pattern: reusable instructions,
dependency gates, explicit stop conditions, tested failure paths, public safety
checks, and the rule that GitHub copies never overwrite private/local skills
unless the user explicitly asks for that reverse import.

## Current Memory Architecture Document

`docs/MEMORY_HUB_ARCHITECTURE.md` is also a detached public teaching document. It describes a generic event-sourced memory architecture and must not contain private hostnames, local drive paths, API keys, passwords, endpoint URLs, or deployment details from any private installation.
