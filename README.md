# VS Code LLM Seminar

Starter materials for a hands-on seminar on using LLM agents inside VS Code.

The core idea:

```text
Prompting is temporary. Project instructions, skills, tools, memory, and verification are infrastructure.
```

## What This Repo Contains

- `skills/` - reusable starter skills participants can inspect, copy, or adapt.
- `adapters/codex/` - an example Codex adapter pattern from ProjectPulse.
- `memory/` - a simple Markdown wiki memory starter inspired by Andrej Karpathy's LLM Wiki pattern.
- `docs/` - skill architecture notes and the boundary between this public repo and Mike's private ProjectPulse skills.

## Recommended Seminar Flow

1. Install VS Code.
2. Install one AI extension, not all of them:
   - Codex / ChatGPT: `openai.chatgpt`
   - Claude Code: `anthropic.claude-code`
   - GitHub Copilot if access is already active
3. Open this repository as a folder in VS Code.
4. Ask the agent to read `README.md` and `AGENTS.md` without editing.
5. Open one real project folder you care about.
6. Use `skills/create-agents-md/SKILL.md` to create that folder's first `AGENTS.md`.
7. Use skills for practical work: setup, debugging, review, and memory.

## Starter Skills

| Skill | Path | Use |
|---|---|---|
| `create-agents-md` | `skills/create-agents-md/SKILL.md` | Create a workspace-specific `AGENTS.md` from local inspection plus a short interview. |
| `setup-python-environment` | `skills/setup-python-environment/SKILL.md` | Choose the simplest Python/VS Code setup that works for the user and project. |
| `systematic-debugging` | `skills/systematic-debugging/SKILL.md` | Reproduce, inspect, patch minimally, and verify a bug or failing test. |
| `code-review-quality` | `skills/code-review-quality/SKILL.md` | Review code with findings first, line evidence, and missing-test risks. |
| `simple-wiki-memory` | `skills/simple-wiki-memory/SKILL.md` | Maintain a durable Markdown wiki memory from raw sources, index, and log files. |
| `search-outlook-email` | `skills/search-outlook-email/SKILL.md` | Search Classic Outlook on Windows through COM after verifying `OUTLOOK.EXE` is running. |
| `search-gmail-email` | `skills/search-gmail-email/SKILL.md` | Search Gmail through IMAP using environment variables and app-password/OAuth-compatible setup. |

## Skill Architecture

Read [docs/SKILL_ARCHITECTURE.md](docs/SKILL_ARCHITECTURE.md) for the bundle structure and skill-writing rules.

Important boundary: this public repository contains copied starter skills. It is not a live mirror of Mike's private ProjectPulse skills. Editing a GitHub skill here will not change the local ProjectPulse skill library. See [docs/PUBLIC_COPY_BOUNDARY.md](docs/PUBLIC_COPY_BOUNDARY.md).

## Copy-Paste Prompts

### Verify Workspace Access

```text
Read README.md and AGENTS.md. Do not edit files yet.

Tell me:
- what this repository is for
- which folders matter
- which skills are available
- what privacy or safety rules are present

Only use facts from files you actually read. If you cannot read a file, say so.
```

### Create AGENTS.md For Your Own Project

Open your own project folder in VS Code, then paste:

```text
Use skills/create-agents-md/SKILL.md if available.

I want to create an AGENTS.md file for this workspace so future AI sessions understand how to work here.

First inspect the current folder. Read any existing AGENTS.md, README.md, docs, config files, notebooks, scripts, tests, and obvious entry points.

Then ask me a short set of questions before drafting. Focus on:
- what this project is for
- who the outputs are for
- which files are sources of truth
- which commands or checks verify work
- what must never be exposed, deleted, overwritten, or sent externally
- what should be updated at the end of a session

After I answer, create a practical AGENTS.md for this workspace.
Do not invent facts. Distinguish facts found in files from answers I gave you.
```

### Start A Markdown Wiki Memory

```text
Use skills/simple-wiki-memory/SKILL.md.

Initialize or update the memory wiki in this repository. Read memory/wiki/index.md and memory/wiki/log.md first. Then ask me what source or note I want to ingest.
```

### Search Email Safely

Outlook requires Classic Outlook for Windows:

```text
Use skills/search-outlook-email/SKILL.md.

First verify Classic Outlook is running as OUTLOOK.EXE. Then run a metadata-only search for "keyword" over the last 30 days. Do not print message bodies unless I explicitly approve.
```

Gmail requires IMAP/OAuth/app-password setup:

```text
Use skills/search-gmail-email/SKILL.md.

First check that the required Gmail environment variables are set. Then run a metadata-only search for "keyword" over the last 30 days. Do not print message bodies unless I explicitly approve.
```

## Memory Wiki

The memory example follows the pattern in Andrej Karpathy's `llm-wiki.md`: raw sources stay immutable, and the LLM maintains a structured set of interlinked Markdown pages that accumulate over time.

- `memory/raw/` - put source notes, articles, transcripts, or copied references here.
- `memory/wiki/index.md` - content-oriented map of wiki pages.
- `memory/wiki/log.md` - chronological record of ingests, queries, and maintenance.
- `memory/wiki/*.md` - topic, entity, source, and synthesis pages maintained by the agent.

Source idea: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## Codex Adapter

`adapters/codex/projectpulse-canonical-skills/SKILL.md` is included as an example of a Codex adapter that points to a separate canonical skill library.

It is mainly useful to Mike's local ProjectPulse setup. Seminar participants should usually use the skills in this repository directly rather than that adapter.

## Safety Rules

- Do not paste private email, student data, credentials, API keys, or unpublished research into a public demo.
- Do not let an agent claim it has run a command unless it actually ran it.
- If a tool, library, or file is unavailable, the agent should say so rather than silently bypassing the step.
- Review generated `AGENTS.md` and wiki pages before trusting them.
