# ProjectPulse Memory Hub Architecture

Public implementation blueprint for a multi-machine LLM memory system.

This document is a sanitized teaching architecture. It is designed so another LLM, on another person's computer, can implement the pattern without needing access to any private ProjectPulse infrastructure.

## Design Goal

Build durable memory for LLM-assisted work across multiple machines.

The system should preserve:

- what happened in prior sessions
- which workspace the work belonged to
- decisions, claims, summaries, and next actions
- enough provenance to audit where a memory came from
- enough structure to rebuild search indexes, wiki pages, dashboards, or vector stores later

The core rule:

```text
The accepted event log is the source of truth.
Everything else is a projection.
```

## Non-Goals

Do not build the first version around:

- a vector database as the canonical store
- a Markdown wiki as the canonical store
- a dashboard as the canonical store
- one shared SQLite file edited by every machine
- browser/chat history copied manually between computers

Those can all be useful projections, but they should be rebuildable from the accepted event log.

## Architecture Overview

```text
LLM host / editor / CLI
        |
        v
capture adapter
        |
        v
local event store + outbox
        |
        v
sync client
        |
        v
Memory Hub API
        |
        v
canonical accepted event log
        |
        +--> summary projection
        +--> full-text search projection
        +--> vector projection
        +--> graph projection
        +--> Markdown/wiki projection
        +--> dashboard projection
```

Each machine writes locally first. A background sync process pushes local events to the hub and pulls accepted events from the hub. The hub validates identity, event hashes, schema versions, and ordering before accepting events.

## Component Responsibilities

### 1. Capture Adapter

The capture adapter turns local LLM activity into structured events.

Examples of capture inputs:

- chat transcript files
- editor extension session files
- CLI session logs
- explicit commands such as `save_session`
- manual event capture for decisions or skill changes

The capture adapter should:

- detect new local session material
- extract stable metadata
- create events
- write events to the local store
- mark capture checkpoints only after events are safely persisted

It should not:

- treat model memory as ground truth
- skip events silently because parsing failed
- overwrite previously captured material without recording why

### 2. Local Event Store

Every machine has its own local durable store.

Recommended first implementation:

```text
memory_hub/
  local/
    events.sqlite
    outbox.sqlite
    checkpoints.sqlite
```

SQLite is enough for the local store. Avoid sharing one live SQLite database across cloud drives between machines.

The local store should contain:

- local events waiting to sync
- accepted events pulled from the hub
- capture checkpoints
- push/pull cursors
- local projection state

### 3. Outbox

The outbox is the reliability boundary between local capture and remote sync.

An event should be placed in the outbox before the agent claims it has been saved to multi-machine memory.

Each outbox row should track:

- event ID
- payload
- payload hash
- target hub URL or profile name
- status: `pending`, `accepted`, `rejected`, `retry`
- attempt count
- last error
- timestamps

### 4. Sync Client

The sync client is a background process or manual command.

It should:

- push pending outbox events
- pull accepted events since the last hub watermark
- write pulled events to the local store
- update cursors only after durable writes
- back off on network failures
- never drop rejected events without recording the rejection reason

Simple command shape:

```bash
python -m memory_hub sync --once
python -m memory_hub sync --watch
python -m memory_hub status
```

### 5. Memory Hub API

The hub is the authority for accepted events.

It should:

- authenticate replicas
- reject unregistered replicas
- reject spoofed replica IDs
- recompute payload hashes server-side
- validate schemas
- assign a monotonic hub watermark
- store accepted events immutably
- expose pull endpoints for replicas
- expose read endpoints for projections

It should not:

- trust client-supplied identity blindly
- let one replica write events as another replica
- treat vector/graph/wiki state as canonical

### 6. Canonical Event Log

The accepted event log is append-only.

Every accepted event should have:

```yaml
event_id: evt_01HXYZ...
replica_id: replica_laptop_a
created_at: "2026-05-18T12:00:00Z"
received_at: "2026-05-18T12:00:03Z"
actor: "codex"
workspace_key: "example_project"
event_type: "session_summary"
entity_id: "session:abc123"
schema_version: 1
payload_hash: "sha256:..."
payload:
  summary: "Implemented feature X and ran test Y."
  messages:
    - role: user
      text: "Please fix the failing test."
    - role: assistant
      text: "Patched parser.py and reran pytest."
```

