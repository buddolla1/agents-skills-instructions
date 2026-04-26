---
description: 'Architecture, layering, Java coding standards, and anti-pattern guidance for Spring Boot codebases.'
applyTo: '**/*.java'
---

# Architecture and Coding Standards

## Standard Project Structure

```text
src/main/java/com/company/project
 ├── config
 ├── controller
 ├── service
 ├── repository
 ├── jdbc
 ├── dto
 ├── entity
 ├── mapper
 ├── exception
 ├── security
 ├── client
 ├── util
 └── ProjectApplication.java
```

## Structure Rules

- Controllers handle HTTP transport only.
- Services contain business logic and transaction boundaries.
- Repositories handle persistence concerns only.
- `jdbc` contains JDBC/JdbcTemplate repositories and row mappers.
- DTOs must not be used as JPA entities.
- Entities must not be returned directly from controllers.

## Architecture Guidelines

- Prefer separation of concerns.
- Prefer constructor-based dependency injection.
- Use interface-driven design when it improves testability and clarity.
- Keep the flow `Controller → Service → Repository`.
- Keep domain logic isolated from transport and persistence logic.
- Avoid business logic in controllers.
- Avoid database access directly from controllers or services without repository abstraction.
- Avoid circular dependencies.
- Avoid field injection.
- Avoid leaking persistence concerns into API contracts.

## Coding Standards

- Use PascalCase for classes, camelCase for methods and variables, and UPPER_SNAKE_CASE for constants.
- Prefer constructor injection over field injection.
- Keep methods small and intention-revealing.
- Keep classes focused on a single responsibility.
- Use enums instead of magic strings.
- Avoid static mutable state.
- Prefer immutable DTOs and value objects where practical.
- Use Lombok selectively.
- Prefer explicit code over clever code.

## Null and Optional Usage

- Do not return `null` from service or repository APIs unless clearly documented.
- Use `Optional<T>` for return types where absence is valid.
- Do not use `Optional` for entity fields, DTO fields, or method parameters.
- Prefer empty collections over `null` collections.

## Java Standards

- Use Java 21+ features where they improve clarity and maintainability.
- Prefer records for immutable DTOs where appropriate.
- Use sealed classes only where they clearly model constrained hierarchies.
- Prefer modern switch expressions where readable.
- Favor composition over inheritance.
- Program to interfaces where it improves design.
- Keep fields private.
- Make invalid states hard to represent.
- Keep methods short and avoid deep nesting.
- Prefer self-documenting code and meaningful names.

## Anti-Patterns

- God classes
- Tight coupling
- Hardcoded configuration
- Ignoring exceptions
- Returning entities directly from controllers
- Field injection
- Database logic in controllers
- Remote calls inside transactions
- String-concatenated SQL
- Blind use of JPA for every data access pattern
