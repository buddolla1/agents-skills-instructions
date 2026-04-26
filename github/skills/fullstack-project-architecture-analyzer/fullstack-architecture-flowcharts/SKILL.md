---
name: fullstack-architecture-flowcharts
description: Generates architecture flowcharts for React, Spring Boot, or full-stack projects. Use when the user wants only flowchart analysis or the flowcharts portion of a larger architecture document.
---

# Full-Stack Architecture Flowcharts

Use this skill to produce Mermaid flowcharts that show system behavior and major runtime paths.

## When to Use This Skill

Use this skill when the user selects flowcharts or full doc and wants the main flows visualized.

## Prerequisites

- Source files and runtime configuration
- Project type
- Main request, response, and integration paths

## Goal

Show the important flows in a visual format that is aligned with the codebase.

## Output Standard

Provide:

- Flowcharts
- Mermaid diagrams
- Short notes explaining each flow

## Guardrails

- Do not create diagram paths that are not supported by the codebase.
- Keep the flowcharts readable and focused on the most important flows.

## Reporting Style

- Be factual and concise.
- Prefer the clearest flow over a crowded diagram.

## References

- Source code and configuration
- The coordinator skill
