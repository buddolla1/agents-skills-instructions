---
name: code-review-skill
description: Coordinates full repository and git-diff code review into focused skills for null safety, exception handling, and code quality. Use when reviewing changed files or an entire repo for runtime safety, failure handling, and maintainability risks.
---

# Code Review Agent

Use this skill as the coordinator for professional static code review across Java and general-purpose codebases.

## When to Use This Skill

Use this skill when the user asks for a full repo scan, a git-diff scan, or a review focused on null checks, exception handling, and code quality.

## First Question

If the scope is not specified, ask:

- Full repository scan
- Git diff only

Use these meanings:

- Full repository scan: review the total repo.
- Git diff only: review only the modified files.

## Clarification Points

Ask a follow-up question when needed instead of guessing:

- If the failure contract is unclear, ask what should happen on invalid input or missing data.
- If an exception path is unclear, ask whether the failure should propagate, retry, or fall back.
- If code quality concerns overlap with behavior, ask whether the issue is intended or accidental.
- If the diff depends on nearby code, read the smallest related file set before deciding.

## Progressive Loading Model

1. Load [code-review-null-pointer-check](code-review-null-pointer-check/SKILL.md) for null dereferences, unsafe assumptions, and incomplete validation.
2. Load [code-review-exception-analysis](code-review-exception-analysis/SKILL.md) for swallowed exceptions, missing root causes, rollback issues, and weak failure logging.
3. Load [code-review-code-quality](code-review-code-quality/SKILL.md) for maintainability, readability, cohesion, naming, and code-smell review.

## Source of Truth

- The project root or git diff being reviewed
- The behavior that must remain unchanged
- Any tests, examples, or docs that define expected behavior

## Step-by-Step Workflow

1. Confirm whether the scan covers the full repository or only the git diff.
2. For full repository scans, review the total repo.
3. For git-diff reviews, review only the modified files unless a dependency requires a nearby file read.
4. Review null-safety risks first because they often become runtime failures.
5. Review exception paths next so failure handling, rollback, and logging stay correct.
6. Review code quality last to capture maintainability issues without duplicating functional findings.
7. Deduplicate overlapping findings and keep the highest-severity interpretation.
8. Produce a markdown report ranked by impact.

## Output Contract

The final report must stay in markdown and preserve this section order when relevant:

1. `Summary`
2. `Critical Issues`
3. `Major Issues`
4. `Minor Issues`
5. `Null Safety Findings`
6. `Exception Findings`
7. `Code Quality Findings`
8. `Refactored Code Suggestions`

## Guardrails

- Do not force a full repo scan when the user only asked for the diff.
- Do not treat every null check or catch block as a defect.
- Do not lose the original exception cause when recommending fixes.
- Do not report style-only concerns unless they create maintainability risk.
- Do not duplicate the same root cause across multiple findings.

## Reporting Style

- Be direct, specific, and production-oriented.
- Tie each finding to concrete behavior, not preference.
- Prefer root-cause analysis over cosmetic comments.
- If the renderer supports HTML, use inline color labels for severity: red for critical, orange for major, yellow for minor, blue for informational sections.

## References

- The source code and changed files
- The specialized code review skills in this directory
