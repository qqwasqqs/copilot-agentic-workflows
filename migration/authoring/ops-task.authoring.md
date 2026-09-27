# Operational Task Authoring Guide

Intent
- Standardize non-feature (chore / ops) tasks: tooling, linting, local dev setup, docs updates, CI, security hardening.
- Keep tasks atomic, low-risk, and easy to review.

When to use
- Work that supports engineering velocity or quality but isn’t a product feature.
- Examples: add ESLint, adjust CI workflow, improve CONTRIBUTING.md, update Copilot instructions, set up local dev script, rotate keys, cleanup obsolete files.

Categories (use the template dropdown)
- Tooling / Linting
- Local Dev Environment
- Documentation / Guides
- Copilot Instructions / Templates
- CI/CD / Automation
- Security / Compliance
- Housekeeping / Cleanup
- Process / Project Hygiene
- Other (if none match)

Sources of truth (priority order)
1. Existing repository config (package.json, workflows, docs)
2. Instruction files (.github/instructions/*, AGENTS.md)
3. Past ops tasks / PRs
4. External authoritative docs (ESLint, GitHub Actions, AWS)
5. If uncertain → add to Risks or create follow-up task

Core principles
- Atomic: prefer one PR per ops task.
- Minimal blast radius: only touch declared paths.
- Reversible: document rollback steps.
- Transparent: provide rationale + validation steps.
- Consistent: adhere to established guardrails (logging/security/dependency policies).

Field guidance

Rationale
- Focus on problem + outcome. Avoid implementation detail until Steps section.

Scope
- Explicit in-scope vs out-of-scope boundaries. Prevents silent expansion (e.g., “do not refactor unrelated services”).

Affected Paths
- Repo-relative list. Only include paths to modify/create. Avoid broad globs (no src/** unless necessary).

Steps / Plan
- Each step should map to one or more small commits. Keep verbs clear (Add / Update / Remove / Document).

Deliverables
- Name concrete files, config changes, docs pages produced.

Risks / Impact
- Think adoption, performance, build times, compatibility (Windows/Linux/Mac), security, developer friction.

Rollback
- Provide line-of-command or revert actions (e.g., “git revert <commit>”, “remove lint workflow”, “restore previous config from tag v0.4.2”).

Validation / Verification
- Commands + expected results (e.g., “npm run lint returns exit code 0”, “docs build has 0 broken links”).

Acceptance Criteria
- 3–7 checkboxes; each must be objectively testable. Avoid vague wording (“improved docs”)—use measurable outcomes (“new section added: Local Dev Setup”).

References / Links
- External docs, prior issues/PRs, internal guides.

Effort sizing heuristic
- XS: ≤1h (e.g., add a README section)
- S: ≤1 day (new ESLint config, single workflow)
- M: 1–3 days (convert build system, restructure docs)
- L: >3 days (large CI overhaul; split if possible)

Notes / Follow-ups
- Capture future enhancements without expanding current scope (e.g., pre-commit hooks after ESLint baseline).

Quality checklist before submitting
- Scope fence is clear (no ambiguous “maybe” items).
- All paths exist or are to be created intentionally.
- Rollback steps feasible and safe.
- Validation commands reproducible locally.
- Acceptance criteria map directly to deliverables.
- No secrets or credentials exposed in examples.
- Effort is realistic; Large tasks considered for split.

Example skeleton

Rationale
- We need consistent linting to reduce style churn and catch basic errors earlier.

Scope
In scope:
- Add ESLint config (.eslintrc.cjs)
- Add CI workflow for lint on PRs
Out of scope:
- Prettier setup
- Style refactors across existing code

Affected Paths
- .eslintrc.cjs
- package.json (scripts)
- .github/workflows/lint.yml
- docs/contributing.md

Steps / Plan
- [ ] Add base ESLint config (typescript/recommended)
- [ ] Add npm script: lint & lint:fix
- [ ] Create GitHub Action workflow: run on pull_request
- [ ] Update contributing guide with lint instructions

Deliverables
- .eslintrc.cjs
- Updated package.json scripts
- New workflow file
- Contributing doc section “Code Quality”

Risks / Impact
- Risk: slower PR feedback. Mitigation: cache node_modules.
- Risk: existing code fails lint. Mitigation: start with warnings; tighten later.

Rollback
- Remove workflow file
- Delete .eslintrc.cjs
- Revert package.json changes

Validation
- npm run lint passes
- Workflow green on a test PR
- Docs render updated section

Acceptance Criteria
- [ ] Lint config committed
- [ ] CI lint workflow runs on PRs
- [ ] Contributing guide updated
- [ ] No new dependencies beyond eslint + plugins approved

References
- ESLint docs
- Prior internal style guide

Final tips
- Prefer additive changes.
- Keep ops tasks lean; split if complexity grows.
- If a change affects developer workflow significantly, communicate in docs and changelog.
