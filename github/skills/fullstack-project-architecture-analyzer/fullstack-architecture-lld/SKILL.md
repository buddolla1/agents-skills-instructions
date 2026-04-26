---
name: fullstack-architecture-lld
description: Generates LLD architecture content for React, Spring Boot, or full-stack projects. Use when the user wants only the low-level design, implementation flowcharts, detailed components, or the LLD portion of a larger architecture document.
---

# Full-Stack Architecture LLD

Use this skill to produce the low-level design view of the system.

## When to Use This Skill

Use this skill when the user selects LLD or full doc and the implementation-level design needs to be written.

## Prerequisites

- Source files and runtime configuration
- Project type
- Relevant controllers, services, repositories, components, and data flows

## Goal

Describe the system at a lower level with implementation-oriented structure and behavior.

## Output Standard

Provide:

- LLD
- Detailed components and responsibilities
- Data flow and interaction notes
- Sequence or flow diagrams when useful
- Implementation notes or constraints that are logically relevant

## Guardrails

- Do not repeat the HLD verbatim.
- Do not invent implementation details not present in the codebase.
- Do not add diagrams that do not improve understanding.

## Reporting Style

- Be precise and implementation-aware.
- Keep the LLD practical for engineers.

## References

- Source code and configuration
- The coordinator skill
