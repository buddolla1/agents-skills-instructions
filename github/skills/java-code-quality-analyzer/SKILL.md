---
name: java-code-quality-analyzer
description: Coordinates Java code quality review into smaller skills for correctness, security, performance, and design or maintainability. Use when reviewing Java or Spring Boot code and you want progressive loading by concern.
---

# Java Code Quality Analyzer

Use this skill as the coordinator for Java and Spring Boot code reviews.

## When to Use This Skill

Use this skill when reviewing Java or Spring Boot code for bugs, security issues, performance bottlenecks, or maintainability risks.

## First Question

Ask the user what they want to review first:

- Correctness
- Security
- Performance
- Design and maintainability
- Full review

If the request does not specify one of these, ask this question before proceeding.

## Progressive Loading Model

1. Load [java-code-quality-correctness](java-code-quality-correctness/SKILL.md) for correctness, edge cases, and failure handling.
2. Load [java-code-quality-security](java-code-quality-security/SKILL.md) for secrets, injection, auth, and unsafe data handling.
3. Load [java-code-quality-performance](java-code-quality-performance/SKILL.md) for bottlenecks, allocations, blocking work, and hot-path inefficiency.
4. Load [java-code-quality-design](java-code-quality-design/SKILL.md) for maintainability, cohesion, naming, coupling, and refactoring opportunities.
5. For a full review, combine the relevant smaller skills in sequence.

## Source of Truth

- The project root or the diff being reviewed
- The behavior that must remain unchanged
- Any tests or examples that show the intended design

## Guardrails

- Do not force a full review when the user asked for a narrower concern.
- Do not invent behavior that is not covered by the selected skill.
- Do not skip clarification when the request could reasonably map to multiple focus areas.

## References

- The source code and the changed files
- The specialized code quality skills in this directory
