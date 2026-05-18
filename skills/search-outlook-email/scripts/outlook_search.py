"""Public demo helper for searching Classic Outlook via COM.

Requires Windows, Classic Outlook, and pywin32:
    python -m pip install pywin32

This script prints metadata by default. Use --body N only when it is safe to
display the selected message body.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from dataclasses import dataclass


FOLDERS = {
    "inbox": 6,
    "sent": 5,
}


@dataclass
class Hit:
    folder: str
    subject: str
    sender: str
    date: str
    body: str


def load_win32com():
    try:
        import win32com.client  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "pywin32 is not installed in this Python environment. "
            "Install it with: python -m pip install pywin32"
        ) from exc
    return win32com.client


def outlook_process_report() -> str:
    try:
        completed = subprocess.run(
            ["tasklist"],
            capture_output=True,
            text=True,
            check=False,
        )
        lines = [
            line
            for line in completed.stdout.splitlines()
            if "OUTLOOK.EXE" in line.upper() or "OLK.EXE" in line.upper()
        ]
        return "\n".join(lines).strip()
    except Exception:
        return ""


def connect_outlook():
    win32com_client = load_win32com()
    try:
        app = win32com_client.Dispatch("Outlook.Application")
        namespace = app.GetNamespace("MAPI")
        return namespace
    except Exception as exc:
        report = outlook_process_report()
        raise SystemExit(
            "Could not connect to Classic Outlook through COM.\n"
            "Make sure Classic Outlook is installed, signed in, synced, and running as OUTLOOK.EXE.\n\n"
            f"Process check:\n{report or '(no tasklist output)'}\n\n"
            f"Original error: {exc}"
        ) from exc


def to_datetime(value) -> dt.datetime | None:
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        return value.replace(tzinfo=None)
    try:
        return dt.datetime.fromtimestamp(int(value))
    except Exception:
        return None


def item_date(item, folder_name: str) -> dt.datetime | None:
    if folder_name == "sent":
        return to_datetime(getattr(item, "SentOn", None))
    return to_datetime(getattr(item, "ReceivedTime", None))


def search_folder(namespace, folder_name: str, query: str, days: int, max_hits: int) -> list[Hit]:
    folder = namespace.GetDefaultFolder(FOLDERS[folder_name])
    items = folder.Items
    sort_field = "[SentOn]" if folder_name == "sent" else "[ReceivedTime]"
    try:
        items.Sort(sort_field, True)
    except Exception:
        pass

    cutoff = dt.datetime.now() - dt.timedelta(days=days)
    query_lc = query.lower()
    hits: list[Hit] = []

    for item in items:
        try:
            when = item_date(item, folder_name)
            if when and when < cutoff:
                break

            subject = str(getattr(item, "Subject", "") or "")
            sender = str(getattr(item, "SenderName", "") or getattr(item, "To", "") or "")
            body = str(getattr(item, "Body", "") or "")
        except Exception:
            continue

        haystack = f"{subject}\n{sender}\n{body}".lower()

        if query_lc in haystack:
            hits.append(
                Hit(
                    folder=folder_name,
                    subject=subject,
                    sender=sender,
                    date=str(when or ""),
                    body=body,
                )
            )
            if len(hits) >= max_hits:
                break

    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Classic Outlook via COM.")
    parser.add_argument("--search", required=True, help="Keyword to search in subject, sender, and body.")
    parser.add_argument("--days", type=int, default=30, help="Search window in days.")
    parser.add_argument("--max", type=int, default=10, help="Maximum hits to print.")
    parser.add_argument("--folder", choices=["inbox", "sent", "all"], default="inbox")
    parser.add_argument("--body", type=int, help="Print full body for result index N after metadata search.")
    args = parser.parse_args()

    namespace = connect_outlook()
    folders = ["inbox", "sent"] if args.folder == "all" else [args.folder]

    hits: list[Hit] = []
    for folder_name in folders:
        hits.extend(search_folder(namespace, folder_name, args.search, args.days, args.max))
    hits = hits[: args.max]

    if not hits:
        print("No matches found. Try increasing --days, checking spelling, or using --folder all.")
        return 0

    for i, hit in enumerate(hits, 1):
        print(f"[{i}] {hit.date} | {hit.folder} | {hit.sender} | {hit.subject}")

    if args.body:
        index = args.body - 1
        if index < 0 or index >= len(hits):
            raise SystemExit(f"--body index out of range. Choose 1-{len(hits)}.")
        print("\n" + "=" * 80)
        print(f"BODY FOR RESULT {args.body}")
        print("=" * 80)
        print(hits[index].body)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
