# Run ledger and resumable recovery

Keep a ledger in your working context from the first GitHub write. It turns a
partially failed batch into a resumable state instead of a guess.

## Shape

| # | Class | Title | Status | Issue | Id | Linked | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | feature-brief | Feature: scheduled report export | created | #123 | 2841… | n/a | parent |
| 2 | maintainer-task | Decide the retention policy | created | #124 | 2841… | native | |
| 3 | agent-task | Implement the export endpoint | created | #125 | 2841… | backlink only | sub_issue_write denied |
| 4 | agent-task | Add export scheduling job | failed | — | — | — | 403 on create |
| 5 | tbd | Resolve the pagination model | skipped | — | — | — | preserved in parent index |

`Status` is one of `pending`, `created`, `failed`, or `skipped`.
`Linked` is one of `native`, `backlink only`, or `failed`.

## Rules during a run

- Write the row **immediately** after each operation returns, before the next
  one starts. A crash between operations must not lose an issue number.
- A failure never aborts the batch. Mark it `failed`, keep going.
- Track the parent task-list update as its own final row.

## Reconciling before a retry

Never recreate an issue that already exists. Before retrying:

1. Read the parent's existing children (`issue_read` with
   `method: get_sub_issues`, or the sub-issues REST endpoint).
2. Read the parent body's Sub-Issue Index for already-linked references.
3. Search the target repository for open issues whose titles match the intended
   titles of `failed` rows.
4. Treat any match as already created: fix only what is missing — the native
   relationship, the backlink, or the parent index entry.

Only rows with no match anywhere are recreated.

## Resume instruction

End every run that had failures with a concrete instruction, for example:

> Resume: Feature Brief #123 exists with children #124 and #125. Sub-issue 4
> ("Add export scheduling job") failed to create with HTTP 403, and #125 has a
> textual backlink but no native sub-issue relationship. Rerun the Sub-Issues
> Planner against #123 asking it to create only the missing child and attach
> #125. Do not recreate #124 or #125.

The instruction must name the parent, what exists, what is missing, and what
must not be repeated.
