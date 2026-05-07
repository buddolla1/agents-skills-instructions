---
name: ultimate-codebase-analysis-instruction-compliance
description: Verifies repository behavior against a provided instruction or policy source and reports evidence-backed violations. Use when codebase analysis should include instruction compliance review.
---

# Ultimate Codebase Analysis Instruction Compliance

Use this skill to compare the repository against an instruction or policy source.

## When to Use This Skill

Use this skill only when an instruction source is available or the user explicitly asks for compliance review tied to a known policy file.

## Modes

- `findings-only`: return compliance findings for aggregation
- `standalone-report`: write a focused markdown report to `instruction-compliance-report.md`

## What to Analyze

- Rules explicitly stated in the instruction source
- Code or configuration that appears to violate those rules
- Missing required structures or conventions when the policy makes them mandatory

## Output Standard

Return:

- compliance summary
- evidence-backed violations
- compliance score if and only if the scoring model is defined by the instruction source or the requesting workflow

For each violation, provide:

- violated rule
- location
- evidence
- impact
- recommended fix

When running in `standalone-report` mode, write `instruction-compliance-report.md` with these sections when relevant:

1. `Summary`
2. `Compliance Summary`
3. `Compliance Violations`
4. `Required Fixes`
5. `Recommendations`

## Guardrails

- Do not fabricate rules that are not present in the instruction source.
- Do not assign a compliance score when no scoring model exists.
- Do not mix general code quality findings into the compliance section.
