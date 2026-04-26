---
name: react-test-generator
description: Generate tests for React applications. Use when creating or reviewing component tests, hook tests, event tests, rendering behavior, user interactions, or React testing-library and Jest/Vitest setups in JavaScript or TypeScript projects.
---

# React Test Generator

Use this skill when creating tests for React components, hooks, and user interactions.

## When to Use This Skill

Use this skill when the task is to write tests for a React application, improve React test coverage, or verify UI behavior with component-level or interaction-level tests. If the project does not have the required testing packages, prompt the user to add them first.

## Prerequisites

- The React component, hook, or page under test
- The project package manifest
- The testing library already used by the project

## Goal

Create stable, behavior-focused tests that verify what the user sees and does in the React application.

## Step-by-Step Workflows

1. Check whether the project already has React testing packages installed.
2. Identify the behavior, interaction, or branch that needs coverage.
3. Choose the appropriate test type: component, hook, or interaction test.
4. Write assertions against user-visible behavior and meaningful state changes.
5. Prompt the user to add missing packages before relying on them.

## Package Check Rule

- If `@testing-library/react`, `@testing-library/user-event`, `jest`, or `vitest` are missing, prompt the user to add them.
- Do not assume the project uses React Testing Library unless the manifest or lockfile shows it.

## Guardrails

- Do not over-mock the component tree.
- Do not assert on implementation details when user behavior is the real contract.
- Do not generate tests that pass only because the setup is too shallow.

## Output Standard

For each test set, provide:

- Component or hook under test
- Behavior covered
- Missing coverage
- Package or tooling note

## Reporting Style

- Be practical and user-focused.
- Prefer clear interaction tests over brittle internals.
- Tie every test to the behavior it protects.

## Troubleshooting

- If the test is flaky, wait on user-visible outcomes instead of internal state.
- If the project lacks testing packages, ask the user to add them first.
- If the component is too large, break the test by behavior or interaction.

## References

- React testing-library conventions
- Project-specific React test patterns

