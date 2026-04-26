---
name: fullstack-architecture-external-apis
description: Documents external APIs and integrations for React, Spring Boot, or full-stack projects. Use when the user wants only external API mapping, flowcharts, dependency notes, or the external APIs portion of a larger architecture document.
---

# Full-Stack Architecture External APIs

Use this skill to document outbound integrations and external service dependencies.

## When to Use This Skill

Use this skill when the user selects External APIs or full doc and the integration surface needs to be documented.

## Prerequisites

- `application.yaml`, `application.yml`, `bootstrap.yaml`, or `bootstrap.yml`
- Runtime source files that call external services
- Known integration endpoints, base URLs, or client libraries

## Goal

Identify and document the real external APIs and integration points used by the project.

## Output Standard

Provide:

- External APIs
- Short description of each integration
- Mermaid flowchart when useful
- Integration notes that are logically relevant, such as auth, retries, or endpoint boundaries

## Guardrails

- Do not invent integrations that are not in the codebase or config.
- If no explicit endpoint exists, state that the default library endpoint is implied.
- Do not list speculative APIs as confirmed integrations.

## Reporting Style

- Be factual and specific.
- Call out only verified integrations.

## References

- Source code and configuration
- The coordinator skill
