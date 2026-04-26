---
name: test-coverage-analyzer
description: Analyze test coverage to identify low-coverage areas and missing tests. Use when reviewing Java codebases, CI reports, or changed files to find untested branches, risky logic, exception paths, and areas that need unit, integration, or regression tests.
---

# Test Coverage Analyzer

## When to Use This Skill

Use this skill when coverage numbers or change sets need to be translated into concrete test gaps.

## Prerequisites

- The coverage report or changed files being analyzed
- The application area that carries the most risk
- Existing unit, integration, or regression coverage for comparison

## Goal

Find the tests that matter most by focusing on risk, branch coverage, and behavior that can regress silently.

## What to Detect

- Low-coverage classes, methods, and branches
- Untested error handling and exception paths
- Missing assertions around important business rules
- Code paths exercised only indirectly or not at all
- Changes that reduced coverage in risky areas
- Tests that exist but do not validate meaningful behavior

## Step-by-Step Workflows

1. Identify the changed or low-coverage code paths.
2. Separate structural coverage from behavioral coverage.
3. Prioritize gaps by business risk, not raw percentage alone.
4. Map each gap to the most appropriate test type.
5. Recommend the smallest set of tests that closes the meaningful risk.

## Gap Prioritization

- Highest priority: business rules, branching logic, error handling, and integration boundaries
- Medium priority: mapping, validation, and transformation logic
- Lower priority: simple getters, trivial delegations, and framework plumbing

## Missing Test Suggestions

- Happy path for each important branch
- Negative tests for invalid input and failure modes
- Exception handling and fallback behavior
- Regression tests for fixed bugs
- Integration tests where unit tests cannot cover the real risk

## Output Standard

For each gap, provide:

- File or method
- Why coverage is low or misleading
- Missing test scenario
- Recommended test type
- Risk if left untested

## Reporting Style

- Be specific about the behavior that is untested.
- Prefer tests that prove a business rule over tests that only raise a percentage.
- Call out when existing tests are too shallow to count as meaningful coverage.

## Troubleshooting

- If the coverage is low but the code is trivial, do not over-prioritize it.
- If the missing path is a business rule, add a focused regression test.
- If the current tests are shallow, treat them as incomplete coverage even if the metric is high.

## References

- Coverage reports from CI
- Related unit and integration test suites
