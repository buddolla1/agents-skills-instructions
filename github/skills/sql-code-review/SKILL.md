---
name: sql-code-review
description: Review SQL code for security, maintainability, and code quality issues. Use when checking SQL for injection risks, access control, standards, and anti-patterns.
---

# SQL Code Review

Use this skill when SQL code needs correctness, quality, and security review.

## When to Use This Skill

Use this skill when reviewing SQL statements, stored logic, or schema-driven queries for quality and safety issues.

## Prerequisites

- The SQL statement or database artifact being reviewed
- The target database platform if it matters
- Any performance or security concerns already known

## Goal

Identify SQL code issues that could cause defects, security problems, or maintenance debt.

## Step-by-Step Workflows

1. Read the SQL in context.
2. Check for injection risks and unsafe string handling.
3. Review access control, joins, filters, and query shape.
4. Flag readability or maintainability issues.
5. Recommend the smallest safe improvement.

## Guardrails

- Do not assume parameterization if the code does not show it.
- Do not confuse optimization advice with security review.
- Do not report style issues as defects unless they matter.

## Output Standard

For each issue, provide:

- Location
- SQL concern
- Why it matters
- Recommended fix

## Reporting Style

- Be specific and direct.
- Tie findings to risk.
- Keep recommendations practical.

## Troubleshooting

- If the SQL is generated dynamically, inspect the source of the parameters.
- If the platform matters, call out database-specific behavior.
- If the query is hard to read, break it into smaller parts.

## References

- SQL standards for the project
- Database security and access conventions

