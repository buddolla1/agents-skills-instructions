---
name: npe
description: 'Review Java code for null-pointer risks, trace nullable flows, suggest minimal fixes, and propose focused regression tests. Use when analyzing Java, Spring, JPA, DTO, and service-layer code for NPE failure paths.'
---

# NPE Review

## When to Use This Skill

Use this skill when reviewing Java code for null-pointer risks, runtime dereference failures, and safe fixes.

Typical cases:

- a value may be null from API input, repository calls, config, or integrations
- a nested getter or chained call may dereference a null reference
- a service flow conditionally assigns an object before use
- framework behavior in Spring, JPA, REST, or DTO mapping may introduce nulls
- a user asks for safe fixes or tests for NPE-prone code

## Goal

Identify the most credible null source, trace how it reaches the dereference site, explain risk clearly, and recommend the smallest safe fix with a focused regression test.

## Null Flow Tracing

Trace where null can originate and how it reaches a dereference point.

### Apply this when

- a value comes from API input
- a repository or service may return null
- a nested getter chain exists
- an object is conditionally assigned

### Method

1. Identify the nullable source.
2. Track the assignment and call path.
3. Check guards, defaults, and contracts before usage.
4. Confirm the dereference site.
5. Mark confidence based on code evidence.

## Java Dereference Risk Detection

Spot direct and indirect dereference patterns that often fail at runtime.

### Detect patterns

- chained getters
- method calls on nullable references
- collection element dereference
- map lookup dereference
- wrapper unboxing
- `optional.get()`

### Output expectations

- nullable source
- exact risky line or operation
- safe alternative

## Framework-Aware Null Safety Review

Understand common NPE sources in Spring, JPA, REST, and service layers.

### Spring checks

- field injection risks
- missing bean wiring
- nullable request payloads
- missing config values
- unsafe response body access

### JPA checks

- nullable columns
- lazy-loaded references
- repository null returns
- incomplete projections

### API and DTO checks

- missing nested request fields
- partial response contracts
- optional JSON fields treated as required

## Safe Fix Generation

Generate minimal, practical fixes instead of overengineering.

### Preferred fixes

- early validation
- guard clause
- safe equals
- constructor injection
- `Objects.requireNonNull`
- empty collection default
- better method contract
- `Optional` only where appropriate

### Avoid

- giant refactors
- catch-and-ignore
- blanket null checks everywhere
- behavior-changing defaults without warning

## Null-Safe Test Suggestion

Suggest tests that reproduce or prevent NPE regressions.

### Example test ideas

- null request field
- empty repository result
- missing nested DTO
- null config value
- null external API response field
- collection empty or null case

### Test style

- one focused test per issue
- name the scenario clearly
- verify failure or safe handling

## Findings Prioritization

Rank issues so teams fix the highest-impact NPE risks first.

### Priority order

1. Production request path crashes
2. Service-layer business logic crashes
3. Persistence and integration risks
4. Rare edge cases
5. Preventive code smells

### Severity hints

- Critical: frequent crash path
- High: common business flow
- Medium: conditional path
- Low: preventive hardening

## Reporting Format

Always produce findings in a clean engineering-review format.

### Output template

- Summary
- Findings by severity
- Risk explanation
- Suggested fix
- Suggested test
- Priority fix order

### Rule

Every finding must answer:

- What can be null?
- Where is it dereferenced?
- Why is it risky?
- What is the safest fix?
