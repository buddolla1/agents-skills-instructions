---
name: java-code-quality-design
description: Reviews Java code for maintainability, cohesion, naming, and refactoring opportunities. Use when the user wants a focused design and readability review.
---

# Java Code Quality Design

Use this skill to identify maintainability issues and refactoring opportunities.

## When to Use This Skill

Use this skill when the review should focus on code smells, coupling, abstraction quality, and separation of concerns.

## Prerequisites

- The project root or diff being reviewed
- Any tests or examples that show the intended behavior

## Goal

Find design issues that increase cognitive load or defect risk.

## Output Standard

For each issue, provide:

- Location
- Design concern
- Why it matters
- Recommended fix
- Risk if ignored

## Guardrails

- Do not recommend large redesigns for small problems.
- Do not split abstractions without a clear reason.

## Reporting Style

- Be precise and incremental.
- Prefer root-cause analysis over cosmetic comments.

## References

- The coordinator skill
