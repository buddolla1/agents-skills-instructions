---
name: graphify-first-analyzer
description: Analyze Java and Spring Boot codebases using Graphify first, minimizing Copilot context and asking permission before normal search.
---

# Graphify-First Analyzer

## Purpose
Use Graphify as the primary mechanism for analyzing a Java or Spring Boot codebase. Minimize unnecessary source reads and Copilot token consumption without sacrificing correctness.

## Mandatory workflow
**Graphify → narrow scope → inspect only when necessary → answer.**

### 1. Graphify first
- For questions about execution flows, call relationships, dependencies, or code structure, start with the available Graphify query/path tools or commands.
- Do not begin with repository-wide text search, workspace indexing, or reading whole directories.
- If Graphify is not available or a query fails, follow the fallback permission rule below.

### 2. Narrow scope
- Extract only the relevant symbols, paths, and relationships from Graphify results.
- Prefer shortest relevant paths and focused symbol queries.
- Do not paste or load the entire graph JSON into the model context.
- Avoid repeated Graphify queries when a prior result already answers the question.

### 3. Inspect minimal source only when needed
- Open only the specific methods or small file ranges identified by Graphify when the graph lacks implementation details needed to answer.
- Do not open unrelated classes, whole directories, or entire files when a targeted range is sufficient.
- Clearly distinguish graph-inferred relationships from facts verified in source code.

### 4. Permission required before fallback
If Graphify cannot provide enough information, **do not automatically use normal code search**. Ask:

> Graphify couldn't find enough information to answer confidently. A normal code search may use more tokens. Do you want me to proceed with normal code search?

Wait for an explicit yes before using broad searches or other fallback discovery. If the user declines, explain what Graphify established and what remains unknown.

### 5. Response format
- Answer the user's question directly, using only supported findings.
- Cite relevant symbols, files, and line numbers when available.
- Avoid dumping raw Graphify results or large code excerpts unless requested.
- End with a short **Analysis scope report**:
  - Graphify queries/paths used: number
  - Source files inspected: number
  - Broad code search used: Yes/No
  - Fallback permission requested: Yes/No

## Token-efficiency principles
- Graphify-first is a strategy, not a guaranteed token-reduction percentage.
- Prefer concise tool output and bounded results; do not automatically re-read code already represented sufficiently by the graph.
- For before/after testing, compare identical questions with the same model, repository state, and tool setup, and measure actual token usage when available.
