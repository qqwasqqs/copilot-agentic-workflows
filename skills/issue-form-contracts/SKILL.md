---
name: issue-form-contracts
description: Resolves which issue-form contract governs a GitHub issue body, renders a validated Markdown body from field values, and supplies generalized default contracts for Feature Brief, agent task, maintainer task, and ops task issues. Use whenever an issue body must match a repository's issue form, or when no matching form exists and a portable default is needed.
---

# Issue-form contracts

GitHub issue forms drive the web submission UI. Programmatic issue creation
through the API, MCP, or `gh` takes a **title, labels, and a Markdown body**.
This skill defines how form-aligned content becomes a valid Markdown body, and
which contract wins when a repository has its own forms.

Never assume you can select an issue form through the API. Always render a body.

## Contract precedence

For each issue class — `feature-brief`, `agent-task`, `maintainer-task`,
`ops-task` — resolve the governing contract in this order:

1. **Target-repository form.** Look in the target repository for
   `.github/ISSUE_TEMPLATE/*.yml` / `*.yaml` (also accept `.github/issue_template/`
   on case-sensitive hosts). A form matches a class when its filename, `name`,
   or `title` prefix clearly corresponds to it. If a match exists, **it is
   authoritative** for field labels, ordering, required fields, dropdown
   options, title pattern, and default labels.
2. **Bundled default.** If no target form matches, use this skill's default in
   `contracts/<class>.contract.json`.

Record which contract you used for every issue you render, and say so in your
report: `contract: feature-brief (target-repository: .github/ISSUE_TEMPLATE/feature-brief.yml)`
or `contract: feature-brief (bundled-default)`.

Rules:

- Never write, install, overwrite, or "sync" issue forms into the target
  repository. The bundled forms in `forms/` exist so a maintainer can adopt them
  deliberately, not so an agent can install them.
- When a target form exists but is missing a field the plugin usually produces,
  fold that content into the closest existing field rather than inventing a
  field the form does not have.
- When a target form has extra required fields, you must fill them. If you
  cannot, mark them `[tbd]` and raise it as an open question.
- Mixed resolution is normal and fine: a repository may define a Feature Brief
  form but no ops form.

## Bundled defaults

| Class | Contract | Readable form | Default labels |
| --- | --- | --- | --- |
| `feature-brief` | `contracts/feature-brief.contract.json` | `forms/feature-brief.yml` | `enhancement`, `feature-brief` |
| `agent-task` | `contracts/agent-task.contract.json` | `forms/agent-task.yml` | `agent`, `atomic` |
| `maintainer-task` | `contracts/maintainer-task.contract.json` | `forms/maintainer-task.yml` | `maintainer`, `needs-design` |
| `ops-task` | `contracts/ops-task.contract.json` | `forms/ops-task.yml` | `ops`, `chore` |

The `contracts/*.json` documents are generated from the `forms/*.yml` files and
are the machine-readable source for rendering. The defaults are deliberately
technology-neutral: no cloud provider, language, framework, assignee, or project
board is assumed. Always verify labels exist in the target repository before
applying them, and drop or substitute any that do not.

## Contract document shape

```json
{
  "contract_id": "feature-brief",
  "version": "1.0.0",
  "source": "bundled-default",
  "origin": "skills/issue-form-contracts/forms/feature-brief.yml",
  "title_pattern": "Feature: <name>",
  "labels": ["enhancement", "feature-brief"],
  "fields": [
    {
      "id": "rationale",
      "label": "Rationale & Goals",
      "type": "textarea",
      "required": true,
      "description": "Why this matters and what observable success looks like."
    }
  ]
}
```

Field types are `textarea`, `input`, `dropdown`, and `checkboxes`. `markdown`
blocks are authoring help only and never appear in a rendered body.

## Rendering rule

A rendered body is, for every field that has content, in contract order:

```markdown
### <field label>

<field value>
```

separated by a blank line. Omit optional fields with no content. This matches
how GitHub renders a submitted issue form, so bodies stay consistent whether a
human used the web form or an agent created the issue programmatically.

## Deterministic validation

Use the bundled script rather than eyeballing a body. It needs no third-party
packages for rendering.

```bash
python3 scripts/issue_contract.py render \
  --contract contracts/feature-brief.contract.json \
  --values /tmp/feature-brief.values.json
```

`values.json`:

```json
{
  "title": "Feature: scheduled report export",
  "labels": ["enhancement", "feature-brief"],
  "fields": { "rationale": "...", "scope": "...", "acceptance": "..." }
}
```

The command prints a JSON result with `valid`, `title`, `labels`, `body`,
`tbd_fields`, `errors`, and `warnings`, and exits non-zero when validation
fails. It checks required fields, dropdown values against allowed options,
unreplaced placeholder text such as `<name>` or `your-username`, and it reports
every `[tbd]` marker. A field id that is not in the contract is an **error**,
not a warning, because its content would otherwise be silently dropped from the
issue — map it onto a real field or remove it. Pass `--require-no-tbd`
when the user has asked for a brief with no unresolved markers.

Feed `title`, `labels`, and `body` straight into the issue-creation tool. Never
create an issue from a body that failed validation — fix it or report the
blocker.

Running this script requires shell access, and Copilot will ask for
confirmation. If shell use is denied or unavailable, perform the same checks by
reading the contract directly, and say in your report that validation was
manual rather than script-verified.

## Extracting a target-repository contract

When a target form exists, convert it once:

```bash
python3 scripts/issue_contract.py extract \
  --form .github/ISSUE_TEMPLATE/feature-brief.yml \
  --contract-id feature-brief \
  --out /tmp/feature-brief.contract.json
```

### Manual contract extraction

`extract` needs PyYAML and will fail clearly without it. In that case read the
form yourself and write an equivalent contract JSON by hand: take each `body`
entry whose `type` is `textarea`, `input`, `dropdown`, or `checkboxes`, and
record its `id`, `attributes.label`, `type`, `validations.required`, and (for
dropdowns) `attributes.options`. Skip `markdown` entries. Then render and
validate as usual. State in your report that the contract was extracted
manually.
