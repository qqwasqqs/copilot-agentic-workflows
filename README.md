# Copilot agentic workflows: migration seed

This repository is the **future canonical, versioned home** of an installable
GitHub Copilot plugin for feature-brief planning and issue decomposition. It is
currently **source material only**: no plugin manifest, active agents, or active
skills have been implemented. Nothing in `migration/` is a discoverable agent,
skill, or GitHub issue form in this repository.

## Provenance and inventory

Copied from the folder-backed project
`\\wsl.localhost\UbuntuMain\var\www\project-01-backend` without changing that
project. The source paths below are relative to that root. Staged assets are
verbatim copies; only the integration brief was revised for the plugin
architecture.

| Destination | Source | Purpose |
| --- | --- | --- |
| `docs/github-copilot-agentic-workflow-integration.md` | `docs/github-copilot-agentic-workflow-integration.md` | Revised implementation brief |
| `migration/agents/feature-brief-planner-v2.agent.md` | `.github/agents/feature-brief-planner-v2.agent.md` | Canonical Feature Brief planner input |
| `migration/agents/sub-issues-planner-v2.agent.md` | `.github/agents/sub-issues-planner-v2.agent.md` | Canonical decomposition planner input |
| `migration/agents/ops-issue-planner.agent.md` | `.github/agents/ops-issue-planner.agent.md` | Ops planner input |
| `migration/agents/documentation-agent.agent.md` | `.github/agents/documentation-agent.agent.md` | Optional documentation role input |
| `migration/agents/coding-agent.agent.md` | `.github/agents/coding-agent.agent.md` | Optional coding role input; not required for planning |
| `migration/authoring/feature-brief.authoring.md` | `.github/instructions/feature-brief.authoring.md` | Feature Brief authoring rules |
| `migration/authoring/agent-task.authoring.md` | `.github/instructions/agent-task.authoring.md` | Atomic agent-task authoring rules |
| `migration/authoring/ops-task.authoring.md` | `.github/instructions/ops-task.authoring.md` | Ops-task authoring rules |
| `migration/issue-forms/feature-brief.yml` | `.github/ISSUE_TEMPLATE/feature-brief.yml` | Example Feature Brief form contract |
| `migration/issue-forms/agent-task.yml` | `.github/ISSUE_TEMPLATE/agent-task.yml` | Example agent-task form contract |
| `migration/issue-forms/maintainer-task.yml` | `.github/ISSUE_TEMPLATE/maintainer-task.yml` | Example maintainer-task form contract |
| `migration/issue-forms/ops-task.yml` | `.github/ISSUE_TEMPLATE/ops-task.yml` | Example ops-task form contract |

**Excluded:** obsolete v1 planners
(`.github/agents/feature-brief-planner.agent.md`,
`.github/agents/sub-issues-planner.agent.md`), source backend and infrastructure
instructions, global Copilot instructions, `AGENTS.md`, application and
infrastructure code, and source issue-form configuration. The staged form
examples deliberately are **not** in `.github/ISSUE_TEMPLATE/`: they describe
target-repository contracts, not issues to file in this plugin repository.
Original profiles still contain project-specific assumptions and historical
tool names; do not activate them unreviewed.

## Next stage

1. Recheck the [integration brief](docs/github-copilot-agentic-workflow-integration.md)
   and official plugin guidance; choose the app-compatible plugin manifest,
   agent frontmatter, supported tools, and runtime issue-form precedence.
2. Generalize the staged guides and four form examples into reusable skills and
   bundled fallback contracts. Target-repository forms, instructions, and
   architecture take precedence when supplied or present.
3. Refactor the v2 planners, retain only useful optional specialists, and add
   the orchestrator and versioned plugin manifest. Keep `migration/` outside
   discoverable plugin component directories.
4. Install the plugin in the Copilot app across a separate test project, then
   validate supervised/autonomous modes, issue creation, parent/child linking,
   failure recovery, and safety boundaries before release.

GitHub documents [plugin installation in the Copilot app](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
and [Agent Plugins 1.0 component layout](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference).
This seed is not yet installable as a plugin.
