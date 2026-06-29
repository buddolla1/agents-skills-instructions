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

## Template Ownership

This skill drafts the report-template sections in this order for BDD output:

- Story Count
- Epics
- User Stories (with Story Points)
- Subtasks
- BDD Scenarios
- Story Tasks
- Story Dependencies
- Test Data
- Cross-Cutting Tasks
- Execution Plan
- Risks
- NFRs
- Estimation Summary

For `template`, keep the same heading order and placeholders. For `full_design`, include the architecture sections from the architecture skill as well.

## Step-by-Step Workflows

1. Choose the artifact structure based on `outputMode`.
2. For `bdd`, focus on story count, epics, repeatable story blocks, subtasks, scenarios, story tasks, and test data.
3. Use 5 subtasks per story by default unless the user specifies a different count.
4. For `architecture`, focus on architecture overview, HLD, LLD, data flow, risks, and diagrams.
5. For `full_design`, combine scope, behavior, validation, and architecture sections.
6. For `template`, provide a reusable markdown skeleton with placeholders grounded in the repo context.

## Output Standard

For the markdown artifact, provide the sections that fit the selected mode, such as:

- Story Count
- Architecture Overview
- High-Level Design
- Low-Level Design
- Architecture Diagrams
- Epics
- User Stories
- Subtasks
- BDD Scenarios
- Story Tasks
- Story Dependencies
- Test Data
- Cross-Cutting Tasks
- Execution Plan
- Risks
- Assumptions
- NFRs
- Estimation Summary

## Quality Check

Before handing off, verify that:

- the section set matches the selected `outputMode`
- BDD output reflects the requested `storyCount` and uses 5 subtasks per story by default
- each section is grounded in repo context or explicit assumptions
- the markdown output is cohesive and reviewable

## Reporting Style

- Be structured and specific.
- Prefer headings, tables, and bullets only when they improve scanability.

## References

- The scope skill
