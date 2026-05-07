---
name: ultimate-codebase-analysis-repo-scan
description: Scans a repository or diff and builds the module, file-type, and chunk map for later analysis skills. Use when codebase analysis needs structured scope before running specialized review.
---

# Ultimate Codebase Analysis Repo Scan

Use this skill to build the analyzable map of the repository.

## When to Use This Skill

Use this skill after intake and before loading the deeper analysis skills.

## Goal

Produce the scope map that other skills can rely on without re-scanning the same structure blindly.

## What to Inspect

- Top-level modules, packages, apps, or services
- Build files such as `pom.xml`, `build.gradle`, `package.json`, and lockfiles
- Test directories and CI definitions when testing posture matters
- Instruction or policy files when compliance review is in scope
- Diff-limited file lists when running in `diff_scan`

## Output Standard

Return:

- file tree summary
- modules or feature boundaries
- file types and dominant languages
- candidate chunks for parallel review
- notable hotspots that justify deeper analysis

## Guardrails

- Do not include generated output such as `target/`, `build/`, `dist/`, or `node_modules/` unless the user explicitly asks.
- Do not infer module boundaries that the repository structure does not support.
- Do not make analyzer findings here; this skill only maps scope and chunking.
