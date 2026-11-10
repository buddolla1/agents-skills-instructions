# Orchestrator Agent — Annotated Architecture, Section Explanations & Recommendations

**Source:** 21 screenshots of `agents/orchestrator.agent.md`, approximately lines 1–768.  
**Document type:** Architecture review and proposed improvement guide; **not** a verbatim reconstruction of the original agent.  
**Review status:** Screenshot-based; referenced contracts, scripts, and individual agent definitions have not been inspected.

## How to use this document

Each section explains **Observed design**, **Why it exists**, **Assessment**, and **Recommendation**. Where screenshots are incomplete or text is obscured, details are marked **verify in source**. Do not replace the existing agent file with this review: use it to guide changes after validating the linked contracts and scripts.

## 1. Executive summary

The orchestrator is a permanent coordination role that classifies requests, chooses predefined or custom agent chains, delegates specialized work, validates outputs, handles failures, persists workflow state, and coordinates Git/Bitbucket operations. Its strongest qualities are role separation, explicit gates, recovery, traceability, and specialist integration. Main concerns are conflicting chain rules, repeated policies, overly broad automatic mutation, fragile result parsing, non-atomic concurrency checks, and potential token overhead.

**Prioritized actions:**
1. Reconcile workflow-specific chains with global analysis requirements.
2. Define completion requirements per workflow (including no-PR micro-workflows).
3. Enforce permissions, state transitions, concurrency, and idempotency in deterministic tooling.
4. Validate structured agent results rather than extracting the last JSON fence.
5. Reduce repeated prompt instructions and unnecessary specialist invocations.
6. Instrument actual per-agent token, latency, and retry metrics before quantifying savings.

## 2. Front matter and tool permissions (approximately lines 1–5)

**Observed design:** YAML front matter names `Orchestrator`, describes coordination duties, and enables tools including `vscode`, `execute`, `read`, `agent`, `edit`, `search`, `web`, and `todo`.

**Why:** Establishes role identity and available capabilities.

**Assessment:** Broad tool access may conflict with the rule that the orchestrator must not edit implementation files or execute validation.

**Recommendation:** Restrict tool access where platform support permits. Where restriction is unavailable, enforce command/file policies through dispatch wrappers and audit logs. Document which commands are coordination-only.

## 3. First Line of Defense (approximately lines 7–15)

**Observed design:** Never edit files as orchestrator; never skip analysis; never directly run validation; read shared contract.

**Why:** Prevents role drift and skipped quality gates.

**Assessment:** Valuable guardrail, but 'never skip analysis' conflicts with some workflow diagrams that omit explorer or architect.

**Recommendation:** Define analysis requirements per selected workflow. Retain a short non-negotiable summary here and link to one canonical policy.

## 4. Hard Stop Protocol and HALT rules (approximately lines 16–37)

**Observed design:** HALT-1 through HALT-8 cover unauthorized editing, user corrections, missing analysis, direct validation, analysis traps, invalid routing, iteration limits, and missing correlation context for Git operations.

**Why:** Stops unsafe or invalid actions before execution.

**Assessment:** Strong conceptual defense. Natural-language instructions alone cannot guarantee enforcement. Numbering and references must be verified against `shared/contract.md`.

**Recommendation:** Implement gate checks as machine-enforced preconditions with stable IDs, severity, error codes, and remediation instructions. Keep the full specification in `contract.md`; avoid copying it across files.

## 5. Pre-Work Chain Quick-Check (approximately lines 40–49)

**Observed design:** Checklist before analysis, tests, edits, next-agent routing, fix loops, Git mutations, and workflow startup.

**Why:** Converts policy into an operational preflight.

**Assessment:** Useful but repeats HALT and mandatory delegation rules.

**Recommendation:** Replace repeated prose with a concise preflight decision table that invokes deterministic gate checks. Distinguish new workflows from resumed workflows.

## 6. Purpose, scope, role permanence (approximately lines 51–74)

**Observed design:** Coordinator role remains permanent even when a request is simple or involves editing its own Markdown file. Delegation is preferred for specialist work.

**Why:** Prevents the orchestrator from becoming an implementer.

**Assessment:** Good separation of concerns; 'always delegate' may be excessive for pure coordination and answer-only requests.

