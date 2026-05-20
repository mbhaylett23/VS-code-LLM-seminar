---
name: publish-skills-to-github
description: Publish selected local skill bundles to a public GitHub skills repository after sanitization, without letting GitHub copies overwrite private/local skills. Use when sharing a skill publicly, updating this seminar repo, preparing a colleague-facing skill, or checking that a public skill contains no private information and no conda-only assumptions.
metadata:
  category: infrastructure
  tags: [skills, github, publishing, public-copy, sanitization, fail-fast]
  created: 2026-05-20
  updated: 2026-05-20
---

# Publish Skills To GitHub

## Why This Skill Exists

Public skill repositories should contain reusable, sanitized teaching copies,
not live private working files. The failure modes are publishing private
information, making a public skill depend on private infrastructure, assuming
the user has conda, or accidentally copying a public GitHub version back over a
local canonical skill.

## Publication Boundary

Default direction:

```text
private/local skill -> copy -> sanitize -> public GitHub skill
```

Do not reverse that direction unless the user explicitly asks to import a public
GitHub skill back into their private/local skill library.

This repository publishes public skills under:

```text
skills/<skill-name>/
```

Remote:

```text
https://github.com/mbhaylett23/VS-code-LLM-seminar
```

## Requirements

- Git must be installed and authenticated for the target GitHub repository.
- The target repo must have a clean working tree or only changes belonging to
  the current publication task.
- The public copy must pass sanitization and verification checks before commit.
- If the skill needs Python packages, its public instructions must include a
  standard Python `venv`/`pip` route. Conda may be included as an optional route,
  but must not be the only route.

## Stop Conditions

- `wrong_repo`: the remote is not the expected GitHub skills repository.
- `dirty_public_repo`: unrelated uncommitted changes are present.
- `private_info_detected`: private paths, emails, usernames, hostnames, tokens,
  machine names, internal services, or private project assumptions are present.
- `local_overwrite_risk`: a step would copy GitHub content back into private
  local skills without explicit user request.
- `conda_assumption`: a public skill assumes conda is available and has no
  standard Python route.
- `verification_failed`: frontmatter, dependency gate, script compile, smoke
  test, or public-safety scan fails.

## Steps

### 1. Confirm What Is Being Published

Publish only the skills the user named or clearly approved. Do not bulk-publish
all local skills.

Check the target repo:

```powershell
git remote -v
git status --short --branch
```

Stop if the remote or working tree is not what you expect.

### 2. Copy As A Draft, Not A Sync

Copy the chosen skill into `skills/<skill-name>/` as a draft public artifact.
After copying, rewrite it for a general audience.

Do not use symlinks, submodules, live adapters, or automatic sync jobs between a
private skill library and the public repo.

### 3. Sanitize The Public Copy

Remove or rewrite:

- private absolute paths
- usernames, hostnames, machine names, drive names, cloud-sync paths
- private email addresses, student/participant data, credentials, API keys,
  tokens, passwords, account IDs, and hidden endpoints
- private memory systems, research corpora, email-agent workflows, or services a
  public user cannot reproduce
- links to sibling skills that are not present in the public repo
- any instruction that depends on "my machine", "my environment", or "my private
  workspace"

Run a scan with a deny list appropriate for the project, for example:

```powershell
rg -n "private|internal-only|api[_-]?key|secret|token|password|localhost:[0-9]+|[A-Za-z]:/" . -g "!*.git/**"
```

Some words such as `password` may be acceptable in safety instructions. Real
values, private paths, and private endpoints are blockers.

### 4. Remove Conda-Only Assumptions

For Python-based public skills, include a standard route:

Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install <packages>
.\.venv\Scripts\python.exe scripts/<tool>.py --check-deps
```

macOS/Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install <packages>
./.venv/bin/python scripts/<tool>.py --check-deps
```

Optional conda route:

```powershell
conda create -n <env> -c conda-forge python=3.12 <packages> -y
conda run -n <env> python scripts/<tool>.py --check-deps
```

If a non-Python system tool is required, such as Tesseract OCR, include
OS-specific install options where possible and make the dependency gate fail
loudly when it is missing.

### 5. Verify Before Commit

Minimum checks:

```powershell
Get-ChildItem -Recurse -Filter SKILL.md
git diff --check
git status --short --branch
```

For script-bearing skills:

```powershell
python -m py_compile "skills/<skill-name>/scripts/<script>.py"
```

Run each dependency gate and a small smoke test when feasible. Also test a safe
failure path when the skill is supposed to fail loudly.

### 6. Commit And Push

```powershell
git add -A
git commit -m "Add public <skill-name> skill"
git push origin main
```

Confirm the remote hash matches local `HEAD`:

```powershell
git ls-remote origin refs/heads/main
git rev-parse HEAD
```

### 7. Report Clearly

Final report should include:

- GitHub repo and commit hash.
- Which skills were published.
- Sanitization checks run.
- Dependency and smoke tests run.
- Whether any private/local skill was overwritten from GitHub.

Expected boundary statement:

```text
No private/local skill was overwritten from GitHub.
```

## Pitfalls

- **GitHub is not the private source of truth.** Treat it as a public copy target.
- **Conda-only instructions are not public-friendly.** Include venv/pip first,
  and conda as an option.
- **Private info is broader than secrets.** Paths, hostnames, emails, and
  unreplicable services can also make a skill unsafe or unusable.
- **A passing commit is not enough.** Verify the skill itself, especially
  dependency gates and stop conditions.

## Related Skills

- `../create-new-skill/SKILL.md` - write or update a skill before publishing.
- `../setup-python-environment/SKILL.md` - choose Python setup instructions for different user skill levels.
