---
name: engineering-design-planning
description: Structures the markdown design artifact for BDD, architecture, full design, or template output. Use when the requirement and repo context are clear enough to draft the requested engineering design content.
---

# Engineering Design Planning

Use this skill to draft the main markdown artifact in the correct format for the requested output mode.

## When to Use This Skill

Use this skill after intake and repo-context work are complete.

## Prerequisites

- Feature summary
- Assumptions
- Repo context summary
- Requested `outputMode`

## Goal

Create a markdown artifact whose sections match the requested design outcome.

## Step-by-Step Workflows

1. Choose the artifact structure based on `outputMode`.
2. For `bdd`, focus on stories, scenarios, acceptance criteria, and test data.
3. For `architecture`, focus on architecture overview, HLD, LLD, data flow, risks, and diagrams.
4. For `full_design`, combine scope, behavior, validation, and architecture sections.
5. For `template`, provide a reusable markdown skeleton with placeholders grounded in the repo context.

## Output Standard

For the markdown artifact, provide the sections that fit the selected mode, such as:

- Summary
- Assumptions
- Architecture overview
- High-level design
- Low-level design
- BDD scenarios
- Test data
- Risks

## Quality Check

Before handing off, verify that:

- the section set matches the selected `outputMode`
- each section is grounded in repo context or explicit assumptions
- the markdown output is cohesive and reviewable

## Guardrails

- Do not force sections that do not fit the selected mode.
- Do not hide assumptions inside descriptive prose.
- Do not output JSON in this stage.

## Reporting Style

- Be structured and specific.
- Prefer headings, tables, and bullets only when they improve scanability.

## References

- The scope skill
