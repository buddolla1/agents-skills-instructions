---
name: spring-boot-4-2-gradle-migration
description: Migrate an existing Spring Boot Gradle project to Spring Boot 4.2 by aligning the Gradle plugin, Spring Cloud BOM, and all dependency versions in a controlled, test-backed sequence.
---

# Spring Boot 4.2 Gradle Migration

Use this skill when an existing Spring Boot Gradle project needs a controlled upgrade to Spring Boot 4.2 and its managed dependency set.

## Goal

Move the project to Spring Boot 4.2 with the smallest compatible set of build and dependency changes, then resolve compile, test, and runtime breakage in a staged order.

## Prerequisites

- Current `build.gradle` or `build.gradle.kts`
- `settings.gradle` if version catalogs or included builds are used
- Current Spring Boot plugin version
- Current Spring Cloud BOM and any other BOMs or platform imports
- Java version, Gradle wrapper version, and test coverage
- Any explicit dependency pins, exclusions, or dependency-locking files

## Workflow

1. Inventory the current baseline.
   - Spring Boot plugin version
   - Spring Cloud BOM version
   - Java target
   - Gradle wrapper version
   - Explicitly pinned libraries that may be overridden by the BOM

2. Check compatibility before editing.
   - Confirm the target Spring Boot 4.2 line is appropriate for the project
   - Confirm the matching Spring Cloud release train or BOM for that Boot line
   - Identify libraries that must move together, such as security, data, logging, test, observability, and cloud clients

3. Update the build in a safe order.
   - Update the Gradle wrapper and Spring Boot plugin first if required
   - Update BOM imports next
   - Remove unnecessary hardcoded versions that should come from dependency management
   - Keep intentional overrides only where the project needs them

4. Reconcile dependency drift.
   - Compare old and new resolved dependency trees
   - Flag removed, relocated, or incompatible artifacts
   - Update direct dependency versions only when they are not covered by the BOM
   - Preserve exclusions that are still required

5. Fix source and config breakage.
   - Address compilation errors from API changes
   - Update configuration keys or auto-configuration assumptions where necessary
   - Review tests, starters, and integration points that depend on framework behavior

6. Validate incrementally.
   - Run build, unit tests, and integration tests after each major change
   - Use dependency insight or dependency tree output to verify the managed version set
   - Capture any remaining manual follow-up items instead of guessing

## Guardrails

- Do not bump every jar blindly.
- Do not override the BOM unless there is a clear, documented reason.
- Do not combine build migration, framework refactoring, and feature work in one step.
- Do not remove exclusions or custom dependency pins without checking the impact on runtime behavior.
- Do not assume compile success means the migration is complete.

## Output Standard

When using this skill, report:

- current baseline
- target Spring Boot and Spring Cloud versions
- build files changed
- dependency groups updated
- direct version overrides retained
- compile or test breakages found
- remaining follow-up items

## References to Consult

- Current Gradle build files
- Spring Boot release notes and migration notes
- Spring Cloud compatibility guidance
- Dependency tree output from the project
