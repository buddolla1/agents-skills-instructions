---
name: engineering-design-agent
description: Creates repo-aware engineering design artifacts such as design docs, BDD stories, test data, HLD, LLD, and Mermaid diagrams in markdown. Use when feature requirements must be turned into structured design output aligned with the repository.
---

# Engineering Design Agent

Use this skill as the coordinator for turning a feature requirement into a repo-aware markdown design artifact plus a final JSON status object.

## When to Use This Skill

Use this skill when the user wants a design doc, BDD scenarios, test-data guidance, architecture output, HLD, LLD, or Mermaid diagrams that should match the repository's stack and conventions.

## When Not to Use This Skill

- Do not use this skill for code fixing or source review.
- Do not use this skill when the requirement is too vague to support meaningful design output without clarification.

## Prerequisites

- `requirement`
- Optional `projectType`
- Optional `techStack`
- Optional `architectureType`
- Optional `outputMode`: `bdd`, `architecture`, `full_design`, or `template`

## Goal

Produce a markdown artifact grounded in visible repository context, then return a single JSON object that summarizes what was generated.

## Progressive Loading Model

1. Load [engineering-design-intake](engineering-design-intake/SKILL.md) to confirm the requirement and collect only the minimum missing context.
2. Load [engineering-design-scope](engineering-design-scope/SKILL.md) to inspect repo context from README, build files, and relevant code or config.
3. Load [engineering-design-planning](engineering-design-planning/SKILL.md) to structure the markdown artifact for the requested `outputMode`.
4. Load [engineering-design-validation](engineering-design-validation/SKILL.md) to verify repo-aware claims, required sections, and explicit assumptions.
5. Load [engineering-design-architecture](engineering-design-architecture/SKILL.md) only when architecture output is requested or implied.

## Step-by-Step Workflows

1. Confirm the requested artifact type and the requirement text.
2. If the requirement is too broad, ask the minimum clarifying question needed.
3. Read visible repository context before making stack or architecture claims.
4. Draft the markdown artifact for the selected `outputMode`.
5. Include assumptions explicitly instead of burying them in prose.
6. Add Mermaid diagrams when architecture output is requested.
7. Return a single JSON object describing the generated markdown file.

## Output Contract

Return a single JSON object with this shape:

```json
{
  "summary": "Generated a repo-aware design artifact.",
  "artifactType": "full_design",
  "sectionsGenerated": [
    "Architecture Overview",
    "High-Level Design",
    "BDD Scenarios"
  ],
  "outputPath": "docs/generated/example-design.md",
  "assumptions": [
    "Architecture guidance was limited to visible repository context."
  ]
}
```

## Output Standards

- The generated artifact must be a markdown file.
- Keep the content aligned with the requested `outputMode`.
- Make repo-aware statements traceable to visible repository context.
- Keep assumptions explicit.
- Keep the JSON result limited to the documented fields.

## Quality Check

Before finalizing, verify that:

- the response is a single JSON object
- `outputPath` is explicit and points to the generated markdown file
- the generated sections match the requested artifact type
- Mermaid diagrams are included when architecture output is requested
- assumptions are explicit instead of implied

## Guardrails

- Do not invent technical details that are not supported by repo context or user input.
- Do not claim repo alignment unless relevant files were actually inspected.
- Do not return prose outside the final JSON object when using this skill's contract.

## Reporting Style

- Use concise, formal language.
- Keep the markdown artifact reviewable and implementation-oriented.
- Make the JSON summary concrete and file-oriented.

## Troubleshooting

- If the requirement is vague, stay in intake and ask one clarifying question.
- If repo context is thin, say so and keep recommendations bounded.
- If the user wants only one slice such as BDD or architecture, load only the matching parts of the workflow.

## References

- README, build files, and relevant source or config files
- The specialized skills in this directory
