---
name: engineering-design-validation
description: Produces BDD coverage, Gherkin scenarios, estimate points, test strategy, and test data for engineering design plans. Use when the delivery structure is known and quality validation needs to be documented.
---

# Engineering Design Validation

Use this skill to add quality, test, and estimate detail to the delivery plan.

## When to Use This Skill

Use this skill after planning is complete and the stories are ready for validation and test framing.

## Prerequisites

- Epics
- Story breakdown
- Dependencies
- Confirmed sizing inputs

## Goal

Provide the validation layer of the delivery plan with BDD, Gherkin, estimates, and test guidance.

## Step-by-Step Workflows

1. Translate the stories into BDD coverage.
2. Write concise Gherkin scenarios for the most important flows.
3. Assign estimate points where requested.
4. Define a test strategy that matches the delivery risk.
5. List representative test data.
6. Include acceptance criteria and test data notes for each story when useful.

## Output Standard

For validation, provide:

- BDD
- Gherkin scenarios
- Acceptance criteria
- Estimate points
- Test strategy
- Test data

## Quality Check

Before handing off, verify that:

- BDD and Gherkin cover the primary flows and edge cases
- every story has a point estimate when estimates are requested
- test data notes align with the story behavior
- the validation layer supports the delivery plan clearly

## Guardrails

- Do not repeat the planning section.
- Do not create test cases that do not map to the stories.
- Do not overcomplicate the estimates.

## Reporting Style

- Be practical and review-friendly.
- Keep test guidance tied to actual delivery risk.

## References

- The source `feature.txt`
- The planning skill
