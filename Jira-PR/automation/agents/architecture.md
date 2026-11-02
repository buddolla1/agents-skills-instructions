# Cross-service architecture

Input: normalized story, registered catalog, mandatory user-selected service list, and read-only repository access.

Use explicit service-list mode only. Never infer scope from Jira, scan all catalog repositories, or add repositories automatically. A resumed run reuses saved selection unless the user explicitly changes it. Read relevant API specifications, event schemas, client calls, configuration, and code. Record dependency source file and revision. Separate confirmed dependencies, hypotheses, and unknowns. If selected code references an unselected service, report only evidence in selected repositories and ask the user to add it when required. An unresolved required dependency blocks readiness.

Classify each selected service as `CHANGE_REQUIRED`, `VERIFY_ONLY`, `UNAFFECTED`, or `UNKNOWN`. For changed repositories map acceptance criteria, planned changes, affected consumers/providers, tests, and rationale. Verify-only services receive compatibility tests but no gratuitous branch or PR. Missing access or uncertain material impact blocks the affected gate.

Produce coding, merge, and deployment order and identify cycles. Prefer backward-compatible contract evolution; breaking or cyclic changes need an explicit migration strategy. Record rollout/rollback notes without deploying. Output `impact-plan.json` and a concise summary with source evidence and catalog version. Freeze it before worktree preparation; scope changes invalidate affected plans and approvals.
