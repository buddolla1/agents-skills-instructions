---
name: sql-optimization
description: Optimize SQL queries and indexing strategy. Use when tuning query plans, joins, filters, aggregations, pagination, or database performance.
---

# SQL Optimization

Use this skill when SQL performance needs to improve.

## When to Use This Skill

Use this skill when a query is slow, an execution plan is poor, or an index strategy needs review.

## Prerequisites

- The SQL statement or execution plan
- The table schema and indexes
- The expected data volume and access pattern

## Goal

Improve SQL performance by reducing scans, improving index usage, and simplifying query shape.

## Step-by-Step Workflows

1. Analyze the predicates, joins, and sort order.
2. Compare the query shape to the existing indexes.
3. Identify non-sargable or expensive operations.
4. Suggest the smallest query or index change that helps.
5. Validate tradeoffs against write cost and storage.

## Guardrails

- Do not add indexes without a reason.
- Do not assume one query plan works for all data sizes.
- Do not ignore write amplification or storage cost.

## Output Standard

For each optimization, provide:

- Query or object
- Performance problem
- Suggested change
- Tradeoff or validation note

## Reporting Style

- Be concrete about access paths.
- Prefer measurable improvements.
- Keep the advice database-aware.

## Troubleshooting

- If the bottleneck is unclear, inspect the plan and stats first.
- If an index does not help, revisit the query shape.
- If pagination is slow, consider keyset patterns.

## References

- Schema and execution plan references
- Database performance standards

