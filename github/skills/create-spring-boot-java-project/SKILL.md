---
name: create-spring-boot-java-project
description: Create a Spring Boot Java project skeleton. Use when starting a new Spring Boot application and the goal is to generate the initial structure, dependencies, and project conventions.
---

# Create Spring Boot Java Project

Use this skill when starting a new Spring Boot Java service or application from scratch.

## When to Use This Skill

Use this skill when the user asks for a Spring Boot Java project skeleton or starter structure.

## Prerequisites

- The target Java version
- The build tool preference
- The application type and major dependencies

## Goal

Create a clean starter project with the right baseline structure and conventions.

## Step-by-Step Workflows

1. Confirm the Java version and build tool.
2. Select the standard project layout and base dependencies.
3. Create the application entry point and package structure.
4. Add configuration, test, and resource scaffolding.
5. Verify the skeleton is ready for feature work.

## Guardrails

- Do not add unnecessary dependencies.
- Do not hardcode environment-specific settings.
- Do not create a structure that fights Spring Boot conventions.

## Output Standard

For each project skeleton, provide:

- Java version
- Build tool
- Key dependencies
- Package structure
- Next steps

## Reporting Style

- Be practical and minimal.
- Prefer conventional Spring Boot defaults.
- Keep the starter easy to extend.

## Troubleshooting

- If the version is unclear, ask before scaffolding.
- If custom modules are needed, define them explicitly.
- If the starter is too heavy, trim it to the essentials.

## References

- Spring Boot conventions
- Project build and dependency standards

