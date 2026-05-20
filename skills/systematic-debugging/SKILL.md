---
name: systematic-debugging
description: Use when fixing a failing test, runtime error, or behavior mismatch. Follow a small evidence-driven loop: reproduce, inspect, hypothesize, patch minimally, verify, and summarize.
---

# Systematic Debugging

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

- No special libraries are required for the skill itself.
- If the project has tests, the relevant runtime must be installed.
- For the demo repo, Python 3 is enough:

```powershell
python -m unittest discover -s examples/tiny_python_bug
```

## Workflow

1. Reproduce the failure with the smallest relevant command.
2. Read the failing test, error, and implementation.
3. State the likely cause in one sentence.
4. Patch the smallest relevant code path.
5. Run the check again.
6. Summarize:
   - file changed
   - command run
   - result
   - remaining risk

## Rules

- Do not rewrite unrelated code.
- Do not skip verification if a local check is available.
- If the command cannot run, report the exact blocker.
