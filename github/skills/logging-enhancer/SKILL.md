---
name: logging-enhancer
description: 'Improve Log4j2-based logging and observability in Java or Spring Boot services. Use when reviewing request traceability, ThreadContext correlation IDs, structured JSON or pattern layouts, logger level discipline, exception logging, async logging, and production supportability.'
---

# Logging / Observability Enhancer

## When to Use This Skill

Use this skill when a Java or Spring Boot service uses Log4j2, or should be reviewed against Log4j2-oriented logging standards for production diagnostics and observability.

If the user provides one or more Java files, inspect the current logging format in those files first, then recommend the smallest useful changes before editing anything.

## Prerequisites

- The request boundary and downstream calls that need traceability
- The current Log4j2 configuration and appenders if present
- Any privacy or data-handling constraints that affect log content

## Goal

Make Log4j2 output consistent, queryable, and traceable across request boundaries and service interactions without adding noise or leaking sensitive data.

For file-specific requests, first analyze the current logging statements, explain the recommended changes, and ask for explicit user consent before applying code edits.

## What to Enforce

- `ThreadContext` or equivalent MDC-backed context for correlation identifiers
- Parameterized Log4j2 message style using `{}` placeholders instead of string concatenation
- Structured output through `JsonLayout`, `JsonTemplateLayout`, or a disciplined `PatternLayout`
- Consistent fields for service, operation, status, duration, correlation ID, and error context
- Clear logger naming and log-level discipline across packages and execution paths
- Propagation of request identity across downstream calls and async boundaries
- Clear separation between diagnostic data and sensitive data

## Step-by-Step Workflows

1. If the input is a Java file or a small file set, inspect the current logging statements before proposing any changes.
2. Identify the request entry point, current logger usage, and the Log4j2 configuration that controls output shape when relevant.
3. Check whether a correlation ID is created or accepted at the boundary, stored in `ThreadContext`, propagated, and cleared correctly.
4. Confirm logs are structured enough for querying, either through JSON layout or a stable pattern with named context fields.
5. Review logger names and levels for noisy `INFO` logs, missing `WARN` or `ERROR` signals, and misuse of `DEBUG` in hot paths.
6. Check exception logging for lost stack traces, duplicate logging, or message-only logging that hides the cause.
7. Review async or executor usage for lost context propagation.
8. Recommend the minimum change that improves supportability without leaking secrets.
9. Ask for explicit user consent before making any source-code edits.

## File Input Workflow

When the user provides a Java file as input:

1. Inspect the existing logging style in that file.
2. Summarize the current patterns, such as parameterized logging, string concatenation, missing exception objects, missing context, or noisy levels.
3. List the recommended changes needed to align with the logging standard.
4. Ask whether to apply those changes.
5. Only edit the file after the user clearly approves.

## Log4j2 Configuration Guidance

- Prefer `JsonTemplateLayout` or `JsonLayout` when logs are shipped to a centralized platform.
- If `PatternLayout` is used, ensure the pattern includes timestamp, level, logger, thread, correlation ID from `ThreadContext`, and exception output.
- Keep appender configuration environment-appropriate and avoid local-only assumptions in production services.
- Prefer centralized configuration patterns over ad hoc per-class formatting conventions.

## Correlation and Context Guidance

- Generate or accept a correlation ID at the service boundary.
- Store it in Log4j2 `ThreadContext` using one canonical key per system.
- Propagate it through downstream HTTP, messaging, or async boundaries.
- Ensure executors, schedulers, or custom async flows copy or restore the needed context.
- Clear `ThreadContext` at the end of the request scope to avoid leakage across requests.

## Logger and Level Guidance

- Use class- or package-appropriate loggers with stable names.
- Keep application log statements in normal parameterized Log4j2 form such as `logger.info("User {} logged in from IP {}", username, ipAddress)`.
- Reserve `ERROR` for failed operations that need operator attention.
- Use `WARN` for degraded or unexpected conditions that still allow progress.
- Use `INFO` for lifecycle or business-significant events, not step-by-step tracing.
- Keep `DEBUG` and `TRACE` out of hot paths unless explicitly gated for diagnosis.

## Exception Logging Guidance

- Pass the throwable as the last logger argument, for example `logger.error("Failed to process order {}", orderId, exception)`.
- Log the exception object, not only the exception message.
- Keep one clear log at the right boundary instead of logging and rethrowing at every layer.
- Include enough business and request context to diagnose the failure path.
- Avoid swallowing exceptions after logging unless the fallback behavior is intentional and documented.

## Guardrails

- Do not log secrets, tokens, passwords, or personal data unnecessarily.
- Do not add noisy logs where metrics, traces, or alerts are better tools.
- Do not invent multiple identifiers for the same request path.
- Do not mix incompatible correlation key names across handlers and clients.
- Do not leave `ThreadContext` uncleared in pooled-thread execution models.
- Do not replace clear parameterized log statements with manual string building.
- Avoid logging large payloads unless there is a clear support need.
- Do not edit Java files immediately after analysis; require explicit user consent first.

## Output Standard

For each issue, provide:

- Location
- Current logging pattern
- Log4j2 or traceability gap
- Why it hurts production support
- Recommended Log4j2 configuration, logger usage, or correlation fix
- Any privacy or noise risk

For file-specific reviews, include a short recommendation summary and a direct consent question before any edit is made.

## Reporting Style

- Be specific about the missing `ThreadContext` key, layout field, logger level, or propagation step.
- Describe the current logging statement shape before recommending a replacement.
- Prefer consistent log shape over ad hoc verbosity.
- Explain how the change improves troubleshooting in production.
- Call out whether the issue is in application code, framework wiring, or Log4j2 configuration.
- For code-edit requests, stop after recommendations and wait for approval before changing the file.

## Troubleshooting

- If the logs are noisy, reduce level misuse before adding more fields.
- If correlation is missing, fix `ThreadContext` population and propagation at the service boundary first.
- If async work loses context, inspect executor wrapping and handoff points.
- If sensitive data appears in logs, remove it before expanding the log format.

## References

- Log4j2 configuration and layout conventions for the service or platform
- Tracing and observability standards used by the team
