# VS Code LLM Seminar

Starter materials for a hands-on seminar on using LLM agents inside VS Code.

The core idea:

```text
Prompting is temporary. Project instructions, skills, tools, memory, and verification are infrastructure.
```

## What This Repo Contains

- `skills/` - reusable starter skills participants can inspect, copy, or adapt.
- `memory/` - a simple Markdown wiki memory starter inspired by Andrej Karpathy's LLM Wiki pattern.
- `docs/` - skill architecture notes and the boundary between this public repo and private local skill libraries.

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
7. Use `skills/create-new-skill/SKILL.md` when turning a repeated workflow into a reusable skill.
8. Use skills for practical work: setup, debugging, review, documents, email, grants, and memory.

## Starter Skills

| Skill | Path | Use |
|---|---|---|
| `create-new-skill` | `skills/create-new-skill/SKILL.md` | Create or update a reusable skill with fail-fast dependency gates and tested stop conditions. |
| `how-to-write-a-skill` | `skills/how-to-write-a-skill/SKILL.md` | Compatibility pointer to `create-new-skill` for older prompts or users asking how to write a skill. |
| `publish-skills-to-github` | `skills/publish-skills-to-github/SKILL.md` | Publish selected sanitized skill bundles to GitHub without overwriting private/local skills. |
| `create-agents-md` | `skills/create-agents-md/SKILL.md` | Create a workspace-specific `AGENTS.md` from local inspection plus a short interview. |
| `setup-python-environment` | `skills/setup-python-environment/SKILL.md` | Choose the simplest Python/VS Code setup that works for the user and project. |
| `systematic-debugging` | `skills/systematic-debugging/SKILL.md` | Reproduce, inspect, patch minimally, and verify a bug or failing test. |
| `code-review-quality` | `skills/code-review-quality/SKILL.md` | Review code with findings first, line evidence, and missing-test risks. |
| `dont-write-like-ai` | `skills/dont-write-like-ai/SKILL.md` | Revise serious prose so it is specific, direct, and not generic AI output. |
| `simple-wiki-memory` | `skills/simple-wiki-memory/SKILL.md` | Maintain a durable Markdown wiki memory from raw sources, index, and log files. |
| `search-outlook-email` | `skills/search-outlook-email/SKILL.md` | Search Classic Outlook on Windows through COM after verifying `OUTLOOK.EXE` is running. |
| `search-gmail-email` | `skills/search-gmail-email/SKILL.md` | Search Gmail through IMAP using environment variables and app-password/OAuth-compatible setup. |
| `extract-grant-call-pdf` | `skills/extract-grant-call-pdf/SKILL.md` | Extract source-backed summaries and key details from grant-call PDFs with mandatory OCR/dependency preflight. |
| `grant-ground-truth-ledger` | `skills/grant-ground-truth-ledger/SKILL.md` | Create separated ledgers for bibliography, claims, methods, people, budget, decisions, and open questions. |
| `bibliography-ground-truth` | `skills/bibliography-ground-truth/SKILL.md` | Verify bibliography metadata and audit numeric or stable-reference citations against `ground_truth/bibliography.yml`. |
| `grant-definite-language` | `skills/grant-definite-language/SKILL.md` | Remove internal uncertainty from external grant prose and move unresolved items to `open_questions.yml`. |

## Skill Architecture

Read [docs/SKILL_ARCHITECTURE.md](docs/SKILL_ARCHITECTURE.md) for the bundle structure and skill-writing rules.

Important boundary: this public repository contains copied starter skills. It is not a live mirror of any private local skill library. Editing a GitHub skill here will not change private local skills. See [docs/PUBLIC_COPY_BOUNDARY.md](docs/PUBLIC_COPY_BOUNDARY.md).

The public grant skills are teaching versions. They are deliberately detached from private grant-writing and reference-ground-truth workflows.

For the advanced memory architecture, read [docs/MEMORY_HUB_ARCHITECTURE.md](docs/MEMORY_HUB_ARCHITECTURE.md). It is a sanitized public blueprint for implementing event-sourced LLM memory across multiple machines.

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

### Create Or Improve A Skill

```text
Use skills/create-new-skill/SKILL.md.

I want to turn this repeated workflow into a reusable skill. First check whether an existing skill already covers it. Then define the required dependencies, dependency gate, stop conditions, tests, and public-safety checks before drafting the skill.
```

### Publish A Skill To GitHub

```text
Use skills/publish-skills-to-github/SKILL.md.

I want to publish this skill publicly. Treat the GitHub version as a sanitized copy, not the private source of truth. Do not copy GitHub content back over my local skill unless I explicitly ask. Make sure the public skill contains no private information and does not assume users have conda; include a standard Python route and conda as an option when packages are needed.
```

### Make Writing Sound Less Like AI

```text
Use skills/dont-write-like-ai/SKILL.md.

Revise the text below so it sounds like serious human writing for the intended audience. Remove generic AI phrasing, inflated claims, template structure, and unsupported vague statements. Keep the concrete facts and tell me what changed.
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

### Extract A Grant-Call PDF

```text
Use skills/extract-grant-call-pdf/SKILL.md.

Run the dependency gate first. If OCR/Tesseract or required Python packages are missing, stop and tell me exactly what to install. If the gate passes, extract the PDF and produce a source-backed summary with deadlines, eligibility, budget, required documents, evaluation criteria, and watch-outs.
```

### Set Up Grant Ground Truth

```text
Use skills/grant-ground-truth-ledger/SKILL.md.

Create a ground_truth folder for this project using the public templates. Separate bibliography, claims, methods, people, budget, decisions, and open questions. Do not turn every ground-truth record into a numbered bibliography item.
```

### Audit Bibliography Links

```text
Use skills/bibliography-ground-truth/SKILL.md.

Check that every numeric citation in my proposal text has a matching bibliography record, and that every bibliography record has full title, full author list, year, venue, DOI/PMID/URL/local source, verification status, supported claims, and cited locations.
```

### Remove Internal Grant Notes

```text
Use skills/grant-definite-language/SKILL.md.

Scan this proposal draft for TODO, TBC, "need to check", "maybe", "[CITE]", and other internal uncertainty. Rewrite only verified content in definite funder-facing language, and move unresolved items to ground_truth/open_questions.yml.
```

## Memory Wiki

The memory example follows the pattern in Andrej Karpathy's `llm-wiki.md`: raw sources stay immutable, and the LLM maintains a structured set of interlinked Markdown pages that accumulate over time.

- `memory/raw/` - put source notes, articles, transcripts, or copied references here.
- `memory/wiki/index.md` - content-oriented map of wiki pages.
- `memory/wiki/log.md` - chronological record of ingests, queries, and maintenance.
- `memory/wiki/*.md` - topic, entity, source, and synthesis pages maintained by the agent.

Source idea: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## Safety Rules

- Do not paste private email, student data, credentials, API keys, or unpublished research into a public demo.
- Do not let an agent claim it has run a command unless it actually ran it.
- If a required tool, library, account, service, or file is unavailable, the agent should stop with a clear status and install/recovery instruction rather than silently bypassing the step.
- Review generated `AGENTS.md` and wiki pages before trusting them.