The hub may store the event payload as JSON, but it should also index the fields needed for filtering:

- `event_id`
- `replica_id`
- `workspace_key`
- `event_type`
- `entity_id`
- `created_at`
- `received_at`
- `hub_watermark`

### 7. Projections

Projections are derived views. They can be deleted and rebuilt.

Useful projections:

- current workspace summary
- recent sessions
- full-text search
- semantic/vector search
- entity graph
- decision log
- next action list
- Markdown wiki
- dashboard

Each projection should track its own cursor:

```yaml
projection_name: fts_search
last_hub_watermark: 12345
rebuilt_at: "2026-05-18T12:00:00Z"
schema_version: 1
```

If a projection breaks, rebuild it from the event log instead of patching it as if it were the source of truth.

## Workspace Identity

The same project may live at different local paths on different computers.

Do not use raw absolute paths as workspace identity.

Use a stable `workspace_key`.

Recommended identity order:

1. explicit workspace config value
2. git remote URL normalized to a stable key
3. project manifest ID
4. folder name as a last resort

Local path aliases can map different machine paths to the same logical root:

```yaml
path_aliases:
  research_drive:
    - "<machine-a-research-root>"
    - "<machine-b-research-root>"
  cloud_drive:
    - "<machine-a-cloud-root>"
    - "<machine-b-cloud-root>"
```

Captured events should include:

```yaml
workspace_key: "paper_draft"
path_alias: "cloud_drive"
path_relative: "Projects/paper_draft"
cwd_original: "redacted-or-local-only"
```

For public or shared systems, avoid storing raw local paths unless the user explicitly accepts that privacy tradeoff.

## Replica Identity

A replica is one machine or one installation that can emit events.

Example:

```yaml
replica_id: replica_laptop_a
display_name: "Laptop A"
status: active
created_at: "2026-05-18T12:00:00Z"
```

The hub should derive the authenticated replica identity from a token or key. The client can include `replica_id` for clarity, but the server must verify that it matches the authenticated identity.

Do not commit replica tokens to git.

Use environment variables or an OS keychain:

```bash
MEMORY_HUB_URL="<memory-hub-url>"
MEMORY_HUB_REPLICA_TOKEN="stored-outside-git"
MEMORY_HUB_REPLICA_ID="replica_laptop_a"
```

## Event Types

Start with a small schema set.

### `session_summary`

Use at the end of a work session.

```yaml
event_type: session_summary
entity_id: session:abc123
payload:
  summary: "Short summary of work completed."
  messages:
    - role: user
      text: "Original request or important user instruction."
    - role: assistant
      text: "Work completed, files changed, verification run."
  files_changed:
    - "src/example.py"
  verification:
    - "pytest"
```

### `decision`

Use for durable design decisions.

```yaml
event_type: decision
entity_id: decision:event_log_is_canonical
payload:
  decision: "The event log is the source of truth."
  rationale: "Projections can be rebuilt; cross-machine state needs one authority."
  alternatives_considered:
    - "Shared SQLite file"
    - "Vector store as source of truth"
  status: active
```

### `claim`

Use for verified facts that future sessions may rely on.

```yaml
event_type: claim
entity_id: claim:project_deadline
payload:
  subject: "project"
  predicate: "deadline"
  value: "2026-06-01"
  source: "local file or official URL"
  status: verified
```

### `next_action`

Use for durable todo items.

```yaml
event_type: next_action
entity_id: action:run_final_tests
payload:
  action: "Run final tests before release."
  owner: "user"
  status: open
```

### `skill_event`

Use when a reusable procedure is created or changed.

```yaml
event_type: skill_event
entity_id: skill:systematic-debugging
payload:
  action: created
  skill_name: systematic-debugging
  rationale: "Repeated debugging workflow should be reusable."
```

## Minimal Database Schema

Hub database:

