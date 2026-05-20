---
name: code-review-quality
description: Use when reviewing code for correctness, safety, maintainability, and missing tests. Findings come first, ordered by severity, with file/line evidence.
---

# Code Review Quality

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

## Requirements

- No special libraries are required.
- The agent must be able to read the files under review.
- If line-specific findings are requested, inspect the file before reporting line numbers.

## Output Order

1. Findings first, ordered by severity.
2. Each finding should include:
   - severity
   - file and line reference
   - concrete risk
   - suggested fix
3. Then add open questions or assumptions.
4. Then give a short summary.
5. Mention missing tests or checks.

## Review Axes

- Correctness
- Security and privacy
- Data validation
- Error handling
- Maintainability
- Test coverage

## Rules

- Do not praise the code before listing risks.
- Do not invent line numbers. Read the file.
- If there are no findings, say that clearly and name residual risks.
