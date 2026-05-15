## Prompt index

Prompt files are reusable task templates that help an agent or user start from a stronger, more consistent instruction set. Each prompt captures a repeatable task, the expected inputs, and the intended output shape.

Why prompts are useful:

- They reduce repetition for tasks that need the same framing every time.
- They improve consistency by giving the agent a stable starting instruction.
- They make complex repository tasks easier to reuse across projects.
- They help convert broad goals into structured, actionable requests.
- They reduce drift by keeping task wording aligned with a defined workflow.

Key advantages:

- Faster task setup
- More predictable outputs
- Better reuse across repositories
- Clearer inputs and expected outcomes
- Easier standardization for recurring work

Checklist

- [x] Gather prompt files in `github/prompts/`
- [x] Extract the prompt title and opening purpose from each file
- [x] Provide a short "Why to use" and "How to use" note for each prompt
- [x] Include relative paths for direct lookup

This file lists the repository prompts with a short description, why you would use each one, and a quick way to get started. For full usage details, open the corresponding prompt file.

| Prompt name | Description | Why to use | How to use | Path |
| --- | --- | --- | --- | --- |
| `Architecture Baseline Before Instruction Update` | Reuses an existing root-level architecture document when present, otherwise derives a real architecture baseline from the codebase before rewriting an instruction file. | Use when an instruction file should be updated to match the actual repository architecture instead of a generic template. | Provide `projectRoot`, `instructionFile`, and `instructionTarget`; the prompt checks for an existing architecture baseline, verifies it against the repo, and then rewrites the instruction file. | `architecture-baseline-for-instructions.md` |
| `Create Agent Overview File` | Generates a human-friendly overview document for one or more `.agent.md` files, including what the agent does, when to use it, how it works, and how to prompt it. | Use when you want companion documentation that helps people understand and use agent definition files correctly. | Provide one or more target `.agent.md` files; the prompt creates overview markdown files in sibling `docs/` folders with extracted agent details and usage guidance. | `create-agent-overview-file.prompt.md` |
| `Update Agent Specs To Create-Agentsmd Standard` | Reviews and upgrades agent definition files so they align more closely with the `create-agentsmd` skill guidance and a stronger operational standard. | Use when existing agent specs are incomplete, inconsistent, or need clearer output contracts and operational instructions. | Provide one or more `.agent.md` files and the `create-agentsmd` skill reference; the prompt reviews each file, verifies internal consistency, and applies targeted improvements. | `update-agent-specs-to-create-agentsmd-standard.prompt.md` |
| `Update Copilot Instructions From Real Project Structure` | Rewrites an instruction file so it reflects the real project structure, architecture, conventions, and boundaries already present in the repository. | Use when a repository instruction file has drifted into a generic template and needs to be grounded in the actual codebase. | Provide `projectRoot`, `instructionFile`, and `instructionTarget`; the prompt inspects the current codebase, compares it with the instruction file, and rewrites the instructions to be project-specific. | `update-instructions-from-project.md` |
