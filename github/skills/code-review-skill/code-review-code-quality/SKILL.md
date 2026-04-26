---
name: code-review-code-quality
description: Reviews maintainability, readability, cohesion, naming, and code smells in source code. Use when reviewing a repo or git diff for code quality and refactoring opportunities.
---

# Code Review Code Quality

Use this skill to identify maintainability issues that increase cognitive load or defect risk.

## When to Use This Skill

Use this skill when the review should focus on readability, cohesion, naming, duplication, coupling, and small refactoring opportunities.

## Prerequisites

- The project root or git diff being reviewed
- Any tests or examples that show intended behavior

## Goal

Find design and maintainability issues that make the code harder to change safely.

## Interaction Point

If a change looks awkward but may be intentional, ask whether the shape is required by an external contract, framework, or dependency before calling it a code-quality issue.

## What to Analyze

- Long or crowded methods
- Unclear naming
- Excessive coupling
- Duplicated logic
- Weak separation of concerns
- Overly complex control flow

## Output Standard

For each issue, provide:

- Location
- Code-quality concern
- Why it matters
- Recommended fix

## Guardrails

- Do not recommend large redesigns for small problems.
- Do not treat every style issue as a defect.
- Do not split abstractions unless it lowers real complexity or coupling.

## Reporting Style

- Be precise and incremental.
- Prefer root-cause analysis over cosmetic comments.

## References

- The coordinator skill
