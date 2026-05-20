---
name: grant-definite-language
description: Convert grant, proposal, and research-administration prose from internal working language into definite external-facing language. Use when a draft contains TODOs, TBCs, "need to check", uncertain collaborator notes, unresolved citation placeholders, AI-sounding hedges, or when verified ground-truth records should be turned into funder-facing prose.
---

# Grant Definite Language

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

Use this skill after the ground-truth ledgers exist and before sharing a proposal with collaborators, funders, or administrators.

External grant prose should state verified decisions clearly. Internal uncertainty belongs in `ground_truth/open_questions.yml`, not in the grant text.

## Workflow

1. Identify the text that is intended for external readers.
2. Read the relevant ground-truth ledgers if they exist:
   - `ground_truth/claims.yml`
   - `ground_truth/methods.yml`
   - `ground_truth/people.yml`
   - `ground_truth/budget.yml`
   - `ground_truth/bibliography.yml`
   - `ground_truth/open_questions.yml`
3. Run the uncertainty scanner.
4. For each flagged phrase, decide whether it is:
   - a verified fact that should be rewritten definitely
   - an unresolved internal question that should move to `open_questions.yml`
   - a scientific limitation that should remain as a proper caveat
   - an unsupported claim that should be removed
5. Rewrite only what the ground truth supports.
6. Report remaining blockers separately from the clean external text.

## Scanner

Run from the project root:

```powershell
python skills/grant-definite-language/scripts/scan_uncertainty.py proposal.md
```

For a folder:

```powershell
python skills/grant-definite-language/scripts/scan_uncertainty.py proposal/sections --report admin/uncertainty_scan.md
```

## Rewrite Rules

Use definite language when the fact is verified:

- "The project will..."
- "The protocol uses..."
- "The budget allocates..."
- "The partner has agreed to..."
- "The cited study reports..."
- "The work package delivers..."

Use controlled scientific caution when the evidence requires it:

- "is associated with"
- "is consistent with"
- "will test whether"
- "will evaluate"
- "is designed to estimate"

Do not leave internal working language in the proposal:

- "need to check with John"
- "TBC"
- "probably"
- "maybe"
- "ask later"
- "awaiting confirmation"
- "[CITE]"
- "TODO"

Do not turn uncertainty into false certainty. If the ledger does not verify the fact, move the issue to `open_questions.yml` or remove the sentence.

## Output Standard

Return:

1. revised external prose
2. moved open questions
3. unsupported claims removed or weakened
4. remaining blockers
5. any citations or ledger entries that still need verification

## Stop Conditions

Stop and ask for source material when:

- the requested rewrite depends on unverified partner roles, budgets, deadlines, methods, or claims
- the draft contains placeholders but no ground-truth ledger
- the only basis for a definite statement is model memory or plausible inference
