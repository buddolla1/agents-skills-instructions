---
name: ultimate-codebase-analysis
description: Coordinates repository-wide or diff-wide codebase analysis into smaller independent skills for intake, scanning, static risk, exception risk, dependency health, performance hotspots, instruction compliance, and final report assembly.
---

# Ultimate Codebase Analysis

Use this skill as the coordinator for broad codebase analysis across mixed or backend-heavy repositories.

## When to Use This Skill

Use this skill when the user asks for a full repository review, diff review, or consolidated analysis across runtime risk, dependencies, performance, testing posture, security signals, or instruction compliance.

## First Question

If the request does not specify scope, ask:

- Full repository scan
- Git diff only

If the request does not specify focus, ask which review they want first:

- Runtime risk
- Exceptions and failure handling
- Dependency health
- Performance hotspots
- Instruction compliance
- Full review

## Progressive Loading Model

1. Load [ultimate-codebase-analysis-intake](ultimate-codebase-analysis-intake/SKILL.md) first to confirm scope and focus.
2. Load [ultimate-codebase-analysis-repo-scan](ultimate-codebase-analysis-repo-scan/SKILL.md) to map modules and chunk the review.
3. Load [ultimate-codebase-analysis-static-risk](ultimate-codebase-analysis-static-risk/SKILL.md) for correctness, safety, maintainability, and testing-adjacent risks.
4. Load [ultimate-codebase-analysis-exception-risk](ultimate-codebase-analysis-exception-risk/SKILL.md) for failure propagation and recovery analysis.
5. Load [ultimate-codebase-analysis-dependency-health](ultimate-codebase-analysis-dependency-health/SKILL.md) for build files, outdated libraries, and version conflicts.
6. Load [ultimate-codebase-analysis-performance-hotspots](ultimate-codebase-analysis-performance-hotspots/SKILL.md) for blocking I/O, hot paths, and concurrency signals.
7. Load [ultimate-codebase-analysis-instruction-compliance](ultimate-codebase-analysis-instruction-compliance/SKILL.md) only when an instruction source is present or explicitly requested.
8. Load [ultimate-codebase-analysis-report-assembler](ultimate-codebase-analysis-report-assembler/SKILL.md) last to merge results into the final report.

## Source of Truth

- The project root or git diff being reviewed
- Real source files and configuration, not generated output
- Tests, CI definitions, and instruction files when they are part of the requested review

## Guardrails

- Do not force a full review when the user asked for a narrower concern.
- Do not load every subskill when a smaller set answers the request.
- Do not invent runtime behavior, exploitability, or coverage certainty.
- Do not let the coordinator duplicate logic owned by the smaller skills.

## References

- The source code and changed files
- The specialized analysis skills in this directory
