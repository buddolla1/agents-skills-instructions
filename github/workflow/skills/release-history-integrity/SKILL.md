---
name: release-history-integrity
description: 'Verify that an approved pull-request revision reached the intended target branch and release without unexpected commit or artifact drift.'
---

# Release History Integrity

Use this skill after merge or while preparing a release.

Resolve the approved pull-request head, source and target branches, merge strategy, resulting merge or squash commit, release range, and artifact provenance. Verify ancestry or patch equivalence according to the actual merge strategy. Confirm that required checks applied to the reviewed revision and identify unexpected commits introduced between approval, merge, and release.

For squash or rebase workflows, do not require commit-ID equality; compare provider metadata and patch contents. For merge commits, verify both parent relationships when available.

Return `passed`, `failed`, or `unknown` with commit identifiers and evidence. Do not change history, tags, branches, or releases as part of verification.

