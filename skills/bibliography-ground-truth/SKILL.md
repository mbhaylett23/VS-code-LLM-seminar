---
name: bibliography-ground-truth
description: Build and audit a bibliography ground-truth ledger for grants, reports, theses, and research documents. Use when citation numbers must match bibliography entries, when DOI/PMID/title/full-author metadata must be verified, when a document uses numeric citations such as [1], or when stable source IDs like ref:smith_2021_gamma need to be mapped to rendered references.
---

# Bibliography Ground Truth

Use this skill when references matter enough that "looks plausible" is not good enough.

The rule is simple: bibliography records use stable IDs; numeric citation numbers are rendered output and must be audited.

## Required Pattern

Keep bibliography data in:

```text
ground_truth/bibliography.yml
```

Use stable IDs in the source ledger:

```text
ref:smith_2021_gamma
ref:grant_call_2026
ref:who_guidance_2024
```

Do not use the citation number as the source ID. Citation number `[1]` can change when the document is reordered; `ref:smith_2021_gamma` should not.

## Bibliography Record

Each entry should contain:

- `id`: stable source ID, starting with `ref:`
- `status`: `verified`, `partial`, `unverified`, or `do_not_use`
- `citation_number`: optional rendered number, such as `1`
- `title`: full source title
- `authors`: full author list, not only "et al."
- `year`
- `venue`: journal, conference, funder, official source, or website owner
- one or more source identifiers: `doi`, `pmid`, `pmcid`, `url`, or `local_source`
- `supports_claims`: claim IDs this source supports
- `cited_in`: files or sections where the source is used
- `notes`: limits on what the source actually supports

Example:

```yaml
- id: ref:smith_2021_gamma
  status: verified
  citation_number: 1
  title: "Full paper title"
  authors:
    - "Smith, Alice"
    - "Jones, Ben"
  year: 2021
  venue: "Journal Name"
  doi: "10.xxxx/example"
  pmid: null
  pmcid: null
  url: "https://doi.org/10.xxxx/example"
  local_source: "sources/smith_2021_gamma.pdf"
  supports_claims:
    - claim:gamma_frequency_age
  cited_in:
    - "proposal/background.md"
  notes: "Supports association language only; do not state causality."
```

## Workflow

1. Find the live proposal/report/thesis source files.
2. Find or create `ground_truth/bibliography.yml`.
3. For each source, verify title, full author list, year, venue, DOI/PMID/PMCID/URL/local source from an opened source.
4. Replace vague labels like "Smith et al." in the ledger with full metadata.
5. Use stable IDs such as `[ref:smith_2021_gamma]` while drafting when possible.
6. If the final format requires numeric citations, assign `citation_number` only after the bibliography order is decided.
7. Run the audit script before sharing externally.
8. Fix blocking issues before polishing prose.

## Audit Script

Run from the project root:

```powershell
python skills/bibliography-ground-truth/scripts/audit_bibliography.py --bibliography ground_truth/bibliography.yml --text proposal
```

Use explicit files if the proposal is not in a folder:

```powershell
python skills/bibliography-ground-truth/scripts/audit_bibliography.py --bibliography ground_truth/bibliography.yml --text proposal.md --text background.md --report admin/bibliography_audit.md
```

The script checks:

- duplicate source IDs
- duplicate citation numbers
- missing required metadata
- numeric citations without bibliography entries
- stable `ref:*` citations without bibliography entries
- cited sources marked `unverified` or `do_not_use`
- bibliography entries that are never cited and are not marked `uncited_ok: true`

If PyYAML is missing, install it into the active Python environment or ask the agent to help set up Python first.

## Stop Conditions

Stop and mark the item unresolved when:

- the DOI/PMID/title/full author list cannot be verified from an opened source
- the cited source supports a weaker claim than the prose states
- numeric citation order cannot be reconciled with the bibliography
- the only evidence is model memory, a search snippet, or an old chat
- methods, budget, people, or decisions are being accidentally turned into bibliography numbers
