---
name: engineering-design-validation
description: Verifies that the generated engineering design artifact matches the requested mode, stays repo-aware, and returns the expected markdown contract. Use when the markdown draft is complete and must be checked before final delivery.
---

# Engineering Design Validation

Use this skill to validate the markdown artifact and confirm the final output contract.

## When to Use This Skill

Use this skill after the markdown artifact has been drafted.

## Prerequisites

- Draft markdown artifact
- Requested `outputMode`
- Repo context summary
- Assumptions list
- Intended `outputPath`

## Goal

Verify the artifact and confirm the markdown output contract.

## Template Ownership

This skill checks that the final markdown follows the report-template contract:

- Story Count handling
- architecture and BDD section order
- explicit assumptions
- explicit `outputPath`
- Mermaid usage where it improves the artifact

## Step-by-Step Workflows

1. Check that the draft is a markdown artifact and that `outputPath` is explicit.
2. Verify the sections match the selected `outputMode`.
3. Verify repo-aware statements are grounded in visible repository context.
4. Verify assumptions are explicit.
5. Verify Mermaid diagrams are included wherever they improve the artifact.
6. Verify 5 subtasks per story are used by default unless the user specified otherwise.
7. Confirm the final output is a markdown artifact with a clear file path and explicit assumptions.

## Output Standard

Return a concise markdown validation summary with:

- `sectionsGenerated`
- `outputPath`
- `assumptions`
- `storyCount` when BDD output was requested

## Quality Check

Before handing off, verify that:

- `outputPath` points to a markdown file
- the section order matches the selected `outputMode`
- architecture output includes Mermaid diagrams wherever they are useful
- BDD output reflects the requested story count and default subtask count
- the template headings match the report template when `outputMode` is `template`

## Guardrails

- Do not emit extra prose before or after the validation summary.
- Do not claim repo alignment without evidence.
- Do not leave `outputPath` implicit.

## Reporting Style

- Be exact and compact.
- Treat the validation summary contract as mandatory.

## References

- The planning skill
