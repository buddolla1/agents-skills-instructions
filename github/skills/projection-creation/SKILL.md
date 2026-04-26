---
name: projection-creation
description: Create Spring Data JPA or JDBC projections and DTO views for read paths. Use when designing query-time DTOs, interface projections, constructor projections, or lightweight response models to avoid over-fetching and entity exposure.
---

# Projection Creation

Use this skill when building read models that return only the data a caller needs.

## Goal

Create projections that reduce payload size, avoid loading unnecessary entity graphs, and keep read paths explicit and maintainable.

## When to Use This Skill

Use this skill when building read models that return only the data a caller needs. If the target implementation is not clear, ask the user whether they want a JPA project or a JDBC project before generating the projection guidance.

## Prerequisites

- The target project style: JPA or JDBC
- The read path or repository method being designed
- The fields the caller actually needs

## What to Create

- Interface-based Spring Data JPA projections
- DTO constructor projections
- Nested or flattened read models where appropriate
- Query-specific response shapes for services and APIs

## Step-by-Step Workflows

1. Ask the user whether they want a JPA project or a JDBC project before generating the projection guidance if that choice is not already specified.
2. Identify the fields the caller actually needs.
3. Choose the narrowest projection shape that satisfies the use case.
4. Keep the projection aligned with the query and repository method.
5. Prefer read-only models for read-heavy paths.
6. Validate that the projection avoids exposing full entities unnecessarily.

## Projection Selection Rules

- Use interface projections for simple read-only views.
- Use constructor DTO projections when the shape must be explicit or stable.
- Use nested projections only when the relationship is simple and worth the complexity.
- Prefer flattened DTOs when consumers do not need the entity structure.

## Guardrails

- Do not return entities when a projection is enough.
- Do not over-design projections with fields no caller uses.
- Do not build projections that duplicate full domain models without benefit.
- Keep query and projection names aligned so intent is obvious.

## Output Standard

For each projection, provide:

- Use case or repository method
- Projection type selected
- Fields included
- Why the projection is appropriate
- Any tradeoff or limitation

## Reporting Style

- Be specific about the read path and the data saved by the projection.
- Prefer simple, stable shapes over clever abstractions.
- Explain how the projection reduces query cost or entity coupling.

## Troubleshooting

- If the projection becomes too large, split it into a narrower read model.
- If the caller needs behavior, not just data, keep that logic outside the projection.
- If the data shape changes often, prefer a DTO projection with an explicit constructor.

## References

- Spring Data JPA projection conventions
- Related repository and query definitions
