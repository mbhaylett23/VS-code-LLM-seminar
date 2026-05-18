"""Public demo helper for searching Gmail via IMAP.

Credentials are read from environment variables:
    GMAIL_ADDRESS
    GMAIL_APP_PASSWORD

Prints metadata by default. Use --body N only when it is safe to display the
selected message body.
"""

from __future__ import annotations

import argparse
import datetime as dt
import email
import imaplib
import os
from dataclasses import dataclass
from email.header import decode_header
from email.message import Message
from email.utils import parsedate_to_datetime


@dataclass
class Hit:
    folder: str
    subject: str
    sender: str
    date: str
    body: str


def decode_mime(value: str | None) -> str:
    if not value:
        return ""
    parts = []
    for chunk, encoding in decode_header(value):
        if isinstance(chunk, bytes):
            parts.append(chunk.decode(encoding or "utf-8", errors="replace"))
        else:
            parts.append(chunk)
    return "".join(parts)


def body_from_message(msg: Message) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", "")).lower()
            if content_type == "text/plain" and "attachment" not in disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="replace")
    payload = msg.get_payload(decode=True)
    if payload:
        charset = msg.get_content_charset() or "utf-8"
        return payload.decode(charset, errors="replace")
    return ""


def connect() -> imaplib.IMAP4_SSL:
    address = os.environ.get("GMAIL_ADDRESS")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not address or not password:
        raise SystemExit(
            "Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD environment variables first."
        )
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.login(address, password)
    except imaplib.IMAP4.error as exc:
        raise SystemExit(
            "Gmail IMAP login failed. Check IMAP access, 2-Step Verification, "
            "App Password availability, and Workspace admin policy."
        ) from exc
    return mail


def imap_date(days: int) -> str:
    since = dt.datetime.now() - dt.timedelta(days=days)
    return since.strftime("%d-%b-%Y")


def search_folder(mail: imaplib.IMAP4_SSL, folder: str, query: str, days: int, max_hits: int) -> list[Hit]:
    status, _ = mail.select(f'"{folder}"', readonly=True)
    if status != "OK":
        return []

    status, data = mail.search(None, "SINCE", imap_date(days))
    if status != "OK" or not data or not data[0]:
        return []

    ids = data[0].split()
    ids.reverse()
    query_lc = query.lower()
    hits: list[Hit] = []

    for msg_id in ids:
        status, fetched = mail.fetch(msg_id, "(RFC822)")
        if status != "OK" or not fetched:
            continue
        raw = fetched[0][1]
        msg = email.message_from_bytes(raw)
        subject = decode_mime(msg.get("Subject"))
        sender = decode_mime(msg.get("From"))
        date_header = msg.get("Date", "")
        try:
            date_value = str(parsedate_to_datetime(date_header))
        except Exception:
            date_value = date_header
        body = body_from_message(msg)
        haystack = f"{subject}\n{sender}\n{body}".lower()
        if query_lc in haystack:
            hits.append(Hit(folder=folder, subject=subject, sender=sender, date=date_value, body=body))
            if len(hits) >= max_hits:
                break

    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Gmail via IMAP.")
    parser.add_argument("--search", required=True, help="Keyword to search in subject, sender, and body.")
    parser.add_argument("--days", type=int, default=30, help="Search window in days.")
    parser.add_argument("--max", type=int, default=10, help="Maximum hits to print.")
    parser.add_argument("--sent", action="store_true", help="Search sent mail as well as inbox.")
    parser.add_argument("--sent-folder", default="[Gmail]/Sent Mail", help="IMAP folder name for sent mail.")
    parser.add_argument("--body", type=int, help="Print full body for result index N after metadata search.")
    args = parser.parse_args()

    mail = connect()
    folders = ["INBOX"]
    if args.sent:
        folders.append(args.sent_folder)

    hits: list[Hit] = []
    for folder in folders:
        hits.extend(search_folder(mail, folder, args.search, args.days, args.max))
    hits = hits[: args.max]
    mail.logout()

    if not hits:
        print("No matches found. Try increasing --days, checking spelling, or adding --sent.")
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

