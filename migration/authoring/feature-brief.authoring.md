# Feature Brief Authoring Guide

Intent
- Help humans and agents produce high-quality Feature Briefs using .github/ISSUE_TEMPLATE/feature-brief.yml.
- Reduce ambiguity, prevent scope creep, and standardize output so sub-issues can be generated cleanly.

When to use
- Before any substantial feature work starts. The Feature Brief is the single source of truth.
- Use this to fill out the template thoroughly; then derive maintainer and agent sub-issues from it.

Order of sources (use in this priority)
1) Product/context provided by the requester and linked docs
2) AGENTS.md (personas and scope boundaries)
3) .github/instructions/backend.instructions.md and infrastructure.instructions.md (guardrails)
4) Existing repository patterns and prior Feature Briefs
5) If anything is missing or uncertain → add to “Open Questions” and mark [tbd] items in the tasklist

Field-by-field guidance (cheat sheet)

Priority (1 highest, 5 lowest)
- Pick intentionally. Lower number means higher priority.
- Note: in the template, dropdown defaults are 0-based indexes; we set default: 4 which selects the value "5". Override when necessary.

Rationale & Goals
- One concise paragraph: why this matters, and how we will recognize success (observable outcome).
- Avoid solution details; keep it at outcome/impact level.

Scope / Out of Scope
- Two explicit lists to prevent scope creep. Keep items concrete (files, flows, integrations).
- Example:
  In scope:
  - Add trainer CRUD in GraphQL/API
  - DynamoDB schema and indexes for trainers
  Out of scope:
  - AuthN/AuthZ flows
  - Media upload, payments

API/UX Contracts (authoritative)
- Provide concrete, versionable contracts: GraphQL schema (types/queries/mutations), REST endpoints, payload examples, UX states.
- Use fenced code blocks for schemas/payloads and list error codes (e.g., 400/404/409/5xx).
- Keep breaking changes explicit; prefer additive changes.

Affected Modules / Files (authoritative map)
- Repo-relative paths. Avoid overly broad globs unless necessary.
- Include new files you expect to add and where they will live.
- This list drives sub-issue scoping and agent path constraints later.

Design Artifacts & References
- Link authoritative docs (Figma, ADRs, RFCs, AWS docs). Prefer durable links.

Work Segmentation Plan (Human vs Agent)
- Summarize split at a high level. Detailed assignment happens in the Sub-issue Index.

Open Questions
- List unknowns as Q: ... and move to Answered when resolved. Keep this as the canonical Q&A log.

Architectural Impact / Data Model Changes
- New services/modules, schema changes, indexes, migrations. Note cache or key shape changes.

Non-Functional Requirements
- Measurable targets (latency, throughput, reliability, security, accessibility). Avoid vague terms.

Testing Strategy
- What to test and how: unit, integration, e2e, performance, and security. Include coverage goals or critical scenarios.

Known Risks & Mitigations
- List 2–5 realistic risks, each with a concrete mitigation/plan.

Dependencies & Blockers
- Link issues/tickets and external dependencies; note sequencing constraints.

Success Metrics & Observability
- Core metric(s) and how you’ll observe them (dashboards, logs, alerts, analytics events).

Rollout / Flags / Migration
- Feature flags, staged rollout plan, and any data migrations (expand → migrate → contract).

Rollback Plan
- Concrete, safe steps to revert (disable flags, revert schema, clear caches, manual steps).

Acceptance Criteria (feature-level only)
- 5–8 concise, testable checkboxes. Do not copy sub-issue AC here.

Sub-issue Index (tasklist)
- Use short, atomic stubs; don’t write full acceptance criteria or file-level details yet.
- For each stub include:
  - Title: one action + one object
  - Persona: [human] or [agent] (+ backend / infra)
  - Parseable prefix pattern: - [ ] [human] ..., - [ ] [agent] ..., or - [ ] [tbd] ...
  - Use [tbd] items for unresolved design decisions or risky areas needing a maintainer task.
  - Modify paths: 2–5 directory globs (avoid specific files at this stage unless unavoidable).
    - Exception: include a specific file only if it is the sole focal point (e.g., a single schema file)
  - DoD outline: 1–3 concise bullets (outcome-focused).
  - Depends on / Blocks: issue numbers or “tbd” (replace with links in phase 2).
  - Atomicity: each stub should be feasible as one PR.
- Example:
  - [ ] [human] Design DynamoDB access patterns (backend)
    - Modify: data-access/**, services/** 
    - DoD: access pattern header comments; optimistic concurrency approach chosen
    - Depends on: #123 § API/UX Contracts
  - [ ] [agent] Implement Trainer CRUD resolvers (backend)
    - Modify: resolvers/trainers/**, services/trainers/**, data-access/trainers/**, tests/resolvers/trainers/**
    - DoD: CRUD resolvers implemented; unit + integration tests passing
    - Depends on: design task above
  - [ ] [tbd] Decide pagination model for listings
    - DoD: choose connection vs offset pagination; define max page size
    - Blocks: CRUD list endpoints
- This list is a draft for phase 1. Detailed sub-issues are created in phase 2.
- Draft 5–9 stubs max in phase 1: enough to expose structure, sequencing, and risks without over-specifying.
- If a stub needs heavy design, make it a [human] maintainer task rather than forcing early agent details.
- In phase 2: create actual issues for each stub using the proper template and replace these lines with linked issue references.

Formatting rules
- Use code blocks for contracts (schemas/payloads) and keep examples minimal but representative.
- Paths must be repo-relative (e.g., resolvers/trainers/listTrainers.ts) and avoid src/** unless necessary.
- Prefer numbered lists and short bullets over prose walls.

Don’ts
- Don’t introduce infra changes here without approval; defer to infra sub-issues.
- Don’t invent data models that contradict guardrails or existing patterns.
- Don’t leave critical fields blank—move uncertainty to Open Questions and use [tbd] in tasklist.

Quality checklist before submitting
- Contracts compile conceptually (types/fields consistent with guardrails).
- NFRs are measurable; acceptance criteria are testable.
- Affected paths exist or are planned for creation; segmentation is clear.
- No secrets or PII appear in examples/logging guidance.
- Tasklist items are atomic and labeled with [human]/[agent]/[tbd].

Example skeleton (trim as needed)

Rationale & Goals
- …

Scope / Out of Scope
- In: …
- Out: …

API/UX Contracts
```graphql
# key types/queries/mutations
```

Affected Modules / Files
- resolvers/trainers/**
- services/trainers.service.ts
- data-access/trainers/**

NFR
- P95 ≤ 100ms for single-trainer lookup

Testing Strategy
- Unit: 95% service/resolvers; Integration: CRUD vs local DB; Perf: list 1k items

Risks & Mitigations
- Risk: … Mitigation: …

Acceptance Criteria
- [ ] …

Sub-issue Index
- [ ] [human] …
  - Modify: …
  - DoD: …
  - Depends on: …
- [ ] [agent] …
  - Modify: …
  - DoD: …
  - Depends on: …      
- [ ] [tbd] …
  - DoD: …
  - Blocks: …