**Recommendation:** Define a clear whitelist of permitted coordination actions and a separate list of specialist-only actions. A user correction should trigger reclassification, not automatically rerun the entire workflow.

## 7. Post-delegation waiting and role boundaries (approximately lines 75–82)

**Observed design:** Set `WAITING_FOR`, do not perform delegated work, and interpret user follow-ups in the context of the delegated agent.

**Why:** Avoids duplicate work and role confusion.

**Assessment:** Waiting must not prevent handling cancellation, errors, or a completed agent result.

**Recommendation:** Use explicit `pending_dispatch_id`, `agent_id`, and allowed events (`completed`, `failed`, `cancelled`, `user_changed_scope`).

## 8. Agent Registry — Analysis (approximately lines 83–95)

**Observed design:** `code-explorer` → `code-architect` → `planner`, marked as read-only.

**Why:** Discovery, architecture, and sequencing precede implementation.

**Assessment:** Appropriate for complex work; potentially costly for minor changes. Other workflow mappings omit stages.

**Recommendation:** Specify analysis tiers (minimal, standard, full) or declare each workflow's required sequence as authoritative. Record reasons when an agent is skipped.

## 9. Agent Registry — Implementation (approximately lines 96–114)

**Observed design:** Default `tdd-guide`; specialized build resolvers, `code-simplifier`, `refactor-cleaner`, `performance-optimizer`, `ally-arch`, and `doc-updater` are visible.

**Why:** Assigns code and document mutations to suitable specialists.

**Assessment:** Good specialization. Agent selection can overlap (e.g., simplification vs refactoring).

**Recommendation:** Give each agent explicit triggers, exclusions, expected artifacts, and a deterministic tie-break rule. Confirm agent names against actual files.

## 10. Review Registry and language detection (approximately lines 115–139)

**Observed design:** Language reviewer selected by changed extension (`typescript-reviewer`, `java-reviewer`, `kotlin-reviewer`, `python-reviewer`, or `code-reviewer`); `security-reviewer` follows; optional `silent-failure-hunter`, `pr-test-analyzer`, `database-reviewer`. Mixed-language changes get multiple language reviews plus cross-cutting review.

**Why:** Ensures language-specific validation and targeted quality checks.

**Assessment:** Strong coverage, but always running every reviewer can increase latency. A blanket security review may be required by policy.

**Recommendation:** Define mandatory versus risk-triggered reviews, preserve security minimums, and run independent reviewers in parallel only if state/logging supports it. Use actual changed-file manifests, not only extensions, to determine scope.

## 11. Reviewer verdict aggregation (approximately lines 140–157)

**Observed design:** Reclassifies `FAIL` when all blocking findings are unverified, then aggregates `FAIL`, `PASS`, and `WARN` across reviewers. `fix_category` routes failures.

**Why:** Prevents unsupported findings from blocking execution while preserving actionable failures.

**Assessment:** Potentially dangerous if 'unverified' findings are silently treated as passes. The exact reclassification text is partially obscured.

**Recommendation:** Preserve original verdict, evidence status, and normalized verdict separately. Treat unresolved high-severity security findings as requiring investigation, not automatic pass. Make aggregation a pure tested function.

## 12. Skill registry and out-of-scope operations (approximately lines 158–192)

**Observed design:** Domain skills include Jira, Bitbucket, Confluence, Jenkins, Splunk, Figma, Whimsical, OrgMaster, browser, commit, and deep research. Outlook/Teams are out of scope. Destructive operations such as PR merges, page deletion, comment deletion, and repository deletion are excluded.

**Why:** Separates domain integrations from reasoning and blocks destructive operations.

**Assessment:** Clear capability boundaries; risk of stale skill descriptions as tools evolve.

**Recommendation:** Keep a versioned skill manifest with operation names, permissions, and side-effect classes (`read`, `local_write`, `remote_write`, `destructive`). Verify exclusions in tool implementations.

## 13. Responsibilities and responsibility boundaries (approximately lines 193–222)

**Observed design:** Classify intent, choose agents, minimize delegation, compose handoffs, chain outputs, flag contradictions, route failures, synthesize executed outputs, enforce mutation safety, and coordinate Git through skills. Responsibility table assigns discovery, planning, implementation, validation, build fixes, branches, commits, and PRs.

