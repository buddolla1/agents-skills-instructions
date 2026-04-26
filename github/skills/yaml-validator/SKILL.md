---
name: yaml-validator
description: Validate YAML files for syntax, structure, and maintainability issues. Use when reviewing config files, manifests, CI definitions, or skill files, and when checking URLs that end with / so the user can verify them.
---

# YAML Validator

## When to Use This Skill

Use this skill when validating YAML content for correctness and common configuration mistakes.

## Prerequisites

- The YAML file or snippet being reviewed
- Any expected schema or consuming system
- The URLs or values that need explicit inspection

## Goal

Detect malformed YAML, risky configuration patterns, and obvious content issues early so the file is safe to use.

## What to Validate

- Syntax and indentation
- Key duplication or inconsistent nesting
- Scalar formatting issues
- Empty or suspicious values
- Structural consistency with expected YAML conventions
- URLs or links that end with `/`

## Step-by-Step Workflows

1. Parse the YAML structure and confirm it is syntactically valid.
2. Check indentation, quoting, lists, maps, and multiline values.
3. Compare keys and nesting against the expected schema or usage.
4. Flag suspicious strings, especially URLs ending with `/`.
5. Return a clear validation result with exact locations and remediation notes.

## URL Rule

- If a URL ends with `/`, inform the user to check it.
- Treat the trailing slash as a validation note, not necessarily an error.
- If the URL is meant to be canonical, still call attention to the ending slash.

## Guardrails

- Do not assume schema correctness just because syntax parses.
- Do not silently normalize content if the user needs to review it.
- Do not hide the location of the issue when reporting it.

## Output Standard

For each issue, provide:

- Line or key location
- Validation problem
- Why it matters
- Recommended fix or check

## Reporting Style

- Be precise and direct.
- Distinguish syntax errors from review warnings.
- Call out trailing-slash URLs explicitly so the user can inspect them.

## Troubleshooting

- If the file parses but still looks wrong, check schema expectations.
- If a URL ends with `/`, tell the user to verify whether it is intended.
- If multiline values break parsing, review indentation and quoting first.

## References

- YAML syntax rules for the project
- Related config or manifest schemas
