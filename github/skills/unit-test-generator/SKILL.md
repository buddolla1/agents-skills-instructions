---
name: unit-test-generator
description: Generate JUnit and Mockito unit tests for Java code. Use when creating, expanding, or reviewing tests for services, utilities, and business logic, and when checking coverage of branches, edge cases, and error handling.
---

# Unit Test Generator

## When to Use This Skill

Use this skill when writing or reviewing Java unit tests that should validate behavior with JUnit and Mockito.

## Prerequisites

- The class under test and its collaborators
- The behavior that must be protected by the test
- Any existing tests that show the current coverage shape

## Goal

Produce tests that protect business behavior, cover meaningful branches, and stay readable enough to maintain.

## What to Cover

- Happy path behavior
- Branches, edge cases, and null or invalid inputs
- Exception paths and failure handling
- Interaction with mocked dependencies
- Boundary conditions and regression scenarios
- Important branches that are not yet covered by existing tests

## Step-by-Step Workflows

1. Read the class under test and identify its responsibilities.
2. Separate pure logic from collaborator interactions.
3. Derive tests from behavior, not line coverage alone.
4. Mock external dependencies and verify only meaningful interactions.
5. Add tests for any branch, error path, or rule that could regress.

## Test Design Rules

- One test should verify one behavior or rule.
- Prefer descriptive test names that explain the scenario and outcome.
- Mock dependencies at the boundary, not internal helpers.
- Avoid over-mocking implementation details.
- Keep assertions focused on observable results and important interactions.

## Mockito Guidance

- Use stubs for dependency outputs that drive the branch under test.
- Verify only the interactions that matter to the behavior.
- Avoid stubbing unused methods or chaining mocks too deeply.
- Prefer explicit fixture setup over clever test shortcuts.

## Coverage Checks

- Every conditional branch is exercised where it matters
- Error handling is tested, not assumed
- Important collaborator interactions are verified
- Refactor-safe behavior is covered by regression tests

## Output Standard

For each gap or generated test set, provide:

- Class or method under test
- Behaviors covered
- Behaviors still missing
- Mocking strategy used
- Risk if coverage remains incomplete

## Reporting Style

- Be specific about what the test proves.
- Prefer durable tests over high counts of low-value assertions.
- Call out missing branches, not just missing lines.

## Troubleshooting

- If a test only verifies implementation detail, simplify it to the observable behavior.
- If mocking is too deep, move the test closer to the boundary that matters.
- If a branch is uncovered, add the smallest scenario that exercises the behavior.

## References

- JUnit and Mockito conventions used by the project
- Related integration and regression tests
