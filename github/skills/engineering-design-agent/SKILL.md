---
name: engineering-design-agent
description: Coordinates repo-aware engineering design output in the report-template format, including story-count handling, architecture sections, BDD breakdowns, and validation. Use when feature requirements need to become a structured markdown design artifact aligned with the repository.
---

# Engineering Design Agent

Use this skill to turn a feature requirement into a repo-aware markdown design artifact that matches the report template structure.

## Skill Grouping

- Intake: [engineering-design-intake](engineering-design-intake/SKILL.md)
- Repo context: [engineering-design-scope](engineering-design-scope/SKILL.md)
- Drafting: [engineering-design-planning](engineering-design-planning/SKILL.md)
- Architecture detail: [engineering-design-architecture](engineering-design-architecture/SKILL.md)
- Validation: [engineering-design-validation](engineering-design-validation/SKILL.md)

## Report Template Map

Use the template headings in this order when BDD output is requested:

1. Story Count
2. Architecture Overview
3. High-Level Design (HLD)
4. Low-Level Design (LLD)
5. Architecture Diagrams
6. Epics
7. User Stories (with Story Points)
8. Subtasks
9. BDD Scenarios
10. Test Data
11. Tasks
12. Dependencies
13. Execution Plan
14. Risks
15. Assumptions
16. NFRs
17. Estimation Summary

For architecture-only output, keep the architecture sections and omit the BDD-only sections. For template output, preserve the same heading order with placeholders.

## Workflow

1. Confirm the requirement and desired `outputMode`.
2. If the request is broad, ask the minimum clarifying question needed.
3. If BDD output is requested and `storyCount` is missing, ask how many stories to create.
4. Read visible repository context before making stack or architecture claims.
5. Draft the markdown artifact using the report template structure.
6. Keep assumptions explicit and grounded in observed repository files.
7. Validate the final artifact against the requested mode and template order.

## Output Standards

- Return a markdown artifact with an explicit `outputPath`.
- Use 5 subtasks per story by default unless the user specifies a different count.
- Keep architecture claims tied to visible repository context.
- Include Mermaid diagrams wherever they improve architecture clarity.
- Keep the final artifact aligned to the selected output mode:
  - `bdd`: full report template structure
  - `architecture`: architecture overview, HLD, LLD, diagrams, risks, assumptions
  - `full_design`: combined BDD and architecture sections
  - `template`: reusable skeleton with placeholders and the same heading order

## Guardrails

- Do not invent technical details that are not supported by repo context or user input.
- Do not hide assumptions in prose.
- Do not switch formats away from markdown.

## References

- README, build files, and relevant source or config files
- The specialized skills in this directory
