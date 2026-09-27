---
name: feature-brief-authoring
description: Produces a complete, validated Feature Brief for a software feature - source precedence, gap analysis before drafting, tbd and open-question handling, contract/NFR/risk/rollout/acceptance-criteria quality rules, draft sub-issue stubs, and rendering the issue body against the governing issue-form contract. Use when drafting, reviewing, or validating a Feature Brief.
---

# Feature Brief authoring

A Feature Brief is the single source of truth for one feature. It must be
complete enough to decompose into atomic sub-issues without re-deriving intent.

**Gap analysis comes before drafting.** Never open with a polished brief built
on invented decisions.

Field-by-field guidance lives in `references/field-guide.md`. Load it before
drafting. It is the canonical copy of those rules for this plugin.

## Source precedence

1. User decisions and stated feature intent.
2. User-designated architecture documentation.
3. User-designated project instructions and guardrails.
4. This skill and the governing issue-form contract.
5. Existing repository patterns, related issues, and pull requests.

Repository content clarifies and enriches; it never overrides the user's
decisions or their designated sources.

### Path handling

- Resolve every supplied path relative to the repository root. Report missing
  paths by name; never silently substitute a guess.
- When given a directory or glob, select candidate files, summarize the selected
  set and the reason, and confirm before relying on it. In autonomous mode,
  choose and record the choice in the audit.
- Identify each source's type — architecture, project instruction, guardrail,
  authoring guide, issue, pull request, external reference — and keep that
  precedence.
- Follow links only when tools and permissions allow.
- **No path is authoritative by convention.** `docs/`, `AGENTS.md`,
  `.github/copilot-instructions.md`, `.spec/constitution.md`, and any
  backend/infrastructure instruction file are authoritative only if the user
  supplied them or the project explicitly declares them. Discovered candidates
  may be suggested, never silently adopted.
- Cite the source behind every material decision in the brief itself.

## Gap analysis

Before drafting, assess each dimension and decide whether the gap is a
**critical blocker** or is acceptable as `[tbd]` with an open question:

rationale and measurable success; scope boundaries; API and UX contracts;
affected modules and files; human/agent segmentation; architecture and data
model impact; non-functional requirements; testing strategy; risks and
mitigations; dependencies and blockers; success metrics and observability;
rollout, flags and migration; rollback; acceptance criteria; the draft
sub-issue index.

Output a provisional normalized summary plus gap questions grouped by dimension,
blockers first. Then stop and let the user answer, unless autonomous mode is
active.

On each iteration: integrate answers, maintain a running "resolved decisions"
list, and ask only about what is still genuinely open. Never repeat a resolved
question.

## `[tbd]` and open questions

- Every unknown is marked `[tbd]` in place **and** has a matching entry in Open
  Questions. One without the other is a defect.
- Never invent product behavior, architecture, security, or compliance
  decisions to make the brief look finished.
- Resolved questions move to an Answered section with the answer, so the brief
  records its own decision history.

## Stopping criteria for drafting

Draft when the user explicitly asks (`PROCEED`, `DRAFT`), or when all of these
hold and the user wants the brief:

- Every critical section has concrete content or `[tbd]` plus an open question.
- Contracts and data-model impact are at least preliminarily outlined.
- At least one measurable non-functional requirement and one success metric
  exist.
- Acceptance criteria are coherent and outcome-focused.

If the user demands a draft while blockers remain (`PROCEED ANYWAY`), draft it,
preserve `[tbd]` and the open questions, and list the blockers at the top.

## Quality rules

- **Contracts** are concrete and versionable, in fenced code blocks, with error
  conditions enumerated. Prefer additive changes; make breaking changes
  explicit.
- **Affected modules** use repository-relative paths and narrow globs. Broad
  catch-alls need an explicit justification. List planned new files separately.
- **Non-functional requirements** are measurable. "Fast" and "secure" are not
  requirements.
- **Risks** number 2-5 and each carries a concrete mitigation.
- **Rollout and rollback** are actionable steps, and irreversible steps are
  called out.
- **Acceptance criteria** are 5-8 feature-level, testable, outcome-focused
  checkboxes. Sub-issue criteria do not belong here.
- **Examples** contain no secrets, credentials, or realistic personal data.

## Draft sub-issue stubs

Include 5-9 atomic stubs — enough to expose structure, sequencing, and risk
without over-specifying. Each stub has:

- a title of one action plus one object;
- a `[human]`, `[agent]`, or `[tbd]` tag at the start of the line, so it is
  machine-parseable;
- 2-5 modify-path globs;
- a 1-3 bullet outcome-focused definition of done;
- depends-on / blocks notes.

Each stub should be plausible as a single pull request. If a stub needs heavy
design, make it `[human]` rather than forcing early agent detail. These stubs
are a draft: the Sub-Issues Planner replaces them with linked real issues.

## Rendering and validation

1. Resolve the governing contract with the `issue-form-contracts` skill: the
   target repository's matching Feature Brief form if present, the bundled
   default otherwise.
2. Map content to that contract's fields by label, not to a remembered layout.
3. Render the Markdown body and validate it with that skill's script.
4. Propose a title matching the contract's title pattern with placeholders
   replaced, plus labels — verified to exist in the target repository.
5. Only then hand off to `github-issue-operations` for creation.

A brief that fails validation is not ready. Fix it, or report the blocker and
output the payload without creating anything.