**Why:** Avoids duplicated ownership and fabricated analysis.

**Assessment:** Good boundaries, but later direct Git-command permissions blur skill ownership.

**Recommendation:** Use a responsibility matrix with one owner per operation and explicit allowed orchestration calls. Distinguish 'request Git operation' from 'execute Git operation'.

## 14. Context chain, scope mapping, error recovery (approximately lines 223–246)

**Observed design:** Handoffs carry upstream outputs; `code-explorer` receives an intent-based `analysis_scope`, not `all`. Tool failures use normalized status and logger failure records; blocked subtypes are derived from execution blocks.

**Why:** Controls scope and makes retries actionable.

**Assessment:** Intent-based scope is especially valuable for token efficiency.

**Recommendation:** Standardize a compact handoff schema: goal, scope, relevant files/symbols, evidence references, decisions, risks, next action. Store large artifacts by reference rather than repeating them.

## 15. Chain trace log, recovery and context-loss detection (approximately lines 247–269)

**Observed design:** Correlation IDs; persisted `.agents-state/logs/<correlationId>/`; recovery when ID, chain position, prior results, or decisions are missing; Git state checks.

**Why:** Enables resumable execution after long sessions or context compression.

**Assessment:** Strong. Recovery should not accidentally repeat completed mutations.

**Recommendation:** Make persisted state authoritative. On resume, verify branch/HEAD, agent outputs, outstanding decisions, and operation receipts; reconcile before retrying.

## 16. Confidence aggregation, dispatch guard and iteration memory (approximately lines 270–289)

**Observed design:** Confidence thresholds referenced from contract; dispatch command blocks implementation if analysis outputs are missing; iteration memory and bounded loops.

**Why:** Prevents unsupported implementation and infinite retries.

**Assessment:** Useful, but confidence scores can appear precise without calibration.

**Recommendation:** Combine confidence with evidence coverage and explicit unknowns. Count repeated failure signatures separately from progress-making retries. Emit reason codes for escalation.

## 17. Predefined workflows and chain mappings (approximately lines 290–365)

**Observed design:** Named workflows include `init`, `feature-development`, `bug-fix`, `code-review`, `code-only`, `test-only`, `troubleshoot`, `analyze-improve`, plus visible `docs`, `commit-push`, and `pr-update`. Several route to commit and Bitbucket skills.

**Why:** Gives repeatable, task-specific paths.

**Assessment:** Inconsistency: global full-analysis requirement vs workflows omitting stages. Some read-only paths do not need Git operations.

**Recommendation:** Make the workflow registry the source of truth for required agents, optional reviewers, permitted mutations, terminal artifacts, and completion conditions. Keep the human-readable chain diagram generated from the registry.

### Visible workflow examples (illustrative transcription)

| Workflow | Visible chain / behavior | Check |
|---|---|---|
| feature-development | explorer → architect → planner → TDD → language review → security → commit → Bitbucket | Full chain |
| bug-fix | explorer → planner → TDD → language review → security → commit → Bitbucket | Architect omitted |
| code-review | language review → security → code review → synthesis | Read-only |
| code-only | planner → TDD → language review → security → commit → Bitbucket | Explorer omitted |
| test-only | planner → TDD → PR test analyzer → language review → commit → Bitbucket | Verify validation policy |
| troubleshoot | explorer → build resolver (if needed) → language review → commit/Bitbucket only if changed | Dual exit |
| analyze-improve | explorer → architect → synthesis | Read-only |
| docs | planner → doc-updater → code-reviewer → commit → Bitbucket | Doc-specific checks |
| commit-push | language review → commit → Bitbucket push only | No PR |
| pr-update | explorer → planner → TDD → language review → security → commit → Bitbucket | Existing PR handling |
| init | explorer → synthesis, generating guidance files | Verify ownership of file creation |

## 18. Workflow disambiguation (approximately lines 366–385)

**Observed design:** Ticket + implement → feature development; ticket + fix → bug fix; PR + review → code review; PR + address comments → PR update; stack trace → troubleshoot; no-code analysis → analyze-improve; commit/push intent → commit-push; documentation-only targets → docs. Prefer more specific workflow; ask when still ambiguous.

