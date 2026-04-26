---
name: fullstack-project-architecture-analyzer
description: Coordinates React, Spring Boot, or full-stack architecture analysis into smaller skills for HLD, LLD, External APIs, flowcharts, components, or a full Markdown architecture document. Use when you want progressive loading and want the user to choose the first artifact to create.
---

# Full-Stack Project Architecture Analyzer

Use this skill as the coordinator for architecture analysis across React, Spring Boot, or full-stack projects.

## When to Use This Skill

Use this skill when the user asks for architecture analysis, component mapping, dependency flow, external API review, HLD, LLD, or a Markdown architecture document.

## First Question

Ask the user what they want to create first:

- HLD
- LLD
- External APIs
- Flowcharts
- Components
- Full doc

If the request does not specify one of these, ask this question before proceeding.

## Progressive Loading Model

1. Load [fullstack-architecture-intake](fullstack-architecture-intake/SKILL.md) first to confirm the project type and the requested artifact.
2. Load [fullstack-architecture-hld](fullstack-architecture-hld/SKILL.md) when the user wants an HLD section or HLD-only document.
3. Load [fullstack-architecture-lld](fullstack-architecture-lld/SKILL.md) when the user wants an LLD section or LLD-only document.
4. Load [fullstack-architecture-external-apis](fullstack-architecture-external-apis/SKILL.md) when the user wants only external integrations.
5. Load [fullstack-architecture-flowcharts](fullstack-architecture-flowcharts/SKILL.md) when the user wants flowchart-only analysis.
6. Load [fullstack-architecture-components](fullstack-architecture-components/SKILL.md) when the user wants component mapping only.
7. Load [fullstack-architecture-full-doc](fullstack-architecture-full-doc/SKILL.md) when the user wants the complete architecture document.

## Source of Truth

- Prefer real source files over generated or build output.
- Inspect Spring config first: `src/main/resources/application.yaml`, then `application.yml`, `bootstrap.yaml`, and `bootstrap.yml`.
- Inspect `pom.xml`, `package.json`, routes, controllers, services, repositories, entities, DTOs, hooks, components, and resources.
- Read external integrations and endpoint settings from `application.yaml` when present, including `base-url`, `url`, `uri`, `endpoint`, `host`, `port`, and API-key style properties.
- Exclude `target/`, `dist/`, `build/`, `node_modules/`, and `.git/` unless the user explicitly asks otherwise.

## Guardrails

- Do not generate the full doc until the user explicitly asks for it.
- Do not load later skills before the user chooses the requested artifact.
- Do not invent architecture as if it already exists.
- Do not mix formats; output Markdown only unless the user explicitly asks for something else.

## References

- The source code and configuration of the project
- The specialized architecture skills in this directory
