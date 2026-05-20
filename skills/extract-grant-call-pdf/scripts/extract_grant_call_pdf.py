#!/usr/bin/env python3
"""Extract grant-call PDFs into text, candidate details, and summary packs.

The script fails closed by default:
- PyMuPDF is preferred for text, metadata, images, forms, and rendering.
- pypdf is a fallback text extractor.
- Tesseract OCR is a mandatory preflight dependency unless the caller passes
  --allow-missing-ocr for development-only text-layer debugging.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DETAIL_PATTERNS: dict[str, list[str]] = {
    "deadline": [
        r"\bdeadline\b",
        r"\bclosing date\b",
        r"\bsubmission deadline\b",
        r"\bcut-?off\b",
        r"\bdue date\b",
        r"\bfecha limite\b",
        r"\bfecha limite\b",
        r"\btermini\b",
        r"\bdata limit\b",
    ],
    "budget": [
        r"\bbudget\b",
        r"\bfunding\b",
        r"\bgrant\b",
        r"\bmaximum\b",
        r"\bceiling\b",
        r"\beligible costs?\b",
        r"\bco-?funding\b",
        r"\bfinanciacion\b",
        r"\bimporte\b",
        r"\bsubvencion\b",
        r"(?:\u20ac|\$|\u00a3)\s?\d",
        r"\bEUR\b",
    ],
    "eligibility": [
        r"\beligib",
        r"\bapplicant",
        r"\bbeneficiar",
        r"\bconsortium\b",
        r"\bpartners?\b",
        r"\bwho can apply\b",
        r"\bnot eligible\b",
        r"\brequisitos\b",
        r"\bsolicitantes?\b",
        r"\bentidades\b",
    ],
    "scope": [
        r"\bscope\b",
        r"\bobjective",
        r"\bpriority\b",
        r"\btopic\b",
        r"\bexpected outcome\b",
        r"\bimpact\b",
        r"\bpurpose\b",
        r"\bobjectiu\b",
        r"\bobjetivo\b",
    ],
    "duration": [
        r"\bduration\b",
        r"\bmonths?\b",
        r"\byears?\b",
        r"\bperiod\b",
        r"\bduracion\b",
        r"\bmeses\b",
    ],
    "evaluation": [
        r"\bevaluation\b",
        r"\bcriteria\b",
        r"\bthreshold\b",
        r"\bscore\b",
        r"\bselection\b",
        r"\baward criteria\b",
        r"\bevaluacion\b",
        r"\bcriterios\b",
    ],
    "submission": [
        r"\bsubmit\b",
        r"\bportal\b",
        r"\bapplication form\b",
        r"\bannex\b",
        r"\brequired documents?\b",
        r"\bproposal template\b",
        r"\bpresentacion\b",
        r"\bsolicitud\b",
    ],
    "contact": [
        r"\bcontact\b",
        r"\bemail\b",
        r"\bhelpdesk\b",
        r"\bquestions\b",
        r"\btelefono\b",
        r"\bcorreo\b",
        r"\bconsultas\b",
        r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
    ],
    "call_identifier": [
        r"\bcall\b",
        r"\bcall for proposals\b",
        r"\bprogramme\b",
        r"\btopic id\b",
        r"\breference\b",
        r"\bidentifier\b",
        r"\bconvocatoria\b",
        r"\breferencia\b",
    ],
}

DATE_RE = re.compile(
    r"\b("
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
    r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}|"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}|"
    r"\d{1,2}\s+de\s+[A-Za-z]+\s+de\s+\d{4}"
    r")\b",
    re.IGNORECASE,
)
MONEY_RE = re.compile(
    r"((?:\u20ac|\$|\u00a3)\s?\d[\d.,]*|\b\d[\d.,]*\s?(?:EUR|euros?|USD|GBP)\b)",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
FIELD_LABEL_RE = re.compile(r"^[A-Z][A-Za-z0-9 /&()_.%-]{1,60}:")


@dataclass
class PageResult:
    page: int
    text: str
    extractor: str
    char_count: int
    word_count: int
    image_count: int
    form_fields: list[dict[str, str]]
    warnings: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract grant-call PDFs into summary-ready source packs.")
    parser.add_argument("--input", nargs="+", help="PDF path(s) or glob(s).")
    parser.add_argument("--output", help="Output directory.")
    parser.add_argument("--password", default=None, help="Password for encrypted PDFs.")
    parser.add_argument("--ocr", choices=["auto", "never", "required"], default="auto", help="OCR behavior.")
    parser.add_argument(
        "--allow-missing-ocr",
        action="store_true",
        help="Development-only escape hatch: process text-layer PDFs even if Tesseract is unavailable.",
    )
    parser.add_argument(
        "--check-ocr",
        action="store_true",
        help="Verify Tesseract/OCR availability and exit without processing PDFs.",
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Verify all required package and OCR dependencies, then exit without processing PDFs.",
    )
    parser.add_argument("--max-detail-hits", type=int, default=80, help="Maximum candidate detail lines per PDF.")
    args = parser.parse_args()
    if not (args.check_ocr or args.check_deps):
        if not args.input:
            parser.error("--input is required unless --check-ocr or --check-deps is used.")
        if not args.output:
            parser.error("--output is required unless --check-ocr or --check-deps is used.")
    return args


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def expand_inputs(patterns: Iterable[str]) -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        matches = glob.glob(pattern)
        for item in matches or [pattern]:
            path = Path(item).expanduser()
            if path.suffix.lower() != ".pdf":
                continue
            resolved = path.resolve()
            if resolved not in seen:
                found.append(resolved)
                seen.add(resolved)
    return sorted(found, key=lambda p: str(p).lower())


def clean_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def line_candidates(text: str) -> list[str]:
    physical_lines = []
    for raw in text.splitlines():
        line = clean_text(raw)
        if 3 <= len(line) <= 500:
            physical_lines.append(line)

    logical_lines: list[str] = []
    current: list[str] = []
    for line in physical_lines:
        starts_new_label = FIELD_LABEL_RE.match(line) is not None
        if starts_new_label and current:
            logical_lines.append(clean_text(" ".join(current)))
            current = [line]
        else:
            current.append(line)
    if current:
        logical_lines.append(clean_text(" ".join(current)))
    return [line for line in logical_lines if 10 <= len(line) <= 700]


def detect_detail_lines(pages: list[PageResult], max_hits: int) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    compiled = {
        category: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for category, patterns in DETAIL_PATTERNS.items()
    }
    for page in pages:
        for line in line_candidates(page.text):
            categories = [
                category
                for category, patterns in compiled.items()
                if any(pattern.search(line) for pattern in patterns)
            ]
            if not categories and not (DATE_RE.search(line) or MONEY_RE.search(line) or URL_RE.search(line) or EMAIL_RE.search(line)):
                continue
            if DATE_RE.search(line) and "deadline" not in categories:
                categories.append("date")
            if MONEY_RE.search(line) and "budget" not in categories:
                categories.append("money")
            if URL_RE.search(line) and "submission" not in categories:
                categories.append("url")
            if EMAIL_RE.search(line) and "contact" not in categories:
                categories.append("contact")
            hits.append({"page": page.page, "categories": sorted(set(categories)), "text": line})
            if len(hits) >= max_hits:
                return hits
    return hits


def tesseract_install_help() -> str:
    script = Path(__file__).resolve()
    return "\n".join(
        [
            "OCR HARD STOP: Tesseract is required before extracting grant-call PDFs.",
            "",
            "Install a dedicated conda environment:",
            "  conda create -n grant-pdf-extract -c conda-forge python=3.12 pymupdf pypdf pillow tesseract -y",
            "",
            "Or install into an existing conda environment:",
            "  conda install -n <env> -c conda-forge pymupdf pypdf pillow tesseract -y",
            "",
            "Then verify:",
            f'  conda run -n grant-pdf-extract python "{script}" --check-deps',
            "",
            "Do not summarize scanned/image-only grant PDFs until this check passes.",
        ]
    )


def dependency_install_help(missing: list[str]) -> str:
    missing_text = ", ".join(missing)
    return "\n".join(
        [
            f"DEPENDENCY HARD STOP: required dependency missing: {missing_text}",
            "",
            "Install a dedicated conda environment:",
            "  conda create -n grant-pdf-extract -c conda-forge python=3.12 pymupdf pypdf pillow tesseract -y",
            "",
            "Or install into an existing conda environment:",
            "  conda install -n <env> -c conda-forge pymupdf pypdf pillow tesseract -y",
            "",
            "Then verify:",
            f'  conda run -n grant-pdf-extract python "{Path(__file__).resolve()}" --check-deps',
        ]
    )


def python_dependency_checks() -> list[dict[str, Any]]:
    required_modules = [
        ("pymupdf", "fitz"),
        ("pypdf", "pypdf"),
    ]
    checks: list[dict[str, Any]] = []
    for package, module in required_modules:
        checks.append(
            {
                "package": package,
                "module": module,
                "required": True,
                "available": importlib.util.find_spec(module) is not None,
            }
        )
    return checks


def missing_python_dependencies() -> list[str]:
    return [check["package"] for check in python_dependency_checks() if not check["available"]]


def run_dependency_gate(tesseract_cmd: str | None, tesseract_error: str | None, require_ocr: bool) -> int:
    package_checks = python_dependency_checks()
    missing = [check["package"] for check in package_checks if not check["available"]]
    if require_ocr and not tesseract_cmd:
        missing.append("tesseract")
    report = {
        "status": "dependency_missing" if missing else "ok",
        "python_packages": package_checks,
        "ocr": {
            "required": require_ocr,
            "available": bool(tesseract_cmd),
            "command": tesseract_cmd,
            "error": tesseract_error,
        },
        "missing": missing,
    }
    print(json.dumps(report, indent=2))
    if missing:
        print(dependency_install_help(missing), file=sys.stderr)
        return 3
    return 0


def candidate_tesseract_paths() -> list[Path]:
    candidates: list[Path] = []
    configured = os.environ.get("TESSERACT_CMD")
    if configured:
        candidates.append(Path(configured).expanduser())

    for executable in ("tesseract", "tesseract.exe"):
        found = shutil.which(executable)
        if found:
            candidates.append(Path(found))

    prefixes = [os.environ.get("CONDA_PREFIX"), sys.prefix]
    suffixes = ["bin/tesseract"]
    if os.name == "nt":
        suffixes = [
            "Library/bin/tesseract.exe",
            "Scripts/tesseract.exe",
            "bin/tesseract.exe",
        ]
    for prefix in prefixes:
        if not prefix:
            continue
        root = Path(prefix)
        for suffix in suffixes:
            candidates.append(root / suffix)

    deduped: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate).lower()
        if key not in seen:
            deduped.append(candidate)
            seen.add(key)
    return deduped


def find_tesseract() -> str | None:
    for candidate in candidate_tesseract_paths():
        if candidate.exists():
            return str(candidate)
    return None


def verify_tesseract() -> tuple[str | None, str | None]:
    cmd = find_tesseract()
    if not cmd:
        return None, "Tesseract executable was not found."
    try:
        completed = subprocess.run(
            [cmd, "--version"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        return None, f"Tesseract executable could not be launched: {exc}"
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or f"exit code {completed.returncode}"
        return None, f"Tesseract executable failed its version check: {detail}"
    return cmd, None


def ocr_page(page: Any, tesseract_cmd: str) -> tuple[str, str | None]:
    import fitz

    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "page.png"
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        pix.save(str(png))
        completed = subprocess.run(
            [tesseract_cmd, str(png), "stdout", "-l", "eng"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            return "", completed.stderr.strip()
        return clean_text(completed.stdout), None


def extract_with_pypdf(pdf: Path, password: str | None) -> list[str]:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf))
    if reader.is_encrypted:
        if not password:
            raise PermissionError("encrypted_needs_password")
        result = reader.decrypt(password)
        if result == 0:
            raise PermissionError("bad_password")
    return [clean_text(page.extract_text() or "") for page in reader.pages]


def extract_pdf(pdf: Path, password: str | None, ocr: str, tesseract_cmd: str | None) -> dict[str, Any]:
    import fitz

    result: dict[str, Any] = {
        "source_pdf": str(pdf),
        "sha256": sha256(pdf),
        "size_bytes": pdf.stat().st_size,
        "processed_at": utc_now(),
        "status": "unknown",
        "warnings": [],
        "metadata": {},
        "page_count": 0,
        "pages": [],
        "detail_candidates": [],
        "overall_text_chars": 0,
        "overall_word_count": 0,
        "ocr_used": False,
        "ocr_available": tesseract_cmd is not None,
        "ocr_command": tesseract_cmd,
    }
    pages: list[PageResult] = []
    try:
        doc = fitz.open(pdf)
    except Exception as exc:
        result["status"] = "extraction_failed"
        result["warnings"].append(f"Could not open PDF with PyMuPDF: {exc}")
        return result

    try:
        if doc.needs_pass:
            if not password:
                result["status"] = "encrypted_needs_password"
                result["warnings"].append("PDF is encrypted and no password was provided.")
                return result
            if not doc.authenticate(password):
                result["status"] = "encrypted_bad_password"
                result["warnings"].append("PDF password was provided but did not unlock the document.")
                return result

        result["metadata"] = {k: v for k, v in (doc.metadata or {}).items() if v}
        result["page_count"] = doc.page_count

        pypdf_pages: list[str] | None = None
        for index, page in enumerate(doc, start=1):
            warnings: list[str] = []
            text = clean_text(page.get_text("text", sort=True) or "")
            extractor = "pymupdf"
            image_count = len(page.get_images(full=True))
            widgets = []
            try:
                for widget in page.widgets() or []:
                    widgets.append(
                        {
                            "name": str(widget.field_name or ""),
                            "type": str(widget.field_type_string or ""),
                            "value": str(widget.field_value or ""),
                        }
                    )
            except Exception as exc:
                warnings.append(f"Could not inspect form fields: {exc}")

            sparse = len(text) < 80
            if sparse and ocr != "never" and image_count > 0:
                if tesseract_cmd:
                    ocr_text, ocr_error = ocr_page(page, tesseract_cmd)
                    if ocr_error:
                        warnings.append(f"OCR failed: {ocr_error}")
                    elif ocr_text:
                        text = ocr_text
                        extractor = "tesseract-ocr"
                        result["ocr_used"] = True
                elif ocr == "required":
                    warnings.append("OCR required but tesseract is not available on PATH.")
                else:
                    warnings.append("Sparse text with images: likely scanned page; OCR not available.")

            if len(text) < 20:
                if pypdf_pages is None:
                    try:
                        pypdf_pages = extract_with_pypdf(pdf, password)
                    except Exception as exc:
                        pypdf_pages = []
                        warnings.append(f"pypdf fallback unavailable: {exc}")
                fallback = pypdf_pages[index - 1] if index - 1 < len(pypdf_pages) else ""
                if len(fallback) > len(text):
                    text = fallback
                    extractor = "pypdf"

            pages.append(
                PageResult(
                    page=index,
                    text=text,
                    extractor=extractor,
                    char_count=len(text),
                    word_count=len(text.split()),
                    image_count=image_count,
                    form_fields=widgets,
                    warnings=warnings,
                )
            )
    finally:
        doc.close()

    total_chars = sum(page.char_count for page in pages)
    total_words = sum(page.word_count for page in pages)
    image_pages = sum(1 for page in pages if page.image_count > 0)
    sparse_pages = sum(1 for page in pages if page.char_count < 80)
    result["pages"] = [asdict(page) for page in pages]
    result["overall_text_chars"] = total_chars
    result["overall_word_count"] = total_words
    result["detail_candidates"] = detect_detail_lines(pages, max_hits=10_000)

    if total_chars >= 500 and sparse_pages == 0:
        result["status"] = "ok"
    elif total_chars >= 500 and sparse_pages > 0:
        result["status"] = "mixed_ocr" if result["ocr_used"] else "ok_with_warnings"
        result["warnings"].append(f"{sparse_pages} pages have sparse text; inspect original PDF.")
    elif image_pages > 0 and not result["ocr_used"]:
        result["status"] = "sparse_text" if result["ocr_available"] else "ocr_required"
        if result["ocr_available"]:
            result["warnings"].append(
                "The PDF appears image-heavy or scanned, but OCR did not recover enough text; inspect the original PDF."
            )
        else:
            result["warnings"].append("The PDF appears image-heavy or scanned; install OCR or ask for a text-layer copy.")
    else:
        result["status"] = "sparse_text"
        result["warnings"].append("Very little text was extracted; inspect original PDF before summarizing.")
    return result


def write_extracted_md(result: dict[str, Any], output: Path) -> None:
    lines = [
        f"# Extracted Text - {Path(result['source_pdf']).name}",
        "",
        f"- Status: `{result['status']}`",
        f"- SHA-256: `{result['sha256']}`",
        f"- Pages: {result['page_count']}",
        f"- Words: {result['overall_word_count']}",
        "",
    ]
    if result.get("warnings"):
        lines.append("## Warnings")
        lines.extend(f"- {warning}" for warning in result["warnings"])
        lines.append("")
    for page in result["pages"]:
        lines.append(f"## Page {page['page']}")
        lines.append("")
        lines.append(f"- Extractor: `{page['extractor']}`; words: {page['word_count']}; images: {page['image_count']}")
        if page.get("warnings"):
            lines.extend(f"- Warning: {warning}" for warning in page["warnings"])
        if page.get("form_fields"):
            lines.append("")
            lines.append("### Form fields")
            for field in page["form_fields"]:
                lines.append(f"- `{field['name']}` ({field['type']}): {field['value']}")
        lines.append("")
        lines.append(page["text"] or "[no text extracted]")
        lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def write_summary_pack(result: dict[str, Any], output: Path, max_detail_hits: int) -> None:
    candidates = result.get("detail_candidates", [])[:max_detail_hits]
    lines = [
        f"# Summary Pack - {Path(result['source_pdf']).name}",
        "",
        "Use this pack to produce a source-backed summary. Do not invent missing fields.",
        "",
        "## Extraction Status",
        "",
        f"- Status: `{result['status']}`",
        f"- Pages: {result['page_count']}",
        f"- Words extracted: {result['overall_word_count']}",
        f"- OCR available: {result['ocr_available']}",
        f"- OCR used: {result['ocr_used']}",
        f"- SHA-256: `{result['sha256']}`",
        "",
    ]
    if result.get("warnings"):
        lines.append("## Warnings")
        lines.extend(f"- {warning}" for warning in result["warnings"])
        lines.append("")

    lines.append("## Candidate Important Details")
    lines.append("")
    if not candidates:
        lines.append("- No candidate detail lines were detected. Inspect the extracted text manually.")
    else:
        for item in candidates:
            cats = ", ".join(item["categories"])
            lines.append(f"- p. {item['page']} [{cats}]: {item['text']}")
    lines.append("")

    lines.append("## Page Text Preview")
    lines.append("")
    for page in result["pages"]:
        text = page["text"].strip()
        preview = text[:1200] + ("..." if len(text) > 1200 else "")
        lines.append(f"### Page {page['page']}")
        lines.append(preview or "[no text extracted]")
        lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def safe_stem(path: Path) -> str:
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", path.stem).strip("._")
    return stem or "document"


def main() -> int:
    args = parse_args()
    tesseract_cmd, tesseract_error = verify_tesseract()
    if args.check_deps:
        return run_dependency_gate(
            tesseract_cmd=tesseract_cmd,
            tesseract_error=tesseract_error,
            require_ocr=not args.allow_missing_ocr,
        )
    if args.check_ocr:
        if tesseract_cmd:
            print(f"OCR OK: Tesseract found at {tesseract_cmd}")
            return 0
        print(tesseract_install_help(), file=sys.stderr)
        if tesseract_error:
            print(f"\nDetected problem: {tesseract_error}", file=sys.stderr)
        return 3

    missing_packages = missing_python_dependencies()
    if missing_packages:
        print(dependency_install_help(missing_packages), file=sys.stderr)
        return 3

    if args.ocr == "required" and not tesseract_cmd:
        print(tesseract_install_help(), file=sys.stderr)
        if tesseract_error:
            print(f"\nDetected problem: {tesseract_error}", file=sys.stderr)
        return 3

    if not tesseract_cmd and not args.allow_missing_ocr:
        print(tesseract_install_help(), file=sys.stderr)
        if tesseract_error:
            print(f"\nDetected problem: {tesseract_error}", file=sys.stderr)
        return 3

    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    pdfs = expand_inputs(args.input)
    if not pdfs:
        print("No PDF inputs found.", file=sys.stderr)
        return 2

    manifest = {
        "processed_at": utc_now(),
        "inputs": [str(pdf) for pdf in pdfs],
        "documents": [],
    }
    exit_code = 0
    for pdf in pdfs:
        result = extract_pdf(pdf, args.password, args.ocr, tesseract_cmd)
        result["detail_candidates"] = result.get("detail_candidates", [])[: args.max_detail_hits]
        stem = safe_stem(pdf)
        details_path = output_dir / f"{stem}.details.json"
        extracted_path = output_dir / f"{stem}.extracted.md"
        summary_path = output_dir / f"{stem}.summary_pack.md"
        details_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        write_extracted_md(result, extracted_path)
        write_summary_pack(result, summary_path, args.max_detail_hits)
        row = {
            "source_pdf": str(pdf),
            "status": result["status"],
            "page_count": result["page_count"],
            "overall_word_count": result["overall_word_count"],
            "sha256": result["sha256"],
            "details_json": str(details_path),
            "extracted_md": str(extracted_path),
            "summary_pack_md": str(summary_path),
            "warnings": result.get("warnings", []),
        }
        manifest["documents"].append(row)
        print(f"{pdf.name}: {result['status']} ({result['page_count']} pages, {result['overall_word_count']} words)")
        if result["status"] not in {"ok", "ok_with_warnings", "mixed_ocr"}:
            exit_code = 1

    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {output_dir / 'manifest.json'}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
