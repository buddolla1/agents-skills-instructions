# Engineering Design Agent Skill Overview

## What This Skill Does
This skill coordinates repo-aware engineering design output. It turns a requirement into a markdown artifact such as BDD guidance, architecture design, or a full design document.

## When To Use It
- Use it when feature requirements need to become structured engineering documentation.
- Use it when the output should align with the repository's visible stack and conventions.
- Use it when you need BDD, HLD, LLD, test-data guidance, or Mermaid diagrams.

## When Not To Use It
- Do not use it for code fixes or source review.
- Do not use it when the requirement is too vague to support useful design output without clarification.

## Inputs It Expects
- `requirement`
- optional `projectType`
- optional `techStack`
- optional `architectureType`
- optional `outputMode`: `bdd`, `architecture`, `full_design`, `template`

## How It Works
The coordinator progressively loads smaller skills to confirm the request, inspect repo context, draft the artifact, and validate the final markdown contract.

```mermaid
flowchart TD
    A[Read requirement] --> B{Enough context?}
    B -- No --> C[Ask one clarifying question]
    B -- Yes --> D[Inspect README, build files, and relevant code]
    C --> D
    D --> E[Draft markdown artifact for selected outputMode]
    E --> F{Architecture requested?}
    F -- Yes --> G[Add HLD, LLD, and Mermaid diagrams]
    F -- No --> H[Add diagrams where they help clarity]
    G --> I[Validate repo-aware claims and assumptions]
    H --> I
    I --> J[Return markdown artifact path and section list]
```

## Progressive Loading
1. [engineering-design-intake](./engineering-design-intake-skill-overview.md)
2. [engineering-design-scope](./engineering-design-scope-skill-overview.md)
3. [engineering-design-planning](./engineering-design-planning-skill-overview.md)
4. [engineering-design-validation](./engineering-design-validation-skill-overview.md)
5. [engineering-design-architecture](./engineering-design-architecture-skill-overview.md) when architecture output is required

## Outputs It Produces
- markdown artifact path
- `artifactType`
- `sectionsGenerated`
- explicit assumptions
- markdown artifact path
- section list
- assumptions

## Output Contract

```markdown
docs/generated/example-design.md
```

## Guardrails
- Do not invent repository context.
- Do not hide assumptions in prose.
- Do not return extra text outside the markdown artifact contract.
