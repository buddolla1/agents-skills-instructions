---
name: engineering-design-intake
description: Confirms the requirement and collects only the minimum missing inputs before engineering design output is drafted. Use when the request needs clarification on scope, output mode, or architecture intent.
---

# Engineering Design Intake

Use this skill to confirm the request before any markdown artifact is drafted.

## When to Use This Skill

Use this skill when the user provides a feature or design requirement and the requested output is incomplete or ambiguous.

## Prerequisites

- `requirement`
- Optional `outputMode`
- Optional `projectType`
- Optional `techStack`
- Optional `architectureType`

## Goal

Confirm the requirement and ask the minimum clarifying question needed to proceed.

## Step-by-Step Workflows

1. Read the requirement and requested artifact type.
2. Determine whether `outputMode` is explicit or implied.
3. If the requirement is too broad, ask one targeted clarifying question.
4. If the inputs are sufficient, hand off to the repo-context skill.

## Output Standard

For intake, provide:

- Confirmed requirement summary
- Missing context, if any
- Clarifying question, if needed
- Handoff note for the next skill

## Guardrails

- Do not draft the final artifact in this stage.
- Do not ask more questions than needed.

## Reporting Style

- Be concise and direct.
- Ask only for missing information that changes the artifact materially.

## References

- The coordinator skill
