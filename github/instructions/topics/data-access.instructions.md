---
description: 'Persistence, JPA, JDBC, repository, and transaction management guidance for Spring Boot applications.'
applyTo: '**/*Repository.java, **/repository/**/*.java, **/jdbc/**/*.java, **/entity/**/*.java, **/*Entity.java'
---

# Data Access Standards

## Persistence Strategy

- Use Spring Data JPA / Hibernate for aggregate-oriented CRUD and relational mapping.
- Use Spring JDBC / JdbcTemplate for performance-sensitive queries, reporting queries, bulk operations, and SQL-heavy use cases.

## General Database Rules

- Use database migrations with Flyway or Liquibase.
- Keep schema changes versioned and reversible when feasible.
- Index frequently queried columns.
- Use transactions only where needed.
- Keep write logic consistent and auditable.
- Avoid N+1 query issues.
- Use pagination for large result sets.

## JPA / Hibernate Best Practices

- Use Spring Data JPA for standard CRUD and aggregate persistence.
- Use UUIDs or the organization-approved identifier strategy.
- Default relationships to `FetchType.LAZY` unless eager loading is justified.
- Avoid bidirectional relationships unless clearly needed.
- Use projections or dedicated read models for read-heavy queries.
- Keep entity lifecycle logic minimal.
- Do not put business workflows inside entities.
- Avoid exposing JPA entities outside the service boundary.
- Be explicit about transaction boundaries in service layer methods.
- Keep repository implementations persistence-focused.
- Use `@EntityGraph`, fetch joins, or tailored queries to control loading.

## JDBC / JdbcTemplate Standards

- Use JDBC when SQL needs tight control, performance is critical, or the mapping is simpler in SQL than in ORM.
- Prefer `JdbcTemplate` or `NamedParameterJdbcTemplate` over raw JDBC boilerplate.
- Keep SQL in repository or `jdbc` package classes, not in services or controllers.
- Use named parameters for readability and safety.
- Use row mappers or result set extractors for clear mapping.
- Keep SQL explicit and formatted.
- Parameterize all queries; never concatenate user input into SQL.
- Batch inserts/updates where appropriate.
- Handle empty results explicitly.
- Document complex SQL.
- Services may call JDBC repositories the same way they call JPA repositories.
- Do not mix transaction handling inside JDBC repository classes; transaction boundaries belong in services.

## Transaction Management

- Define transaction boundaries at the service layer.
- Use `@Transactional` on service methods, not controllers.
- Keep transactions short-lived.
- Use `readOnly = true` for read-only transactions where helpful.
- Avoid remote calls inside active database transactions.
- Be explicit about rollback behavior for checked exceptions if needed.
