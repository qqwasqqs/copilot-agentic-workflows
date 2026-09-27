---
name: ops-issue-authoring
description: Authors standalone operational, maintenance, and chore issues - triage against feature work, category selection, scope gating, backout planning, and rendering against the governing ops-task contract. Use for refactors, dependency upgrades, CI/CD, tooling, cleanup, documentation chores, and cost or reliability work that is not part of a Feature Brief.
---

# Ops issue authoring

Ops issues cover engineering upkeep that keeps the system healthy but does not
deliver new product behavior. They stand alone: no Feature Brief parent, no
sub-issue tree.

## Triage first

Route to the feature workflow instead when the request:

- adds or changes user-facing behavior or a public contract;
- needs a decomposition into multiple coordinated issues;
- carries product decisions or a rollout plan.

Route here when it is refactoring, dependency or runtime upgrades, CI/CD and
tooling, test infrastructure, observability plumbing, cleanup, cost or
reliability tuning, or a documentation chore.

Mixed requests are split: state the split and confirm it before authoring.
When it is genuinely borderline, ask; in autonomous mode choose, and record the
choice and its reason.

## Gather before drafting

Establish the rationale and the concrete trigger, the scope boundary, the
affected paths, the verification method, and the risk and backout. Ask focused
questions about what is actually missing — do not re-interview the user about
what they already said.

## Field guidance

Field ids match the bundled ops-task contract; when the target repository has
its own matching form, map onto its labels.

- **category** — pick the single closest one. If the work spans several, that is
  usually a sign it should be split.
- **related** — optional link to a feature or issue that motivated this work.
  Leave it empty rather than inventing a connection.
- **rationale** — the problem and its concrete cost: maintenance burden, risk,
  toil, spend, flakiness, or a deprecation deadline. Include the trigger, such
  as an advisory, an incident, or an end-of-life date. Avoid "good practice" as
  the whole justification.
- **scope** — In Scope and Out of Scope. Ops work sprawls without a fence.
- **steps** — an ordered, executable plan. Sequence anything with a
  compatibility window explicitly.
- **affected_paths** — narrow, repository-relative globs; separate paths that
  change from paths read for context.
- **deliverables** — the observable artifacts: merged changes, updated
  configuration, a new workflow, documentation, a dashboard.
- **risks** — what can break, who is affected, and the blast radius, including
  effects on consumers and running workloads.
- **rollback** — concrete revert steps, with irreversible steps called out. For
  upgrades, state how to pin back.
- **acceptance** — 3-6 testable checkboxes, including how success is verified in
  practice: a green pipeline, a benchmark, a clean scan.
- **links** — advisories, release notes, migration guides, incidents, dashboards.
- **effort** — a realistic estimate; if it exceeds a few days, consider
  splitting.

## Quality rules

- One coherent unit of work per issue; no "misc cleanup" buckets.
- Prefer small, verifiable steps over one sweeping change.
- Anything touching production behavior, data, or security needs an explicit
  risk and backout plan, not a placeholder.
- Never include secrets, credentials, or internal hostnames.
- No unreplaced placeholder text; labels must exist in the target repository.

## Rendering and creation

1. Resolve the governing contract with `issue-form-contracts`: the target
   repository's matching ops form if present, the bundled default otherwise.
2. Render and validate the body with that skill's script.
3. Propose the title and verified labels.
4. Create through `github-issue-operations`. Ops issues are standalone, so there
   is no parent link or task-list update unless the user asks for one.
