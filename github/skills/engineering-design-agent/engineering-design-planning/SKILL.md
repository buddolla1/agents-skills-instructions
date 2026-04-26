---
name: engineering-design-planning
description: Builds epics, story breakdowns, dependencies, and dependency matrices for enterprise feature plans. Use when scope is clear and the delivery structure needs to be organized.
---

# Engineering Design Planning

Use this skill to turn the scoped feature into a structured implementation plan.

## When to Use This Skill

Use this skill after scope has been defined and the epics/stories can be organized.

## Prerequisites

- Feature summary
- Assumptions
- Scope boundaries
- Confirmed sizing inputs

## Goal

Create the delivery structure with epics, stories, and dependency mapping.

## Step-by-Step Workflows

1. Break the feature into logical epics.
2. Expand each epic into user stories with title, description, dependencies, story points, and tasks.
3. Identify upstream and downstream dependencies.
4. Produce a dependency matrix that makes sequencing obvious.
5. Keep the story point scale consistent across the plan.

## Output Standard

For planning, provide:

- Epics
- Story breakdown
- Dependencies
- Dependency matrix
- Story list

## Quality Check

Before handing off, verify that:

- every epic has stories
- every story has a point estimate
- every story has tasks
- dependencies are listed where relevant
- the story list is complete and traceable

## Guardrails

- Do not add BDD or testing content here.
- Do not skip dependency mapping.
- Do not over-split stories without a clear delivery reason.

## Reporting Style

- Be structured and specific.
- Keep the planning sequence easy to review.
- Prefer tables for epics, stories, dependencies, and estimates when they improve clarity.

## References

- The source `feature.txt`
- The scope skill
