# Update Copilot Instructions From Real Project Structure

Use this prompt when you want an instruction file rewritten to match an existing project instead of a generic template. Replace the placeholder inputs with the repository root and instruction file you want updated.

## Why This Helps

1. It keeps the instructions aligned with the real project structure instead of a generic Spring Boot layout.
2. It reduces incorrect guidance caused by assumptions about packages, layers, or persistence choices.
3. It improves consistency across controllers, services, repositories, DTOs, and other project boundaries.
4. It makes future updates easier because the instructions reflect the codebase that already exists.
5. It helps Copilot produce output that is more accurate, maintainable, and specific to this project.

```text
Update the repository instruction file so it matches the actual project structure and architecture.

Inputs:
- `projectRoot`: <project-root>
- `instructionFile`: <instruction-file-path>
- `instructionTarget`: `copilot`, `copilot-instructions`, or `generic-project-instructions`

Goal:
- Inspect the current codebase and rewrite the instruction file so it reflects the real project instead of a generic template.
- Keep the instruction file aligned with the project’s actual packages, layers, modules, conventions, and architecture patterns.

Task:
- Inspect the current codebase and infer the real package layout, module boundaries, naming conventions, and architecture patterns already in use.
- Compare the existing project structure against the current instruction file.
- Rewrite the instructions so they describe the project accurately, not a generic framework template.
- Remove assumptions that do not match the codebase.
- Preserve the existing intent of the instructions, but make them project-specific.

What to update:
- Actual root package name and package hierarchy
- Real layer names and boundaries used in the project
- Whether the project uses layered, clean, hexagonal, modular monolith, frontend-feature, service-oriented, or another style
- Existing conventions for controllers, services, repositories, DTOs, entities, mappers, exceptions, config, clients, security, tests, and utilities
- Actual persistence strategy used in the project
- Existing API style, validation, exception handling, and response conventions
- Existing build tool, modules, and test setup if relevant
- Existing frontend structure, routing, state-management, or UI conventions if relevant
- Existing observability, logging, and configuration conventions if relevant

Reference-check requirements:
- Verify the `projectRoot` and `instructionFile` paths exist.
- Verify any package names, module names, or layer names you mention are present in the codebase.
- Verify topic-file links still point to real files if you keep them.
- Verify the rewritten instructions do not contradict the actual repository structure.

Rules:
- Do not invent structure that is not present in the codebase.
- Keep behavior-preserving guidance.
- Do not recommend architectural refactors unless the codebase already uses them.
- Prefer concise, clear instructions over generic best-practice lists.
- Keep links to topic files if they still make sense.
- If a rule conflicts with the project’s real structure, update the instruction to match the project.
- If a framework, module, or layer is absent, remove or rewrite the related guidance instead of leaving stale assumptions.

Output:
- Return only the revised instruction content unless the user explicitly asks for analysis notes too.
- Make it ready to paste into the target instruction file.
```
