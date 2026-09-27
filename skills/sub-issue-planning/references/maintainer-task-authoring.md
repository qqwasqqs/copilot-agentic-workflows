# Maintainer task authoring

Canonical rules for `[human]` sub-issue bodies. Field ids match the bundled
maintainer-task contract; when the target repository has its own matching form,
map this guidance onto its labels.

A maintainer task exists because a **decision, judgement, or risk** needs a
human — not because the work is merely large. Say which of those it is.

## main_issue — Main Issue Link

Exactly one Feature Brief, by number or URL.

## background — Background / Rationale

Why this work is needed and, explicitly, **why it is human-owned**: an
unresolved decision, sensitive or irreversible change, ambiguous requirements,
or a project guardrail that reserves it. Cite the exact Feature Brief sections
and the guardrail that applies. If the reason came from generic defaults rather
than a project rule, say so.

## design — Design / Plan

The approach at a level a maintainer can act on:

- the options considered and the recommendation, when a decision is the point of
  the task;
- the components, data, and contracts affected;
- the migration or rollout sequence, including irreversible steps;
- the risks and how they are contained;
- what must be decided before dependent agent tasks can start.

Where the decision is genuinely open, present the trade-offs rather than
pretending to have made it.

## acceptance — Acceptance Criteria

3-6 testable, outcome-focused checkboxes. For a decision task, "decided and
documented, with the dependent issues updated" is a legitimate — and often the
correct — criterion.

## notes — Notes / Follow-ups

Follow-on work, open questions, and the issues this unblocks. Record
`Depends on` and `Blocks` with real issue numbers once they exist.

## Relationship to agent tasks

When a maintainer task unblocks agent tasks, say so on both sides: the agent
task's dependencies cite this issue, and this issue's notes list what it
unblocks. That link is what makes the plan's ordering meaningful.

## Common failures to avoid

- "Human because it is complex", with no decision or risk named.
- A plan that restates the Feature Brief without adding actionable direction.
- Acceptance criteria that describe activity rather than an outcome.
- Silently absorbing work that belongs in a separate agent task, or the reverse.
