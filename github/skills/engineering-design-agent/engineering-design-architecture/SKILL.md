---
name: engineering-design-architecture
description: Produces architecture-focused sections such as overview, HLD, LLD, and Mermaid diagrams for engineering design artifacts. Use when the requested output includes architecture design or technical structure.
---

# Engineering Design Architecture

Use this skill to draft architecture-specific sections when the output requires technical design detail.

## When to Use This Skill

Use this skill when `outputMode` is `architecture` or `full_design`, or when the requirement clearly asks for technical design.

## Prerequisites

- Feature summary
- Assumptions
- Repo context summary
- Optional `architectureType`

## Goal

Create architecture sections that are specific enough to guide implementation without inventing unsupported details.

## Step-by-Step Workflows

1. Summarize the architecture at a high level.
2. Write the HLD in terms of components and flows.
3. Write the LLD with implementation-level detail appropriate for the plan.
4. Add Mermaid diagrams when they improve clarity.
5. Capture risks, constraints, and key assumptions.

## Output Standard

For architecture, provide:

- Architecture overview
- HLD
- LLD
- Diagrams
- Risks
- Assumptions

## Guardrails

- Do not invent components or integrations not supported by repo context or user input.
- Do not skip diagrams when architecture output was explicitly requested.
- Do not restate unrelated non-architecture sections.

## Reporting Style

- Be precise and concise.
- Keep the technical design aligned with visible repo conventions.

## References

- README, build files, and relevant source or config files
- The scope, planning, and validation skills
