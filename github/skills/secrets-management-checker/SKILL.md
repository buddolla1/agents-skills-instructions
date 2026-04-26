---
name: secrets-management-checker
description: Detect hardcoded secrets in code, config, and build files. Use when reviewing Java or Spring Boot projects for passwords, API keys, tokens, database credentials, or insecure secret handling, and when recommending Vault, environment variables, or secret managers.
---

# Secrets Management Checker

## When to Use This Skill

Use this skill when reviewing code or configuration for secret exposure and insecure credential handling.

## Prerequisites

- The code, config, or deployment artifact being reviewed
- The expected secret source, such as Vault or environment injection
- Any logging or sample-file rules that affect secret handling

## What to Detect

- Hardcoded passwords, API keys, tokens, certificates, and connection strings
- Secrets embedded in `application.yml`, properties files, scripts, tests, or sample configs
- Credentials checked into source control or duplicated across environments
- Plaintext values passed through logs, exceptions, or debug output
- Secret handling that depends on local defaults instead of runtime injection

## Step-by-Step Workflows

1. Inspect code, config, CI files, and deployment descriptors together.
2. Separate true secrets from harmless constants before raising findings.
3. Identify where the secret enters the system and how it should be injected at runtime.
4. Recommend the smallest secure replacement that fits the platform.
5. Call out any migration or rollback steps needed to rotate the exposed value.

## Preferred Remediations

- Move credentials to Vault, a secret manager, or platform-managed service binding.
- Use environment variables or externalized configuration for non-sensitive runtime values.
- Replace committed defaults with placeholders and fail fast when required secrets are missing.
- Rotate any exposed secret after the code path is corrected.
- Remove secret values from logs, sample files, and test fixtures unless they are explicitly fake.

## Output Standard

For each issue, provide:

- Location
- Secret type
- Why it is risky
- Recommended secure replacement
- Rotation or cleanup note if the secret was exposed

## Reporting Style

- Be precise about whether the finding is a real secret or just a conventionally named value.
- Prefer concrete replacement guidance over generic security advice.
- If a secret is already exposed, treat rotation as part of the fix.

## Troubleshooting

- If a value is uncertain, verify whether it is actually sensitive before flagging it.
- If a secret is exposed, include rotation in the remediation plan.
- If the replacement is unclear, move the value to Vault or environment injection first.

## References

- Secret-management standards for the repository
- Related deployment and configuration conventions
