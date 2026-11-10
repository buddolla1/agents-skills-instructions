# Orchestrator Agent — Key Modifications and Implementation Plan

## Purpose and scope

This document consolidates the highest-priority recommendations from the review of approximately 768 lines of `orchestrator.agent.md` shown in 21 screenshots. It is an **implementation plan**, not a verbatim replacement agent. Findings about supporting scripts and contracts require verification against their source code.

## Executive summary

Preserve the existing multi-agent architecture, FSM, HALT rules, specialist roles, logging, recovery, and integration skills. Prioritize correctness and mutation safety before token optimization.

| Priority | Modification | Problem | Desired outcome |
|---|---|---|---|
| P0 | Resolve workflow-chain conflicts | Global mandatory analysis chain differs from some workflow definitions | One authoritative chain per workflow |
| P0 | Workflow-specific Definition of Done | Commit/push-only flows conflict with PR-required completion | Correct terminal conditions by workflow |
| P0 | Atomic concurrency control | `git status` does not lock a branch | No overlapping writes to a shared branch |
| P0 | Enforce Git authorization | Prompt-only permissions cannot guarantee safe pushes/PRs | Tool-enforced permissions and branch protection |
| P1 | Consolidate duplicate rules | HALT, delegation, and routing instructions recur | Single authoritative policy definitions |
| P1 | Select agents by task risk | Simple tasks may trigger excessive analysis | Appropriate analysis depth without losing gates |
| P1 | Compact structured handoffs | Repeated raw context increases token use | Small, evidence-backed downstream payloads |
| P1 | Schema-validate agent results | Last-JSON-block parsing is fragile | Reliable, machine-readable outcomes |
| P1 | Durable idempotency | Check-then-act can create duplicate remote actions | Safe retries and reconciliation |
| P2 | Instrument usage and quality | No measured savings established | Token, latency, cost, and success baselines |

## 1. Resolve conflicting agent-chain rules (P0)

**Observed:** A global analysis requirement specifies `code-explorer → code-architect → planner`, while workflow examples such as bug fixes omit `code-architect` and custom chains may omit agents.

**Recommendation:** Classify the request, select a workflow, then enforce the required chain for that workflow. Global safety gates remain mandatory, but the full analysis chain should not be universal unless that is a deliberate policy.

| Workflow | Illustrative required chain |
|---|---|
| Complex feature | Explorer → Architect → Planner → Implementor → applicable reviewers |
| Bug fix | Explorer → Planner → Implementor → applicable reviewers |
| Small localized fix | Targeted analysis → Implementor → applicable reviewers |
| Code review | Relevant reviewers → synthesis |
| Troubleshooting | Explorer → resolver; validation if code changes |

**Implementation:** Define workflow-to-agent mapping once in `shared/dispatch-reference.md`; have the dispatcher enforce it. Remove contradictory universal wording from `orchestrator.agent.md`.

**Acceptance test:** A bug-fix request follows its selected chain without being blocked for omitting an architect; a complex feature still invokes the architect.

## 2. Make Definition of Done workflow-specific (P0)

**Observed:** General completion rules require a PR, while `commit-push` explicitly does not.

**Recommendation:** Evaluate completion using the selected workflow's terminal artifacts and required validation.

| Workflow | Done when |
|---|---|
| Feature or bug fix with PR | Required validation passes; authorized commit and push complete; PR created or updated |
| Commit-push | Required checks pass; authorized commit and push complete; no PR required |
| Review-only | Findings and verdict recorded; no mutation required |
| Analysis-only | Findings and recommendations delivered |
| Troubleshoot-only | Diagnosis delivered; if code changed, transition to code-change gates |

**Implementation:** Put terminal conditions in the workflow contract and enforce them in the FSM, rather than relying on a generic checklist.

**Acceptance test:** `commit-push` reaches a valid terminal state without PR creation.

## 3. Add atomic concurrency protection (P0)

**Observed:** Checking `git status` cannot prevent two workflows from starting on a clean branch simultaneously.

**Recommendation:** Acquire an atomic lock keyed by repository and branch before write operations. Record `workflow_id`, owner, acquired time, heartbeat, and expiration. Recover stale locks safely and release locks on completion or abort. Consider isolated Git worktrees for parallel tasks.

**Implementation:** Enforce locks in the dispatcher/workflow engine, not only in the prompt.

**Acceptance test:** Two simultaneous modification workflows targeting the same branch cannot both acquire write permission.

## 4. Enforce Git authorization at the tool layer (P0)

**Observed:** Autonomous flows may commit, push, and create PRs automatically.

**Recommendation:** Track separate permissions for local edits, commits, remote pushes, PR creation, and target branches. Require explicit authorization at workflow start and honor repository branch protections. A prompt instruction is not a security boundary.

**Implementation:** Have commit and Bitbucket skills verify authorization and current workflow state before each mutation.

**Acceptance test:** A workflow authorized for local edits but not remote pushes cannot push, even if an agent requests it.

## 5. Consolidate duplicate orchestrator rules (P1)

**Observed:** HALT, role permanence, first-line defense, pre-work checks, and delegation gates overlap.

