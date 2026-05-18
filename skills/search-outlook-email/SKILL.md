---
name: search-outlook-email
description: Search local Outlook mail from VS Code on Windows using Classic Outlook COM automation. Use when the user wants to find Outlook messages by keyword, inspect sender/date/subject metadata, or extract a selected message body after confirming Classic Outlook is running.
metadata:
  category: email
  tags: [outlook, email, classic-outlook, com, windows, pywin32]
  created: 2026-05-18
  updated: 2026-05-18
---

# Search Outlook Email

## Why this skill exists

Outlook search from an agent is useful, but fragile: it only works through the Windows desktop Outlook COM object model, which means **Classic Outlook** must be installed and running. New Outlook is not enough for this workflow.

## Requirements

- Windows.
- Classic Outlook for Windows installed and signed in.
- Classic Outlook running as `OUTLOOK.EXE`.
- Python 3.
- `pywin32` installed in the Python environment used by VS Code.

Install `pywin32`:

```powershell
python -m pip install pywin32
```

If using Conda:

```powershell
conda install -c conda-forge pywin32
```

## Official Compatibility Note

Microsoft's feature comparison for new vs classic Outlook lists:

- COM add-ins: available in Classic Outlook, not supported in new Outlook.
- Outlook Object Model: available in Classic Outlook, not supported in new Outlook.

Source: https://support.microsoft.com/en-us/office/feature-comparison-between-new-outlook-and-classic-outlook-de453583-1e76-48bf-975a-2e9cd2ee16dd

## Safety And Privacy

- Search metadata first: date, sender, subject, folder.
- Do not print full bodies in a public setting unless the user explicitly approves.
- Never paste private messages into public slides, GitHub issues, or shared prompts.
- If Outlook is not available, say so. Do not pretend the mailbox was searched.

## Workflow

### 1. Verify Classic Outlook Is Running

Run:

```powershell
Get-Process OUTLOOK,olk -ErrorAction SilentlyContinue |
  Select-Object ProcessName,Id,Path
```

Interpretation:

- `OUTLOOK.EXE` = Classic Outlook. COM automation can use this.
- `olk.exe` = new Outlook. This is not enough for COM automation.

If only `olk.exe` appears, open **Classic Outlook** from the Start menu or Microsoft 365 Apps.

### 2. Verify Python Can Load COM Support

```powershell
python -c "import win32com.client; print('pywin32 ok')"
```

If that fails, install `pywin32` in the interpreter selected by VS Code.

### 3. Run A Metadata Search

From the repository root:

```powershell
python .\skills\search-outlook-email\scripts\outlook_search.py --days 30 --search "keyword" --max 10
```

Search Inbox and Sent Items:

```powershell
python .\skills\search-outlook-email\scripts\outlook_search.py --days 90 --search "keyword" --folder all --max 20
```

### 4. Pull A Selected Body

Only after the user confirms it is safe to view message content:

```powershell
python .\skills\search-outlook-email\scripts\outlook_search.py --days 30 --search "keyword" --body 1
```

Keep the same query/options so the selected index refers to the same result set.

## Troubleshooting

- **Only `olk.exe` is running**: open Classic Outlook. New Outlook does not expose the COM object model needed here.
- **`No module named win32com`**: install `pywin32` into the active Python environment.
- **COM connects but no messages appear**: wait for Outlook to finish syncing, then retry with a wider `--days`.
- **Agent says it searched but did not run a command**: reject the result. Mailbox search needs real tool output.
- **Corporate machine blocks COM**: use Outlook's built-in search manually, Microsoft Graph, or an approved institutional connector instead.

