---
name: grant-ground-truth-ledger
description: Create separated ground-truth ledgers for grants, proposals, reports, and research documents. Use when a workspace needs auditable files for bibliography, claims, methods, people, budget, decisions, and open questions, or when factual records must not be mixed into one numbered reference list.
---

# Grant Ground Truth Ledger

Use this skill before drafting a grant or serious research document.

The goal is to separate facts from prose. The external document is rendered from verified ledgers; it is not the place to store uncertainty, reminders, or guesses.

## Folder

Create this structure in the project root:

```text
ground_truth/
  bibliography.yml
  claims.yml
  methods.yml
  people.yml
  budget.yml
  decisions.yml
  open_questions.yml
```

Templates are in:

```text
skills/grant-ground-truth-ledger/assets/ground_truth/
```

Copy those templates into the project if the files do not already exist. If they do exist, merge carefully and do not overwrite user data.

## Ledger Roles

- `bibliography.yml`: publications, official calls, official webpages, and other citeable sources.
- `claims.yml`: scientific, technical, or proposal claims that require evidence.
- `methods.yml`: protocol, equipment, analysis, data-processing, and measurement details.
- `people.yml`: names, roles, affiliations, responsibilities, and verified commitments.
- `budget.yml`: budget lines, totals, units, eligibility rules, calculations, and sources.
- `decisions.yml`: project choices that must stay consistent but are not external facts.
- `open_questions.yml`: unresolved internal questions that must not leak into external prose.

## Workflow

1. Inspect the project folder and identify the live document source files.
2. Create `ground_truth/` from the templates if it is missing.
3. Extract facts from existing notes, call documents, budgets, papers, and correspondence.
4. Put each fact in the right ledger. Do not make everything a bibliography item.
5. Give each record a stable ID:
   - bibliography: `ref:smith_2021_gamma`
   - claim: `claim:gamma_frequency_age`
   - method: `method:eeg.sampling_rate_hz`
   - person: `person:smith.current_role`
   - budget: `budget.total_eur`
   - decision: `decision:scope.no_diagnostic_claim`
   - question: `q:confirm_partner_role`
6. Mark every record with `status`: `verified`, `partial`, `unverified`, or `do_not_use`.
7. Put unresolved operational uncertainty in `open_questions.yml`, not in the grant text.
8. Before drafting, list which records are ready for external prose and which still block the document.

## Source-To-Text Rules

- Bibliography records may become citations.
- Claims must cite bibliography records or official sources.
- Methods, people, budget, and decisions should be referenced by stable handles in working drafts, but should not become numbered bibliography items unless they are actual external sources.
- Budget calculations must record the expression or spreadsheet source used to produce the number.
- Person roles and affiliations must come from an official profile, direct confirmation, or a clearly named local source.
- Decisions are not evidence. They explain what the team chose to do.

## External Prose Boundary

Write external grant text only from records that are verified or explicitly framed as caveats.

Do not write:

- "need to check with X"
- "TBC"
- "probably"
- "maybe"
- "awaiting confirmation"
- "[CITE]"
- "ask later"

Those belong in `open_questions.yml`.

## Stop Conditions

Stop and report the blocker when:

- a fact has no source
- two sources conflict
- the ledger category is unclear
- a required value is still `unverified`
- a user asks for submission-ready prose while blockers remain in `open_questions.yml`
