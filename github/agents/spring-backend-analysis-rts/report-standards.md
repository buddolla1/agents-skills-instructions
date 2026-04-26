# Spring Backend Report Standards

## Purpose

All Spring backend agents in this folder must produce reports using the same assessment model and tone. The goal is to keep findings comparable across agents and to make each report concise, professional, and operationally useful.

## Execution Strategy

All Spring backend agents should follow this shared execution strategy when the runtime supports it:

```json
"strategy": {
  "chunking": "by-module",
  "maxFilesPerAgent": 50,
  "parallelExecution": true,
  "minAgents": 2,
  "maxAgents": 3
}
```

Use the strategy to split large repositories into manageable module-level chunks, run multiple agents in parallel where appropriate, and keep dependencies between passes explicit.

## Required Section Order

1. Executive Summary
2. Scope Observed
3. Findings
4. Risk Assessment
5. Recommendations
6. Conclusion

## Writing Standards

- Keep the report factual and evidence-based.
- Use a professional, enterprise-style tone.
- Keep the facts unchanged; improve clarity, structure, and wording.
- Prefer concise statements over verbose narrative.
- Tie every finding to an observed code path, configuration item, or runtime behavior.

## Content Standards

- Executive Summary must state the overall posture in a short, direct form.
- Scope Observed must describe what the agent actually reviewed.
- Findings must be grouped into numbered or clearly separated items.
- Risk Assessment must describe impact, severity, or operational consequence.
- Recommendations must be actionable and specific.
- Conclusion must summarize the material takeaway without introducing new facts.

## Logging-Focused Guidance

When a report is about logging, it must emphasize:
- outbound-call logging
- exception and error logging
- masking of sensitive data

If other logging details appear, they must remain secondary to those three points unless the user specifically requests otherwise.

## Output Rules

- Write the report to the path defined by the agent.
- Use Markdown only.
- Do not change the section order.
- Do not add unrelated sections unless the user requests them.
