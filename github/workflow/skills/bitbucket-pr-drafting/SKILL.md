---
name: bitbucket-pr-drafting
description: 'Draft or update Bitbucket pull requests with Jira traceability, bounded diff summaries, test evidence, risks, and actionable review annotations.'
---

# Bitbucket Pull Request Drafting

Use this skill after the source branch exists remotely.

Resolve the repository, source branch, target branch, Jira issue, commit range, changed files, and repository pull-request template. Build the title and description from evidence, including purpose, implementation summary, affected services, tests run, configuration or migration notes, risks, rollback considerations, and Jira linkage.

Do not invent test results, reviewers, check status, or deployment safety. Mark missing evidence explicitly. Before creation, check whether an open pull request already covers the same source and target branches.

Creating, editing, commenting on, or assigning reviewers is an external mutation. Execute only with authorization through an authenticated provider. Return the provider's pull-request ID, URL, source and target commits, and mutation results.

