---
name: code-review-null-pointer-check
description: Detects null safety issues, null pointer risks, and unsafe assumptions in source code. Use when reviewing code for null dereferences, incomplete validation, or inconsistent null handling.
---

# Code Review Null Pointer Check

Use this skill to find null-safety defects before they become runtime failures.

## When to Use This Skill

Use this skill when code may dereference null, return null unsafely, or rely on incomplete validation.

## Prerequisites

- The project root or git diff being reviewed
- Any nullability annotations or project conventions if they exist

## Goal

Find null-related failure paths and explain how they surface at runtime.

## Interaction Point

If the null contract is not obvious, ask whether the value may be absent, optional, or guaranteed by the caller before flagging a defect.

## What to Analyze

- Unsafe dereferences
- Missing null checks
- Inconsistent null returns
- Nullable inputs used without guards
- API boundaries that assume non-null data without validation

## Output Standard

For each issue, provide:

- Location
- Null-safety concern
- Why it matters
- Recommended fix

## Guardrails

- Do not flag deliberate nullable contracts as defects.
- Do not recommend defensive checks when the contract already guarantees non-null.

## Reporting Style

- Be concise and concrete.
- Tie each issue to a runtime failure path.

## References

- The coordinator skill
