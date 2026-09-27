# Classification defaults

**Use these only when the project supplies no classification rules.** When the
user supplies project instructions or guardrails, those decide what humans must
own, and these defaults are ignored. When you do fall back to these, tell the
user you applied generic defaults and invite correction.

These heuristics are about **risk, reversibility, and how completely the work is
specified** — never about a particular directory layout, language, or cloud
provider.

## `[human]`

- Product, architecture, or interface **decisions** that are not yet made.
- Nuanced domain logic with rules that are not fully written down.
- Concurrency, transactions, or non-trivial consistency requirements.
- Data migrations, backfills, or schema evolution with meaningful rollback risk.
- Security, privacy, authorization, or compliance-sensitive changes.
- Cross-cutting infrastructure, networking, identity, or cost-bearing changes.
- Anything the project's guardrails reserve for humans.
- Anything irreversible or hard to detect when wrong.

## `[agent]`

- Well-specified work that follows an existing, visible pattern.
- Additive changes whose contracts are already fixed in the Feature Brief.
- Wiring, mapping, and plumbing between already-decided components.
- Small, fully specified, low-risk schema or configuration additions.
- Instrumentation consistent with an established convention.
- Test scaffolding and non-sensitive test additions.
- Work with a clear verification command whose failure is obvious.

## `[tbd]`

- Requirements or ownership are genuinely ambiguous.
- Mixed complexity that needs further decomposition first.
- Blocked on an open product or architecture decision.

A `[tbd]` item is not a dumping ground. Name the specific decision that would
resolve it and what it blocks.

## Deciding between human and agent

When an item looks like both, ask:

1. Is every decision it needs already made and written down? If not → `[human]`
   or `[tbd]`.
2. If it is done wrong, how quickly and cheaply is that detected and reverted?
   Slow or expensive → `[human]`.
3. Does an existing pattern in the repository demonstrate the intended shape?
   Yes → `[agent]` is more plausible.

Record the reason in the plan's "Why this class" column. A classification
without a reason is not reviewable.

## Labels and areas

Derive area labels from the target repository's existing label set and the
paths the work touches. Verify each label exists before applying it. If the
area is ambiguous, ask rather than guessing — and never invent a taxonomy the
repository does not use.
