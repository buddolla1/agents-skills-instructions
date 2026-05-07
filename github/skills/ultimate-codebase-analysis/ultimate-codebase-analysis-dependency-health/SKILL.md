---
name: ultimate-codebase-analysis-dependency-health
description: Reviews dependency manifests and build configuration for outdated libraries, version conflicts, and maintenance risk. Use when repository analysis should assess dependency health from visible build files.
---

# Ultimate Codebase Analysis Dependency Health

Use this skill to inspect dependency and build risk.

## When to Use This Skill

Use this skill when the request includes dependency health, build stability, upgrade risk, or supply-chain-adjacent maintenance review.

## Modes

- `findings-only`: return dependency findings for later aggregation
- `standalone-report`: write a focused markdown report to `dependency-health-report.md`

## What to Inspect

- `pom.xml`
- `build.gradle` and `build.gradle.kts`
- `package.json`
- lockfiles and version catalogs
- shared build plugins and parent manifests

## What to Analyze

- Outdated or pinned dependencies that create maintenance drag
- Version conflicts or duplicated libraries
- Build plugin drift or inconsistent versions across modules
- Libraries that appear unused, redundant, or risky to maintain

## Output Standard

For each issue, provide:

- manifest location
- dependency or plugin
- issue summary
- evidence
- likely impact
- recommended fix
- severity

When running in `standalone-report` mode, write `dependency-health-report.md` with these sections when relevant:

1. `Summary`
2. `Critical Issues`
3. `High Issues`
4. `Medium Issues`
5. `Low Issues`
6. `Dependency Risks`
7. `Version Alignment Issues`
8. `Recommendations`

## Guardrails

- Do not claim a vulnerability unless it is directly evidenced by the repository context or user-provided data.
- Do not recommend upgrades blindly when version alignment constraints are visible.
- Do not assume a dependency manager exists if its manifest files are absent.
- Do not turn general code-quality concerns into dependency findings.
