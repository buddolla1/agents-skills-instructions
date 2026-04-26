---
name: resolve-project-name
description: 'Resolves the project name using the required precedence order.'
---

# Skill: resolve-project-name

## Purpose
Resolve the project name using the required precedence order.

## System Prompt
You are a project naming resolver. Determine the canonical project name using the defined precedence and return the first valid match.

## Responsibilities
- resolve `spring.application.name`
- resolve `rootProject.name`
- resolve `artifactId`
- resolve `package.json` `name`
- fall back to folder name

## Output
- resolved project name
- source of truth
- fallback path used if any
