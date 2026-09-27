# GitHub Copilot Agentic Workflow Plugin Integration

This is a future-implementation brief, not an inventory of implemented plugin
features. The original project assets are copied, unmodified, into `migration/`
in this dedicated plugin repository. They are migration inputs, not installed
agents, active skills, or issue forms for this repository.

## 1. Purpose

This document is an implementation brief for a GitHub Copilot agent working in
this dedicated, versioned plugin repository. Its task is to turn the staged
planning system into an installable plugin for the GitHub Copilot app across
projects. This plugin repository is the canonical home for the portable
orchestrator, specialist agents, skills, and bundled default issue-form
contracts; target repositories own their project-specific context.

The finished system must let a user:

1. Start a feature-planning session and provide the locations of:
   - Architecture documentation.
   - Project-specific instructions and guardrails.
   - Authoring guides or other relevant source material.
2. Produce a complete Feature Brief and, when authorized, create it as a GitHub
   issue.
3. Break the approved Feature Brief into atomic human, agent, and unresolved
   sub-issues.
4. Create and link those sub-issues in GitHub.
5. Run either:
   - Interactively, with review checkpoints; or
   - End to end without workflow-level intervention when the user explicitly
     requests autonomous execution.

The implementation must be portable within the GitHub Copilot ecosystem and must
not depend on the source project's backend, infrastructure, or product conventions.

## 2. Required outcome

Implement a hybrid system made of:

- **Custom agents** for durable roles, tool boundaries, interaction modes, and
  lifecycle control.
- **Agent skills** for reusable procedures, templates, validation rules, and
  supporting resources.
- **Issue-form contracts**: forms in a target repository take precedence; bundled,
  generalized default form contracts apply only when the target lacks a
  corresponding form.
- **A top-level workflow orchestrator** as the primary entry point for users who
  want the complete workflow.

Do not replace every custom agent with a skill. Agents and skills serve different
purposes:

- An agent defines who is acting, which tools it may use, what it may change, and
  when it must stop.
- A skill defines how to perform a reusable task and may bundle instructions,
  examples, templates, or scripts.

The workflow must also remain usable one stage at a time. A user must be able to
select the Feature Brief planner or Sub-Issues planner directly instead of always
using the orchestrator.

## 3. Existing assets and their disposition

### 3.1 Canonical agents

The v2 planners are the only valid planner versions; their source copies are:

- `migration/agents/feature-brief-planner-v2.agent.md`
- `migration/agents/sub-issues-planner-v2.agent.md`

Use their behavior as the starting point, but refactor them to use the new skills
and remove project-specific assumptions.

The following source-project v1 files are obsolete and were not imported:

- `.github/agents/feature-brief-planner.agent.md`
- `.github/agents/sub-issues-planner.agent.md`

Do not migrate them into the plugin. Do not retain two discoverable definitions
for the same role. The source project is out of scope for edits.

### 3.2 Other existing agents

Review these agents independently:

- `migration/agents/ops-issue-planner.agent.md`
- `migration/agents/documentation-agent.agent.md`
- `migration/agents/coding-agent.agent.md`

Expected disposition:

- Keep the Ops Issue Planner if it can be made repository-agnostic. Give it an
  ops-task authoring skill.
- Keep the Documentation Agent if post-feature documentation is part of the
  desired lifecycle. Give it a post-feature documentation skill or keep its
  workflow self-contained if a skill would not be reused.
- Do not make the generic Coding Agent a required part of feature planning and
  decomposition. Keep it only if it adds value beyond the Copilot app's built-in
  implementation agent. Avoid maintaining a redundant generic persona.

### 3.3 Authoring guides

These files contain reusable workflow knowledge and are relevant:

- `migration/authoring/feature-brief.authoring.md`
- `migration/authoring/agent-task.authoring.md`
- `migration/authoring/ops-task.authoring.md`

Move or adapt their portable content into skills. After implementation, avoid
keeping two independently maintained copies of the same normative rules. Either:

