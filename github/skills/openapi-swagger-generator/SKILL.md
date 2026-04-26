---
name: openapi-swagger-generator
description: Generate and validate OpenAPI or Swagger API documentation. Use when working on Spring Boot APIs, controller changes, request or response models, endpoint descriptions, or when checking contract consistency between implementation and published docs.
---

# OpenAPI / Swagger Generator

## When to Use This Skill

Use this skill when creating or validating API documentation for Spring-based services.

## Prerequisites

- The controller, DTO, and error model being documented
- The source of truth for the API contract
- Any generated spec or handwritten OpenAPI file to compare against

## Goal

Keep API docs accurate, machine-readable, and aligned with the implemented contract so consumers can rely on them.

## What to Detect

- Missing or stale endpoint documentation
- Request or response schema drift
- Path, method, or parameter mismatches between code and docs
- Undocumented status codes, headers, or error bodies
- Incorrect examples, descriptions, or field constraints
- Contract changes that are not reflected in published OpenAPI output

## Step-by-Step Workflows

1. Read the controller, DTOs, validation rules, and exception model together.
2. Compare the implemented contract to the generated or handwritten OpenAPI spec.
3. Flag any mismatch that could break client generation or consumer expectations.
4. Prefer documentation changes that derive directly from code annotations or schema definitions.
5. Verify the resulting spec is stable and consistent across environments.

## Consistency Checks

- Endpoint paths and HTTP methods match implementation
- Query, path, header, and body parameters are documented correctly
- Required vs optional fields are accurate
- Validation constraints are reflected in schema metadata
- Success and error responses are complete and realistic
- Examples match current payload shapes and naming conventions

## Recommended Fixes

- Annotate controllers and DTOs so the spec is generated from source of truth.
- Centralize shared error responses and schema components.
- Remove stale examples and descriptions that no longer match the contract.
- Regenerate and review the spec whenever the API surface changes.
- Treat breaking contract changes as versioned changes, not documentation-only updates.

## Output Standard

For each issue, provide:

- Location
- Contract inconsistency
- Why it matters to consumers
- Recommended documentation or code fix
- Validation note if the spec must be regenerated

## Output Location

- Write generated API documentation artifacts to the repository `doc/` folder unless the user explicitly requests a different path.

## Reporting Style

- Be explicit about whether the source of truth is code, annotations, or a static spec.
- Prefer corrections that make the documentation deterministic and maintainable.
- Call out consumer impact when the published contract diverges from implementation.

## Troubleshooting

- If the spec and code differ, identify which one is authoritative before editing.
- If examples are stale, regenerate them from the actual payload shape.
- If the contract has changed, make sure versioning or compatibility is addressed.

## References

- OpenAPI or Swagger conventions used by the project
- Related controller and DTO definitions
