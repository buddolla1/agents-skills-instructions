---
name: pull-request-approval-gate
description: 'Evaluate pull-request findings, tests, required checks, reviewer policy, and unresolved discussions to produce an evidence-backed approval recommendation.'
---

# Pull Request Approval Gate

Evaluate the actual pull-request head commit so stale results cannot approve a newer revision.

Collect required checks and their states, review findings, required reviewer count or groups, unresolved tasks and discussions, test evidence, and repository-specific merge policy. Return:

- `approve` only when all required evidence passes and no blocking finding remains
- `request_changes` when a confirmed blocker or required check fails
- `needs_human_review` when policy demands a person or evidence is incomplete or ambiguous

Include the evaluated head commit and reasons for the decision. Static analysis cannot substitute for mandatory human review, runtime tests, or provider branch restrictions.

An approval recommendation is not permission to submit an approval or merge. Perform provider mutations only when explicitly requested and authorized, and never let an agent approve its own changes when policy prohibits it.

