---
name: java-code-quality-security
description: Reviews Java code for security risks, secrets exposure, and unsafe data handling. Use when the user wants a focused security review of Java or Spring Boot code.
---

# Java Code Quality Security

Use this skill to identify security defects and risky data-handling patterns.

## When to Use This Skill

Use this skill when the review should focus on secrets, injection, authorization, sensitive data, and unsafe request or response handling.

## Prerequisites

- The project root or diff being reviewed
- Any security requirements or threat model context

## Goal

Find explicit security risks and explain their production impact.

## Output Standard

For each issue, provide:

- Location
- Security concern
- Why it matters
- Recommended fix
- Risk if ignored

## Guardrails

- Do not flag harmless patterns as security defects.
- Do not omit data exposure, injection, or authz concerns.

## Reporting Style

- Be explicit and production-oriented.
- Tie each finding to a real attack or exposure path.

## References

- The coordinator skill
