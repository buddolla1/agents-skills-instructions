---
name: java-code-quality-performance
description: Reviews Java code for performance bottlenecks and hot-path inefficiency. Use when the user wants a focused performance review of Java or Spring Boot code.
---

# Java Code Quality Performance

Use this skill to identify bottlenecks, excessive allocations, and avoidable work.

## When to Use This Skill

Use this skill when the review should focus on latency, throughput, blocking I/O, repeated work, and other performance risks.

## Prerequisites

- The project root or diff being reviewed
- Any metrics, traces, or symptoms of slow behavior

## Goal

Find the highest-cost performance issues and explain why they matter.

## Output Standard

For each issue, provide:

- Location
- Performance symptom
- Root cause
- Recommended fix
- Tradeoff or validation note

## Guardrails

- Do not recommend micro-optimizations without evidence.
- Do not add caching or async processing without a clear justification.

## Reporting Style

- Be specific about the bottleneck type.
- Prefer end-to-end impact over local tuning.

## References

- The coordinator skill
