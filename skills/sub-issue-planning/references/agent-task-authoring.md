# Agent task authoring

Canonical rules for `[agent]` sub-issue bodies. Field ids match the bundled
agent-task contract; when the target repository has its own matching form, map
this guidance onto its labels and skip anything it does not have.

The goal is a task an agent can execute confidently, in one pull request,
without asking clarifying questions — and without wandering.

## main_issue — Main Issue Link

Exactly one Feature Brief, by number or URL.

## context — Context / Links

Cite the **precise sections** of the Feature Brief this task depends on, not the
brief as a whole. Add the project guardrail documents that apply. Contracts,
risks, and non-functional requirements flow down from the brief; reference them,
never redefine them.

## affected_paths — Affected Paths (Scope Gate)

Split into **Modify** and **Reference Only**.

- Modify: 4-8 specific files or narrow globs the agent may edit or create.
- Reference Only: read-for-context paths that must not change.
- Anything outside Modify requires asking first. Say so explicitly.
- Broad catch-all globs defeat the scope gate; justify one or narrow it.

## files_symbols — Files / Symbols to Touch

The authoritative action list. One bullet per file with an explicit
`Add` / `Edit` / `Delete`, plus the symbols to introduce or change and whether
each is new. Deletions are rare and need a reason. Going beyond this list
requires asking first.

## allowed_forbidden — Allowed vs Forbidden Changes

A few allowed actions and several forbidden ones, chosen for **this** task.
Common forbidden items: new dependencies, infrastructure or deployment changes,
global configuration edits, unrelated refactors, removing public interfaces.

## contracts_alignment — Contracts to Honor

Copy only the relevant invariants from the Feature Brief: type or operation
names, error semantics, pagination rules, authorization expectations, and any
non-functional budget that constrains the implementation. This is what stops an
agent drifting on public contracts.

## objective — Objective (Definition of Done)

3-6 checkboxes, each testable and observable. Cover the behavior, its tests, and
its instrumentation, plus an explicit "no forbidden changes" item.

## technical — Technical Details

Hard constraints — style, performance budget, data-access rules, compatibility —
and the side effects that are intentional, so they are not mistaken for scope
creep.

## observability — Observability Hooks

The logging, metrics, and tracing to add, named concretely, and where they are
emitted. State explicitly that no secrets or personal data may be logged.

## dependencies — Depends On / Blocks

Real issue numbers once they exist. Populate these after the dependency-ordered
creation pass, or update the issue afterwards.

## test_data — Test Data & Verification Steps

Fixtures the agent can construct, the exact commands to run, and the expected
observable result. This is how the agent knows it is finished. Avoid realistic
personal data.

## diff_size — Expected Diff Size

Prefer Small. A Large estimate is a signal the task should be split.

## pr_boundaries — PR Boundaries

What the pull request includes and, explicitly, what it excludes.

## security_privacy — Security / Privacy Checks

Acknowledge the checks that apply: input validation, authorization enforcement,
no secrets or personal data in logs, non-leaky error messages, idempotency for
writes.

## rollout_nature — Roll-forward Nature

Additive, Migration, or Risky. Migration and Risky items usually belong to a
maintainer task instead, or need a paired one.

## tests — Tests & Validation

What must be covered and the bar for green.

## agent_instructions — Agent Instructions

Keep the operating rules: stay inside Modify paths, do not exceed the
Files/Symbols list without asking, propose a plan before non-trivial or
public-interface changes, iterate until verification passes, and link both this
task and the Feature Brief in the pull request.

## Common failures to avoid

- Over-broad Modify globs, which let the agent wander.
- A Files/Symbols list that omits a file the task obviously needs.
- Contracts left as a pointer instead of copied invariants.
- Verification steps that cannot actually be run in the repository.
- Silent schema or infrastructure changes not declared anywhere.