```sql
CREATE TABLE replicas (
  replica_id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  token_hash TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE events (
  hub_watermark INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id TEXT NOT NULL UNIQUE,
  replica_id TEXT NOT NULL REFERENCES replicas(replica_id),
  created_at TEXT NOT NULL,
  received_at TEXT NOT NULL,
  actor TEXT NOT NULL,
  workspace_key TEXT NOT NULL,
  event_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  schema_version INTEGER NOT NULL,
  payload_hash TEXT NOT NULL,
  payload_json TEXT NOT NULL
);

CREATE INDEX idx_events_workspace ON events(workspace_key, hub_watermark);
CREATE INDEX idx_events_type ON events(event_type, hub_watermark);
CREATE INDEX idx_events_entity ON events(entity_id, hub_watermark);
```

Local database:

```sql
CREATE TABLE local_events (
  event_id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  workspace_key TEXT NOT NULL,
  event_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  payload_hash TEXT NOT NULL,
  event_json TEXT NOT NULL,
  sync_status TEXT NOT NULL DEFAULT 'pending',
  last_error TEXT
);

CREATE TABLE accepted_events (
  hub_watermark INTEGER PRIMARY KEY,
  event_id TEXT NOT NULL UNIQUE,
  event_json TEXT NOT NULL
);

CREATE TABLE cursors (
  name TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

## API Contract

Minimum endpoints:

```text
GET  /health
POST /v1/events/push
GET  /v1/events/pull?since=<hub_watermark>&limit=<n>
GET  /v1/events/<event_id>
GET  /v1/workspaces/<workspace_key>/snapshot
```

### Push Request

```json
{
  "replica_id": "replica_laptop_a",
  "last_seen_hub_watermark": 42,
  "events": [
    {
      "event_id": "evt_01HXYZ",
      "replica_id": "replica_laptop_a",
      "created_at": "2026-05-18T12:00:00Z",
      "actor": "codex",
      "workspace_key": "example_project",
      "event_type": "session_summary",
      "entity_id": "session:abc123",
      "schema_version": 1,
      "payload_hash": "sha256:...",
      "payload": {}
    }
  ]
}
```

### Push Response

```json
{
  "accepted": ["evt_01HXYZ"],
  "rejected": [],
  "hub_watermark": 43
}
```

### Pull Response

```json
{
  "events": [
    {
      "hub_watermark": 43,
      "event_id": "evt_01HXYZ",
      "event": {}
    }
  ],
  "next_since": 43
}
```

## Sync Algorithms

### Capture

```text
for each new transcript/session file:
    read source
    extract workspace_key, actor, messages, files changed, verification
    build event
    compute payload_hash
    write event to local_events with sync_status='pending'
    update capture checkpoint after write succeeds
```

### Push

```text
load pending local_events ordered by created_at
send batch to /v1/events/push
for accepted events:
    mark local sync_status='accepted'
for rejected events:
    mark sync_status='rejected' and store reason
on network failure:
    leave events pending or retry
```

### Pull

```text
load last_pull_watermark from cursors
GET /v1/events/pull?since=last_pull_watermark
write events to accepted_events in one transaction
advance last_pull_watermark only after commit
run projections from old watermark to new watermark
```

### Projection Rebuild

```text
clear projection tables
set projection cursor to 0
replay accepted_events ordered by hub_watermark
update projection rows
advance projection cursor after each committed batch
```

## Startup Context

At the start of an LLM session, the agent should load a bounded snapshot.

Suggested command:

```bash
python -m memory_hub startup --workspace example_project
```

The snapshot should include:

- workspace summary
- recent sessions
- active decisions
- open next actions
- relevant verified claims
- relevant skills or project instructions
- staleness warnings

Keep this bounded. A memory system should retrieve useful context, not paste the entire database into the chat.

## End-Of-Session Save

At the end of a session, the agent should create a `session_summary` event.

Suggested command:

```bash
python -m memory_hub save-session \
  --workspace example_project \
  --summary "Implemented X and verified Y." \
  --messages "user: asked for X|assistant: changed files A and B, ran test Y"
