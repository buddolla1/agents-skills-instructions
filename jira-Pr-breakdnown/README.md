# Jira → Bitbucket implementation breakdown

The full workflow is split into small, independently testable steps. Complete and validate one step before moving to the next.

| Step | Scope | Status |
|---|---|---|
| 01 | Jira connectivity and read-only story retrieval | Implemented |
| 02 | Story normalization and acceptance criteria | Not started |
| 03 | Service catalog and repository selection | Not started |
| 04 | Architecture impact plan | Not started |
| 05 | Git worktree and branch preparation | Not started |
| 06 | Repository implementation and checks | Not started |
| 07 | Cross-service contract verification | Not started |
| 08 | Review and approval gate | Not started |
| 09 | Bitbucket commit, push, and pull requests | Not started |
| 10 | Jira result synchronization and recovery | Not started |

Start with [01-jira-connectivity/README.md](01-jira-connectivity/README.md). Step 1 performs no Jira writes.
