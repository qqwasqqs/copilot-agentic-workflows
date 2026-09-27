# Feature Brief field guide

Canonical field-by-field guidance for the Feature Brief. Field ids below match
the bundled default contract; when a target repository supplies its own Feature
Brief form, map this guidance onto **its** labels and drop anything it has no
field for.

## rationale — Rationale & Goals

One concise paragraph: why this matters and how success will be recognized as an
observable outcome. Keep solution detail out; this is impact level.

## scope — Scope / Out of Scope

Two explicit lists. Concrete items: flows, integrations, surfaces. Out of Scope
is the scope-creep fence and is as important as In Scope.

## contracts — API/UX Contracts (authoritative)

Concrete and versionable. Include operations or endpoints, request and response
payload examples in fenced code blocks, error conditions and their meaning, and
versioning implications. For user interfaces, cover idle, loading, success,
empty, and error states plus accessibility expectations. Prefer additive
changes; state breaking changes explicitly.

## affected — Affected Modules / Files

Repository-relative paths that drive sub-issue scoping and agent path limits.
Use narrow globs; a broad catch-all needs a written justification. List planned
new files separately from existing ones.

## artifacts — Design Artifacts & References

Durable links only: designs, specifications, architecture documents, ADRs,
related issues and pull requests.

## segmentation — Work Segmentation Plan

High-level split between human-owned and agent-suitable work, with the reason.
Per-item assignment happens in the Sub-Issue Index, not here.

## open_questions — Open Questions

The canonical question log. Every `[tbd]` elsewhere in the brief has an entry
here. Resolved items move to an Answered subsection with the answer, preserving
the decision history.

## arch_impact — Architectural Impact / Data Model Changes

New or changed components, entities, relationships, indexes, caching and key
shapes, and migrations. Name the migration strategy — typically expand, migrate,
contract — and any irreversible step.

## nfr — Non-Functional Requirements

Measurable targets: latency, throughput, scalability, reliability, availability,
security, privacy, accessibility. At least one must be measurable. Vague
adjectives are not requirements.

## testing — Testing Strategy

What is tested and how: unit, integration, end-to-end, performance, security.
Name the key scenarios and edge cases and where coverage matters most, rather
than only quoting a percentage.

## risks — Known Risks & Mitigations

2-5 realistic risks, each with a concrete mitigation or fallback. Prefer risks
specific to this feature over generic engineering risks.

## dependencies — Dependencies & Blockers

Internal and external dependencies — services, teams, pending decisions — plus
sequencing constraints. Link issues where they exist.

## metrics — Success Metrics & Observability

The metric that determines whether the feature worked, and the signals used to
observe it: dashboards, alerts, logs, events. Tie back to the goals in
`rationale`.

## rollout — Rollout / Flags / Migration

Flags and their defaults, the staged rollout plan, the signals watched at each
stage, and any data or configuration migration.

## rollback — Rollback Plan

Concrete steps to disable or revert, in order. Explicitly call out anything that
cannot be undone.

## acceptance — Acceptance Criteria

5-8 feature-level, testable, outcome-focused checkboxes describing what must be
true when the feature is done. Not implementation steps, and not a copy of
sub-issue criteria.

## tasklist — Sub-issue Index

Draft stubs only, 5-9 of them. Format:

```markdown
- [ ] [human] Decide the retention policy
  - Modify: <area>/**, <area>/**
  - DoD: policy chosen and documented; migration implications recorded
  - Depends on: #123 - API/UX Contracts
- [ ] [agent] Implement the export endpoint
  - Modify: <area>/**, tests/<area>/**
  - DoD: endpoint implemented; unit and integration tests pass
  - Depends on: the decision above
- [ ] [tbd] Resolve the pagination model
  - DoD: pagination style and maximum page size chosen
  - Blocks: the list endpoint work
```

The `[human]` / `[agent]` / `[tbd]` tag must begin the checkbox text so the
Sub-Issues Planner can parse it. Avoid code blocks inside the index.

## Quality checklist before submitting

- Contracts are internally consistent and honour the project's stated
  constraints.
- Non-functional requirements are measurable; acceptance criteria are testable.
- Affected paths exist or are explicitly planned; segmentation is clear.
- No secrets or personal data appear in examples or logging guidance.
- Every `[tbd]` has a matching open question.
- Stubs are atomic and correctly tagged.
- No unreplaced placeholder text remains in the title or body.
