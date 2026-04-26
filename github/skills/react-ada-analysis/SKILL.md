---
name: react-ada-analysis
description: Analyze React projects for ADA accessibility issues. Use when reviewing React components, forms, navigation, color contrast, keyboard support, ARIA usage, screen-reader behavior, or when required accessibility packages are missing and the user should be prompted to add them.
---

# React ADA Analysis

Use this skill when reviewing a React project for accessibility and inclusive interaction quality.

## When to Use This Skill

Use this skill when the task is to check a React codebase for accessibility problems, missing semantics, or ADA compliance risks. If the required accessibility packages are not available in the project, prompt the user to add them before proceeding.

## Prerequisites

- The React components or pages being reviewed
- The project `package.json` or equivalent dependency manifest
- The accessibility tooling the project already uses

## Goal

Find accessibility issues early and recommend practical fixes that improve keyboard use, screen-reader support, and semantic correctness.

## What to Analyze

- Semantic HTML usage
- Keyboard navigation and focus management
- Form labels, instructions, and error messaging
- ARIA usage and misuse
- Color contrast and visible state changes
- Interactive element behavior for mouse and keyboard users
- Screen-reader friendly structure and content order

## Step-by-Step Workflows

1. Check whether the project already has the accessibility packages or lint rules needed for analysis.
2. If required packages are missing, prompt the user to add them before continuing.
3. Review components, forms, and interactions for semantic and keyboard accessibility.
4. Flag issues that would block assistive technology or create confusing user flows.
5. Recommend the smallest safe fix that improves accessibility without changing business behavior.

## Package Check Rule

- Verify the project dependencies before suggesting package-based analysis or tests.
- If packages such as accessibility lint rules, axe tooling, or testing helpers are missing, ask the user to add them.
- Do not assume the project has the tooling unless it is present in the repository.

## Guardrails

- Do not use ARIA to replace valid native semantics.
- Do not call a component accessible just because it renders.
- Do not recommend tooling the project cannot use without first asking for the dependency.
- Prefer native controls and semantic markup over custom interaction patterns.

## Output Standard

For each issue, provide:

- Location
- Accessibility concern
- Why it matters for users
- Recommended fix
- Any missing package or tooling note

## Reporting Style

- Be direct and practical.
- Tie each issue to a user impact, not just a guideline.
- Distinguish true accessibility defects from low-value style preferences.

## Troubleshooting

- If the project lacks accessibility packages, stop and ask the user to add them.
- If a custom component replaces a native one, verify keyboard and screen-reader behavior first.
- If ARIA is overused, simplify the markup before adding more attributes.

## References

- React accessibility patterns
- Project accessibility tooling and lint rules

