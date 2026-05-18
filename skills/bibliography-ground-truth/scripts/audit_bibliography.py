#!/usr/bin/env python
"""Audit bibliography.yml against proposal text.

This public teaching script is local and generic. It has no dependency on any
separate private skill library.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


REF_RE = re.compile(r"\[ref:([A-Za-z0-9_.:-]+)\]")
NUMERIC_RE = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")


def load_yaml(path: Path) -> list[dict[str, Any]]:
    try:
        import yaml  # type: ignore
    except ImportError:
        print(
            "PyYAML is required for this audit. Install it in the active Python "
            "environment, for example: python -m pip install pyyaml",
            file=sys.stderr,
        )
        raise SystemExit(2)

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        raise SystemExit(f"{path} must contain a YAML list of bibliography records.")
    for i, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise SystemExit(f"{path} record {i} is not a mapping/object.")
    return data


def iter_text_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
            files.extend(sorted(path.rglob("*.txt")))
        elif path.exists():
            files.append(path)
        else:
            print(f"WARNING: text path does not exist: {path}", file=sys.stderr)
    return files


def extract_citations(files: list[Path]) -> tuple[dict[str, list[str]], dict[int, list[str]]]:
    ref_hits: dict[str, list[str]] = {}
    number_hits: dict[int, list[str]] = {}
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            loc = f"{path}:{line_no}"
            for ref_id in REF_RE.findall(line):
                normalized = ref_id if ref_id.startswith("ref:") else f"ref:{ref_id}"
                ref_hits.setdefault(normalized, []).append(loc)
            for group in NUMERIC_RE.findall(line):
                for number in re.findall(r"\d+", group):
                    number_hits.setdefault(int(number), []).append(loc)
    return ref_hits, number_hits


def has_source_identifier(record: dict[str, Any]) -> bool:
    return any(record.get(key) for key in ("doi", "pmid", "pmcid", "url", "local_source"))


def audit(records: list[dict[str, Any]], text_files: list[Path]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    by_number: dict[int, dict[str, Any]] = {}

    for index, record in enumerate(records, start=1):
        rid = record.get("id")
        if not rid:
            errors.append(f"record {index}: missing id")
            continue
        if not isinstance(rid, str) or not rid.startswith("ref:"):
            errors.append(f"{rid}: id should be a stable ref:* identifier")
        if rid in by_id:
            errors.append(f"{rid}: duplicate bibliography id")
        by_id[str(rid)] = record

        number = record.get("citation_number")
        if number not in (None, ""):
            try:
                number_i = int(number)
            except (TypeError, ValueError):
                errors.append(f"{rid}: citation_number is not an integer: {number!r}")
            else:
                if number_i in by_number:
                    errors.append(f"{rid}: duplicate citation_number {number_i}")
                by_number[number_i] = record

        for field in ("title", "authors", "year", "venue", "status", "supports_claims"):
            if not record.get(field):
                errors.append(f"{rid}: missing required field {field}")

        authors = record.get("authors")
        if authors and not isinstance(authors, list):
            errors.append(f"{rid}: authors must be a full-author list")

        if not has_source_identifier(record):
            errors.append(f"{rid}: missing DOI/PMID/PMCID/URL/local_source")

        status = str(record.get("status", "")).lower()
        if status in {"unverified", "do_not_use"}:
            warnings.append(f"{rid}: status is {status}")

    ref_hits, number_hits = extract_citations(text_files)
    cited_ids = set(ref_hits)

    for ref_id, locations in sorted(ref_hits.items()):
        if ref_id not in by_id:
            errors.append(f"{ref_id}: cited with no bibliography record at {', '.join(locations[:5])}")

    for number, locations in sorted(number_hits.items()):
        if number not in by_number:
            errors.append(f"[{number}]: numeric citation has no bibliography citation_number at {', '.join(locations[:5])}")
        else:
            cited_ids.add(str(by_number[number].get("id")))

    for rid, record in sorted(by_id.items()):
        if rid not in cited_ids and not record.get("uncited_ok"):
            warnings.append(f"{rid}: bibliography record not cited in scanned text")
        if rid in cited_ids and str(record.get("status", "")).lower() != "verified":
            warnings.append(f"{rid}: cited but status is {record.get('status')!r}, not verified")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit bibliography.yml against proposal text.")
    parser.add_argument("--bibliography", required=True, type=Path)
    parser.add_argument("--text", action="append", default=[], type=Path, help="Markdown/text file or folder to scan. May be repeated.")
    parser.add_argument("--report", type=Path, help="Optional Markdown report path.")
    args = parser.parse_args()

    records = load_yaml(args.bibliography)
    text_files = iter_text_files(args.text) if args.text else []
    errors, warnings = audit(records, text_files)

    lines = ["# Bibliography Audit", ""]
    lines.append(f"- Bibliography records: {len(records)}")
    lines.append(f"- Text files scanned: {len(text_files)}")
    lines.append("")
    lines.append("## Blocking Issues")
    if errors:
        lines.extend(f"- {item}" for item in errors)
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Warnings")
    if warnings:
        lines.extend(f"- {item}" for item in warnings)
    else:
        lines.append("- None")
    report = "\n".join(lines) + "\n"

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    print(report)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
