---
description: 'Guidance for broad codebase analysis across architecture, runtime risk, dependencies, performance, and compliance when performing repository-wide or diff-wide technical review.'
applyTo: '**/*.java, **/*.kt, **/*.js, **/*.jsx, **/*.ts, **/*.tsx, **/*.py, **/*.go, **/*.rb, **/*.cs, **/*.php, **/*.rs, **/*.scala, **/*.swift, **/*.yml, **/*.yaml, **/*.json, pom.xml, build.gradle, build.gradle.kts, package.json, README.md'
---

# Codebase Analysis Guidance

Use this instruction when performing broad repository analysis, diff review, or multi-area technical assessment. This file defines how to structure large-scope analysis so findings stay evidence-based, deduplicated, and actionable.

## Purpose

Analyze codebases by splitting review into scoped analysis stages and consolidating the result into one structured, actionable assessment.

## When To Use

- Use this guidance for broad repository analysis, diff reviews, or multi-area technical assessments.
- Use this guidance when the scope spans architecture, dependencies, runtime risk, performance, and instruction compliance together.
- Use this guidance when the deliverable should be one consolidated report rather than disconnected point findings.

## When Not To Use

- Do not use this guidance for narrow single-file reviews where a specialist review is more efficient.
- Do not use this guidance when the repository scope is too small to justify orchestration.
- Do not invent sub-analysis findings that are not grounded in source evidence.

## Expected Inputs

- Source files across the selected repository or diff scope.
- Build and dependency files such as `pom.xml`, `build.gradle`, `package.json`, lockfiles, or similar dependency definitions.
- Instruction or policy files when compliance review is requested.
- Module, package, or feature structure that can be used to chunk large repositories.

## Recommended Review Structure

Organize the final analysis under these sections when the task calls for a structured report:

- `summary`
- `scanScope`
- `moduleMap`
- `findings`
- `compliance`
- `recommendations`
- `reportPath`

When reporting findings, prefer evidence-based categories such as:

- `staticIssues`
- `exceptionIssues`
- `dependencyIssues`
- `performanceIssues`

Adapt category names when the stack requires more accurate labels, but keep the structure stable and easy to scan.

## Workflow

1. Scan the repository and build the analysis scope.
2. Determine whether the task is effectively a full scan or a diff scan.
3. Chunk large repositories by module, package, feature, or service boundary when needed.
4. Review static defects, exception handling, dependencies, and performance in parallel when relevant.
5. Run compliance verification after the core analysis if instruction sources are present.
6. Merge duplicate findings, normalize severity, and consolidate them into one final report.

## Verification Steps

- Confirm the selected scan mode matches the user request.
- Verify findings are grouped by evidence-based category.
- Check that duplicate findings are merged before the final output.
- Ensure compliance results remain separate from general code-quality findings.
- Qualify low-confidence conclusions instead of presenting them as proven defects.

## Required Checks Before Returning

- Verify the final result has a clear summary, scope, findings, and recommendations.
- Verify all high-severity findings include clear evidence or scoped explanation.
- Verify the report path is explicit when a markdown artifact is produced.
- Verify compliance scoring is omitted or qualified when no instruction source is available.
- Verify conclusions stay proportional to the available code evidence.

## Escalation And Ambiguity Handling

- If the requested scope is unclear, ask whether to run a full scan or diff scan.
- If the repository is too large, continue with chunked review and state the limitation.
- If a branch lacks enough context for a confident conclusion, lower confidence and record the missing inputs.
- If the instruction source is missing, do not fabricate compliance scoring.
- If a conclusion depends on runtime-only evidence that is not available from code, mark it as likely or inferred.

## Practical Rules

- Prefer evidence over coverage theater.
- Keep compliance findings separate from general code quality.
- Deduplicate overlapping issues before finalizing the report.
- Prioritize runtime-safety and correctness issues ahead of cleanup-level refactors.
- Prefer one consolidated report over fragmented summaries when the scope is broad.

## Example Prompts

- `Run a full codebase analysis and produce a consolidated report`
- `Review this repository diff for runtime, dependency, and performance issues`
- `Assess this codebase for architecture, maintainability, and compliance risk`
