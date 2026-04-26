---
name: engineering-design-scope
description: Captures the feature summary, assumptions, and scope boundaries for engineering design plans. Use when the intake inputs are confirmed and the delivery document needs business framing.
---

# Engineering Design Scope

Use this skill to define what the feature is, what it includes, and what it explicitly excludes.

## When to Use This Skill

Use this skill after intake has confirmed the sizing inputs and the feature intent is clear enough to frame the scope.

## Prerequisites

- Confirmed sizing inputs
- Feature requirements or feature.txt content
- Any business context, constraints, or known exclusions

## Goal

Capture the feature summary, assumptions, scope, and boundaries in a concise and reviewable form.

## Step-by-Step Workflows

1. Summarize the feature in plain business language.
2. Capture assumptions explicitly instead of implying them.
3. Define in-scope and out-of-scope boundaries.
4. State the delivery intent at a high level.

## Output Standard

For scope, provide:

- Feature summary
- Executive summary
- Assumptions
- Scope
- Out of scope items

## Guardrails

- Do not introduce epics or story details here.
- Do not invent architectural decisions.

## Reporting Style

- Keep the framing concise and factual.
- Separate confirmed facts from assumptions.

## References

- The source `feature.txt`
- The intake skill
