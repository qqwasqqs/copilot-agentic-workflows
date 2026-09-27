# Agentic feature workflow

An installable **GitHub Copilot plugin** that turns a feature idea into a
validated Feature Brief issue and a dependency-ordered set of linked sub-issues,
in any repository, without hardcoding one project's conventions.

It ships three planning agents, one documentation agent, five reusable skills,
and bundled default issue-form contracts that are used only when the target
repository has no form of its own.

## What you get

| Component | Kind | Use it for |
| --- | --- | --- |
| `agentic-feature-workflow` | agent | End-to-end: brief → parent issue → decomposition → linked sub-issues |
| `feature-brief-planner` | agent | Just the Feature Brief |
| `sub-issues-planner` | agent | Decompose an existing Feature Brief |
| `ops-issue-planner` | agent | Standalone chores, upgrades, CI/CD, refactors |
| `feature-documentation-author` | agent | Read-only feature documentation |
| `feature-brief-authoring` | skill | Brief field rules, gap analysis, `[tbd]` handling |
| `sub-issue-planning` | skill | Atomicity, `[human]`/`[agent]` classification, traceability |
| `ops-issue-authoring` | skill | Ops issue triage and fields |
| `issue-form-contracts` | skill | Target-form precedence, rendering, deterministic validation |
| `github-issue-operations` | skill | Creation order, sub-issue linking, backlinks, resumable failures |

## Installation

**Copilot app** — Customize → Plugins → add `qqwasqqs/copilot-agentic-workflows`.

**Copilot CLI**

```bash
copilot plugin install qqwasqqs/copilot-agentic-workflows
```

**Cloud agent** — in `.github/copilot/settings.json` of the target repository:

```json
{ "enabledPlugins": ["qqwasqqs/copilot-agentic-workflows"] }
```

Reload or restart the client, then confirm the agents appear in the agent
picker.

## Usage

Supervised is the default: the agent stops at checkpoints and waits for your
approval before writing anything.

```text
@agentic-feature-workflow Plan a scheduled report export feature for
owner/repo. Architecture: docs/architecture/reporting.md. Guardrails:
docs/engineering-guardrails.md.
```

```text
@feature-brief-planner Draft a Feature Brief for offline mode in owner/repo,
using docs/adr/0012-sync.md.
```

```text
@sub-issues-planner Decompose owner/repo#412 into sub-issues.
```

```text
@ops-issue-planner Upgrade the test runner in owner/repo and open an ops issue.
```

### Autonomous mode

Only runs without checkpoints when you say so explicitly:

```text
@agentic-feature-workflow ... Run autonomously: create the Feature Brief and
all sub-issues without stopping for approval.
```

It still validates every body before creating it, records an audit trail of the
decisions it made on your behalf, and stops on an unrecoverable error rather
than guessing.

### Supplying your own sources

Pass architecture documents, project instructions, guardrails, and authoring
guides by path. No path is authoritative by convention — the agents use what you
give them, then the target repository's own patterns, and they cite the source
behind each material decision.

### Issue forms

If the target repository has issue forms for feature briefs or tasks, **those
are authoritative**; the plugin extracts a contract from them at runtime. If it
has none, the bundled defaults in
[`skills/issue-form-contracts/forms/`](skills/issue-form-contracts/forms) are
used. Those forms are deliberately **not** in `.github/ISSUE_TEMPLATE/` here:
they are contracts, not templates for this repository.

## Development

```bash
python3 scripts/validate_plugin.py   # manifest, frontmatter, links, contracts
bash scripts/smoke-test.sh           # negative validator cases + render round trips
bash scripts/regen-contracts.sh      # regenerate contracts after editing a form
```

`scripts/regen-contracts.sh` needs PyYAML; everything else is standard library.

## Repository layout

```text
plugin.json                  Agent Plugins 1.0 manifest
com.github.copilot/agents/   Copilot custom agents
skills/                      Agent Skills, bundled forms and contracts
scripts/                     Validation and maintenance scripts
docs/                        Implementation brief and compatibility decisions
migration/                   Unmodified historical source material (not discoverable)
```

## Documentation

- [Implementation brief and compatibility decisions](docs/github-copilot-agentic-workflow-integration.md)
- [About plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
- [Plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
- [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [About Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

## License

MIT.
