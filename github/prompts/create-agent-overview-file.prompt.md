# Create Agent Overview File

Use this prompt to generate a human-friendly overview document for one or more agent definition files. The overview file should be created in a `docs/` folder inside the same directory as each target `.agent.md` file and should explain what the agent does, when to use it, how it works, and how to prompt it effectively. Include Mermaid flowcharts where they add value.

```text
Create an overview markdown file for each of the following agent definition files:

- <agent-file-1>
- <agent-file-2>
- <agent-file-n>

Inputs:
- `agentFiles`: list of one or more `.agent.md` files

Goal:
- For each input agent file, create a companion overview markdown file in a `docs/` subdirectory inside the same directory as the agent file.
- The overview should help a human quickly understand the agent, use it correctly, and choose effective prompts.

File placement:
- Create the overview file in a `docs/` folder inside the same folder as the source agent file.
- Create the `docs/` folder if it does not already exist.
- Use a consistent naming convention based on the agent file name.
- Preferred naming:
  - `<agent-name>.overview.md`
- Example:
  - `.github/agents/foo/my-agent.agent.md`
  - `.github/agents/foo/docs/my-agent.overview.md`

Your job:
1. Read the target `.agent.md` file carefully.
2. Extract the agent’s:
   - name
   - id
   - description
   - tools
   - purpose
   - inputs
   - outputs
   - workflow
   - guardrails
   - examples
3. Create a concise but useful overview markdown file for humans.
4. Keep the overview aligned with the source agent file. Do not invent capabilities that are not documented.
5. If the source file is missing details, note the limitation clearly instead of guessing.

Required sections in each overview file:

- `# <Agent Name> Overview`
- `## What This Agent Does`
- `## When To Use It`
- `## When Not To Use It`
- `## How It Works`
- `## Inputs It Expects`
- `## Outputs It Produces`
- `## Tools It Uses`
- `## How To Prompt It`
- `## Example Prompts`
- `## Limits And Guardrails`

Mermaid requirements:

- Add Mermaid flowcharts wherever they meaningfully clarify the agent behavior.
- At minimum, include one Mermaid flowchart for the main workflow if the source agent defines a workflow or a multi-step process.
- Use simple, readable flowcharts rather than overly dense diagrams.
- Do not add Mermaid just for decoration.

Recommended Mermaid examples:
- workflow from input to analysis to output
- decision branch for ambiguity, confirmation, or manual verification
- analysis vs fix path when the agent distinguishes those modes

Content requirements:

- Explain the agent in plain English for a human reader.
- Describe how a user should invoke the agent and what kind of context to provide.
- Summarize the workflow in a readable sequence.
- Convert structured source-agent information into practical usage guidance.
- Include example prompts that are realistic and aligned with the documented behavior.
- If the agent has confirmation rules, ambiguity handling, or manual verification requirements, call them out explicitly.

How To Prompt It section must explain:

- what kind of request works well
- what context to provide
- how specific the user should be
- when to include files, page URLs, user flows, or code snippets
- what not to ask the agent to do

Outputs It Produces section must explain:

- the main output fields or response shape
- whether the output is analytical, actionable, or code-modifying
- whether the user should expect JSON, prose, diffs, or manual verification steps

Tools It Uses section must explain:

- each declared tool
- why the agent needs it
- any important limits implied by the tool list

Constraints:

- Preserve fidelity to the source `.agent.md` file.
- Do not rewrite the source agent file unless explicitly asked.
- Do not invent missing workflows, tools, or guarantees.
- Keep the overview practical and easy to scan.
- Prefer direct language over marketing language.

Expected outcome:

- Each target `.agent.md` file gets a companion overview markdown file in a `docs/` folder beside the agent file.
- The overview clearly explains the agent, how to use it, how it works, and how to prompt it.
- Mermaid flowcharts are included where they improve clarity.
```
