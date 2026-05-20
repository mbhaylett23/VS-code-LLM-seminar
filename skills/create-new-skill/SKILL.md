---
name: create-new-skill
description: Design, write, test, and publish a reusable skill bundle with clear triggers, fail-fast dependency gates, explicit stop conditions, and public-safe instructions. Use when creating a new skill, updating an existing skill, or teaching participants how skills differ from one-off prompts.
metadata:
  category: infrastructure
  tags: [skills, authoring, workflow, agents, vscode, fail-fast]
  created: 2026-05-20
  updated: 2026-05-20
---

# Create New Skill

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

## Why This Skill Exists

Skills turn a recurring workflow into durable instructions, scripts, and checks
that an agent can reuse inside VS Code. The risk is writing a nice-looking skill
that silently skips missing tools, unsupported files, or failed verification.

## When To Use

- Creating a reusable skill for a repeated workflow.
- Updating an existing skill after discovering a better procedure.
- Teaching participants how skills differ from chat prompts, project
  instructions, hooks, agents, plugins, APIs, and MCP tools.

## Do Not Create A Skill If

- The task is one-shot and unlikely to recur.
- A short answer in chat would fully solve it.
- The information belongs in `AGENTS.md`, a README, or project docs instead.
- An existing skill already covers the workflow; update that skill instead.

## Steps

### 1. Check For Existing Coverage

Search the current skill folder before creating a new one:

```powershell
rg -n "<keyword>" "skills" -g "SKILL.md"
```

If a matching skill exists, update it instead of creating a duplicate.

### 2. Define Failure Semantics First

Every skill must fail fast. Silent failure is a skill bug.

Before writing the skill, list:

- Required dependencies: packages, CLIs, services, accounts, environment
  variables, OS features, permissions, and source files.
- Optional dependencies: only optional when the requested outcome can still be
  completed correctly without them.
- Verification gates: commands or checks that prove required dependencies work.
- Stop conditions: statuses where the agent must stop instead of producing a
  degraded answer.
- Recovery path: exact install command, permission request, or user-facing
  blocker message.

Rules:

- A required dependency must be checked before substantive work starts.
- If the agent can safely install a missing dependency, it installs it and
  reruns the dependency gate.
- If installation is not possible, the agent stops and gives the exact install
  command or manual step.
- Optional tools become required when the user's request depends on them. OCR is
  optional for a text-layer PDF, but required for a scanned PDF or explicit OCR
  request.
- Scripts exit nonzero on missing required dependencies, unsupported inputs,
  failed external commands, failed verification gates, or incomplete required
  outputs.
- Skills report explicit statuses such as `ok`, `ok_with_warnings`,
  `dependency_missing`, `needs_password`, `ocr_required`, or
  `verification_failed`.

### 3. Create The Bundle

Use this layout:

```text
skills/<skill-name>/
  SKILL.md          # required
  scripts/          # optional deterministic helper scripts
  references/       # optional deeper docs
  assets/           # optional templates or test inputs
```

Name rules:

- Lowercase, hyphen-separated.
- Specific: `extract-grant-call-pdf`, not `pdf-helper`.
- Directory name matches frontmatter `name`.

### 4. Write `SKILL.md`

Use this skeleton:

```markdown
---
name: <skill-name>
description: <specific action and "Use when..." trigger>
metadata:
  category: <category>
  tags: [<searchable>, <keywords>]
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
---

# <Skill Title>

## Why This Skill Exists
<recurring task and silent failure mode>

## Requirements
- Required tools/packages/accounts
- Dependency gate command
- Install/stop rule

## When To Use
- <specific trigger>

## Stop Conditions
- `dependency_missing`: <what to do>
- `unsupported_input`: <what to do>
- `verification_failed`: <what to do>

## Steps
### 1. <action>
Runnable command or concrete instruction.

## Pitfalls
- **<mistake>**: <why it matters and how to avoid it>

## Related Skills
- `../<name>/SKILL.md` - <why it helps>
```

### 5. Put Reusable Code In `scripts/`

If the skill needs more than about 20 lines of code, put real runnable code in
`scripts/` instead of a long Markdown code block. The skill should tell the
agent when to run the script and what output/status to expect.

### 6. Test Happy And Failure Paths

At minimum, test:

- Happy-path input.
- Missing required dependency path.
- Unsupported, corrupt, encrypted, private, or blocked input path when relevant.
- Partial-output path when a tool can return incomplete results.
- Optional-capability path where the user request makes the optional dependency required.

Each failure path must fail loudly with a nonzero exit code or explicit stop
status, plus a recovery instruction.

### 7. Update Public Indexes

When adding a skill to this repo, update:

- `README.md`
- `AGENTS.md`
- `docs/SKILL_ARCHITECTURE.md`, if the authoring rule changed
- `docs/PUBLIC_COPY_BOUNDARY.md`, if the public/private boundary changed

## Public-Safety Checklist

Before publishing a skill:

- No private local paths.
- No private email addresses, student data, credentials, keys, tokens, or hidden endpoints.
- No dependency on a private workspace, server, memory system, or non-public corpus.
- No instructions that tell participants to use someone else's machine-specific setup.
- No claim that something was tested unless the test was actually run.

## Pitfalls

- **Silent failure**: continuing after missing requirements, unsupported input,
  failed commands, or unverifiable output.
- **Duplicated skills**: two skills with overlapping scope confuse both humans and agents.
- **Vague descriptions**: generic descriptions make the skill hard to retrieve.
- **Too much prose**: long manuals belong in references or project docs.
- **Private assumptions**: public skills must be detached from private workflows.
