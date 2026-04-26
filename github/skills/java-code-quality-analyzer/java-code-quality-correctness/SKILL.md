---
name: java-code-quality-correctness
description: Reviews Java code for correctness bugs, edge cases, and unsafe assumptions. Use when the user wants a focused review of behavior, failure handling, and defect risk.
---

# Java Code Quality Correctness

Use this skill to identify correctness issues that can break application behavior.

## When to Use This Skill

Use this skill when the review should focus on bugs, edge cases, contract violations, and failure handling.

## Prerequisites

- The project root or diff being reviewed
- The expected behavior
- Any tests or examples that show the intended design

## Goal

Find correctness defects and explain how they affect behavior.

## Output Standard

For each issue, provide:

- Location
- Defect description
- Why it matters
- Recommended fix
- Risk if ignored

## Guardrails

- Do not overstate style problems as defects.
- Do not ignore boundary conditions or unsafe assumptions.

## Reporting Style

- Be direct and behavior-focused.
- Prefer concrete examples from the code.

## References

- The coordinator skill
