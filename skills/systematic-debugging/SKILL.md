---
name: systematic-debugging
description: Use when fixing a failing test, runtime error, or behavior mismatch. Follow a small evidence-driven loop: reproduce, inspect, hypothesize, patch minimally, verify, and summarize.
---

# Systematic Debugging

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