**Why:** Reduces misrouting.

**Assessment:** Good foundation. Keyword-only routing can misclassify mixed requests.

**Recommendation:** Use intent, target artifact, requested side effects, ticket/PR references, and ambiguity confidence together. Confirm only materially ambiguous or high-risk actions.

## 19. Custom chain composition (approximately lines 386–396)

**Observed design:** Analysis precedes implementation; review follows mutation; omit unneeded agents but retain order.

**Why:** Supports tasks outside predefined workflows.

**Assessment:** Conflicts with statements that full analysis chain is always required.

**Recommendation:** Establish one precedence rule: global safety invariants > workflow-specific required chain > optional specialists > custom composition. Never let custom composition bypass enforced gates.

## 20. Micro-workflows and commit-push resume (approximately lines 397–417)

**Observed design:** `commit-push`, `replay`, and `show-trace` are FSM-exempt; commit-push resume inspects staged, committed, and pushed state.

**Why:** Avoids heavyweight lifecycle overhead for narrow operations.

**Assessment:** Sensible optimization, but 'FSM-exempt' must not mean unaudited or unauthorized. Restart-from-scratch could duplicate side effects.

**Recommendation:** Use a minimal auditable micro-workflow state model; reconcile receipts before retrying. Explicitly prohibit replay from performing mutations.

## 21. Workflow FSM and full autonomy (approximately lines 418–449)

**Observed design:** Logger FSM is canonical. Full autonomy routes through agents and Git/PR steps without user pauses; analysis display is informational. Reviewer failure routes to fixes.

**Why:** Enables end-to-end autonomous work.

**Assessment:** Efficient when explicitly authorized, risky if interpreted as blanket permission.

**Recommendation:** Bind each workflow to an authorization profile (read-only, edit, local commit, remote push, PR create). Enforce protected-branch and destructive-operation policies in tools. Preserve cancellation and escalation paths.

## 22. Analysis display checkpoint (approximately lines 450–480)

**Observed design:** Displays understanding, config/patterns, affected files, plan, risks, confidence, then continues automatically.

**Why:** Keeps users informed without pausing.

**Assessment:** Clear and useful; detailed outputs may be redundant if repeated verbatim later.

**Recommendation:** Make the display concise, sourced from persisted analysis outputs; provide a reference to full findings rather than duplicating them.

## 23. Auto-commit/push/PR sequence and idempotency (approximately lines 481–527)

**Observed design:** Stage, commit, push, create PR if none exists; skip empty commits and in-sync pushes; post rich completion summary.

**Why:** Automates final delivery and avoids common duplicates.

**Assessment:** Requires authorization and race-safe checks. A PR may exist but be closed, wrong target, or tied to an old branch state.

**Recommendation:** Check exact source/target branch and PR state; persist operation receipts; make commit/push/PR idempotent where possible. Do not infer success solely from command execution attempts.

## 24. Human-in-the-loop enforcement (approximately lines 528–538)

**Observed design:** Refers to canonical pre-auto-commit verification checklist; heading says 'NEVER BYPASS'.

**Why:** Ensures governance before remote mutations.

**Assessment:** Wording appears to conflict with zero-pause full autonomy unless the checklist is automated or authorization is obtained earlier.

**Recommendation:** Clarify which conditions require explicit human approval and which can be automatically verified. Treat user authorization as a precondition, not an optional prompt.

## 25. FSM enforcement and Definition of Done (approximately lines 539–557)

**Observed design:** Transitions use logger commands; abort supported; iteration count increments on validation loops. Completion requires agents, reviews, commit/push/PR, no unresolved decisions, and state consistency.

**Why:** Prevents premature success reporting.

**Assessment:** A universal PR requirement conflicts with `commit-push` (push-only) and read-only workflows.

**Recommendation:** Define per-workflow terminal criteria, such as `analysis_report`, `local_commit`, `remote_push`, `open_pr`, or `no_change`. Separate workflow execution success from external merge approval.

## 26. Delegation protocol and execution modes (approximately lines 558–573)

**Observed design:** Gate check → mode → compose → dispatch → parse → persist → validate → route; autonomous and inline agent modes.

**Why:** Standardizes agent invocation.

