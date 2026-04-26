---
name: code-review-exception-analysis
description: Analyzes exception handling quality in source code. Use when reviewing for swallowed exceptions, missing root causes, async failure leaks, rollback problems, and weak error logging.
---

# Code Review Exception Analysis

Use this skill to identify exception-handling weaknesses systematically.

## When to Use This Skill

Use this skill when the review should focus on exception handling, failure propagation, rollback behavior, and production diagnosability.

## Prerequisites

- The project root or git diff being reviewed
- Any failure symptoms, logs, or incident context if available

## Goal

Find exception-handling issues that hide failures, break rollback behavior, or reduce diagnosability.

## Interaction Point

If the intended failure behavior is unclear, ask whether the code should propagate, translate, retry, or safely fall back before reporting the exception path as a defect.

## What to Analyze

- Generic exception categories when the exact type matters less than the failure mode
- Broad `catch` blocks and swallowed exceptions
- Exception wrapping that loses the original cause
- Missing or weak error logging
- Async and background-task exception leaks
- Transaction rollback behavior when exceptions are handled locally
- Error translation that hides important failure context

## Generic Exception Category

Use a generic exception category when a broad failure pattern is more important than the exact class name. Group findings by behavior, such as:

- Validation and bad input failures
- Null dereference and unsafe state access
- Async and timeout failures
- Persistence and transaction failures
- Security and authorization failures
- I/O, parsing, and serialization failures
- Misuse of broad handlers such as `catch (Exception)` or `catch (Throwable)`

In this category, focus on:

- Whether the code preserves the original cause
- Whether the failure is converted too early into a success or fallback path
- Whether the caller can still distinguish the failure class
- Whether the log message or exception context is specific enough for diagnosis

## Runtime Exception Category

Use a runtime exception category for common unchecked failures that usually indicate bad input, unsafe state, or local implementation defects. Include cases such as:

- `IllegalArgumentException`
- `IllegalStateException`
- `NullPointerException`
- `UnsupportedOperationException`
- `NoSuchElementException`
- `IndexOutOfBoundsException`
- `ClassCastException`
- `ArithmeticException`
- `NumberFormatException`
- `DateTimeParseException`
- `ConcurrentModificationException`
- `RejectedExecutionException`

Group runtime exceptions by behavior instead of by class name:

- Bad input
- Bad state
- Unsafe null access
- Collection or index access
- Parsing or conversion
- Concurrency or thread-pool rejection

When reviewing runtime exceptions, check whether:

- The exception is allowed to surface at the right boundary
- The failure is converted into a clearer domain error when appropriate
- The original cause and context are preserved
- The code is hiding a deterministic defect behind a generic fallback

## Output Standard

For each issue, provide:

- Location
- Exception-handling concern
- Why it matters
- Recommended fix
- Severity or risk score

## Guardrails

- Do not report every catch block as a defect.
- Do not recommend losing the original exception cause.
- Do not split the review so far that cross-cutting failure patterns are missed.

## Reporting Style

- Be concise, direct, and system-oriented.
- Prefer root-cause analysis over isolated syntax comments.
- Explain how the exception path behaves under load, retries, and rollback.

## References

- The source code and changed files
- The specialized exception-handling conventions in the codebase
