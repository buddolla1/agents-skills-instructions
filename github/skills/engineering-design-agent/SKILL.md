---
name: engineering-design-agent
description: Coordinates feature.txt analysis into a staged enterprise delivery plan with epics, stories, dependencies, BDD, Gherkin scenarios, estimates, architecture, and Mermaid diagrams. Use when a feature needs progressive loading across smaller planning, validation, and architecture skills.
---

# Engineering Design Agent

Use this skill as the coordinator for turning feature requirements into a formal delivery document that is suitable for product, engineering, and QA review.

## When to Use This Skill

Use this skill when the request mentions `feature.txt`, epics, user stories, task breakdowns, dependencies, BDD coverage, Gherkin scenarios, estimate points, HLD, LLD, or Mermaid diagrams.

## Prerequisites

- Raw `feature.txt` content
- Requested number of epics
- Requested number of user stories per epic
- Requested number of tasks per story
- Optional context: requirement, tech stack, architecture type, include estimates, include dependencies, include Gherkin

## Goal

Produce a polished enterprise delivery document by progressively loading smaller skills only when the user input is sufficient for the next stage.

## Progressive Loading Model

1. Load [engineering-design-intake](engineering-design-intake/SKILL.md) first to confirm the feature input and sizing values.
2. Load [engineering-design-scope](engineering-design-scope/SKILL.md) next to capture summary, assumptions, and boundaries.
3. Load [engineering-design-planning](engineering-design-planning/SKILL.md) to generate epics, stories, dependencies, and the dependency matrix.
4. Load [engineering-design-validation](engineering-design-validation/SKILL.md) to produce BDD, Gherkin, estimates, test strategy, and test data.
5. Load [engineering-design-architecture](engineering-design-architecture/SKILL.md) to finalize the architecture overview, HLD, LLD, diagrams, risks, and next steps.

## Step-by-Step Workflows

1. Start with the intake skill and do not advance until the required sizing inputs are confirmed.
2. If epic count, stories per epic, or tasks per story are missing, ask for all three together.
3. Once sizing is confirmed, load the scope skill and capture the business framing.
4. Load the planning skill to structure the delivery plan.
5. Load the validation skill to complete quality and test coverage sections.
6. Load the architecture skill to finish the technical design sections.
7. Keep each stage concise and do not skip ahead.

## Output Contract

The final document must preserve this section order:

1. `cover-page`
2. `feature-summary`
3. `executive-summary`
4. `assumptions`
5. `scope`
6. `epics`
7. `story-breakdown`
8. `dependencies`
9. `dependency-matrix`
10. `stories`
11. `bdd`
12. `gherkin-scenarios`
13. `estimate-points`
14. `test-strategy`
15. `test-data`
16. `architecture-overview`
17. `hld`
18. `lld`
19. `diagrams`
20. `risks`
21. `next-steps`

## Output Standards

- Keep the structure predictable and presentation-ready.
- Prefer tables for epics, stories, dependencies, and estimates when they improve readability.
- Keep story points consistent across the document.
- Make dependencies explicit and traceable.
- Keep BDD and Gherkin aligned to the described story behavior.
- Make the document read like a delivery artifact, not a rough draft.

## Quality Check

Before finalizing, verify that:

- every epic has stories
- every story has a point estimate
- every story has tasks
- dependencies are listed where relevant
- BDD and Gherkin cover the primary flows and edge cases
- the document is polished and review-ready

## Guardrails

- Do not proceed past intake without the three sizing inputs if they are missing.
- Do not load later skills before earlier stages are satisfied.
- Do not invent architecture details that are not supported by the feature input.
- Do not change the final section order unless the user explicitly asks for a different format.

## Reporting Style

- Use concise, formal language.
- Keep the document polished and enterprise-ready.
- Present dependencies, BDD, estimates, and architecture in a way that supports product, engineering, and QA review.

## Troubleshooting

- If the feature description is vague, stay in intake and ask for clarification before drafting the plan.
- If the sizing inputs are missing, request epic count, stories per epic, and tasks per story together.
- If the user only wants one slice of the output, load only the matching skill and stop there.
- If the architecture is unclear, capture assumptions explicitly rather than inventing details.

## References

- The source `feature.txt`
- Related architecture and delivery planning conventions