**Assessment:** Good protocol; multiple procedural references can be difficult to keep synchronized.

**Recommendation:** Put canonical dispatch behavior in a single tested dispatcher. Use the agent file for intent and constraints, not step-by-step shell orchestration.

## 27. Role-switch logging anchors and two-tier outputs (approximately lines 574–616)

**Observed design:** Log dispatch on role entry and completion on exit. Uses role buckets (`Analyzer`, `Implementor`, `Reviewer`, `Orchestrator`), individual sub-agent tags, per-agent raw Markdown, and compressed role handoff files.

**Why:** Supports auditability and context-efficient handoffs.

**Assessment:** Excellent two-tier model, but manual tagging can create identity mismatches and dangling events.

**Recommendation:** Dispatcher should assign immutable `dispatch_id`, `role`, `agent_id`, and output paths automatically. Write events and output files atomically or recoverably. Keep full raw output separate from compact handoffs.

## 28. Post-return routing and structured result parsing (approximately lines 617–625)

**Observed design:** Verify chain completeness, persist outputs, parse the last JSON code block, and route according to execution status.

**Why:** Converts specialist results into the next workflow decision.

**Assessment:** Parsing the last fenced JSON block is fragile.

**Recommendation:** Require a validated result schema with fields such as `dispatch_id`, `agent_id`, `status`, `changed_files`, `findings`, `evidence`, `validation`, `next_action`, and `fix_category`. Reject malformed outputs without silently guessing.

## 29. Execution rules, workflow bootstrapping and logger calls (approximately lines 626–665)

**Observed design:** Check for active workflows; initialize logger and branch gate; log transitions, dispatches and completions; verify chain completeness; route reviews and Git operations.

**Why:** Makes the workflow auditable and recoverable.

**Assessment:** Many commands are repeated from earlier sections. A broad 'present output verbatim' rule undermines compressed handoffs.

**Recommendation:** Replace command-by-command repetitions with a single canonical dispatcher procedure. Show concise summaries by default; preserve full raw reports in logs or on request.

## 30. Mandatory delegation and allowed coordination commands (approximately lines 666–685)

**Observed design:** File edits, tests, validation, and package-manager mutations are delegated. Orchestrator may read, discover files, inspect Git, run logger commands, write workflow logs, and apparently run certain Git mutations.

**Why:** Protects role separation.

**Assessment:** Direct Git permissions overlap with skills' stated ownership.

**Recommendation:** Resolve the ownership conflict: allow only designated skills/CLI wrappers to mutate Git; keep read-only inspection and logger coordination with the orchestrator. Explicitly list exceptions, if any.

## 31. Required input and synthesis outputs (approximately lines 686–716)

**Observed design:** Accepts natural-language or structured requests, optional workflow/ticket/PR flags. PR synthesis includes summary, changed files, testing, tradeoffs, risks, and uncertainties. Evidence verification is required after reviews.

**Why:** Produces consistent, useful delivery reports.

**Assessment:** Strong output contract, but evidence must come from actual agent/tool results.

**Recommendation:** Require links or IDs to test runs, commits, PRs, and reviewer evidence. Mark unavailable data as not verified rather than inventing outcomes.

## 32. Analysis-only synthesis (approximately lines 717–730)

**Observed design:** Analysis summary, categorized findings, prioritized recommendations with S/M/L effort, risks, and next steps.

**Why:** Separates informational workflows from mutation workflows.

**Assessment:** Appropriate.

**Recommendation:** Add confidence/evidence per finding and distinguish observations from hypotheses. Do not force Git or PR requirements for read-only analysis.

## 33. Decision boundaries (approximately lines 731–735)

**Observed design:** One-agent requests can delegate immediately; contradictions go to user; failures route to fix mode; unmatched requests use custom chains; duplicates are checked; implemented changes go to review; waiting agents remain owners.

**Why:** Clarifies ambiguous edge cases.

**Assessment:** 'Delegate immediately' must still respect gates. 'Promote to completed after review' conflicts with Git-required completion.

**Recommendation:** Replace ambiguous prose with state-based decisions and workflow-specific completion checks. Escalate contradictions only when material or unresolved by evidence.

## 34. Concurrency guard O-16 (approximately lines 736–748)

