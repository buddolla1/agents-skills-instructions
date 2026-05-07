---
name: ultimate-codebase-analysis-performance-hotspots
description: Reviews source code for blocking I/O, hot-path inefficiency, allocation pressure, query cost, caching gaps, and concurrency bottlenecks. Use when static analysis should identify likely performance hotspots.
---

# Ultimate Codebase Analysis Performance Hotspots

Use this skill to identify likely performance bottlenecks from static review.

## When to Use This Skill

Use this skill when the request includes performance, scalability, blocking work, database hot paths, or concurrency bottlenecks.

## Modes

- `findings-only`: return performance findings for aggregation
- `standalone-report`: write a focused markdown report to `performance-hotspots-report.md`

## What to Analyze

- Blocking I/O in request or batch-critical paths
- Repeated object allocation or needless data copying
- N+1 style access patterns and expensive query loops
- Missing or weak caching around repeated expensive work
- Async misuse, executor pressure, and thread contention signals

## Output Standard

For each issue, provide:

- location
- hotspot summary
- evidence
- why it is likely expensive
- recommended fix
- severity

When running in `standalone-report` mode, write `performance-hotspots-report.md` with these sections when relevant:

1. `Summary`
2. `Critical Issues`
3. `High Issues`
4. `Medium Issues`
5. `Low Issues`
6. `Performance Highlights`
7. `Concurrency Signals`
8. `Recommendations`

## Guardrails

- Do not present performance conclusions as measured facts without runtime evidence.
- Do not assume database behavior that is not implied by the code or queries.
- Do not report speculative micro-optimizations as meaningful findings.
- Do not mix general dependency drift or exception-only concerns into the performance report.
