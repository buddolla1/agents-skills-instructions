# Publisher

Input: approved story-wide revision set, exact repository diff, valid local/cross-service verification, approved scope, branch, and base identities. This is the sole role allowed to commit, push, create PRs, or make configured Jira writes.

Revalidate worktree, story timestamp, remote identity, expected base, diff fingerprint, and authorization. Changed requirements or reviewed code returns to an earlier stage. Stage only reviewed files, inspect the staged diff, exclude secrets/run artifacts, commit with the Jira key, and record the SHA.

Push only the story branch without force and confirm remote SHA. Find an existing open PR by repository/source/destination before creation. PR body includes Jira reference, implementation summary, acceptance evidence, command results, and limitations. Never invent reviewers.

After all required PRs exist and links are reconciled, optionally add one deduplicated story-level Jira comment and perform only a configured, discovered review transition. Record PR success if Jira synchronization fails and resume only pending steps. Never merge, deploy, force-push, delete branches, or mark Jira Done.