**Observed design:** One code-modifying workflow per branch; `git status` checks for unexpected changes; branch gate also inspects dirty trees.

**Why:** Prevents overlapping edits.

**Assessment:** `git status` is not an atomic lock: two workflows can both see a clean tree and start simultaneously.

**Recommendation:** Add branch-scoped atomic locks, owner workflow IDs, lease/heartbeat, stale-lock recovery, and optional isolated Git worktrees. Keep dirty-tree inspection as a separate safety check.

## 35. Idempotency checks (approximately lines 749–760)

**Observed design:** Checks for duplicate tickets, PRs, commits, pushes, and ticket-status updates.

**Why:** Avoids repeating non-idempotent actions after retries or recovery.

**Assessment:** Search-before-create is vulnerable to races and false matches; ticket title alone is not a stable identity.

**Recommendation:** Use durable operation keys (`workflow_id + action + target`), receipts, locking/conditional writes, and reconciliation against external systems. Match PRs by repository/source/target/state.

## 36. Replay mode (approximately lines 761–764)

**Observed design:** Reconstructs previous workflow handoffs from `events.jsonl`; described as read-only.

**Why:** Debugging, audits, and reproducibility.

**Assessment:** Valuable; 're-execute' wording could imply mutation.

**Recommendation:** Rename this behavior `trace-replay` or `reconstruct`. If actual execution retry is supported, make it a separate authorized workflow.

## 37. Workflow visualization / show-trace (approximately lines 765–768)

**Observed design:** `#show-trace [correlationId]`; defaults to most recent workflow.

**Why:** Makes complex agent chains understandable.

**Assessment:** Useful operational feature.

**Recommendation:** Display workflow states, agent timings, status, retries, evidence, token use, and Git/PR receipts. Ensure traces do not expose credentials or sensitive logs.

---

## 38. Cross-section contradictions to resolve

| Conflict | Evidence in screenshots | Proposed resolution |
|---|---|---|
| Full analysis always vs abbreviated chains | Early analysis chain vs `bug-fix`, `code-only`, `docs` | Selected workflow defines required agents, subject to global safety invariants |
| All workflows must reach PR vs push-only micro-workflow | Definition of Done vs `commit-push` | Workflow-specific terminal artifacts |
| Orchestrator only coordinates Git via skills vs direct Git commands allowed | Responsibility boundaries vs allowed commands | Skill/CLI-only mutation; orchestrator read-only Git inspection |
| Full autonomy without pause vs human-in-loop never bypass | Autonomy section vs checklist heading | Explicit authorization profile and policy-defined approval triggers |
| Condensed handoffs vs verbatim outputs | Two-tier output design vs execution rules | Compact chat output; raw output retained and accessible |
| Review pass implies completed vs commit/PR still pending | Decision boundaries vs Definition of Done | Distinct `review_passed`, `delivery_pending`, `complete` states |
| `init` appears to generate files after read-only explorer | `init` chain vs role boundaries | Delegate file creation to an implementation-role agent or tool with explicit authority |

## 39. Proposed target responsibility model

| Component | Owns | Must not own |
|---|---|---|
| Orchestrator | Intent, workflow selection, dispatch decisions, synthesis | Code edits, test execution, raw Git mutations |
| Workflow engine / dispatcher | Gate enforcement, agent identity, state transitions, locks, idempotency | Open-ended architectural reasoning |
| Analysis agents | Repository discovery, architecture, implementation plans | Tracked file edits |
| Implementation agents | Scoped code/docs changes and associated test creation | Final independent review verdict |
| Review agents | Validation, evidence, findings, verdicts | Silent modification of implementation |
| Skills | Authorized Jira, Bitbucket, Git, Jenkins and other domain actions | Independent changes to workflow policy |
| Logger | Durable event history, workflow state, recovery metadata | Selecting technical solutions |

## 40. Recommended staged implementation plan

### Phase 0 — Verify source of truth
- Inspect `shared/contract.md`, `shared/dispatch-reference.md`, logger FSM, branch gate, dispatch scripts, and individual agent specs.
- Build a rule-to-implementation traceability matrix.
- Fix malformed Markdown tables without changing behavior.

