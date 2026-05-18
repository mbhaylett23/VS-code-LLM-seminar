---
name: code-review-quality
description: Use when reviewing code for correctness, safety, maintainability, and missing tests. Findings come first, ordered by severity, with file/line evidence.
---

# Code Review Quality

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
