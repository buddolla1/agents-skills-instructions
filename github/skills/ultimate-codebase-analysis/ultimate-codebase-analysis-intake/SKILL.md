---
name: ultimate-codebase-analysis-intake
description: Resolves codebase-analysis scope, scan mode, and focus areas before deeper review. Use when a repository or diff review request needs intake, narrowing, or review planning.
---

# Ultimate Codebase Analysis Intake

Use this skill to determine the minimal review scope before analysis begins.

## When to Use This Skill

Use this skill at the start of a repository-wide or diff-wide analysis request.

## Goal

Resolve scan mode, requested focus, instruction-source availability, and whether the review needs chunking.

## Inputs

- Repository root
- Optional diff or changed-file list
- Optional instruction source
- User-stated goals or focus areas

## Workflow

1. Determine whether the request is `full_scan` or `diff_scan`.
2. Identify focus areas explicitly requested by the user.
3. Check whether instruction or policy files are available when compliance is requested.
4. Decide whether the repository likely needs chunking by module, package, or feature boundary.
5. Produce a short plan for which downstream skills should run.

## Output Standard

Return:

- selected scan mode
- selected focus areas
- instruction-source status
- chunking recommendation
- downstream skills to load

## Guardrails

- Do not default to full scan when the request clearly targets changed files.
- Do not assume compliance review is possible without an instruction source.
- Do not broaden the focus area without a reason grounded in the request.
