---
name: sub-issue-planning
description: Decomposes an approved Feature Brief into atomic sub-issues - atomicity rules, human/agent/tbd classification, acceptance-criterion traceability, dependency ordering, rendering agent and maintainer issue bodies against their governing contracts, and batch validation before creation. Use when breaking a Feature Brief into child issues or reviewing such a breakdown.
---

# Sub-issue planning

Turn one approved Feature Brief into a set of atomic, traceable, dependency-
ordered child issues. Plan first; author second; create only when authorized.

Body-authoring detail lives in `references/agent-task-authoring.md` and
`references/maintainer-task-authoring.md`. Load the one matching each class
before rendering. They are the canonical copies of those rules for this plugin.

## Atomicity

- Each sub-issue is a plausible **single pull request**.
- One concern per issue. Never merge unrelated work; never create a catch-all
  "misc" issue.
- Schema, data-migration, and infrastructure changes are never introduced "in
  passing" — they get their own explicitly scoped issue.
- If a slice is too large or mixes concerns, split it before authoring.
- If a slice is engineering upkeep rather than feature work, use the
  `ops-issue-authoring` skill instead.

## Classification

Classify every item `[human]`, `[agent]`, or `[tbd]`.

**The project's own supplied guardrails are the classification authority.** Read
the instruction and guardrail paths the user supplied, and apply their rules
about what humans must own. Only when the project supplies no such rules may you
fall back to the generic defaults in `references/classification-defaults.md`,
and then you must present them as suggestions and say that is what you did.

Never apply another project's path conventions as universal heuristics.

## Traceability

Every acceptance criterion in the Feature Brief must map to at least one
sub-issue, or to an explicitly documented unresolved item. Every sub-issue must
tie back to at least one acceptance criterion or be a clearly necessary enabling
task, and say which.

If a criterion cannot be mapped, name it under Gaps / Questions as a gap to
resolve or deliberately defer. Do not quietly leave it uncovered.

## Dependency ordering

Determine which issues must exist first — decisions, contracts, schema, shared
scaffolding — and order creation accordingly so later bodies can cite real issue
numbers. Record `Depends on` and `Blocks` for every issue that has them. Flag
dependency cycles instead of silently breaking one.

## Plan output format

Produce exactly these sections:

### Proposed Sub-Issue Plan

| # | Title | Class | Description | Why this class | Primary paths | References |
| --- | --- | --- | --- | --- | --- | --- |

### Traceability

Each Feature Brief acceptance criterion, with the sub-issue numbers covering it.

### Gaps / Questions

Numbered open items (`Q1:` …), including any uncovered acceptance criterion.

### Suggested Counts

`Suggested counts: X human / Y agent / Z tbd.`

Then ask for `APPROVE`, `ADJUST`, or `QUESTIONS` — unless autonomous mode is
active, in which case proceed directly to authoring.

Keep descriptions concise. Summarize the brief; never paste large parts of it
back. Do not print classification heuristics verbatim to the user.

## Authoring

For each approved item:

1. Resolve the governing contract with `issue-form-contracts`:
   `[agent]` → agent-task class, `[human]` → maintainer-task class. For `[tbd]`,
   create a blocked placeholder only when the user allows placeholders or
   autonomous mode is active and the item is actionable; otherwise preserve it
   in the Feature Brief index and the report.
2. Fill the contract's fields using the matching authoring reference.
3. Include a textual backlink to the Feature Brief and cite the exact sections
   it draws on — for example `#123 - API/UX Contracts`.
4. Render and validate the body with the `issue-form-contracts` script.
5. Create and link it through `github-issue-operations`.

## Batch validation before creation

Before the first write, confirm all of the following:

- Every body passed contract validation.
- Every title has its placeholders replaced and follows the contract's pattern.
- Every label exists in the target repository.
- No assignees, project ids, or example data were copied from a template.
- Creation order respects the dependency graph.
- The traceability table covers every acceptance criterion.
- The count in the plan equals the number of issues about to be created.

## Failure handling

- Never silently omit an approved sub-issue. Report every failure.
- Continue the batch after a recoverable failure; record it in the run ledger.
- Never recreate an issue that already succeeded — reconcile first, per
  `github-issue-operations`.
- If details are missing for one sub-issue, ask a focused question about that
  issue rather than stalling the whole batch. If the user insists on creating it
  anyway, mark it clearly as blocked, and state what is missing and what would
  unblock it.
