# Public Copy Boundary

This repository is a public teaching artifact. It is not the canonical ProjectPulse skills repository.

## What Is Safe To Edit Here

Safe:

- `README.md`
- `AGENTS.md`
- `skills/*/SKILL.md`
- `skills/*/references/*`
- `skills/*/assets/*`
- `memory/wiki/*`
- `docs/*`

Edits here affect only:

```text
G:/My Drive/PythonCode/VS-code-LLM-seminar/
https://github.com/mbhaylett23/VS-code-LLM-seminar
```

They do not modify:

```text
G:/My Drive/PythonCode/ProjectPulse/pulse_memory/skills/
```

## What Not To Do

- Do not replace this repo with symlinks to ProjectPulse.
- Do not create automatic sync from GitHub back to ProjectPulse.
- Do not tell participants to use Mike's private `G:/.../ProjectPulse` paths.
- Do not publish internal-only skills without manual sanitization.

## Why This Boundary Exists

Mike's ProjectPulse skills are carefully curated for his machines, email tools, research corpus, Memory Hub, and private workflows.

The GitHub repo is for a general audience. It should be simpler, safer, and easier to understand.

The two can share ideas, but they should not share live files.

## Current Grant Skills

The public grant-related skills in this repo are detached teaching versions:

- `skills/grant-ground-truth-ledger/`
- `skills/bibliography-ground-truth/`
- `skills/grant-definite-language/`

They should not import, symlink, auto-sync, or depend on Mike's private ProjectPulse grant-writing skills.

## Current Memory Architecture Document

`docs/MEMORY_HUB_ARCHITECTURE.md` is also a detached public teaching document. It describes a generic event-sourced memory architecture and must not contain private hostnames, local drive paths, API keys, passwords, endpoint URLs, or deployment details from any private installation.
