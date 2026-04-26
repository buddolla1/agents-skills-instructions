---
name: logging-observability-enhancer
description: Improve logging and observability with structured logs and correlation IDs. Use when reviewing Java or Spring Boot services for traceability, request context propagation, log consistency, production debugging, and observability hygiene.
---

# Logging / Observability Enhancer

## When to Use This Skill

Use this skill when improving application logs so production issues can be traced and diagnosed quickly.

## Prerequisites

- The request boundary and downstream calls that need traceability
- The logging framework or conventions already used by the service
- Any privacy or data-handling constraints that affect log content

## Goal

Make logs consistent, machine-readable, and traceable across request boundaries and service interactions.

## What to Enforce

- Structured logging instead of free-form text where practical
- Correlation IDs or trace IDs on every request path
- Consistent fields for service, operation, status, duration, and error context
- Propagation of request identity across downstream calls
- Clear separation between diagnostic data and sensitive data

## Step-by-Step Workflows

1. Identify the request entry point and the log context that should follow it.
2. Check whether a correlation ID is created, propagated, and included in all relevant logs.
3. Confirm log messages are structured enough for querying and aggregation.
4. Look for missing error context, inconsistent field names, or log spam.
5. Recommend the minimum logging change that improves supportability without leaking secrets.

## Structured Logging Guidance

- Log stable key-value fields instead of embedding data only in message text.
- Keep field names consistent across services and handlers.
- Include operation name, request identifier, outcome, and timing where useful.
- Log errors with enough context to diagnose without requiring source code access.

## Correlation ID Guidance

- Generate or accept a correlation ID at the service boundary.
- Propagate it through downstream HTTP, messaging, or async boundaries.
- Include it in all request-scoped logs and error reports.
- Prefer one canonical identifier strategy per system.

## Guardrails

- Do not log secrets, tokens, passwords, or personal data unnecessarily.
- Do not add noisy logs where metrics or traces are better.
- Do not invent multiple identifiers for the same request path.
- Avoid logging large payloads unless there is a clear support need.

## Output Standard

For each issue, provide:

- Location
- Logging or traceability gap
- Why it hurts production support
- Recommended structured logging or correlation fix
- Any privacy or noise risk

## Reporting Style

- Be specific about the missing field or propagation step.
- Prefer consistent log shape over ad hoc verbosity.
- Explain how the change improves troubleshooting in production.

## Troubleshooting

- If the logs are noisy, reduce volume before adding more fields.
- If correlation is missing, fix propagation at the service boundary first.
- If sensitive data appears in logs, remove it before expanding the log format.

## References

- Logging conventions for the service or platform
- Tracing and observability standards used by the team
