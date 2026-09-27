# Agent Task Authoring Guide

Intent
- Help humans and agents create high-quality, atomic sub-issues using .github/ISSUE_TEMPLATE/agent-task.yml.
- Make tasks safe, scoped, and automatable so agents can execute confidently with minimal back-and-forth.

When to use
- For any work item intended for an AI agent (backend or infra) that is small and self-contained.
- Each agent task should map to a single PR whenever possible.

Relationship to the Feature Brief
- Every agent task must link a single main Feature Brief (the “Main Issue Link” field).
- Contracts, risks, NFRs, and success metrics flow down from the Feature Brief. Don’t redefine them; reference them.

Order of sources (use in this priority)
1) The linked Feature Brief and its references
2) AGENTS.md (persona selection and decision boundaries)
3) .github/instructions/backend.instructions.md or infrastructure.instructions.md (guardrails applied by path)
4) Existing repository patterns & prior sub-issues
5) If something is missing → add questions to the Feature Brief’s Open Questions and block or mark [tbd] as needed

Persona selection
- Prefer labels: agent:backend or agent:infra (and/or area:*).
- Fallback heuristics (if labels missing):
  - Backend if paths include functions/**, resolvers/**, services/**, data-access/**, graphql/**, appsync/**
  - Infra if paths include amplify/**, infra/**, cdk/**, stacks/**

Field-by-field guidance

Main Issue Link (required)
- Paste the Feature Brief URL or issue number. Use section anchors in Context/Links to reference exact specs (e.g., § API/UX Contracts).

Context / Links (required)
- Link to precise sections: contracts, NFRs, testing strategy.
- Include guardrails and AGENTS.md. Example:
  - Main spec: #123 § API/UX Contracts, § NFR
  - Guardrails: .github/instructions/backend.instructions.md
  - Personas: AGENTS.md

Affected Paths (Scope Gate) (required)
- Split into Modify (edit/create allowed) and Reference Only (read-only context).
- Keep Modify specific (4–8 globs/files). Avoid src/** unless necessary.
- Rule: Agent must ask before touching anything outside Modify; never change Reference Only files.
- Tip: Align with guardrails `applyTo` globs so the correct backend/infra instructions auto-apply.

Files / Symbols to Touch (Authoritative) (required)
- Bullet list with action per file: Add / Edit / Delete. Call out symbols to implement or update.
- This is the authoritative action list. If the agent needs more, it must ASK first.
- Minimal format example:
  - Edit: services/trainers.service.ts – add getTrainerByEmail()
  - Add: resolvers/trainers/listTrainers.ts – implement listTrainers()
  - Add: tests/resolvers/listTrainers.spec.ts – pagination & error cases
  - Edit: graphql/schema.graphql – add TrainerConnection + query
  Symbols:
  - TrainerService.getTrainerByEmail (new)
  - listTrainers resolver function
  - TrainerConnection type

Allowed vs Forbidden Changes (required)
- Enumerate a few allowed actions and several common forbidden ones to constrain blast radius.
- Typical forbidden: new deps, infra changes, global config edits, removing public APIs.

Contracts to Honor (required)
- Copy key invariants from the Feature Brief’s Contracts section: type names, error codes, pagination rules, and auth expectations.
- This prevents agents from drifting on public contracts.

Objective (Definition of Done) (required)
- 3–6 checkboxes. Testable, observable. Include instrumentation and constraints.

Technical Details (required)
- Constraints (perf, no new deps, DynamoDB no scans, conditional writes, etc.) and intentional side effects.

Observability Hooks (required)
- List logger, metrics, tracing changes. No PII in logs. Correlate with requestId.

Depends On / Blocks
- Link sub-issues that must precede or will be unblocked by this task.

Test Data & Verification Steps (required)
- Fixtures/seeds to reproduce locally; exact commands to run unit/integration tests; expected outcomes.

Expected Diff Size & PR Boundaries
- Choose Small/Medium/Large. Keep atomic. In PR Boundaries, state what’s included/excluded.

Security / Privacy Checks
- Acknowledge no secrets/PII in logs; input validation; authz checks; non-leaky errors; idempotency for writes.

Roll-forward Nature
- Select Additive vs Migration vs Risky. Migration/Risky tasks need rollback notes (usually a maintainer task).

Tests & Validation (required)
- Reiterate what must be covered: unit + integration; performance if applicable; all suites green.

First Response Structure (Agent Plan)
- The template includes a read-only markdown block with the required first response plan format.
- The agent must post that plan and wait for acknowledgment before any code changes.
- Any change outside Modify paths or beyond Files/Symbols must be explicitly proposed and approved.

Common pitfalls
- Missing label → persona misapplied. Add `agent:backend` or `agent:infra`.
- Over-broad Modify globs → agent wanders. Make them specific.
- Editing Reference Only files → breaks scope. Keep read-only unless approved.
- Silent schema changes → must be declared in Files/Symbols and Contracts to Honor.
- Adding new dependencies → forbidden unless explicitly allowed.

Quality checklist before submitting
- Main issue linked; Context includes precise sections.
- Modify vs Reference Only paths are clear and specific.
- Files/Symbols list is complete; deletions are rare and justified.
- Allowed/Forbidden constraints reflect this task; Contracts to Honor are copied in.
- Observability hooks defined; security/privacy checks acknowledged.
- Test data and commands included; expected results stated.
- Diff size marked; PR Boundaries define include/exclude.

Example skeleton (trim as needed)

Main Issue Link
- #123

Context / Links
- #123 § API/UX Contracts, § NFR
- .github/instructions/backend.instructions.md
- AGENTS.md

Affected Paths (Scope Gate)
Modify:
- resolvers/trainers/**
- services/trainers.service.ts
- data-access/trainers/**
Reference Only:
- graphql/schema.graphql

Files / Symbols to Touch
- Edit: services/trainers.service.ts – add listTrainers()
- Add: resolvers/trainers/listTrainers.ts – resolver
- Add: tests/resolvers/listTrainers.spec.ts – pagination tests
Symbols:
- TrainerService.listTrainers
- listTrainers resolver

Allowed vs Forbidden
- Allowed: add resolver, extend service, add tests
- Forbidden: new deps, infra edits, unrelated refactors

Contracts to Honor
- Types: Trainer, TrainerConnection
- Errors: 400 invalid input; 404 not found
- Pagination: nextToken

Objective (DoD)
- [ ] Resolver + service implemented
- [ ] Tests pass
- [ ] Metrics/tracing added

Technical Details
- No scans; queries with keys; strict TS

Observability Hooks
- trainer.list.success/failure; requestId in logs; tracing annotations

Depends On / Blocks
- Depends: none; Blocks: #124 (UI)

Test Data & Verification Steps
- Seed 3 trainers + 1 inactive; run npm test; expect nextToken when > limit

Diff Size & PR Boundaries
- Small; include resolver/service/tests; exclude infra/dep changes

Security / Privacy Checks
- No PII in logs; validation present; authz enforced

Roll-forward Nature
- Additive

Tests & Validation
- Unit + integration + perf smoke

References
- Feature Brief template: .github/ISSUE_TEMPLATE/feature-brief.yml
- Backend guardrails: .github/instructions/backend.instructions.md
- Infrastructure guardrails: .github/instructions/infrastructure.instructions.md
- Personas: AGENTS.md
