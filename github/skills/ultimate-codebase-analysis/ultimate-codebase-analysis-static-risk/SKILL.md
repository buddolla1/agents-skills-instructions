---
name: ultimate-codebase-analysis-static-risk
description: Analyzes static correctness, safety, maintainability, testing-adjacent, and security-signal issues in repository code. Use when reviewing source code for evidence-backed runtime risk without relying on execution.
---

# Ultimate Codebase Analysis Static Risk

Use this skill to identify correctness and maintainability risks from static code evidence.

## When to Use This Skill

Use this skill when the review should focus on runtime risk, correctness, code quality, testing-adjacent gaps, or security signals visible in source.

## Modes

- `findings-only`: return structured findings for an orchestrator or report assembler
- `standalone-report`: write a focused markdown report to `static-risk-report.md`

## What to Analyze

- Null-safety and unchecked state assumptions
- Unsafe collection, parsing, or conversion behavior
- Resource-handling problems and local concurrency risks
- Dead code, cohesion issues, and maintainability signals
- Missing nearby regression coverage for high-risk changed paths
- Security-adjacent code smells such as sensitive-value logging or weak validation

## Output Standard

For each issue, provide:

- location
- issue summary
- evidence
- likely impact
- recommended fix
- severity

When running in `standalone-report` mode, write `static-risk-report.md` with these sections when relevant:

1. `Summary`
2. `Critical Issues`
3. `High Issues`
4. `Medium Issues`
5. `Low Issues`
6. `Static Risk Findings`
7. `Testing-Adjacent Gaps`
8. `Security Signals`
9. `Recommendations`

## Guardrails

- Do not state runtime failure as certain unless the code path is direct and unambiguous.
- Do not claim security exploitation from static hints alone; mark those as signals.
- Do not report style-only nits unless they create a real maintainability or correctness risk.
- Do not mix focused static-risk output with dependency-only or exception-only content unless the evidence clearly overlaps.
