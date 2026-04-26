---
name: engineering-design-intake
description: Reads feature.txt for engineering design work and collects missing sizing inputs before planning begins. Use when the feature request needs confirmation of epic count, stories per epic, and tasks per story.
---

# Engineering Design Intake

Use this skill to confirm the starting inputs before the full delivery plan is generated.

## When to Use This Skill

Use this skill when the user provides feature requirements and you need to verify whether the sizing inputs are complete.

## Prerequisites

- Raw `feature.txt` content
- Requested number of epics
- Requested number of user stories per epic
- Requested number of tasks per story

## Goal

Confirm the feature scope and collect the minimum sizing data needed to proceed.

## Step-by-Step Workflows

1. Read the feature input and identify missing sizing values.
2. If epic count, stories per epic, or tasks per story are missing, ask the user for all three together.
3. If the inputs are complete, confirm them and hand off to the scope skill.
4. Keep this stage short and focused on intake only.

## Output Standard

For intake, provide:

- Confirmed feature summary
- Missing sizing values, if any
- Clarifying questions, if needed
- Handoff note for the next skill

## Guardrails

- Do not draft epics, stories, or architecture in this stage.
- Do not continue until the sizing inputs are confirmed.

## Reporting Style

- Be concise and direct.
- Ask only for the missing data needed to continue.

## References

- The source `feature.txt`
- The coordinator skill
