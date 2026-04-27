---
name: stored-procedure-function-explainer
description: Explain stored procedures and functions for Oracle or MySQL. Use when the user wants to understand database routines, review SQL logic, or asks for an Oracle versus MySQL explanation of a stored procedure or function.
---

# Stored Procedure / Function Explainer

Use this skill when the task is to analyze a stored procedure or function and explain what it does in plain language.

## When to Use This Skill

Use this skill when the user provides a stored procedure or function and wants it explained, reviewed, or summarized for Oracle or MySQL. If the database platform is not specified, ask the user to choose Oracle or MySQL before proceeding.

## Prerequisites

- The stored procedure or function text
- The database platform: Oracle or MySQL
- Any schema or table context needed to understand the SQL

## Goal

Translate database routines into clear, accurate explanations that describe purpose, inputs, outputs, control flow, side effects, and optional execution flow diagrams when useful.

## Step-by-Step Workflows

1. Ask the user to specify Oracle or MySQL if it is not already clear.
2. Read the routine signature, parameters, and return behavior.
3. Trace the SQL statements, control flow, and dependencies.
4. If the logic has branching, loops, phases, or non-trivial control flow, generate a Mermaid flow diagram that reflects the execution path.
5. Summarize the routine in plain language.
6. Call out risks, assumptions, and anything the user should verify.

## Platform Rules

- For Oracle, account for PL/SQL-specific constructs and package or exception behavior.
- For MySQL, account for SQL/PSM syntax, delimiters, and routine scope.
- Do not mix platform rules unless the user explicitly wants a comparison.

## Guardrails

- Do not guess at table intent without checking the SQL.
- Do not simplify away important side effects.
- Do not explain the routine as if Oracle and MySQL behave identically.
- Do not proceed without the platform choice if it affects interpretation.

## Output Standard

For each routine, provide:

- Platform
- Routine name
- Purpose
- Inputs and outputs
- Step-by-step behavior
- Mermaid flow diagram when the control flow is complex enough to benefit from one, or when the user asks for it
- Important side effects or risks

## Reporting Style

- Be clear and technical, but readable.
- Use the database platform the user selected.
- Prefer structured explanations over long prose.
- When including a diagram, use Mermaid flowchart syntax and keep node labels concise.
- Ensure the diagram matches the described SQL flow and does not invent branches that are not present.

## Troubleshooting

- If the platform is unclear, ask whether it is Oracle or MySQL.
- If the routine depends on tables or packages not shown, note the missing context.
- If the SQL is complex, break the explanation into phases.
- If the routine is too large for a single clean diagram, provide a high-level phase diagram instead of an unreadable line-by-line chart.

## References

- Oracle PL/SQL conventions
- MySQL routine conventions
- Related schema and table definitions