**Recommendation:** Keep a brief summary in `orchestrator.agent.md`; define detailed gates once in `shared/contract.md`. Avoid duplicating potentially contradictory policies across files.

**Implementation:** Assign a canonical location to each rule, use stable rule IDs, and replace duplicate paragraphs with references.

**Acceptance test:** Each operational rule has one authoritative definition and no conflicting copies.

## 6. Use risk-based agent selection (P1)

**Observed:** Mandatory multi-agent analysis may be excessive for localized tasks.

**Recommendation:** Determine analysis depth using scope, architectural impact, security sensitivity, data migration risk, and uncertainty. Do not skip mandatory review or safety gates simply to save tokens.

**Example:** A null-check fix may use targeted exploration, implementation, and relevant review; a cross-service contract change should use architecture and planning agents.

**Acceptance test:** Simple fixes use fewer unnecessary invocations; high-risk changes still run the full required checks.

## 7. Compress agent handoffs without losing evidence (P1)

**Observed:** The design stores raw outputs and compact role summaries, but verbatim output requirements can undermine compression.

**Recommendation:** Preserve raw outputs in logs, while passing only task-relevant evidence to downstream agents and showing concise summaries by default.

**Illustrative handoff:**

```yaml
workflow_id: wf-123
agent: code-explorer
status: SUCCESS
affected_files:
  - src/main/java/example/CustomerService.java
finding: Missing null validation at the identified call site
evidence_refs:
  - outputs/code-explorer-raw.md
next_action: Implement a guard and focused regression test
```

**Acceptance test:** The implementor can execute from a compact handoff and retrieve original evidence when needed.

## 8. Require schema-validated agent outputs (P1)

**Observed:** Parsing the last JSON code block is error-prone.

**Recommendation:** Define a versioned result schema, validate it before FSM transitions, and reject or repair invalid outputs within bounded retries. Preserve the original response for diagnostics.

```json
{
  "schema_version": "1.0",
  "agent_id": "java-reviewer",
  "status": "SUCCESS",
  "verdict": "PASS",
  "findings": [],
  "evidence_refs": [],
  "validation": { "build": "PASS", "tests": "PASS" }
}
```

**Acceptance test:** Malformed, missing, or mismatched agent output cannot silently advance workflow state.

## 9. Strengthen idempotency and replay semantics (P1)

**Observed:** The orchestrator checks for duplicate tickets, commits, pushes, and PRs, but check-then-act alone is not atomic.

**Recommendation:** Persist stable operation keys and results. Lock around unsupported external operations and reconcile ambiguous outcomes. Distinguish **trace replay** (read-only reconstruction) from **execution retry** (may mutate systems and must pass normal gates).

**Acceptance test:** Retrying an uncertain PR creation does not create a second PR; read-only replay never mutates external systems.

## 10. Measure tokens and workflow performance (P2)

**Recommendation:** Track per-agent input/output tokens, repeated context, invocation count, elapsed time, retries, validation failures, and end-to-end workflow success. Compare representative workloads before and after changes.

**Acceptance test:** A baseline and post-change report show measurable savings without unacceptable regression in correctness or review coverage.

## File-by-file change plan

| File / component | Changes |
|---|---|
| `orchestrator.agent.md` | Keep role, intent classification, routing overview, escalation, and synthesis; remove duplicate detailed rules |
| `shared/contract.md` | Canonical HALT, authorization, validation, and terminal-state contracts |
| `shared/dispatch-reference.md` | Workflow chains, routing conditions, structured handoff/result schemas |
| Logger / FSM | Validate transitions and workflow-specific completion; persist event identity |
| Dispatcher CLI | Enforce schema, locks, authorization, idempotency, and retry controls |
| Commit skill | Check permissions, staged changes, branch policy, and retry safety |
| Bitbucket skill | Enforce push/PR authorization and duplicate-PR reconciliation |
| Replay utility | Separate read-only trace replay from mutation-capable retries |

## Recommended rollout

### Phase 1 — Correctness and safety
1. Reconcile global versus workflow-specific chains.
2. Define completion rules per workflow.
3. Enforce atomic locks and Git authorization.
4. Test failure, cancellation, and recovery scenarios.

### Phase 2 — Token efficiency
1. Consolidate duplicated policy text.
2. Introduce task/risk-based agent selection.
3. Use compact evidence-backed handoffs.
4. Measure invocation count and token usage.

### Phase 3 — Reliability
1. Validate structured outputs and agent identity.
2. Add durable idempotency records.
3. Clarify replay versus retry.
4. Test interrupted operations and partial external successes.

### Phase 4 — Verification
1. Run the same representative tasks before and after refactoring.
2. Compare quality, tokens, latency, and retries.
3. Roll out incrementally with rollback options.

## What not to remove

Preserve permanent orchestrator role separation, specialized analysis/implementation/review agents, mandatory safety gates, correlation IDs, durable logging, FSM, bounded fix loops, recovery, and skills-based integrations. Optimize their implementation rather than discarding these protections.

## Verification caveat

These findings come from screenshots of the orchestrator instructions, not a source-code audit of the dispatcher, FSM, contract, or skills. Verify actual runtime behavior before treating any recommendation as an already-confirmed implementation defect.
