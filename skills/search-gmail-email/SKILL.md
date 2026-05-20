---
name: search-gmail-email
description: Search Gmail through IMAP from VS Code using environment variables and a public-safe helper script. Use when the user wants to find Gmail messages by keyword, inspect sender/date/subject metadata, include sent mail, or extract a selected body after setting up Gmail IMAP access.
metadata:
  category: email
  tags: [gmail, email, imap, app-password, oauth, privacy]
  created: 2026-05-18
  updated: 2026-05-18
---

# Search Gmail Email

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

Gmail search from an agent should be explicit, bounded, and private. This public starter uses IMAP with credentials stored in environment variables, not in code.

## Requirements

- Python 3.
- Gmail account with IMAP access allowed.
- A safe authentication method:
  - Preferred for production: OAuth through an approved app or connector.
  - Simple workshop path: Gmail App Password, if the account supports it.

No third-party Python libraries are required for the included demo script.

## Official Compatibility Note

Google's Gmail Help says App Passwords require 2-Step Verification. Google Workspace admin docs also state that password-only "less secure app" access is no longer supported for Workspace accounts from 2025-05-01; use OAuth or an app password where allowed by policy.

Sources:

- https://support.google.com/mail/answer/185833
- https://support.google.com/a/answer/6260879

## Safety And Privacy

- Store credentials in environment variables, never in Git.
- Search metadata first: date, sender, subject, folder.
- Do not print full bodies in a public setting unless the user explicitly approves.
- If IMAP/authentication fails, report the blocker. Do not pretend Gmail was searched.

## Setup

### 1. Enable IMAP / Confirm Admin Policy

For personal Gmail, check Gmail settings and confirm IMAP is enabled.

For Google Workspace, the administrator may control IMAP and app-password access. If IMAP or app passwords are unavailable, use an approved institutional connector or OAuth workflow instead.

### 2. Create A Gmail App Password, If Allowed

For the simple local demo path:

1. Enable 2-Step Verification on the Google account.
2. Open Google Account security settings.
3. Create an App Password for mail/IMAP.
4. Copy the generated app password once.

Do not commit the app password to GitHub.

### 3. Set Environment Variables

PowerShell:

```powershell
$env:GMAIL_ADDRESS = "your.name@example.com"
$env:GMAIL_APP_PASSWORD = "your-16-character-app-password"
```

macOS/Linux/Git Bash:

```bash
export GMAIL_ADDRESS="your.name@example.com"
export GMAIL_APP_PASSWORD="your-16-character-app-password"
```

Use session variables for workshops. If you persist them, use your OS credential manager or a private `.env` file that is ignored by Git.

## Workflow

### 1. Run A Metadata Search

```powershell
python .\skills\search-gmail-email\scripts\gmail_search.py --days 30 --search "keyword" --max 10
```

Include sent mail:

```powershell
python .\skills\search-gmail-email\scripts\gmail_search.py --days 90 --search "keyword" --sent --max 20
```

### 2. Pull A Selected Body

Only after the user confirms it is safe to view message content:

```powershell
python .\skills\search-gmail-email\scripts\gmail_search.py --days 30 --search "keyword" --body 1
```

Keep the same query/options so the selected index refers to the same result set.

### 3. Widen Searches Deliberately

If no result appears:

1. Check spelling, accents, names, and domains.
2. Increase `--days`.
3. Try a sender/domain keyword.
4. Add `--sent` if the message may be one you sent.

## Troubleshooting

- **Authentication failed**: confirm `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`, 2-Step Verification, and account policy.
- **IMAP disabled**: enable IMAP in Gmail settings or ask the Workspace admin.
- **App Password unavailable**: the account may use policy restrictions or passkey/security-key-only settings. Use OAuth or an approved connector.
- **Search is slow**: reduce `--days` or use a more specific keyword.
- **Agent says it searched but did not run a command**: reject the result. Mailbox search needs real tool output.

