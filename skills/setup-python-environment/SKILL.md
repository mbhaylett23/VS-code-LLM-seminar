---
name: setup-python-environment
description: Choose and verify the simplest workable Python setup from AGENTS.md, user coding comfort, project files, OS, and installed tools. Use when setting up Python in VS Code, deciding between no local Python, python.org, uv, venv, Conda/Miniforge/Anaconda, notebooks, or Codespaces, or when the user wants the agent to handle environment setup with minimal intervention.
metadata:
  category: setup
  tags: [python, vscode, conda, miniforge, miniconda, anaconda, uv, venv, notebooks, codespaces, beginner-setup]
  created: 2026-05-17
  updated: 2026-05-17
---

# Setup Python Environment

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

Python setup can swallow a workshop. This skill makes the agent read the workspace contract first, detect what is already installed, choose the least-complex route for the user's coding level and project needs, and verify a working interpreter in VS Code.

## Requirements

- **Works on**: Windows, macOS, Linux, WSL, Codespaces, and VS Code-style workspaces.
- **Required applications**: VS Code or a compatible editor for interpreter selection; Python/Conda/uv only if the chosen track needs them.
- **Python packages**: None required to run the skill. Project packages are installed only after reading `AGENTS.md` permission boundaries.
- **Account/API requirements**: Codespaces requires GitHub access if used as the fallback path.
- **Privacy/safety warning**: This skill may inspect local paths and installed tools. It must ask before installing software, changing PATH/shell profiles, editing VS Code settings, or modifying environments unless `AGENTS.md` explicitly permits it.
- **Verification command**: At minimum, run a Python version/executable check from the chosen interpreter; run project tests or notebook kernel checks when relevant.

## When to use

- The user asks to get Python running for a project, workshop, notebook, script, data analysis, or VS Code.
- The user is unsure whether they need Python, `uv`, virtual environments, Conda, Miniforge, Miniconda, Anaconda, notebooks, or Codespaces.
- `AGENTS.md` already records the user's coding comfort level and package-management boundaries.
- An agent needs to set up enough Python tooling to run a project with minimal user intervention.

## Safety rule

Minimal intervention does not mean silent system changes.

Allowed without asking:

- read `AGENTS.md`, README/setup files, and environment files
- inspect installed commands and versions
- identify candidate setup tracks
- run non-mutating verification commands

Ask or require explicit approval before:

- installing Python, Conda, Miniforge, Miniconda, Anaconda, `uv`, VS Code extensions, or system packages
- changing PATH, shell profiles, app execution aliases, or global defaults
- installing packages into any environment
- creating, deleting, or modifying environments unless `AGENTS.md` explicitly allows the agent to manage packages/environments
- editing `.vscode/settings.json`, `AGENTS.md`, or project setup files

Never install into Conda `base` unless the user explicitly requests it after warning them.

## Steps

### 1. Read the workspace contract first

Read, in order if present:

```text
AGENTS.md
README.md
README.*
docs/setup*
environment.yml
environment.yaml
requirements.txt
pyproject.toml
uv.lock
.python-version
*.ipynb
```

Extract:

- coding comfort level
- whether the user wants beginner-friendly explanations
- whether the agent may manage packages/environments or must ask first
- source-of-truth setup files
- safety/privacy boundaries
- whether the project needs scripts, notebooks, scientific/data packages, web apps, or only Markdown/workspace memory

If coding comfort or package-management permission is missing, ask only the missing high-impact questions:

```text
1. Do you want the simplest path that works, or do you already prefer Python/uv/Conda/Anaconda?
2. Are you comfortable with terminal commands: none, basic copy-paste, or confident?
3. May I create environments and install packages, or should I propose commands first?
```

### 2. Inspect what is already installed

Windows PowerShell:

```powershell
Get-Command python, py, python3, conda, mamba, micromamba, uv, code -ErrorAction SilentlyContinue |
  Select-Object Name,Source

python --version
py --version
conda --version
uv --version
code --version
```

macOS/Linux/Git Bash/WSL:

```bash
for cmd in python3 python conda mamba micromamba uv code; do
  command -v "$cmd" >/dev/null 2>&1 && printf "%s -> %s\n" "$cmd" "$(command -v "$cmd")"
done

python3 --version || true
python --version || true
conda --version || true
uv --version || true
code --version || true
```

If a command is missing, record it as missing. Do not treat missing commands as fatal until the decision step.

### 3. Choose the least-complex working track

