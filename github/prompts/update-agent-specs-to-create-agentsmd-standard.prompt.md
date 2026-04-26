# Update Agent Specs To Create-Agentsmd Standard

Use this prompt to upgrade one or more agent definition files so they are clearer, more operational, and better aligned with the `create-agentsmd` skill guidance in [.github/skills/create-agentsmd/SKILL.md](/Users/maheswarbuddolla/softwares/agents-skills-instructions/.github/skills/create-agentsmd/SKILL.md). Replace the placeholder inputs with the agent files you want reviewed.

```text
Review and update the provided agent definition files to a stronger operational standard.

Agent files:
- <agent-file-1>
- <agent-file-2>
- <agent-file-n>

Reference standard:
- .github/skills/create-agentsmd/SKILL.md

Inputs:
- `agentFiles`: list of one or more `.agent.md` files to review and update
- `referenceSkill`: `.github/skills/create-agentsmd/SKILL.md`

Your job:
1. Review the referenced `SKILL.md` carefully.
2. Check whether each agent file aligns with the spirit of the `create-agentsmd` guidance:
   - clarity
   - completeness
   - actionability
   - explicit operational instructions
   - consistency of structure
3. Check accurate references before making changes:
   - verify file paths exist
   - verify any agent ids, names, and example invocations are internally consistent
   - verify section titles and tool declarations match the agent’s real responsibilities
   - verify the changes you add do not contradict the existing prompt behavior
4. Apply targeted edits rather than rewriting the files unnecessarily.

Make these changes in each agent file:

- Add a concrete output contract.
- Define the expected output structure explicitly.
- Include a realistic JSON example for each file.
- Add short field-level expectations so the output is consistent and machine-consumable.

- Add these operational sections:
  - When To Use
  - When Not To Use
  - Expected Repo Inputs
  - Verification Steps
  - Required Checks Before Returning
  - Escalation And Ambiguity Handling

- Fix the `tools:` declarations:
  - inspect the agent’s actual responsibilities
  - keep the minimum correct tool set
  - remove tools that are not required
  - do not guess extra capabilities

Specific review requirements:

- Check whether the files are truly “up to the standard” of `create-agentsmd`, while recognizing that `create-agentsmd` is written for repository `AGENTS.md` files rather than per-agent prompt specs.
- If there is a mismatch between that standard and the purpose of these agent files, preserve the agent format but incorporate the most relevant qualities from the skill:
  - specific instructions
  - actionable guidance
  - clear workflows
  - explicit boundaries
  - operational completeness

Constraints:

- Preserve the existing purpose, tone, and core prompt behavior.
- Do not rewrite the whole file unless necessary.
- Keep wording concrete and operational.
- Prefer conservative edits that improve consistency and usability.
- Do not add vague filler sections.

Expected outcome:

- Every reviewed agent file has an explicit JSON output contract.
- Every reviewed agent file includes the new operational sections.
- The `tools:` block in each file matches the documented behavior.
- The resulting files better reflect the clarity and actionability encouraged by `create-agentsmd`.
- Any inconsistencies discovered during reference checking are either fixed or called out explicitly.
```