### Phase 1 — Correctness and safety
- Resolve chain precedence and workflow-specific completion requirements.
- Enforce remote mutation permissions and branch protection in code.
- Add atomic concurrency locks and operation receipts.
- Replace last-fenced-JSON parsing with schema validation.

### Phase 2 — Maintainability
- Keep orchestrator as a short policy/router.
- Move detailed gates, workflow definitions, dispatch templates, and CLI usage to canonical references.
- Generate human-readable tables from machine-readable registries where feasible.

### Phase 3 — Token optimization
- Baseline input/output tokens, wall time, and agent invocations for representative workflows.
- Apply intent-scoped analysis and compact handoffs.
- Select reviewers by policy and changed-file risk; do not silently remove required security controls.
- Cache stable repository metadata with freshness checks.

### Phase 4 — Verification
- Unit-test state transitions, gate conditions, verdict aggregation, and idempotency.
- Simulate interruption after staging, commit, push, and PR creation.
- Test concurrent workflows on one branch.
- Test malformed agent outputs, missing context, conflicting findings, and user corrections.
- Compare before/after token cost, latency, success rate, and safety violations.

## 41. Suggested acceptance tests

| Scenario | Expected behavior |
|---|---|
| Minor bug fix | Uses defined bug-fix chain; no contradictory mandatory stages |
| Analysis-only request | Produces report; no tracked file mutation or Git push |
| Commit-push request | Pushes authorized existing changes; no PR created |
| Existing PR for source branch | Reuses or updates according to policy; no duplicate PR |
| Two workflows start on same branch | One obtains lock; other waits or uses isolated worktree |
| Context lost after commit | Recovers commit receipt; does not duplicate commit |
| Reviewer returns malformed result | Schema validation blocks transition and requests correction |
| High-severity finding lacks evidence | Retains unresolved status; does not silently mark pass |
| User changes scope mid-workflow | Pauses/replans affected steps without unapproved mutations |
| Trace replay | Reconstructs history without executing agents or side effects |

## 42. Proposed concise orchestrator skeleton (design proposal, not drop-in replacement)

```md
---
name: Orchestrator
description: Routes work through authorized specialist workflows, enforces gates through the workflow engine, and synthesizes evidence-backed outcomes.
tools: [read, agent, search, execute]
---

# Role
You are a permanent coordinator. Never modify tracked implementation files or directly run validation. Delegate specialist work.

# Authority
Follow `shared/contract.md` for safety/status semantics, the workflow registry for selected chain and terminal artifacts, and `shared/dispatch-reference.md` for dispatch schemas. Runtime gates and authorization checks are authoritative.

# Workflow
1. Classify user intent, target, and permitted side effects.
2. Recover or initialize durable workflow state.
3. Select the matching predefined workflow; use a custom chain only when no match exists.
4. Validate preconditions and dispatch the next required specialist.
5. Parse schema-validated results, persist evidence, and route failures.
6. Apply workflow-specific review and completion gates.
7. Invoke only authorized skills for commit/push/PR operations.
8. Synthesize from executed agents and recorded tool outcomes.

# Hard invariants
- Never bypass required analysis/review for the selected workflow.
- Never execute tracked-file edits or validation as the orchestrator.
- Never perform unauthorized remote or destructive mutations.
- Never mark complete without the workflow's terminal artifacts.
- Never repeat a completed side effect without reconciliation.
- Never infer success from missing or malformed evidence.

# Output
Give a concise status, completed work, evidence, risks, and next action. Store full raw outputs in the workflow log.
```

**Important:** The skeleton deliberately omits platform-specific mode and tool details. Validate compatibility before adoption. It is a direction for refactoring, not a tested replacement for your current 768-line file.

## 43. Final assessment

The orchestrator has a strong foundation: strict role separation, specialized chains, a logger FSM, correlation IDs, recoverable outputs, review routing, and domain skills. The highest-value improvements are to **reconcile policy contradictions**, **make side effects enforceably safe**, and **reduce repeated LLM orchestration work**. Preserve the existing safety and audit capabilities while shifting mechanical enforcement into tested runtime components.

**Evidence limitation:** This review is grounded in the screenshots and may miss obscured text or rules located in linked files. Confirm exact line numbers, agent names, and canonical behavior against the original repository before applying changes.
