# AGENTS.md Question Bank

Use this question bank to create workspace-specific `AGENTS.md` files. Ask only what is needed. A good `AGENTS.md` is specific, operational, and short enough that an agent will actually use it.

## Core Interview: 8 Questions

Use these before writing `AGENTS.md`. Keep the interview short; the goal is a practical workspace instruction file, not a full project audit.

1. What is this project/workspace for?
2. Who are the outputs for: you, students, collaborators, customers, reviewers, participants, or the public?
3. How much coding experience do you have for this workspace: none, beginner, intermediate, or advanced?
4. What Python or package setup do you use, if any: none, system Python, Anaconda/Miniconda/Miniforge/Conda, `uv`, notebooks only, or unknown?
5. Should the agent install/manage packages for you, propose commands only, or always ask before touching environments?
6. Which files or folders are the source of truth?
7. What should the agent never edit, expose, delete, overwrite, or send?
8. What should be updated at the end of a session: `projectpulse.md`, a wiki, a changelog, a lab notebook, or nothing?

## Section Map

Use answers to build sections like this:

- Project purpose, audience -> `Workspace Identity`
- Coding level, Python setup, package autonomy -> `User Setup And Tooling`
- Source-of-truth files -> `Important Files`
- Safety/privacy boundaries -> `Safety And Privacy`
- Session-end update rules -> `End Of Session`
- If session-end update is `wiki` -> optional `Simple Wiki Memory`

## Minimum Viable AGENTS.md

If time is short, create only these sections:

```markdown
# <Workspace Name>

## Purpose
<What this folder is for.>

## Audience
<Who the outputs are for.>

## User Setup And Tooling
- Coding comfort: <none | beginner | intermediate | advanced>
- Python/package setup: <none | system Python | Conda/Anaconda/Miniconda/Miniforge | uv | notebooks only | unknown>
- Package policy: <agent may install | propose commands only | ask before touching environments>

## Important Files
- `<path>` - <why it matters>

## Safety
- Do not expose, edit, delete, overwrite, or send: <boundaries>

## End Of Session
- Update `<status/memory/log file or "nothing">`.

## Simple Wiki Memory
Use only if the workspace uses wiki memory:
- `memory/wiki/index.md` lists pages.
- `memory/wiki/log.md` records chronological updates.
- `memory/wiki/topics/*.md` stores durable knowledge.
```
