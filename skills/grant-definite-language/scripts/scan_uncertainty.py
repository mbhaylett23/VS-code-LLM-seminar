#!/usr/bin/env python
"""Scan external-facing grant prose for internal uncertainty markers."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATTERNS = [
    r"\bTODO\b",
    r"\bTBC\b",
    r"\bTBD\b",
    r"\[CITE\]",
    r"\?\?\?",
    r"\bneed to check\b",
    r"\bneeds to be checked\b",
    r"\bcheck with\b",
    r"\bask [A-Z][A-Za-z-]+\b",
    r"\bask later\b",
    r"\bawaiting confirmation\b",
    r"\bto be confirmed\b",
    r"\bprobably\b",
    r"\bmaybe\b",
    r"\bI think\b",
    r"\bnot sure\b",
    r"\bplaceholder\b",
]


def iter_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
            files.extend(sorted(path.rglob("*.txt")))
        elif path.exists():
            files.append(path)
    return files


def scan(files: list[Path]) -> list[str]:
    hits: list[str] = []
    compiled = [(pattern, re.compile(pattern, flags=re.IGNORECASE)) for pattern in PATTERNS]
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for label, regex in compiled:
                if regex.search(line):
                    hits.append(f"{path}:{line_no}: {label}: {line.strip()}")
                    break
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan grant text for internal uncertainty markers.")
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown/text files or folders to scan.")
    parser.add_argument("--report", type=Path, help="Optional Markdown report path.")
    args = parser.parse_args()

    files = iter_files(args.paths)
    hits = scan(files)

    lines = ["# Uncertainty Scan", ""]
    lines.append(f"- Files scanned: {len(files)}")
    lines.append(f"- Hits: {len(hits)}")
    lines.append("")
    lines.append("## Findings")
    if hits:
        lines.extend(f"- {hit}" for hit in hits)
    else:
        lines.append("- None")
    report = "\n".join(lines) + "\n"

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    print(report)
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
