---
name: ultimate-codebase-analysis-report-assembler
description: Merges findings from independent codebase-analysis skills into one deduplicated markdown report with severity ordering and actionable recommendations. Use when repository review outputs must be consolidated into a final artifact.
---

# Ultimate Codebase Analysis Report Assembler

Use this skill to build the final report from the outputs of the other analysis skills.

## When to Use This Skill

Use this skill after the selected analysis skills have completed and their findings are available.

## Goal

Produce one evidence-backed markdown report that is easy to act on.

## Required Sections

Write `codebase-analysis-report.md` with these sections when relevant:

1. `Summary`
2. `Critical Issues`
3. `High Issues`
4. `Medium Issues`
5. `Low Issues`
6. `Static Risk Findings`
7. `Exception Findings`
8. `Dependency Risks`
9. `Performance Highlights`
10. `Compliance Summary`
11. `Compliance Violations`
12. `Recommendations`

## Assembly Rules

- Deduplicate overlapping findings and keep the strongest evidence-backed framing.
- Separate compliance violations from general code quality findings.
- Prefer severity ordering over source-skill ordering in the top issue sections.
- Preserve precise file and behavior context so the report stays actionable.

## Guardrails

- Do not invent missing sections to make the report look fuller.
- Do not downgrade or upgrade severity without a stated reason.
- Do not lose evidence when merging duplicate findings.
- Do not mix speculative guidance with evidence-backed findings.
