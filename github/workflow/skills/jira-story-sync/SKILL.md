---
name: jira-story-sync
description: 'Read, normalize, comment on, or transition Jira stories for an engineering workflow when an authenticated Jira integration is available.'
---

# Jira Story Sync

Use this skill when engineering work must be traced to a Jira issue.

## Read

Resolve the exact site, project, and issue key. Fetch only fields needed for the task: summary, description, acceptance criteria, status, issue type, priority, labels, links, assignee, and relevant comments. Preserve Jira text separately from any normalized interpretation.

## Mutate

Comments, field updates, assignments, and transitions are external mutations. Confirm the exact issue and intended change, retain the user's authorization boundary, and execute only through an authenticated Jira tool or API. Do not infer a valid transition name; inspect available transitions first.

For completion transitions, require evidence appropriate to the workflow, such as the merged commit, deployment identifier, environment, and passed health decision. If the connector is unavailable or evidence is incomplete, return `blocked` and a precise missing prerequisite.

Never report an update from a proposed payload alone. Record the resulting issue key, new status or comment identifier, and provider response.

