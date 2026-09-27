---
name: github-issue-operations
description: Creates, links, and updates GitHub issues safely for planning workflows - tool selection, pre-write safety checks, dependency-aware creation order, native sub-issue relationships, textual backlinks, parent task-list updates, and resumable recovery from partial batch failures. Use whenever a planning agent is about to create or link GitHub issues.
---

# GitHub issue operations

This skill governs every GitHub write a planning agent performs. Planning agents
create and update **issues** only: never commits, branches, or pull requests.

## Tool selection

Resolve the write path once at the start of a run, then state which one you are
using. Tool identifiers change over time, so probe rather than assume.

1. **Native GitHub tools exposed to the client.** Prefer these.
2. **A GitHub MCP server available in the session.** As of the GitHub MCP
   server's current tool set, the relevant tools are:

   | Purpose | Tool | Key arguments |
   | --- | --- | --- |
   | Read an issue, its comments, labels, parent, or children | `issue_read` | `method`: `get`, `get_comments`, `get_labels`, `get_parent`, `get_sub_issues` |
   | Create or update an issue | `issue_write` | `method`: `create` or `update`; `owner`, `repo`, `title`, `body`, `labels`, `issue_number`, `parent_issue_number` |
   | Add, remove, or reorder a sub-issue | `sub_issue_write` | `method`: `add`, `remove`, `reprioritize`; `issue_number` (parent), `sub_issue_id` (child **numeric id**, not its number) |
   | Check a label exists | `get_label`, `list_label` | `owner`, `repo`, `name` |
   | Find probable duplicates | `search_issues`, `list_issues` | scoped to `owner`/`repo` |

   The server is commonly registered as `github`, so tools appear as
   `github/issue_write`. Some sessions register it under a different name; if
   the tools are not present under either the plain or the `github/` prefixed
   name, fall through to the next option rather than guessing identifiers.
3. **Authenticated `gh` CLI**, if the session exposes shell access and policy
   permits. See `references/github-cli-fallback.md`.

If none is available, do not pretend. Produce the validated title, labels, and
body for every issue, state clearly that **nothing was created**, and give the
user a copy-ready payload plus the exact blocker.

## Before any write

1. **Confirm the target `owner/repo` with the user.** Never infer it silently
   from the working directory.
2. **Verify every label exists.** Drop or substitute unknown labels and say so.
   Do not create labels unless the user asks.
3. **Reject placeholder data.** No example assignees, no project board ids, no
   unreplaced `<...>` title placeholders. Leave assignees empty unless the user
   named someone real.
4. **Validate the body** against its contract using `issue-form-contracts`.
5. **Check for likely duplicates** with a scoped search on the title's
   distinctive terms. Report candidates; in supervised mode ask before creating
   a probable duplicate, in autonomous mode record the decision in the audit.

## Creating the parent Feature Brief

Create it first. Immediately capture and keep:

- issue `number`
- issue numeric `id` (needed for `sub_issue_write`)
- `html_url`

Do not proceed to children until the parent's identifiers are recorded.

## Creating and linking sub-issues

Work in **dependency-aware order**: an issue that others depend on is created
before its dependents, so their bodies can reference real numbers.

For each child:

1. Render and validate the body against its class contract.
2. Include a **textual backlink** in the body, always — for example
   `Parent Feature Brief: #123`. Do this even when the native relationship
   succeeds, because the backlink survives tooling differences and shows in
   plain Markdown views.
3. Create the issue. Two equivalent paths:
   - `issue_write` with `method: create` **and** `parent_issue_number` set to
     the Feature Brief's number, which creates and attaches in one operation.
     Prefer this: it is atomic and avoids needing the child's numeric id.
   - Or create first, then `sub_issue_write` with `method: add`,
     `issue_number` = parent number, `sub_issue_id` = the **child's numeric id**
     from the create response. Passing the child's issue *number* here is the
     most common mistake; it will attach the wrong issue or fail.
4. Record the result in the ledger before moving on.

If native sub-issue relationships are unavailable, continue with textual
backlinks and the parent task list, and report exactly which children have no
native relationship so a human can attach them later.

## Updating the parent task list

After the batch, update the Feature Brief's Sub-Issue Index so each stub becomes
a linked reference, preserving its classification tag:

```markdown
- [ ] [human] #124 Decide the retention policy
- [ ] [agent] #125 Implement the export endpoint
- [ ] [tbd] Resolve the pagination model
```

Use `issue_write` with `method: update` and the full new body. Read the current
body first and edit only the index section — never overwrite unrelated content,
and never drop a stub that was not created; leave it unlinked and explain why.

## Resumable partial failure

Maintain a run ledger from the first write. See
`references/run-ledger.md` for the shape and the exact resume procedure.

Core rules:

- A failed issue never blocks the rest of the batch. Continue, then report.
- **Never recreate an issue that already succeeded.** Before any retry,
  reconcile: read the parent's existing children and the linked stubs in its
  index, and match on title.
- Report every failure with the class, intended title, the failing operation
  (create / link / parent update), and the error.
- End with a resume instruction precise enough that rerunning completes only the
  missing work.

## Honesty rules

- Report exactly what exists on GitHub, never what you intended to create.
- If a relationship, label, or parent update failed, say so explicitly rather
  than summarizing the run as successful.
- Permission prompts, policy blocks, and missing authentication are reported as
  blockers, never worked around.
