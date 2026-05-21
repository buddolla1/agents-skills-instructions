---
name: dead-code-and-unreferenced-methods-checker
description: 'Detect dead code and unreferenced methods in application code. Use when reviewing a repository or diff to find methods, classes, constants, and private helpers that appear unused, unreachable, redundant, or only indirectly referenced through frameworks, reflection, annotations, templates, or configuration.'
---

# Dead Code and Unreferenced Methods Checker

## When to Use This Skill

Use this skill when the user wants to find code that can likely be removed or reviewed for removal:

- Unreferenced private methods
- Dead helper functions
- Unused classes, fields, and constants
- Unreachable branches
- Legacy methods left behind after refactors
- Code paths kept alive only by framework wiring, reflection, annotations, templates, or configuration

## Prerequisites

- Repository root or changed files
- Target language or framework when known
- Build files, routing configuration, dependency injection setup, or template/config references when they affect reachability

## Goal

Identify code that is probably dead, distinguish it from indirectly used code, and give the user a defensible shortlist for cleanup.

## Working Method

1. Start with the narrowest requested scope: file, module, package, or full repository.
2. Find candidate symbols that have zero or near-zero call sites in source.
3. Check non-obvious entry points before calling anything dead:
   - Framework routing
   - Dependency injection
   - Reflection
   - Annotations
   - Serialization hooks
   - Template bindings
   - SQL or XML mappings
   - CLI registration
   - Tests that intentionally invoke the code
4. Separate likely dead code from code that is merely low-traffic, extension-oriented, or externally invoked.
5. Report only evidence-backed candidates and state the uncertainty level.

## What to Detect

- Private methods with no call sites
- Package-local or public methods with no internal references and no clear external contract
- Duplicate implementations where one path is no longer used
- Feature-flagged branches that can no longer execute
- Exception or fallback paths that have become unreachable after logic changes
- Constants, fields, or utility classes with no live references
- Old adapters, DTO mappers, or service wrappers left behind after migrations

## Guardrails

- Do not mark public APIs as dead without checking whether they are externally consumed.
- Do not mark controller handlers, listeners, scheduled jobs, ORM callbacks, serializer hooks, or DI-managed methods as dead just because grep shows no direct call site.
- Do not treat test-only references as production reachability unless the user explicitly wants all dead code, including production code used only by tests.
- Do not overclaim when reflection, code generation, plugins, or configuration may be involved.
- Prefer "likely dead", "possibly indirect", and "needs contract check" over false certainty.

## Language and Framework Checks

Before concluding that a method is dead, inspect the reachability mechanisms that fit the codebase:

- Java and Spring: `@RequestMapping`, `@EventListener`, `@Scheduled`, `@Bean`, JPA callbacks, interface implementations, XML wiring
- JavaScript and TypeScript: exports, dynamic imports, framework routes, JSX bindings, test harnesses, config-driven registration
- Python: decorators, entry-point registration, Django or Flask routes, Celery tasks, signal handlers
- C# and .NET: attributes, DI registration, ASP.NET routes, reflection-heavy framework use
- SQL or data layers: mapper XML, stored procedure bindings, migration hooks

## Evidence Standard

A strong dead-code candidate usually has most of these signals:

- No direct call sites in repository source
- No references in config, templates, routes, or mappings
- No overrides or interface contracts requiring it
- No test that documents a supported behavior around it
- Surrounding code shows the old path was replaced

If only some signals are present, downgrade confidence and explain why.

## Output Standard

For each candidate, provide:

- File and symbol
- Candidate type: method, class, field, constant, branch, or module
- Why it appears dead
- What indirect-use checks were performed
- Confidence: high, medium, or low
- Recommended next action: remove, verify externally, or keep

## Reporting Style

- Lead with the highest-confidence removals.
- Group low-confidence findings separately.
- Be explicit about framework assumptions.
- Prefer a smaller accurate list over a long speculative one.

## References

- Source files and build configuration
- Routing, DI, and framework metadata
- Templates, mappings, and generated-code inputs when present
