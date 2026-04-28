# Tour Creation Prompts

These are the prompts used to create or refine CodeTour files for this repository.

## Primary prompt used for the included tour

```text
@.github/agents/code-tour/code-tour.agent.md
Scan the repo and create a new developer onboarding tour for this Spring AI project. Put the output in .tours/ics-overview.tour and cover app entry point, configuration, controllers, services, vector store usage, and PDF ingestion.
```

## Refinement prompt

```text
@.github/agents/code-tour/code-tour.agent.md
Review .tours/ics-overview.tour and improve the step descriptions, titles, and navigation order. Keep all file paths valid for the current repository layout.
```

## Maintenance prompt

```text
@.github/agents/code-tour/code-tour.agent.md
Validate every file path and line reference in .tours/ics-overview.tour against the current codebase and update any stale steps.
```
