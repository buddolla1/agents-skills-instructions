---
name: fullstack-architecture-intake
description: Confirms the project type and asks whether the user wants HLD, LLD, External APIs, or the full architecture document. Use when starting architecture analysis and the target artifact is not yet selected.
---

# Full-Stack Architecture Intake

Use this skill to start architecture work by selecting the target artifact.

## When to Use This Skill

Use this skill when the user has not yet chosen whether to create HLD, LLD, External APIs, or the full document.

## Prerequisites

- Repository or module scope
- Project type context if already known
- The artifact choice from the user

## Goal

Ask the user what they want to create first and collect just enough context to route to the right specialized skill.

## Step-by-Step Workflows

1. Ask the user what they want to create first: HLD, LLD, External APIs, or full doc.
2. Confirm the project type if it is not already clear.
3. Route to the matching architecture skill after the user answers.
4. Keep the intake short and do not draft the architecture yet.

## Output Standard

For intake, provide:

- Requested artifact choice
- Project type, if known
- Any missing context needed to continue
- Handoff note for the next skill

## Guardrails

- Do not start analysis until the artifact choice is known.
- Do not write HLD, LLD, or API findings in intake.

## Reporting Style

- Be concise and direct.
- Ask one clear question when possible.

## References

- The coordinator skill
