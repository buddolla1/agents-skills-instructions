---
name: ultimate-codebase-analysis-exception-risk
description: Analyzes exception handling, failure propagation, retry behavior, fallback logic, and diagnosability in source code. Use when code review should focus on how failures are handled and exposed.
---

# Ultimate Codebase Analysis Exception Risk

Use this skill to review failure-handling quality and production diagnosability.

## When to Use This Skill

Use this skill when the request focuses on exception handling, runtime failures, rollback behavior, retries, or fallback logic.

## Modes

- `findings-only`: return structured exception findings for aggregation
- `standalone-report`: write a focused markdown report to `exception-risk-report.md`

## What to Analyze

- Broad or swallowed catch blocks
- Lost root causes during wrapping or translation
- Missing retry, fallback, or propagation behavior where it matters
- Weak logging around production failures
- Async or background-task exception leaks
- Transaction or rollback risk when errors are handled locally

## Output Standard

For each issue, provide:

- location
- exception-handling concern
- evidence
- why it matters
- recommended fix
- severity

When running in `standalone-report` mode, write `exception-risk-report.md` with these sections when relevant:

1. `Summary`
2. `Critical Issues`
3. `High Issues`
4. `Medium Issues`
5. `Low Issues`
6. `Exception Findings`
7. `Retry and Fallback Risks`
8. `Recommendations`

## Guardrails

- Do not report every catch block as a defect.
- Do not recommend losing the original exception cause.
- Do not assume the intended failure contract when the code or request leaves it unclear.
- Do not mix general style concerns into the exception report unless they materially affect failure handling.
