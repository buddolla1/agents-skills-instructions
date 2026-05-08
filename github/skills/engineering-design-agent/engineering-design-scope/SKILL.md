---
name: engineering-design-scope
description: Reads repository context and captures assumptions and scope boundaries for repo-aware engineering design output. Use when the requirement is clear enough to align the artifact with the repository.
---

# Engineering Design Scope

Use this skill to ground the design artifact in the repository before writing technical recommendations.

## When to Use This Skill

Use this skill after intake has confirmed the requirement and before drafting repo-aware content.

## Prerequisites

- Confirmed requirement
- README, build files, and relevant source or config files
- Any known constraints from the user

## Goal

Capture visible repo context, assumptions, and boundaries so later sections stay grounded.

## Step-by-Step Workflows

1. Read the README and build files first.
2. Inspect relevant source or config files tied to the requirement.
3. Infer the stack and architecture only from visible evidence.
4. Record assumptions and any scope limits caused by missing context.

## Output Standard

For repo context, provide:

- Feature summary
- Repo context summary
- Assumptions
- Scope
- Context limits

## Guardrails

- Do not invent stack details that were not observed.
- Do not make architecture claims without evidence in repo files.

## Reporting Style

- Keep confirmed facts separate from assumptions.
- Keep the evidence trail easy to follow.

## References

- README, build files, and relevant source or config files
- The intake skill
