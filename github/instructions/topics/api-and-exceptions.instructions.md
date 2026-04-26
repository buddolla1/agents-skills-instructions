---
description: 'REST API design, validation, exception handling, and response contract guidance for Spring Boot services.'
applyTo: '**/*Controller.java, **/*Exception.java, **/*Advice.java, **/*Request*.java, **/*Response*.java, **/*Dto.java'
---

# API and Exception Standards

## REST API Design

- Use nouns, not verbs, in resource paths.
- Keep API versioning explicit where required by the organization.
- Use consistent error response structure.
- Do not expose internal entity structure directly.
- Paginate list endpoints.
- Support filtering and sorting for large collections where applicable.

## HTTP Methods

- `GET` for fetch
- `POST` for create
- `PUT` for full update
- `PATCH` for partial update
- `DELETE` for remove

## Validation

- Validate at the API boundary.
- Use Jakarta Bean Validation annotations such as `@Valid`, `@NotNull`, `@NotBlank`, `@Size`, `@Email`, and `@Pattern`.

## Exception Handling

- Use `@RestControllerAdvice` for centralized exception handling.
- Define domain-specific exceptions.
- Never expose stack traces or internal class names to API consumers.
- Map exceptions to stable, documented error codes.
- Log exceptions with enough context for troubleshooting.
- Wrap low-level persistence or integration exceptions in meaningful business exceptions where appropriate.

## Response Standards

- Keep success and error responses stable and documented.
- Do not change public response envelopes casually.
- Prefer backward-compatible additions over removals.
