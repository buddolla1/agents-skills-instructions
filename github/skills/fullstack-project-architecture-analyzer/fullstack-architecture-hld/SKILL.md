---
name: fullstack-architecture-hld
description: Generates HLD architecture content for React, Spring Boot, or full-stack projects. Use when the user wants only the high-level design, component overview, flowcharts, or the HLD portion of a larger architecture document.
---

# Full-Stack Architecture HLD

Use this skill to produce the high-level design view of the system.

## When to Use This Skill

Use this skill when the user selects HLD or full doc and the high-level architecture needs to be written.

## Prerequisites

- Source files and runtime configuration
- Project type
- Any known external systems or boundaries

## Goal

Describe the system at a high level with components, boundaries, and top-level flows.

## Output Standard

Provide:

- Project overview
- HLD
- Main components
- High-level flowchart when useful
- Related context that clarifies boundaries or integrations when logically needed

## Guardrails

- Do not drift into implementation detail that belongs in LLD.
- Do not invent components not supported by the codebase.
- Do not force extra sections when they do not add value.

## Reporting Style

- Be factual and concise.
- Keep the HLD easy to scan.

## References

- Source code and configuration
- The coordinator skill
