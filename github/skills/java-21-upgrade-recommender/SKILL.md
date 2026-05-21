---
name: java-21-upgrade-recommender
description: Reviews Java source and build configuration, infers the likely baseline version, and recommends a practical path to Java 21 with a markdown report under docs/. Use when you want upgrade guidance before doing the migration work.
---

# Java 21 Upgrade Recommender

Use this skill to assess Java source and build configuration, infer the current Java baseline, identify upgrade blockers, and produce a markdown upgrade report plus a final JSON summary.

## When to Use This Skill

Use this skill when:

- a Java codebase needs upgrade guidance toward Java 21
- the current baseline may be Java 5, Java 8, Java 11 to 17, or mixed
- you want practical recommendations before changing source code
- you need a saved markdown report under `docs/`

## When Not to Use This Skill

- Do not use this skill as a compiler, build runner, or automatic refactoring engine.
- Do not use this skill for framework-only migration advice when Java runtime compatibility is out of scope.
- Do not claim Java 21 readiness without build, dependency, and runtime evidence.

## Prerequisites

- Java source files in scope
- Build files when available, such as `pom.xml`, `build.gradle`, or `build.gradle.kts`
- Optional tests, dependency configuration, or toolchain configuration
- Optional `analysisScope`: `single_file`, `package`, `module`, or `repo`
- Optional `currentJavaVersion`
- Optional `focusAreas`: `language_features`, `deprecated_apis`, `removed_apis`, `collections`, `concurrency`, `exceptions`, `build_config`, `build_toolchain`, `preview_features`, `testing`
- Optional `targetJavaVersion`, default `21`
- Optional `reportDirectory`

## Intake Rule

- If the user provides one or more files, analyze those files first and limit the assessment to that explicit scope unless the user asks for a broader review.
- If the user does not provide files or a clear module or repository scope, ask them to provide the relevant Java source files and build files before proceeding.
- If only a Java source file is provided and no build file is available, continue with source-level findings but clearly lower confidence for baseline and compatibility conclusions.

## Goal

Produce a code-backed Java 21 upgrade assessment that:

- infers the likely current Java baseline
- separates compatibility blockers from optional modernization
- recommends a practical migration path
- writes a markdown report to `docs/`
- returns a single JSON object describing the result

## Step-by-Step Workflows

1. Confirm the analysis scope from the user-provided files, module, package, or repository.
2. If no files or scope are provided, ask the user to provide the files to review before continuing.
3. Read Java source and build configuration in the requested scope.
4. Infer the current baseline from visible evidence instead of guessing.
5. Classify findings into blockers, required migration changes, optional modernization, and preview-only items where relevant.
6. Build a staged migration path based on baseline age and risk.
7. Write the markdown report to `docs/java-21-upgrade-report-<scope>.md`.
8. Return the final JSON object with output path, findings, recommendations, migration plan, and report summary.

## Version-Specific Guidance

### If the Code Appears to Be Java 5 or Earlier 

- Prioritize generics cleanup, enhanced for-loops, enums, annotations, and safer collections usage.
- Flag raw types, iterator-heavy loops, older concurrency patterns, and manual boilerplate common to early Java.
- Prefer a staged migration path instead of broad Java 21 syntax adoption.

### If the Code Appears to Be Java 8

- Prioritize runtime, build, and dependency compatibility first.
- Flag old `Date` and `Calendar` usage, verbose anonymous classes, manual null handling, and dated stream usage.
- Recommend records, pattern matching, switch expressions, text blocks, and `var` only after compatibility is stable.

### If the Code Appears to Be Java 11 to 17

- Focus on closing the remaining compatibility gap to Java 21.
- Check removed modules, preview assumptions, and ecosystem support.
- Look for cases where records, sealed classes, pattern matching, switch expressions, and text blocks improve clarity.

### If the Code Appears to Be Java 17

- Prioritize Java 21 runtime and ecosystem compatibility first.
- Consider virtual threads for blocking I/O workloads only when they fit the code.
- Review whether sequenced collections or newer pattern-matching improvements materially improve the code.
- Keep preview-only ideas clearly non-default.

## Output Contract

Return a single JSON object with this shape:

```json
{
  "outputPath": "docs/java-21-upgrade-report-order-service.md",
  "summary": "The codebase appears to target Java 8 and can move toward Java 21, but several legacy APIs and build settings should be addressed first.",
  "detectedBaseline": {
    "version": "8",
    "confidence": "high",
    "evidence": [
      "Build configuration sets sourceCompatibility to 1.8."
    ]
  },
  "issues": [
    {
      "issueType": "legacy_date_time_api",
      "severity": "medium",
      "confidence": "high",
      "location": "OrderService.java:42",
      "description": "The code relies on mutable legacy date/time APIs.",
      "impact": "This increases migration and maintenance risk.",
      "recommendation": "Prefer java.time types where appropriate.",
      "upgradeStage": "baseline_modernization"
    }
  ],
  "recommendations": [
    "Upgrade build toolchains and compiler settings to support Java 21 explicitly."
  ],
  "migrationPlan": {
    "recommendedPath": "8_to_21_staged",
    "steps": [
      "Confirm dependency and framework support for Java 21.",
      "Update compiler and runtime configuration."
    ]
  },
  "manualChecks": [
    "Verify third-party libraries and plugins support Java 21."
  ],
  "riskSummary": {
    "overallRisk": "medium",
    "focus": ["build_config", "deprecated_apis", "runtime_compatibility"]
  },
  "report": {
    "title": "Java 21 Upgrade Assessment",
    "scope": "repo",
    "buildFindings": ["Compiler configuration still targets Java 8."],
    "sourceFindings": ["Several legacy APIs remain in active use."],
    "java21Opportunities": ["Pattern matching and records may simplify some code after baseline compatibility is addressed."],
    "conclusion": "A staged migration is the safest path."
  }
}
```

## Markdown Report Requirements

The report written to `docs/` should include:

- title
- analyzed scope
- detected baseline and evidence
- executive summary
- migration risk summary
- prioritized findings
- recommended migration path
- optional Java 21 modernization opportunities
- manual checks
- conclusion

Use this structure when drafting the markdown report:

```md
# Java 21 Upgrade Report

## Title
Java 21 Upgrade Assessment

## Scope
- Analysis scope:
- Files or module reviewed:
- Report generated on:

## Detected Baseline
- Detected Java version:
- Confidence:

### Evidence
- 

## Executive Summary
Summarize whether the codebase appears to be closest to Java 5, Java 8, Java 11 to 17, or later, and state the safest migration direction toward Java 21.

## Migration Risk Summary
- Overall risk:
- Main risk areas:
- Expected migration approach:

## Prioritized Findings
| Severity | Type | Location | Description | Recommendation | Classification |
| --- | --- | --- | --- | --- | --- |
| medium | example | `OrderService.java:42` | Legacy date/time API usage. | Prefer `java.time` types where appropriate. | `required_migration_change` |

## Recommended Migration Path
1. Confirm build, framework, and dependency compatibility with Java 21.
2. Update compiler, toolchain, and runtime configuration.
3. Fix required migration blockers and removed API assumptions.
4. Run tests and resolve runtime or build incompatibilities.
5. Apply optional Java 21 modernizations where they improve clarity.

## Optional Java 21 Modernization Opportunities
- Records for data carrier classes.
- Pattern matching for clearer branching.
- Switch expressions where they simplify control flow.
- Virtual threads only when blocking I/O use cases justify them.

## Manual Checks
- Verify third-party dependency support for Java 21.
- Check for reflection, agents, bytecode manipulation, or internal JDK API usage.
- Confirm deployment runtime and container base image compatibility.

## Conclusion
State whether the upgrade should be staged or direct, and identify the highest-value next step.
```

## Classification Rules

When useful, explicitly classify recommendations as:

- `compatibility_blocker`
- `required_migration_change`
- `optional_modernization`
- `preview_only`

## Quality Check

Before finalizing, verify that:

- the response is a single JSON object
- `outputPath` points to the markdown report file created under `docs/`
- the detected baseline includes evidence and confidence
- every issue has a location or a clearly scoped build/config target
- required migration work is separated from optional modernization
- preview-only items are clearly labeled
- the markdown report name is logical for the analyzed scope

## Guardrails

- Do not modify source files as part of this skill.
- Do not proceed with a repository-wide assessment when the user has not provided files or a clear scope.
- Do not infer compatibility from language syntax alone when build files disagree.
- Do not recommend Java 21 features purely for novelty.
- Do not mix preview-only suggestions with baseline migration requirements.
- Do not hide uncertainty when source and build evidence conflict.

## Reporting Style

- Be practical and evidence-based.
- Prioritize safe migration sequencing over broad modernization.
- Keep compatibility blockers separate from optional cleanup.
- Prefer recommendations that reduce complexity or migration risk.

## Troubleshooting

- If build files are missing, infer the baseline from source patterns and lower confidence accordingly.
- If the code mixes multiple Java eras, call out the ambiguity and recommend validating the actual compiler target.
- If framework or dependency support is likely to block Java 21, state that code changes alone are insufficient.
- If an idea is helpful but not required for Java 21 compatibility, mark it as optional.

## References

- Java source and build files in scope