```

Include:

- exact user request
- work completed
- files changed
- commands run
- tests or checks passed/failed
- blockers
- next steps

Do not include:

- passwords
- API keys
- private email bodies
- sensitive student/patient data
- unpublished confidential material unless the user explicitly wants local private memory to store it

## Multi-Machine Deployment

Recommended roles:

```text
Machine A: local capture + local store + sync client
Machine B: local capture + local store + sync client
Machine C: local capture + local store + sync client
Hub: authenticated API + canonical event log + projections
```

The hub can run on:

- a local always-on computer
- a small private server
- a NAS
- a cloud VM
- a single laptop for a one-person setup

For a first implementation:

1. Run the hub locally on one machine.
2. Register one replica.
3. Capture and save sessions locally.
4. Add a second replica.
5. Add push/pull sync.
6. Add projections.
7. Add vector or graph search only after event sync is reliable.

## Security And Privacy

Required:

- store tokens outside git
- hash tokens server-side
- authenticate every push
- derive replica identity from auth
- validate payload hashes server-side
- log rejections
- provide a redaction layer before storing transcripts
- exclude secrets by pattern

Recommended redaction patterns:

```text
API keys
passwords
bearer tokens
private SSH keys
OAuth refresh tokens
student IDs
patient identifiers
private email bodies
```

For sensitive teams, add:

- encryption at rest
- per-workspace access control
- audit logs
- retention policies
- manual export/delete commands

## Implementation Phases

### Phase 1: Local Event Store

Deliver:

- event schema
- local SQLite store
- `save-session`
- `startup`
- basic full-text search

Acceptance test:

- save a session
- close the terminal
- run startup
- see the saved summary

### Phase 2: Hub API

Deliver:

- `replicas` table
- token auth
- `/health`
- `/v1/events/push`
- `/v1/events/pull`
- server-side payload-hash verification

Acceptance test:

- unregistered replica is rejected
- spoofed replica ID is rejected
- bad payload hash is rejected
- valid event is accepted and assigned a watermark

### Phase 3: Cross-Machine Sync

Deliver:

- outbox
- push command
- pull command
- sync cursor
- retry behavior

Acceptance test:

- Machine A saves event
- Machine A pushes
- Machine B pulls
- Machine B startup includes Machine A's event

### Phase 4: Projections

Deliver:

- recent sessions projection
- active decisions projection
- open actions projection
- Markdown/wiki projection
- dashboard or CLI status

Acceptance test:

- delete projection database
- rebuild from event log
- output matches previous projection

### Phase 5: Semantic And Graph Retrieval

Deliver:

- vector projection built from accepted events
- entity/relationship projection built from accepted events
- rebuild command

Acceptance test:

- delete vector/graph store
- rebuild from event log
- recall still works

## Tests Another LLM Should Implement

Core tests:

- event hash recomputation rejects tampering
- duplicate event IDs are idempotent or rejected consistently
- unregistered replicas cannot push
- authenticated replica cannot spoof another replica ID
- pull returns events in watermark order
- cursors advance only after durable commit
- projection rebuild produces deterministic output
- startup snapshot respects token budget
- redaction catches sample secrets before storage

Failure tests:

- network unavailable during push
- hub unavailable during startup
- partial batch accepted/rejected
- corrupt local event row
- invalid schema version
- two machines emit events for the same workspace concurrently

## Minimal File Layout

```text
memory_hub/
  __init__.py
  cli.py
  config.py
  events.py
  local_store.py
  sync.py
  redaction.py
  projections/
    recent_sessions.py
    decisions.py
    search.py
    wiki.py
  server/
    app.py
    auth.py
    db.py
    schemas.py
  tests/
    test_events.py
    test_auth.py
    test_sync.py
    test_projections.py
```

## Implementation Prompt For Another LLM

Use this prompt with another LLM in a fresh repo:

```text
Implement the Memory Hub architecture described in docs/MEMORY_HUB_ARCHITECTURE.md.

Start with Phase 1 and Phase 2 only:
- local SQLite event store
- event schema
- save-session CLI
- startup CLI
- FastAPI hub with /health, /v1/events/push, and /v1/events/pull
- replica token authentication
- server-side payload-hash verification
- tests for auth, hash validation, event acceptance, and pull ordering

Do not implement vector search, graph search, or dashboards until the event log and sync tests pass.
Do not store secrets in the repo.
Do not use machine-specific absolute paths.
Keep all configuration in environment variables or a local ignored config file.
```

## Final Architectural Invariants

- Event log first.
- Local write before network sync.
- Authenticated replica identity.
- Server-side hash verification.
- Workspace identity independent of local absolute paths.
- Projections are disposable.
- Vector, graph, wiki, and dashboard layers are rebuildable.
- Secrets never go in git.
- Startup retrieves bounded context.
- End-of-session save records what changed and how it was verified.
