# Architecture Baseline Before Instruction Update

Use this prompt when you want to reuse an existing root-level architecture document if one exists, otherwise document the real project architecture first, then rewrite an instruction file so it matches the existing codebase. Replace the placeholders with the repository root and target instruction file.

## Why This Helps

For an existing project, a baseline-first approach keeps the instructions anchored to what is actually in the repository instead of drifting into a generic template.

This is useful because it:

1. Aligns the instruction file with the actual project architecture.
2. Reduces false assumptions about packages, modules, layers, persistence, and integration patterns.
3. Improves consistency across controllers, services, repositories, DTOs, clients, tests, and supporting code.
4. Reuses an existing architecture snapshot when the repository already has one.
5. Helps Copilot produce output that is more accurate, maintainable, and project-specific.

```text
Create an architecture baseline for the current project before updating the instruction file.

Inputs:
- `projectRoot`: <project-root>
- `instructionFile`: <instruction-file-path>
- `instructionTarget`: `copilot`, `copilot-instructions`, or `generic-project-instructions`

Goal:
- Check whether the repository already has a root-level architecture document and use it if it exists.
- Otherwise inspect the existing codebase and produce a concise architecture baseline grounded in real files and configuration.
- Use that baseline to rewrite the target instruction file so it reflects the actual repository structure and conventions.

Task:
1. Verify that `projectRoot` and `instructionFile` exist.
2. Check the repository root for an existing architecture document such as `architecture.md` or a similarly named `*architecture*.md` file.
3. If a root-level architecture document exists:
   - read it first
   - treat it as an input baseline, not as unquestioned truth
   - verify its major claims against the current codebase before relying on it
   - update or correct any stale assumptions when rewriting the instruction file
4. If no root-level architecture document exists, inspect the current codebase and identify the real architecture:
   - package or module layout
   - layer boundaries
   - naming conventions
   - persistence style
   - API patterns
   - frontend structure when relevant
   - testing, configuration, logging, security, and observability conventions when relevant
5. Document the architecture baseline before editing the instruction file.
6. Compare the documented baseline against the current instruction file.
7. Rewrite the instruction file so it matches the real codebase instead of a generic framework template.
8. Verify the rewritten instructions do not contradict the baseline.

What the architecture baseline should cover:
- Executive summary of the project shape
- Key findings and noteworthy constraints
- Package, module, or folder structure
- Layer responsibilities and boundaries
- Persistence and transaction patterns
- API, validation, and exception-handling conventions
- Frontend structure, routing, and state-management conventions when relevant
- Security, configuration, logging, observability, and testing conventions when relevant

Reference-check requirements:
- Verify whether a root-level architecture document exists before generating a new baseline from scratch.
- Verify any existing architecture document is still consistent with the current repository before using it as a source of truth.
- Verify all major architecture claims against visible files, folders, modules, or configuration.
- Verify any package names, module names, or layer names you mention are present in the repository.
- Verify any retained links or referenced topic files still exist.
- Verify the final rewritten instruction content is consistent with the documented baseline.

Rules:
- Do not invent architecture that is not present in the codebase.
- Do not trust an existing architecture document blindly if the codebase has drifted.
- Do not leave stale generic framework assumptions in the final instructions.
- Preserve the original intent of the instruction file where possible, but make it project-specific.
- Prefer concise, operational guidance over long best-practice lists.
- If a framework, layer, or module is absent, remove or rewrite the related guidance.
- If the codebase is mixed or inconsistent, document that honestly instead of normalizing it away.

Output:
- First return the architecture baseline.
- Then return the revised instruction content.
- Keep the revised instructions ready to paste into the target file.
- Keep the final result aligned with the actual repository, not a generic template.
```
