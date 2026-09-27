# GitHub CLI fallback

Use this only when no native tool and no MCP server can write issues, the
session exposes shell access, and policy permits it. Confirm with the user in
supervised mode before the first command.

Scope limit: `gh issue` and `gh api` calls against issues in the confirmed
target repository. Nothing else. No `git`, no `gh pr`, no repository or workflow
mutation.

## Check authentication first

```bash
gh auth status
```

If this fails, stop and report the blocker. Do not attempt to authenticate on
the user's behalf.

## Create an issue

```bash
gh issue create --repo OWNER/REPO \
  --title "Feature: scheduled report export" \
  --label enhancement --label feature-brief \
  --body-file /tmp/feature-brief.body.md
```

Always use `--body-file` with a file written from the validated render output.
Passing long Markdown inline mangles fenced code blocks and checkbox lines.

Capture the returned URL, then read back the identifiers you need:

```bash
gh issue view 123 --repo OWNER/REPO --json id,number,url,title
```

`id` here is the GraphQL node id. The sub-issues REST endpoint needs the
**numeric database id**, which you get from:

```bash
gh api repos/OWNER/REPO/issues/124 --jq '.id'
```

## Attach a sub-issue

```bash
gh api --method POST repos/OWNER/REPO/issues/123/sub_issues \
  -f sub_issue_id=NUMERIC_ID_OF_CHILD
```

`123` is the **parent issue number**; `sub_issue_id` is the child's numeric
database id, not its issue number. Related endpoints:

```bash
gh api repos/OWNER/REPO/issues/123/sub_issues        # list children
gh api repos/OWNER/REPO/issues/124/parent            # read the parent
```

## Update the parent body

```bash
gh issue edit 123 --repo OWNER/REPO --body-file /tmp/feature-brief.body.updated.md
```

Read the current body first (`gh issue view 123 --json body --jq '.body'`),
modify only the Sub-Issue Index section, and write the complete new body.

## Verify labels exist

```bash
gh label list --repo OWNER/REPO --json name --jq '.[].name'
```

## Reporting

Whenever this fallback is used, say so in the final report: which operations
went through `gh`, and whether the account was authorized for writes.
