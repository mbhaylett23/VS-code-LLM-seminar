---
name: simple-wiki-memory
description: Use when creating or maintaining a simple Markdown wiki memory for a project, inspired by Karpathy's LLM Wiki pattern. The agent ingests raw sources, updates interlinked wiki pages, maintains index.md and log.md, answers questions from the wiki, and performs lightweight lint checks without requiring a vector database.
metadata:
  category: memory
  tags: [memory, markdown, wiki, llm-wiki, obsidian, project-context]
  created: 2026-05-18
  updated: 2026-05-18
---

# Simple Wiki Memory

## Why this skill exists

Chat disappears. A Markdown wiki persists. This skill teaches the agent to maintain a small project memory as files, so knowledge compounds across sessions without requiring a database or RAG stack.

The pattern is inspired by Andrej Karpathy's LLM Wiki idea:

```text
raw sources -> maintained Markdown wiki -> index/log -> future context
```

## Requirements

- No Python packages or external services are required.
- Works in any folder where the agent can read and edit Markdown.
- Optional: Obsidian, VS Code Markdown preview, or git history.
- Do not ingest private or sensitive sources into a public repository.

## Directory Layout

Use this layout unless the workspace already defines another one:

```text
memory/
  raw/           # source notes, transcripts, articles; agent reads but does not rewrite
  wiki/
    index.md    # content map of wiki pages
    log.md      # chronological activity log
    *.md        # topic, entity, source, and synthesis pages
```

## Source Of Truth

- `memory/raw/` is the source layer. Treat it as immutable unless the user explicitly asks to clean or rename a source file.
- `memory/wiki/` is the maintained memory layer. The agent may create and update these pages.
- `memory/wiki/index.md` is the navigation layer.
- `memory/wiki/log.md` is the audit trail.

Do not invent source facts. If a claim is not in a source or an existing wiki page, mark it as an inference or ask the user.

## Page Format

Use concise YAML frontmatter for wiki pages:

```markdown
---
title: Page Title
type: topic
updated: YYYY-MM-DD
sources: []
tags: []
---

# Page Title

## Summary

## Key Points

## Links

## Open Questions
```

Allowed `type` values: `topic`, `entity`, `source`, `synthesis`, `decision`, `question`.

## Workflow: Initialize

If `memory/wiki/index.md` or `memory/wiki/log.md` is missing:

1. Create the missing files.
2. Add a short description of the wiki purpose.
3. Add a first log entry.
4. Do not fabricate pages just to fill the wiki.

## Workflow: Ingest A Source

1. Read the source from `memory/raw/` or from a user-provided note.
2. Identify:
   - main topic
   - entities
   - decisions or claims
   - contradictions with existing wiki pages
   - open questions
3. Create or update one source page in `memory/wiki/`.
4. Update relevant topic/entity pages.
5. Add links between pages using relative Markdown links.
6. Update `memory/wiki/index.md`.
7. Append a dated entry to `memory/wiki/log.md`.
8. Report which pages changed and what remains uncertain.

## Workflow: Answer A Question

1. Read `memory/wiki/index.md` first.
2. Search wiki pages for relevant terms.
3. Read the most relevant pages.
4. Answer from the wiki, citing page links.
5. If the answer depends on raw sources, read and cite those too.
6. If the answer creates a useful synthesis, ask whether to save it as a wiki page.

## Workflow: Lint The Wiki

Periodically check for:

- orphan pages not listed in `index.md`
- pages listed in `index.md` that no longer exist
- missing backlinks between closely related pages
- stale claims superseded by newer sources
- contradictions that should be flagged
- pages with no sources
- important terms mentioned repeatedly but lacking a page

Return a short maintenance list before making broad edits.

## Rules

- Keep pages short enough to read.
- Prefer updating existing pages over creating near-duplicates.
- Preserve uncertainty and disagreements.
- Separate source facts from synthesis.
- Never delete or rename source files without user approval.
- Do not claim the wiki has been searched unless you actually read or searched it.
- For public seminar repos, use fake or non-sensitive examples only.
