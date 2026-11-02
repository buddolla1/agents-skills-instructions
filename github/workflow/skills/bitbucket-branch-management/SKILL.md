---
name: bitbucket-branch-management
description: 'Create and verify Jira-linked Git branches in Bitbucket repositories while preserving local work, branch policy, and history safety.'
---

# Bitbucket Branch Management

Use this skill for story-linked branch creation or verification.

Resolve the repository, remote, target base branch, issue key, branch naming convention, and base commit before changing state. Inspect the worktree and never discard, overwrite, or hide unrelated local changes.

Prefer the repository's documented naming convention. If none exists, propose `feature/<issue-key>-<short-slug>` and show the resolved name before creating it. Check that the branch does not already exist locally or remotely and handle an existing branch explicitly rather than silently resetting it.

Create or push only with user authorization and authenticated Git or Bitbucket access. Do not force-push or rewrite shared history. Verify success by resolving the local and remote branch commit IDs and report both.

