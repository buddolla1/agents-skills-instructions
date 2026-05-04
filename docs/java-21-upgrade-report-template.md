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
