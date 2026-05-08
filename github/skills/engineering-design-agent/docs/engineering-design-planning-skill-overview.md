# Engineering Design Planning Skill Overview

## What This Skill Does
This skill drafts the main markdown artifact based on the selected `outputMode`.

## When To Use It
- Use it after intake and repo-context work are complete.
- Use it when the artifact needs to be structured for BDD, architecture, full design, or template output.

## Inputs It Expects
- feature summary
- assumptions
- repo context summary
- requested `outputMode`

## How It Works

```mermaid
flowchart TD
    A[Select outputMode] --> B{Mode}
    B -- bdd --> C[Draft stories, scenarios, acceptance criteria, test data]
    B -- architecture --> D[Draft architecture overview, HLD, LLD, diagrams, risks]
    B -- full_design --> E[Combine scope, behavior, validation, and architecture]
    B -- template --> F[Create reusable markdown skeleton]
    C --> G[Produce cohesive markdown artifact]
    D --> G
    E --> G
    F --> G
```

## Outputs It Produces
- markdown draft
- section set matched to `outputMode`
- explicit assumptions

## Guardrails
- Do not force sections that do not fit the selected mode.
- Do not output JSON in this stage.

