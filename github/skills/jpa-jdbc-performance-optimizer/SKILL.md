---
name: jpa-jdbc-performance-optimizer
description: Analyze JPA and JDBC code for performance bottlenecks. Use when reviewing Spring Boot repositories, ORM mappings, or SQL access paths for N+1 queries, lazy loading issues, excessive round trips, inefficient fetch strategies, and query optimization opportunities.
---

# JPA / JDBC Performance Optimizer

## When to Use This Skill

Use this skill when assessing database access patterns in Java services and recommending safe, high-impact performance improvements.

## Prerequisites

- The repository, query, or stack trace being reviewed
- Knowledge of the transaction boundary and runtime access pattern
- Any relevant database schema or execution plan information

## Goal

Reduce database round trips, eliminate avoidable ORM inefficiencies, and choose fetch strategies that match the access pattern instead of the object model.

## What to Detect

- N+1 query patterns in service, repository, or serialization paths
- Lazy loading that triggers hidden database access outside the intended transaction
- Over-fetching caused by loading entire graphs when only a subset is needed
- Repeated lookups inside loops or stream pipelines
- Inefficient fetch plans, joins, or batching behavior
- JDBC code that issues one statement per row when batching or set-based queries are possible

## Step-by-Step Workflows

1. Trace the data path from controller or service call to database access.
2. Count logical round trips, not just lines of code.
3. Identify where entities are accessed after the transaction boundary.
4. Determine whether the caller needs entities, projections, or a smaller read model.
5. Recommend the least risky fetch strategy that removes the bottleneck.

## Detection Heuristics

- Accessing a collection or lazy association inside a loop is a likely N+1 risk.
- Serializing entities directly often exposes hidden lazy loads.
- Multiple repository calls for related data should be evaluated as a single query or batched access.
- A query that returns far more columns or rows than the caller uses is usually over-fetching.
- JDBC code that builds SQL in a loop is usually the wrong shape for the workload.

## Recommended Fixes

- Use `join fetch` only when the association is always needed and result cardinality stays safe.
- Prefer entity graphs, projections, or DTO queries when the caller needs a subset of data.
- Use batch fetching or subselect fetching when eager joins would explode row counts.
- Move repeated row-by-row JDBC work to batch updates or set-based SQL.
- Keep transactional boundaries aligned with the data access that requires them.

## Decision Rules

- Choose `join fetch` for predictable, small graphs.
- Choose projections or DTOs for read-heavy endpoints with narrow data needs.
- Choose batch fetching when many parents need the same child association.
- Avoid global eager loading unless the association is universally required.

## Output Standard

For each issue, provide:

- Location
- Performance symptom
- Root cause
- Recommended fetch or query strategy
- Tradeoff or risk of the proposed fix

## Reporting Style

- Be specific about the access pattern, not just the ORM feature.
- Prefer fixes that reduce round trips without changing business behavior.
- Call out when a query plan improvement may affect memory, cardinality, or pagination.

## Troubleshooting

- If the bottleneck is not clear, distinguish round trips, hydration cost, and contention.
- If the fix changes fetch behavior, check pagination and result size impact.
- If the issue is only theoretical, confirm it with a realistic call path or plan.

## References

- Database schema and query plan documentation
- JPA and JDBC usage patterns in the codebase
