# Agent Prompts

Use these prompts with the custom CodeTour agent:

`@.github/agents/code-tour/code-tour.agent.md`

## General tour creation

```text[..](..)
@.github/agents/code-tour/code-tour.agent.md
Create a primary CodeTour for this repo that explains the main architecture and onboarding flow. Save it under .tours/getting-started.tour.
```

## Authentication or feature walkthrough

```text
@.github/agents/code-tour/code-tour.agent.md
Analyze this codebase and generate a tour for the authentication flow. Include step titles, file references, and line anchors.
```

## Repair existing tours

```text
@.github/agents/code-tour/code-tour.agent.md
Update the existing .tour files so they match the current project structure and fix any broken file paths.
```

## Multi-tour onboarding

```text
@.github/agents/code-tour/code-tour.agent.md
Create a multi-tour onboarding sequence:
1 - Project Overview
2 - Backend Flow
3 - Frontend Flow
Mark the first tour as primary and link the next tours.
```

## Repo-specific prompt for this project

```text
@.github/agents/code-tour/code-tour.agent.md
Scan the repo and create a new developer onboarding tour for this Spring AI project. Put the output in .tours/ics-overview.tour and cover app entry point, configuration, controllers, services, vector store usage, and PDF ingestion.
```
