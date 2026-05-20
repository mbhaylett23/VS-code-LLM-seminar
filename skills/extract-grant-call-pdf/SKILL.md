---
name: extract-grant-call-pdf
description: Extract grant-call PDF text with a mandatory OCR/dependency preflight, classify extraction quality, capture candidate deadlines/budgets/eligibility/scope/evaluation details, and produce a source-backed summary pack. Use when asked to summarize a grant call, funding call, tender, call-for-proposals PDF, official guidance PDF, or scanned/encrypted PDF where important details must be extracted without hallucinating or silently skipping OCR.
metadata:
  category: documents
  tags: [pdf, grant-call, funding-call, extraction, summary, deadlines, eligibility, budget, ocr, scanned-pdf]
  created: 2026-05-20
  updated: 2026-05-20
---

# Extract Grant Call PDF

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

## Why this skill exists

Grant-call PDFs hide important details in tables, footnotes, annexes, and scanned
pages. The failure mode is a polished summary that invents a deadline, budget,
eligibility rule, or submission condition that was not actually extracted from
the document.

## Requirements

- Required Python packages: `pymupdf`, `pypdf`, and `pillow`.
- Required OCR tool: `tesseract`.
- Choose one Python command for this skill:

```text
Windows venv: .\.venv\Scripts\python.exe
macOS/Linux venv: ./.venv/bin/python
Conda option: conda run -n grant-pdf-extract python
```

Standard Python setup on Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install pymupdf pypdf pillow
winget install UB-Mannheim.TesseractOCR
```

Standard Python setup on macOS/Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install pymupdf pypdf pillow
# macOS: brew install tesseract
# Ubuntu/Debian: sudo apt-get install tesseract-ocr
```

Optional conda environment:

```powershell
conda create -n grant-pdf-extract -c conda-forge python=3.12 pymupdf pypdf pillow tesseract -y
```

Or install into an existing conda environment if the user already uses conda:

```powershell
conda install -n <env> -c conda-forge pymupdf pypdf pillow tesseract -y
```

OCR is mandatory for colleague-facing grant-call extraction. If Tesseract is not
installed or cannot launch, stop and install it before summarizing. Do not treat
missing OCR as a warning for scanned PDFs.

## When To Use

- Summarizing a grant call, funding call, tender, call-for-proposals document,
  programme guide, or official guidance PDF.
- Extracting deadlines, budget limits, eligibility, scope, evaluation criteria,
  required documents, submission route, or contact details from a PDF.
- Checking whether a PDF has a usable text layer, is scanned/image-only, is
  encrypted, contains forms, or needs OCR/password/manual table review.

## Steps

### 1. Run The Dependency Gate

From this skill directory:

```powershell
<python> "scripts/extract_grant_call_pdf.py" --check-deps
```

Proceed only when the status is `ok`. If the status is `dependency_missing`,
install the missing tool or package and rerun the check. Do not continue in
best-effort mode. Replace `<python>` with the venv Python path or the conda
option listed above.

### 2. Run Extraction

Single PDF:

```powershell
<python> "scripts/extract_grant_call_pdf.py" `
  --input "path/to/call.pdf" `
  --output "grant_call_extraction"
```

Multiple PDFs:

```powershell
<python> "scripts/extract_grant_call_pdf.py" --input "*.pdf" --output "grant_call_extraction"
```

Encrypted PDF:

```powershell
<python> "scripts/extract_grant_call_pdf.py" --input "call.pdf" --password "<password>" --output "grant_call_extraction"
```

The script writes:

- `<stem>.extracted.md` - page-aware extracted text and form-field notes.
- `<stem>.details.json` - machine-readable extraction status and candidate details.
- `<stem>.summary_pack.md` - compact source pack for the LLM to summarize.
- `manifest.json` - one row per input PDF.

### 3. Check Extraction Status Before Summarizing

Open `manifest.json` or the top of `<stem>.summary_pack.md`.

Proceed when status is `ok`, `ok_with_warnings`, or `mixed_ocr`. For
`ok_with_warnings`, include the warnings in the final summary and manually
inspect sparse/table-heavy pages. Stop and report when:

- `dependency_missing` - install the missing package or OCR dependency, then rerun the dependency gate.
- `encrypted_needs_password` - ask for the password.
- `ocr_required` - OCR is required before this PDF can be summarized safely.
- `extraction_failed` - the PDF may be corrupt or unsupported.
- `sparse_text` - extraction produced too little text; inspect the original PDF or rerun with OCR.

Do not fill missing details from intuition. Write `not found in extracted text`
when the pack does not support a field.

### 4. Produce The Summary

Use `<stem>.summary_pack.md` first, then inspect `<stem>.extracted.md` for
supporting page text before making any claim.

Return this structure:

```markdown
## Plain-Language Summary
<5-10 bullets, no invented facts>

## Important Details
| Field | Extracted value | Source page | Confidence / note |
|---|---|---|---|
| Call identifier | ... | p. ... | ... |
| Funder / programme | ... | p. ... | ... |
| Main objective / scope | ... | p. ... | ... |
| Who can apply | ... | p. ... | ... |
| Funding amount / budget | ... | p. ... | ... |
| Duration | ... | p. ... | ... |
| Deadline(s) | ... | p. ... | ... |
| Submission route | ... | p. ... | ... |
| Required documents | ... | p. ... | ... |
| Evaluation criteria | ... | p. ... | ... |
| Restrictions / exclusions | ... | p. ... | ... |
| Contact / helpdesk | ... | p. ... | ... |

## Watch-Outs
- <ambiguous, missing, table-risk, OCR-risk, or verify-in-original items>
```

Every row must cite a source page or say `not found in extracted text`.

### 5. Verify High-Risk Details Against The Original PDF

Before sending the summary to a colleague, manually check these in the original
PDF view:

- Final deadline and time zone.
- Funding ceiling, co-funding percentage, eligible costs, and VAT rules.
- Eligibility and consortium composition rules.
- Required forms/annexes.
- Evaluation criteria and thresholds.
- Any table-derived value.

If the PDF contains tables or footnotes, say whether they were text-extracted
cleanly or require manual review.

## Pitfalls

- **Text layer does not mean table extraction is correct.** Tables can be
  flattened into strange reading order. Verify table-derived values manually.
- **OCR text is noisy.** Treat `mixed_ocr` as usable for recall, not final proof.
- **Encrypted PDFs need the right password.** Do not summarize a locked document from metadata.
- **Scanned PDFs are not optional OCR cases.** If OCR is missing, stop and install it.
- **Candidate details are not final facts.** The script collects likely lines;
  the agent must still decide what each line means and cite the page.

## Related Skills

- `../grant-ground-truth-ledger/SKILL.md` - store extracted grant facts as auditable records.
- `../bibliography-ground-truth/SKILL.md` - verify citation and bibliography metadata in proposal drafts.
- `../grant-definite-language/SKILL.md` - turn verified grant requirements into definite external-facing language.
