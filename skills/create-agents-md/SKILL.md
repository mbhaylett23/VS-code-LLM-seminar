---
name: create-agents-md
description: Create or update workspace-level AGENTS.md instructions from a user interview and local project inspection. Use when the user asks to create AGENTS.md, improve agent instructions, make a project brief for AI assistants, onboard an LLM to a folder, or turn project context into reusable workspace guardrails.
---

# Create AGENTS.md

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

## Purpose

Create a concise, useful `AGENTS.md` that tells AI agents what the workspace is, who the work is for, what files matter, how to handle local Python/package tooling, what safety boundaries apply, and what should be updated at the end of a session.

## Requirements

- Read the existing workspace files before drafting when they are available.
- Do not overwrite an existing `AGENTS.md` without reading it first.
- Use verified local facts when possible.
- Ask the user for missing high-impact context instead of inventing it.
- Keep the final `AGENTS.md` practical. It is an operating file, not a brochure.

## Workflow

1. Inspect the workspace.
   - Check for existing `AGENTS.md`, `CLAUDE.md`, `README.md`, `projectpulse.md`, docs, config files, tests, and obvious entry points.
   - List important files with `rg --files` or the closest available file search.

2. Load the question bank when needed.
   - Use `references/question-bank.md` for the full interview.
   - Ask only the 8 core interview questions unless the user asks for a deeper project audit.
   - Always clarify the user's coding comfort, Python/package setup, and whether the agent may manage packages or should only propose commands.

3. Choose the workspace type.
   - Software project
   - Research or data project
   - Teaching or course workspace
   - Writing, proposal, or document workspace
   - Personal/admin workspace
   - Demo or public starter repo
   - Mixed workspace

4. Draft or update `AGENTS.md`.
   - Start from `assets/AGENTS.template.md` when creating from scratch.
   - Keep sections with real content.
   - Remove irrelevant sections rather than leaving many placeholders.
   - Mark unknowns as `Unknown` or `Ask user`, not as guessed facts.

5. Include operational details.
   - Project purpose.
   - Output audience.
   - User setup level: coding comfort, Python availability, Conda/Anaconda/Miniforge/uv/notebook status, and package-install approval rules.
   - Files that are source of truth.
   - Files, folders, data, or actions the agent must not expose, edit, delete, overwrite, or send.
   - Session-end update rules.
   - If the user chooses `wiki` as the session-end update target, add a simple Markdown wiki memory section.

6. Validate the result.
   - Re-read the file.
   - Check that paths mentioned exist or are intentionally placeholders.
   - Confirm that instructions do not expose secrets or private data.
   - Confirm the file is short enough to be read at the start of future sessions.

## Output Rules

- Put durable rules in `AGENTS.md`, not in chat only.
- Prefer concrete commands and file paths over general advice.
- Do not include private tokens, passwords, API keys, or personal data.
- Do not copy large project history into `AGENTS.md`; summarize current state and link files.
- If the project already has a memory file, put detailed history there and keep `AGENTS.md` focused on operating rules.
- If adding wiki memory, keep it simple: `memory/wiki/index.md`, `memory/wiki/log.md`, and `memory/wiki/topics/` are enough for a first version.

## Good Final Shape

Use this order unless the project clearly needs another:

1. Workspace Identity
2. Audience
3. User Setup And Tooling
4. Important Files
5. Safety, Privacy, And Do-Not-Edit Rules
6. End Of Session

## Optional Simple Wiki Memory

Use this only if the user asks for wiki-style memory or chooses `wiki` as the session-end update target.

The pattern follows Andrej Karpathy's LLM Wiki idea: raw sources stay immutable, the LLM maintains a structured Markdown wiki, and `AGENTS.md` defines the schema/workflow.

Reference: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Suggested starter structure:

```text
memory/
  wiki/
    index.md
    log.md
    topics/
```

Rules to include in `AGENTS.md`:

- Read `memory/wiki/index.md` before answering memory-dependent questions.
- Store durable knowledge in `memory/wiki/topics/*.md`.
- Append chronological updates to `memory/wiki/log.md`.
- Prefer updating an existing page over creating near-duplicates.
- Do not store secrets, private emails, student records, participant data, API keys, or confidential documents in the wiki.
- Add source lines for factual claims when the source is a file, URL, paper, or meeting note.

Do not create database, vector, or sync infrastructure for beginners unless the user explicitly asks. The first useful version is plain Markdown.