- Make the skill the canonical source and reduce the old guide to a pointer; or
- Keep the guide as a skill resource and have `SKILL.md` explicitly load it.

Choose one ownership model and document it.

### 3.4 Issue forms

These forms are part of the orchestration system:

- `migration/issue-forms/feature-brief.yml`
- `migration/issue-forms/agent-task.yml`
- `migration/issue-forms/maintainer-task.yml`
- `migration/issue-forms/ops-task.yml`

These are target-repository examples and migration inputs, **not** issue forms
for this plugin repository; do not place them under this repository's
`.github/ISSUE_TEMPLATE/`. In a target repository, its own matching forms are
the canonical field names and required fields. When a matching target form is
absent, use a generalized contract bundled with the plugin. Generalize these
copies during implementation, not during this seed. Do not overwrite or
install forms into target repositories without authorization.

Known issues to address include:

- The Feature Brief form currently uses the misspelled label `enhacement`.
- Help text refers directly to the source project's backend/infra instructions,
  `AGENTS.md`, Copilot instructions, and constitution.
- Maintainer-task defaults contain placeholder assignee data.
- Examples assume a specific backend/AWS architecture.

Do not delete useful examples merely because they are backend-oriented. Replace
them with neutral examples or clearly mark them as examples that may be overridden
by supplied project guidance.

## 4. Mandatory discovery before editing

GitHub Copilot app and plugin support evolve. Before implementing active plugin
components, consult current official GitHub and (where relevant) VS Code
documentation and verify the exact plugin structure and profile schema supported
by the GitHub Copilot app. The staging layout here is deliberately not a plugin
component layout.

At minimum, determine:

1. Which plugin format and component locations the app discovers, and which
   custom-agent filenames are supported there.
2. Whether `.agent.md`, plain `.md`, or both are supported in the plugin's
   agent directory.
3. Which frontmatter properties are supported by the app, including:
   - `name`
   - `description`
   - `tools`
   - `agents`
   - `handoffs`
   - `user-invocable`
   - Model or target-specific properties
4. How plugin skills under `skills/<skill-name>/SKILL.md` are discovered and
   explicitly invoked.
5. Whether a selected custom agent can:
   - Invoke skills automatically.
   - Delegate to another plugin-bundled custom agent.
   - Use handoffs in the Copilot app.
   - Continue the complete workflow in one session.
6. Which GitHub tools are available for:
   - Reading issues.
   - Creating issues.
   - Updating the Feature Brief's task list.
   - Creating true GitHub sub-issue relationships.
   - Adding labels.
7. Whether the app can use repository-configured MCP servers, built-in GitHub
   tools, or authenticated `gh` CLI commands for missing operations.

Use current official documentation as the authority. Do not blindly preserve old
tool identifiers such as `runSubagent`,
`github/github-mcp-server/issue_write`, or extension-specific tool names if the
Copilot app uses different identifiers.

If a capability differs between VS Code and the GitHub Copilot app, optimize for
the app while retaining VS Code compatibility when that can be done without
duplicating agents or weakening behavior.

Record important compatibility decisions in a short section in this document or
another existing relevant document. Do not create an unnecessary collection of
design notes.

### Verified plugin compatibility (GitHub documentation, checked September 2026)