| Situation | Recommended track |
|---|---|
| User only needs to learn `AGENTS.md`, skills, Markdown memory, or project organization | No local Python required; use VS Code + LLM extension |
| Local setup is broken and the workshop must continue | Codespaces or presenter/shared environment, if available |
| Beginner, simple scripts, no heavy scientific packages | Existing working Python if present; otherwise official Python install + VS Code Python extension |
| Project has `pyproject.toml`, `uv.lock`, or `.python-version`, and user can tolerate a modern CLI | Use `uv` if already installed; ask before installing it |
| Project has `environment.yml` / `environment.yaml` | Use Conda/Mamba/Micromamba; create/update a named env from the file |
| Scientific/data/notebook stack with NumPy/SciPy/Pandas/PyTorch/compiled dependencies | Prefer Miniforge or Miniconda/Conda env; avoid full Anaconda unless already installed |
| User already uses Anaconda Navigator and is low-comfort | Use existing Anaconda/Navigator path rather than forcing a CLI migration |
| No local install allowed or machine is locked down | Codespaces, remote machine, or read-only participation |

Prefer existing working tools over installing new ones. Prefer project-local or named environments over global installs.

### 4. Build the smallest environment needed

If no packages are needed:

```powershell
python -c "print('Python is working')"
```

If a simple project-local virtual environment is appropriate and the user/AGENTS allows it:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.version)"
```

On macOS/Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -c "import sys; print(sys.executable); print(sys.version)"
```

If Conda is appropriate, create a named env only after approval or explicit `AGENTS.md` permission:

```powershell
conda create -n <project-env> -c conda-forge python=3.12 -y
conda run -n <project-env> python -c "import sys; print(sys.executable); print(sys.version)"
```

If `environment.yml` is the source of truth:

```powershell
conda env create -f environment.yml
conda env list
```

If `uv` is appropriate and already installed:

```powershell
uv python list
uv sync
uv run python -c "import sys; print(sys.executable); print(sys.version)"
```

If notebooks are required, verify a kernel is available:

```powershell
python -c "import ipykernel; print('ipykernel ok')"
```

Install `ipykernel` only according to the package-management permission in `AGENTS.md`.

### 5. Connect VS Code to the interpreter

If the VS Code CLI is available, list extensions:

```powershell
code --list-extensions
```

Check for:

```text
ms-python.python
ms-toolsai.jupyter
```

If missing, ask before installing:

```powershell
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
```

Tell the user how to select the interpreter:

```text
Ctrl+Shift+P -> Python: Select Interpreter -> choose the .venv / Conda / uv interpreter for this workspace.
```

Only edit `.vscode/settings.json` if the user or `AGENTS.md` explicitly allows workspace config edits.

### 6. Verify with real project evidence

Run the smallest meaningful proof:

- Python version command
- import check for required packages
- project test command if present
- notebook kernel import if notebooks matter
- one tiny script if no tests exist

Examples:

```powershell
python -c "import sys; print(sys.executable); print(sys.version)"
python -m pytest
python -m unittest discover
```

Do not say setup is done unless a verification command succeeds.

### 7. Report and optionally update project instructions

Report:

- files read
- coding comfort and package policy inferred from `AGENTS.md` or user answers
- installed tools detected
- chosen track and why
- commands run
- interpreter path selected
- packages/envs created or changed
- verification result
- blockers or manual steps left

If `AGENTS.md` lacks the final environment rule, propose a short patch such as:

```text
Python setup: use the `<env-name>` Conda environment / `.venv` / uv-managed environment.
Package policy: the agent may/may not install packages without asking.
Verification: run `<command>` before saying work is complete.
```

## Pitfalls

- **Skipping `AGENTS.md`**: the setup path depends on user comfort and permission boundaries.
- **Over-installing**: many participants only need VS Code and the LLM extension; do not make Python the price of admission.
- **Forcing Conda on beginners**: use Conda when scientific/compiled dependencies justify it, not by habit.
- **Ignoring existing Anaconda users**: if Anaconda already works for a low-comfort user, use it rather than forcing a migration.
- **Installing into `base`**: create a named env instead.
- **Trusting `python` on Windows without checking**: it may be a Microsoft Store alias. Check `py`, `python`, and the executable path.
- **Claiming VS Code is configured without selecting/verifying the interpreter**: run an actual command from the selected environment.

## Source links to check when installing

- VS Code Python environments: `https://code.visualstudio.com/docs/python/environments`
- Microsoft Python on Windows: `https://learn.microsoft.com/windows/python/get-started/python-for-scripting`
- Python on Windows: `https://docs.python.org/3/using/windows.html`
- Conda getting started: `https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html`
- Miniforge: `https://conda-forge.org/download/`
- uv Python versions: `https://docs.astral.sh/uv/concepts/python-versions/`
- GitHub Codespaces: `https://docs.github.com/en/codespaces/about-codespaces/codespaces-features`
