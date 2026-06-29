# Fullstack Project Architecture Orchestrator Overview

## What This Agent Does
This agent generates an architecture document for React, Spring Boot, or full-stack repositories, including diagrams and component structure.

## When To Use It
- Use it for architecture documentation.
- Use it when the output should be a production-ready markdown artifact.

## When Not To Use It
- Do not use it for narrow bug fixing.
- Do not use it when a lightweight summary is enough.

## How It Works
It acts like an orchestrator over a small set of analysis stages or sub-agent roles. It first classifies the repository and resolves the project name, then scans and chunks the codebase, runs dependency-mapping, process-flow, and diagram-generation work, and finally assembles the architecture document.

```mermaid
flowchart TD
    A[Orchestrator Request] --> B[Project Classifier]
    B --> C[Project Name Resolver]
    C --> D[Repository Scanner and Chunker]
    D --> E[Dependency Mapping Sub-Agent]
    D --> F[Process Flow Extraction Sub-Agent]
    D --> G[Diagram Generation Sub-Agent]
    E --> H[Report Assembler]
    F --> H
    G --> H
    H --> I[Architecture Markdown Output]
```

Main sub-agent stages:
- `Project Classifier`: identifies whether the repo is React, Spring Boot, or full-stack.
- `Project Name Resolver`: derives the output name from repository evidence.
- `Repository Scanner and Chunker`: maps modules, boundaries, and analyzable scope.
- `Dependency Mapping Sub-Agent`: extracts dependency and component relationships.
- `Process Flow Extraction Sub-Agent`: identifies request, data, and control flows.
- `Diagram Generation Sub-Agent`: turns extracted structure and flows into Mermaid-ready diagrams.
- `Report Assembler`: merges all outputs into the final architecture document.

## Inputs It Expects
- repository root
- optional mode and focus

## Outputs It Produces
- JSON summary
- final architecture markdown path

## Tools It Uses
- `codebase`: reads repository structure
- `file_operations`: writes the architecture artifact

## How To Prompt It
Specify whether you want full-repo or diff mode and whether the focus is overall architecture, APIs, UI, or data flow.

## Example Prompts
- `Generate a full architecture document for this repository.`
- `Generate architecture analysis in full-repo mode.`
- `Generate architecture analysis in git-diff mode.`
- `Generate the architecture for this React repository.`
- `Generate the architecture for this Spring Boot repository.`
- `Generate the architecture for this full-stack repository.`
- `Generate the overall architecture for this repo with focus on architecture.`
- `Generate the overall architecture for this repo with focus on APIs.`
- `Generate the overall architecture for this repo with focus on UI.`
- `Generate the overall architecture for this repo with focus on data flow.`
- `Generate an HLD for this repository.`
- `Generate an LLD for this repository.`
- `Generate external API analysis for this repository.`
- `Generate flowcharts for this repository.`
- `Generate component analysis for this repository.`
- `Generate the complete architecture markdown document.`
- `Generate the architecture document with dependency mapping and Mermaid diagrams.`

## Limits And Guardrails
- It should not invent components or dependencies.
- It should keep diagrams aligned with visible code structure.
