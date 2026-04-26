---
description: 'Top-level Spring Boot engineering guidance that routes to deeper topic-specific instruction files when needed.'
applyTo: '**/*.java, **/*.yml, **/*.yaml, **/*.properties, pom.xml, build.gradle, build.gradle.kts, settings.gradle, settings.gradle.kts, README.md'
---

# Spring Boot Engineering Standards

Use this file as the entry point for Spring Boot work in this repository. It is the default guidance source; load the topic files below only when the task needs deeper rules.

## Baseline Context

- Language: Java 21+
- Framework: Spring Boot 3.x+
- API style: REST
- Architecture: layered, clean, or hexagonal depending on the service
- Build tool: Maven or Gradle

## When To Load Topic Files

The deeper instruction files for this guidance live in the `topics/` folder next to this file.

- [architecture-and-coding.instructions.md](topics/architecture-and-coding.instructions.md): package structure, layering, Java style, and anti-patterns
- [api-and-exceptions.instructions.md](topics/api-and-exceptions.instructions.md): REST design, validation, exception handling, and response contracts
- [data-access.instructions.md](topics/data-access.instructions.md): JPA, JDBC, repositories, and transaction boundaries
- [quality-and-ops.instructions.md](topics/quality-and-ops.instructions.md): security, testing, logging, performance, build, deployment, and documentation

## Working Rules

### Existing Code

- Preserve local style, naming, structure, and intent.
- Avoid broad formatting-only changes.
- Avoid architectural refactoring unless explicitly requested.
- Preserve behavior, public API contracts, and transaction boundaries.

### New Code

- Follow this document as the default standard.
- Match the repository's existing package structure and conventions.
- Prefer explicit, readable, maintainable code over clever abstractions.

### Conflict Resolution

- Preserved behavior wins over new conventions.
- Apply new standards only when they do not change behavior or contracts.

## Hard Constraints

- Do not refactor large sections without instruction.
- Do not introduce breaking architectural changes.
- Do not change API contracts, transaction semantics, or persistence strategy unless explicitly requested.
- Do not leak persistence, transport, or internal framework details across boundaries.

## Practical Defaults

- Use constructor injection.
- Keep controllers focused on HTTP concerns.
- Keep business logic in services.
- Keep repositories focused on persistence.
- Prefer immutable DTOs and value objects where practical.
- Use clear validation, explicit exceptions, and stable response shapes.
- Prefer tests and small targeted changes over speculative cleanup.
