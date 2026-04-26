---
name: spring-3x-to-4x-modernization
description: Modernize Spring Framework 3.x applications to Spring Framework 4.x while improving structure safely. Use when migrating legacy Spring XML, upgrading framework APIs, resolving compatibility gaps, reducing technical debt, or refactoring code paths without changing behavior.
---

# Spring 3.x to 4.x Modernization

## When to Use This Skill

Use this skill when upgrading a Spring Framework 3.x application to 4.x and you need to preserve behavior while improving structure and maintainability.

## Prerequisites

- The current Spring version and module layout
- The application entry points, configuration style, and dependency graph
- The behavior that must remain stable during the migration
- Existing tests or runtime checks that protect the old contract

## Goal

Move a legacy Spring 3.x application to Spring 4.x with minimal behavioral drift, explicit compatibility handling, and a clear rollback path.

## What to Modernize

- Spring XML, Java config, and component wiring that depend on 3.x-era conventions
- Framework APIs that changed between Spring 3.x and 4.x
- Controllers, services, and repositories that can be simplified safely during the upgrade
- Error handling, validation, and transaction boundaries that need compatibility review
- Repetitive framework-heavy boilerplate that can be reduced once the 4.x path is proven

## Step-by-Step Workflows

1. Inventory the existing Spring 3.x application style, bootstrapping model, and configuration surface.
2. Identify framework APIs, XML namespaces, annotations, and libraries that change in Spring 4.x.
3. Classify upgrade work by risk: low-risk mechanical changes, compatibility fixes, and behavior-sensitive refactors.
4. Upgrade one boundary at a time: configuration, wiring, web layer, service layer, then persistence.
5. Add or preserve tests before changing framework-dependent code.
6. Validate each step against the same runtime behavior the legacy system already provides.

## Migration Rules

- Prefer compatibility-first changes over broad rewrites.
- Keep Spring 3.x and 4.x specific code isolated only as long as needed.
- Remove framework ceremony only after the replacement path is proven.
- Make migration steps small enough to review and roll back.
- Use Spring 4.x capabilities only where they do not alter required behavior.
- Treat deprecated or removed APIs as migration blockers, not cleanup opportunities.

## Structural Improvements

- Extract focused classes where legacy code has multiple responsibilities.
- Replace scattered configuration with centralized, typed configuration where appropriate.
- Simplify startup and dependency wiring only after the 4.x path is validated.
- Reduce manual object creation and lifecycle management where the framework upgrade allows it.
- Preserve public contracts while improving internal organization.

## Guardrails

- Do not change behavior as a side effect of cleanup.
- Do not combine migration and redesign in the same step unless risk is understood.
- Do not delete 3.x compatibility paths until the 4.x path is validated.
- Keep rollback simple for each migration increment.
- Do not assume a framework upgrade is safe because the code compiles.

## Output Standard

For each modernization step, provide:

- Legacy area or component
- Spring 4.x replacement or equivalent
- Behavior that must stay unchanged
- Structural improvement made
- Validation or rollback note

## Reporting Style

- Be explicit about what is being preserved versus improved.
- Prefer incremental migration paths over big-bang rewrites.
- Call out where legacy code should remain temporarily to reduce risk.
- Explain any compatibility gaps in plain terms.

## Troubleshooting

- If the migration step is too large, split it at the configuration or wiring boundary.
- If behavior changes, restore the previous path and add missing coverage.
- If the Spring 4.x path is unproven, keep the 3.x path until validation is complete.
- If an API is removed or renamed, isolate that change before refactoring.

## References

- Spring 3.x and 4.x migration notes
- Existing architecture and integration test coverage
