---
name: fullstack-architecture-full-doc
description: Generates the full Markdown architecture document for React, Spring Boot, or full-stack projects. Use when the user wants the complete architecture report with HLD, LLD, flowcharts, components, external APIs, findings, recommendations, and any other logically relevant sections.
---

# Full-Stack Architecture Full Doc

Use this skill to generate the complete architecture report.

## When to Use This Skill

Use this skill when the user selects full doc and wants the complete architecture document.

## Prerequisites

- Source files and runtime configuration
- Project type
- External integrations and dependency boundaries

## Goal

Produce the full Markdown architecture document with the same core sections as the original analyzer.

## Output Contract

Generate these sections in order:

1. `Project Overview`
2. `HLD`
3. `LLD`
4. `Flowcharts`
5. `Components`
6. `External APIs`
7. `Findings`
8. `Recommendations`

- Render `External APIs` as a Mermaid flowchart plus a short description of each integration.
- Write the report to `docs/Architecture.md`.
- Include only additional sections that are logically justified by the codebase and improve clarity.
- Prefer concise subsections under the main headings when extra detail is needed.

## Guardrails

- Do not invent future architecture as if it already exists.
- Always include an `External APIs` section, even when it is empty.
- Keep diagrams aligned with the actual codebase and config.
- Do not add decorative sections that do not help the reader understand the system.

## Reporting Style

- Be factual and specific about what exists.
- Prefer concise, maintainable architecture notes over long narrative text.

## References

- Source code and configuration
- The coordinator skill