- [About GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
  describes plugins as installable across Copilot CLI, cloud agent, and the
  GitHub Copilot app; the app installs them through **Customize > Plugins**.
- [Creating a plugin](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)
  and the [CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
  recommend Agent Plugins 1.0 for new plugins unless configurable component
  paths are required. It uses root `plugin.json` with the Agent Plugins 1.0
  schema, `skills/<name>/SKILL.md`, and Copilot-specific
  `com.github.copilot/agents/*.agent.md`. Legacy manifests without that schema
  use `agents/` and `skills/` by default; do not mix the formats accidentally.
  A repository root can be installed with `copilot plugin install OWNER/REPO`.
- These references establish packaging and installation, **not** that the
  staged legacy tool IDs, agent handoffs, all frontmatter properties, or
  GitHub issue/sub-issue operations work in the app. Verify those capabilities
  in the implementation stage before choosing exact identifiers or fallbacks.

## 5. Target architecture

### 5.1 Workflow orchestrator agent

Create a plugin-bundled custom agent with a clear name such as:

`Agentic-Feature-Workflow`

This is the preferred Copilot app entry point. It coordinates the full lifecycle:

1. Resolve and read user-supplied source paths.
2. Run Feature Brief planning.
3. Create the Feature Brief issue when allowed.
4. Run sub-issue decomposition against the created issue.
5. Create and link sub-issues when allowed.
6. Return a final index of created artifacts and unresolved items.

The orchestrator should not duplicate every authoring rule in its profile. It
should invoke the relevant skills.

If the Copilot app reliably supports custom-agent delegation, the orchestrator may
delegate stages to the two specialist agents. If it does not, the orchestrator
must execute the same stages itself by loading the skills. The end-user experience
must not depend on an unsupported handoff.

### 5.2 Feature Brief planner agent

Refactor the v2 Feature Brief planner into a portable specialist.

Inputs:

- Feature idea, goal, or problem.
- One or more architecture-document paths or URLs supplied by the user.
- Optional project-instruction and guardrail paths supplied by the user.
- Optional authoring-guide paths supplied by the user.
- Requested execution mode: supervised or autonomous.

Behavior:

1. Validate that supplied repository paths exist and report missing paths.
2. Read the supplied sources in this priority:
   - User decisions and feature intent.
   - User-designated architecture documentation.
   - User-designated project instructions and guardrails.
   - Feature Brief skill and issue-form contract.
   - Existing repository patterns and related issues/PRs.
3. Normalize the proposal against the Feature Brief fields.
4. Perform gap analysis without inventing missing product or architecture
   decisions.
5. Mark unresolved information as `[tbd]` and maintain explicit open questions.
6. Produce a valid Feature Brief issue body.
7. Create the issue only according to the active execution mode.

Do not hardcode `docs/`, `AGENTS.md`, backend instructions, infrastructure
instructions, or any constitution as universally authoritative. The user will
tell the agent which architecture documents, instructions, and authoring guides
to use. The agent may discover likely sources and suggest them, but must not
silently treat them as authoritative.

### 5.3 Sub-Issues planner agent

Refactor the v2 Sub-Issues planner into a portable specialist.

Inputs:

- A Feature Brief issue number or URL.
- Optional updated decisions.
- Optional project-instruction and guardrail paths.
- Requested execution mode.

Behavior:

1. Fetch the Feature Brief.
2. Load the sub-issue planning skill and relevant issue-form resources.
3. Produce an atomic decomposition.
4. Classify work as `[human]`, `[agent]`, or `[tbd]`.
5. Trace every Feature Brief acceptance criterion to one or more sub-issues.
6. Identify dependencies and a safe creation order.
7. Create issues according to the active execution mode.
8. Create real GitHub sub-issue relationships when the available GitHub API/tool
   supports them.
9. Update the Feature Brief's Sub-Issue Index with links to created issues.
10. Never omit a requested issue silently. Report failures and leave a
    resumable summary.

Classification must be informed by user-supplied project guardrails rather than
hardcoded backend/infra path heuristics. Generic default heuristics are acceptable
only as suggestions when the project supplies no classification rules.

### 5.4 Skills

Create focused plugin skills under the app-supported plugin skill location.
The intended Agent Plugins 1.0 structure, subject to app smoke testing, is:

```text
plugin.json
com.github.copilot/
  agents/
    agentic-feature-workflow.agent.md
    feature-brief-planner.agent.md
    sub-issues-planner.agent.md
skills/
  feature-brief-authoring/
    SKILL.md
    references/...
  sub-issue-planning/
    SKILL.md
    references/...
  ops-issue-authoring/
    SKILL.md
    references/...
```

Add a post-feature documentation skill only if the Documentation Agent remains in
scope and the workflow is reusable outside that one agent.
Bundle generalized fallback issue-form contracts as non-discoverable plugin
resources (for example, skill `references/`); the `migration/issue-forms/`
copies are unmodified inputs, not the finished defaults.

#### Feature Brief authoring skill

Own:

- Feature Brief field-by-field guidance.
- Source-priority rules.
- Gap analysis.
- `[tbd]` and open-question handling.
- Contract, NFR, risk, rollout, rollback, and acceptance-criteria quality rules.
- Feature-level sub-issue stubs.
- Rendering a GitHub issue body matching the target Feature Brief form, or the
  bundled fallback contract if no matching target form exists.
- Validation before issue creation.

#### Sub-issue planning skill

Own:

- Atomic decomposition.
- Human/agent/tbd classification.
- Acceptance-criterion traceability.
- Dependency ordering.
- Rules for rendering agent and maintainer issue bodies against matching target
  forms, or bundled fallback contracts when absent.
- Scope gates, files/symbols, contracts, verification, security, observability,
  and PR-boundary guidance.
- Batch-creation validation.
- Feature Brief task-list update behavior.

#### Ops issue authoring skill

Own the portable content currently in
`.github/instructions/ops-task.authoring.md`, including atomicity, rollback,
validation, and rendering against `ops-task.yml`.

### 5.5 Skill resources and scripts

Skills may bundle reference files and deterministic helper scripts when this
improves reliability.

Consider a renderer/validator that:

- Reads the matching target-repository issue-form YAML if present, or the
  plugin's generalized default contract otherwise.
- Verifies all required fields have content.
- Converts field values into a stable Markdown issue body.
- Detects unresolved `[tbd]` entries.
- Checks title and label proposals.
- Emits machine-readable output for an issue-creation tool.

Do not add a script merely to duplicate simple model instructions. Add one when it
provides deterministic validation or avoids malformed issue bodies.

Issue forms control GitHub's web form, but API/MCP/CLI issue creation usually
requires a title and Markdown body. The implementation must therefore define how
target-form-aligned (or fallback-contract-aligned) content is rendered for
programmatic issue creation; it must not assume that selecting a form through
the API is supported.

## 6. Execution modes

Every orchestrating/planning agent must support two explicit modes.

### 6.1 Supervised mode

This is the default when the user does not request autonomous execution.

Required checkpoints:

1. Review gap analysis and answer questions.
2. Approve the Feature Brief draft.
3. Confirm Feature Brief issue creation.
4. Approve the proposed sub-issue plan.
5. Confirm sub-issue creation.

The agent should combine checkpoints when the user has already given the relevant
approval. It must not ask the same question repeatedly.

### 6.2 Autonomous mode

Activate only when the user explicitly asks to run the whole workflow
autonomously, without intervention, or uses an equivalent unambiguous instruction.

In autonomous mode:

- Do not stop at normal workflow review checkpoints.
- Make reasonable, low-risk decisions from supplied sources.
- Preserve non-critical uncertainty as `[tbd]`.
- Create the Feature Brief and eligible sub-issues automatically.
- Create blocked `[tbd]` issues only when useful; otherwise preserve them in the
  Feature Brief and final report.
- Continue through recoverable failures.
- Return a full audit summary of assumptions, issue links, classifications,
  dependency relationships, unresolved questions, and failures.

Autonomous mode does **not** override:

- GitHub or Copilot permission prompts.
- Repository protection or organization policies.
- Security boundaries.
- Missing authentication.
- Destructive-operation safeguards.
- A requirement for explicit owner approval imposed by supplied project
  instructions.

If issue creation is impossible because no authenticated tool is available, the
agent must still produce validated, ready-to-create issue payloads and clearly
state the blocker. It must not claim that issues were created.

## 7. GitHub issue operations

Implement issue operations using this priority:

1. Native GitHub tools available to the Copilot app.
2. A repository-configured GitHub MCP server supported by the app.
3. Authenticated `gh` CLI, if the app session exposes it and policy permits.

Do not couple the profiles permanently to one historical tool identifier. Declare
the minimum necessary tool capability in each profile and use the exact current
identifier found during discovery.

Before writes in the **target** repository:

- Confirm the target owner/repository.
- Verify required labels exist.
- Avoid placeholder assignees and project IDs.
- Validate issue title and body against the relevant form.
- Check for likely duplicate open issues when practical.

For sub-issues:

- Create issues in dependency-aware order.
- Capture every created issue number immediately.
- Attach each issue to the Feature Brief using GitHub's sub-issue relationship
  API/tool when available.
- Also include a textual backlink in every child issue.
- Update the parent Feature Brief's task list using linked issue references.
- Treat partial batch failure as a resumable state, not a reason to recreate
  successful issues.

## 8. Repository-agnostic behavior

The portable plugin may define process rules, but must not embed the source
project's engineering rules. The target repository supplies its own architecture
documents, instructions, guardrails, and issue forms; matching target forms
override the plugin defaults. Read target instructions as project constraints,
not as content to migrate into the plugin.

Remove hard dependencies on:

- `.github/copilot-instructions.md`
- `.github/instructions/backend.instructions.md`
- `.github/instructions/infrastructure.instructions.md`
- `.spec/constitution.md`
- `AGENTS.md`
- AWS, Amplify, DynamoDB, AppSync, or backend-specific path conventions

These may still be consumed when the user explicitly provides them or when a
project-specific wrapper declares them.

The system should use neutral concepts:

- Architecture sources.
- Project instructions.
- Project guardrails.
- Product contracts.
- Human-only constraints.
- Agent-suitable work.
- Modifiable and reference-only paths.

## 9. Context and path handling

The workflow must accept multiple source locations, not only a single file.

For every supplied source:

- Resolve repository-relative paths safely.
- Read directories selectively rather than loading everything blindly.
- Follow links only when tools and permissions allow.
- Identify the source type: architecture, project instruction, authoring guide,
  issue, PR, or external reference.
- Preserve source precedence.
- Cite the source used for material decisions in the generated issue.

If the user names a directory such as `docs/`, discover likely architecture files
and summarize the selected set before relying on it. In autonomous mode, choose
the most relevant files and record that choice in the final audit.

## 10. Tool boundaries

Planning agents should have:

- Repository and documentation read tools.
- GitHub issue/PR read tools.
- GitHub issue write/update/sub-issue tools when creation is enabled.
- Skill loading.
- Optional read-only research delegation.

Planning agents should not have:

- General code-editing tools.
- Unrestricted shell execution unless needed solely for an approved,
  well-defined GitHub fallback.
- PR creation or implementation tools.

The workflow orchestrator may have the union of tools required by its stages, but
it remains a planning and issue-authoring role. It must not implement feature
code.

## 11. Recommended implementation sequence

The next-stage implementing Copilot agent should:

1. Read this document and inventory the staged `migration/` assets. This seed
   does not implement or activate them.
2. Recheck the official documentation in Section 4 and test app compatibility.
3. Choose the Agent Plugins 1.0 component layout unless a verified requirement
   calls for legacy paths; decide supported profile syntax and tool identifiers.
4. Design skill boundaries and eliminate duplicated normative content.
5. Create the Feature Brief, Sub-Issue planning, and (if retained) Ops authoring
   skills from the staged guides and planner rules.
6. Generalize bundled fallback form contracts from the four staged examples,
   fixing invalid placeholders, labels, and project-specific references. At
   runtime inspect target-repository forms first and use matching target
   contracts in preference to defaults.
7. Refactor the two staged v2 planners into plugin specialists that consume
   the skills, target contracts, and supplied source paths.
8. Create the plugin's top-level workflow orchestrator and consistent
   supervised/autonomous mode handling.
9. Review the staged optional agents and retain only useful portable roles.
   Never import the v1 planner profiles into active plugin directories.
10. Add a versioned manifest and concise installation/usage documentation.
11. Validate component discovery and behavior in the GitHub Copilot app with a
    separate, explicitly approved target/test repository.

Use precise, surgical changes. Do not edit the source project, rewrite a target
repository's unrelated instructions, or implement application code.

## 12. Validation plan

### 12.1 Static validation

Verify:

- All YAML frontmatter parses.
- All issue-form YAML parses and satisfies GitHub issue-form requirements.
- Every skill has valid required frontmatter and a focused description that lets
  Copilot select it appropriately.
- Skill-relative links resolve.
- Agent references to skills, tools, agents, and handoffs use supported syntax.
- No obsolete planner remains discoverable.
- No required workflow file references a missing resource.
- No placeholder usernames, project IDs, domains, or misspelled labels remain.
- Matching target forms override bundled fallback contracts; absent target
  forms resolve to valid plugin defaults without writing to the target repo.

### 12.2 Copilot app discovery test

Install the plugin in the GitHub Copilot app for a test project and verify:

- The orchestrator appears exactly once.
- The Feature Brief planner appears exactly once.
- The Sub-Issues planner appears exactly once.
- Retained optional agents appear exactly once.
- Skills are installed/discovered from the plugin in the target project.
- The agents can load the expected skills.
- No unsupported tool errors occur when starting a planning session.

If the app does not expose a deterministic machine-readable discovery check,
perform this as a documented manual smoke test.

### 12.3 Supervised workflow test

Use a small fictional feature and temporary/test repository or explicitly approved
test issues:

1. Start the orchestrator in supervised mode.
2. Supply an architecture document and project instruction path.
3. Verify it performs gap analysis.
4. Verify it pauses at the documented checkpoints.
5. Verify the Feature Brief matches the issue-form fields.
6. Verify the proposed sub-issues cover all acceptance criteria.
7. Verify issue creation and parent/child links after confirmation.
8. Verify the parent task list contains linked child issues.

### 12.4 Autonomous workflow test

Start a fresh session with an explicit instruction to run end to end without
workflow-level intervention.

Verify:

- The orchestrator does not pause at its normal review checkpoints.
- It still honors platform permission prompts and project-level mandatory gates.
- It records assumptions instead of fabricating facts.
- It creates the Feature Brief and eligible sub-issues.
- It establishes available parent/child relationships.
- It produces a final audit summary.
- Rerunning after partial failure does not duplicate successfully created issues.

### 12.5 Specialist-agent tests

Verify that the Feature Brief and Sub-Issues agents can each run independently,
without the orchestrator, using the same skills and output contracts.

## 13. Acceptance criteria

- [x] Current official documentation has been checked and the chosen Copilot app
      plugin structure and tool identifiers are documented.
- [x] A versioned plugin manifest enables installation across projects.
- [x] A discoverable top-level workflow orchestrator exists.
- [x] Only the v2 Feature Brief and Sub-Issues planner behavior remains
      discoverable.
- [x] Feature Brief authoring rules are packaged as a reusable skill.
- [x] Sub-issue planning and authoring rules are packaged as a reusable skill.
- [x] Retained Ops planning rules are packaged as a reusable skill.
- [x] Agents accept user-provided architecture, project-instruction, guardrail,
      and authoring-guide paths.
- [x] The core system has no hard dependency on the source project's backend or
      infrastructure instructions.
- [x] Target-repository issue forms take precedence over valid bundled default
      contracts when present; this plugin repository does not publish those
      defaults as its own issue forms.
- [x] Supervised mode implements clear, non-repetitive checkpoints.
- [x] Explicit autonomous mode can run the complete workflow without normal
      workflow-level pauses.
- [x] Feature Brief issues are rendered and validated against the matching
      target form, or the bundled fallback contract if absent.
- [x] Agent and maintainer sub-issues are rendered and validated against their
      matching target forms, or bundled fallback contracts if absent.
- [x] Every Feature Brief acceptance criterion is traceable to at least one child
      issue or an explicitly documented unresolved item.
- [x] Child issues link textually to the Feature Brief and use native GitHub
      sub-issue relationships when supported. (Implemented; not live-verified.)
- [x] The Feature Brief task list is updated with created issue links.
      (Implemented; not live-verified.)
- [x] Partial GitHub write failures are reported and resumable without duplicate
      issue creation. (Implemented; not live-verified - see note below.)
- [ ] The installed plugin's workflow and skills are successfully discovered
      and smoke-tested in the GitHub Copilot app for a target project.
- [x] Concise user documentation explains how to run the orchestrator and each
      specialist agent.

Items marked *not live-verified* are fully specified and statically validated,
but no GitHub issue-write tooling or authorized test repository was available in
the implementation session, so they were never executed against a live
repository. See `Implementation decisions` for the manual smoke tests that
close this gap.

## 14. Expected usage after implementation

### Full supervised workflow

```text
Use the Agentic Feature Workflow in supervised mode.

Feature:
<describe the feature>

Architecture sources:
- docs/architecture.md
- docs/data-model.md

Project instructions and guardrails:
- <paths supplied by the user>

Additional authoring guidance:
- <paths supplied by the user>
```

### Full autonomous workflow

```text
Run the complete Agentic Feature Workflow autonomously, from architecture review
through Feature Brief and sub-issue creation. Do not pause at normal workflow
review checkpoints. Honor platform permissions and mandatory project guardrails.

Feature:
<describe the feature>

Architecture sources:
- docs/architecture.md

Project instructions and guardrails:
- <paths supplied by the user>
```

### Feature Brief stage only

```text
Use the Feature Brief Planner to analyze this feature. Read architecture from
<paths>, project instructions from <paths>, and authoring guidance from <paths>.
Use supervised mode.
```

### Decomposition stage only

```text
Use the Sub-Issues Planner for Feature Brief #<number>. Read project guardrails
from <paths>. Propose the atomic breakdown in supervised mode.
```

## 15. Non-goals

This integration does not:

- Implement the product features described by generated issues.
- Make current project-specific backend or infrastructure instructions portable.
- Bypass GitHub, organization, or Copilot security controls.
- Guarantee fully unattended operation when the platform requires tool approval.
- Replace GitHub issue forms with an unrelated issue schema.
- Require every repository to use the same architecture-document layout.
- Change the source project's files or install/overwrite target issue forms.

## 16. Definition of done for the implementing agent

Do not stop after generating proposed files. The implementation is complete only
when:

1. This plugin repository contains an installable, versioned plugin with
   app-compatible agents, skills, and generalized fallback contracts.
2. Obsolete planner profiles have not been imported as discoverable agents;
   staged migration copies remain explicitly non-discoverable.
3. Static validation passes.
4. Plugin installation and discovery in the GitHub Copilot app have been verified
   in a target project.
5. At least one supervised and one autonomous dry run has been completed as far
   as the available permissions safely allow.
6. Any platform limitation has a documented fallback that preserves validated
   issue output and an honest failure report.

## 17. Implementation decisions

Recorded during implementation (section 4 required this). Documentation was
checked against the live GitHub docs at implementation time.

### 17.1 Packaging

Agent Plugins 1.0: root `plugin.json` with
`$schema: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`,
`skills/<name>/SKILL.md`, and `com.github.copilot/agents/*.agent.md`.
Component paths are **fixed** in 1.0, so the legacy `agents`/`skills` manifest
fields are deliberately absent; including them would be an unknown top-level
field, silently ignored, and would suggest a layout the runtime does not use.
`scripts/validate_plugin.py` fails the build if one reappears.

### 17.2 Agent frontmatter

`description` is the only required property. Dropped from the staged profiles:

- `handoffs` - a VS Code concept, ignored on GitHub. Orchestration is expressed
  in prose plus the `agent` tool instead, so the orchestrator degrades to doing
  the work itself when subagent delegation is unavailable.
- `argument-hint` - ignored on GitHub.
- `infer` - retired.

The validator treats all three as errors so they cannot creep back.

### 17.3 `include-custom-instructions` is left unset

Enabling it would make the target repository's custom instructions
automatically authoritative, which contradicts section 5.2: the user's supplied
sources take precedence, and repository conventions are read explicitly and
cited. Agents read those files as ordinary sources instead.

### 17.4 Tool identifiers

The staged profiles' historical identifiers
(`github/github-mcp-server/issue_write`, `runSubagent`,
`github.vscode-pull-request-github/issue_fetch`) are not used. Current GitHub
MCP identifiers are `issue_read`, `issue_write`, `sub_issue_write`, `get_label`,
`search_issues`, and `list_issues`. `issue_write` with `create` accepts
`parent_issue_number`, which creates and attaches a sub-issue in one call and is
the preferred path.

Agents grant the aliases `read, search, web, todo, agent, execute` plus both
`github/*` and `github-mcp-server/*`, because the server's registered name
varies by host and unrecognized tool names are silently ignored. A documented
`gh` fallback covers hosts with no MCP server at all;
`feature-documentation-author` is read-only and is granted neither `execute` nor
`edit`.

**Sub-issue gotcha:** the REST `sub_issues` endpoint takes `sub_issue_id`, the
child's numeric database id - not its issue number, and not the GraphQL node id
that `gh issue view --json id` returns.

### 17.5 Agent disposition

- v1 planners: never imported.
- Ops planner: retained, generalized, backed by `ops-issue-authoring`.
- Documentation agent: retained with a real `name`/`description`, deliberately
  self-contained with no skill, because its workflow is not reused elsewhere
  (permitted by section 5.4).
- Generic coding agent: dropped as redundant with the built-in implementation
  agent.

### 17.6 Rule ownership

Skills are the single canonical home of every normative rule. `migration/`
stays an unmodified historical input and is excluded from all discoverable
component directories; the validator asserts this. Rules were generalized -
the misspelled `enhacement` label, the placeholder assignee, and every
AWS/DynamoDB/GraphQL/`AGENTS.md`/constitution reference were removed.

### 17.7 Issue forms and validation

Issue forms cannot be selected through the API, so bodies are rendered as
`### <field label>` blocks matching GitHub's own rendering of a submitted form.
Contracts are generated from the bundled YAML forms so the two cannot drift, and
the render path is standard-library only; PyYAML is needed only to extract a
contract from a target repository's form, with a documented manual fallback.
A field id absent from the contract is an error, not a warning, because its
content would otherwise be dropped silently.

`allowed-tools` is intentionally omitted from the skills so Copilot prompts
before running the bundled script; every skill documents a manual-validation
fallback for when shell access is denied.

### 17.8 Validation performed

- `scripts/validate_plugin.py` - 184 checks, 0 errors, 0 warnings: manifest
  schema and name rules, no legacy fields, agent and skill frontmatter, skill
  name/directory agreement, prompt size limit, every relative link, every
  referenced skill exists, contract provenance and origin resolution,
  contract/form pairing, no `.github/ISSUE_TEMPLATE/`, no obsolete agent.
- `scripts/smoke-test.sh` - 15 assertions: six deliberately broken copies of
  the plugin prove the validator actually fails, four contracts render valid
  bodies, and missing-required-field, unresolved-`[tbd]` and unknown-field-id
  inputs are all rejected; contracts confirmed to match their forms.

### 17.9 Not verified, and how to close the gap

No GitHub issue-write tooling and no authorized test repository were available
in the implementation session, and plugin discovery inside the Copilot app is
not machine-verifiable from a folder session. These remain manual smoke tests:

1. Install the plugin and confirm all five agents and five skills are listed.
2. In a scratch repository, run the orchestrator supervised end to end and
   confirm the checkpoints, the created parent issue, the linked children, the
   native sub-issue relationships, and the updated parent task list.
3. Repeat with an explicit autonomous instruction and review the audit trail.
4. Interrupt a run mid-creation, then resume it and confirm no duplicate issues
   are created.
5. Repeat step 2 in a repository that has its own feature/task issue forms, and
   confirm those forms - not the bundled defaults - governed the bodies.

Fallback if an MCP issue tool is unavailable: the `gh` commands in
`skills/github-issue-operations/references/github-cli-fallback.md` perform the
same operations, including the numeric-id lookup for sub-issue linking.
