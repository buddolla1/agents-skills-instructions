---
name: engineering-design-validation
description: Verifies that the generated engineering design artifact matches the requested mode, stays repo-aware, and returns the required JSON contract. Use when the markdown draft is complete and must be checked before final delivery.
---

# Engineering Design Validation

Use this skill to validate the markdown artifact and assemble the final JSON result.

## When to Use This Skill

Use this skill after the markdown artifact has been drafted.

## Prerequisites

- Draft markdown artifact
- Requested `outputMode`
- Repo context summary
- Assumptions list
- Intended `outputPath`

## Goal

Verify the artifact and produce the required single JSON object.

## Step-by-Step Workflows

1. Check that the draft is a markdown artifact and that `outputPath` is explicit.
2. Verify the sections match the selected `outputMode`.
3. Verify repo-aware statements are grounded in visible repository context.
4. Verify assumptions are explicit.
5. Build the final JSON object with `summary`, `artifactType`, `sectionsGenerated`, `outputPath`, and `assumptions`.

## Output Standard

Return a single JSON object with:

- `summary`
- `artifactType`
- `sectionsGenerated`
- `outputPath`
- `assumptions`

## Quality Check

Before handing off, verify that:

- the final response is only the JSON object
- `artifactType` matches the requested mode
- `sectionsGenerated` reflects the markdown content
- `outputPath` points to a markdown file

## Guardrails

- Do not emit extra prose before or after the JSON object.
- Do not claim repo alignment without evidence.
- Do not leave `outputPath` implicit.

## Reporting Style

- Be exact and compact.
- Treat the JSON contract as mandatory.

## References

- The planning skill
