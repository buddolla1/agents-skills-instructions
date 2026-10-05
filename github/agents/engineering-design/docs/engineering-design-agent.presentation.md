# Engineering Design Agent Presentation

## Slide 1: Title Slide
### Title
Engineering Design Agent
### Subtitle
Repo-aware BDD, architecture, and design report generation from feature briefs
### Visual Suggestion
Flow diagram showing feature input to markdown output
### Speaker Notes
Introduce the agent as a structured design assistant that converts feature briefs into reviewable engineering artifacts.

## Slide 2: Executive Summary
### Key Points
- Generates repo-aware engineering design documents in markdown
- Supports BDD stories, architecture sections, full design reports, and reusable templates
- Accepts `feature.txt` or equivalent feature brief input
- Asks for `storyCount` when BDD scope is missing
### Visual Suggestion
Three-column summary: input, processing, output
### Speaker Notes
Focus on the agent’s purpose: reduce design drafting time while keeping the output grounded in repository evidence.

## Slide 3: Problem Statement
### Key Points
- Design output is often inconsistent across teams
- Feature requirements are frequently vague or incomplete
- Architecture and BDD documents drift away from repository reality
- Manual report drafting is slow and repetitive
### Visual Suggestion
Pain-point list with a before/after comparison
### Speaker Notes
Frame the agent as a response to inconsistency, ambiguity, and slow documentation cycles.

## Slide 4: How It Works
### Key Points
- Reads repository context from README, build files, source, and config
- Interprets the feature brief and clarifies missing scope
- Generates the requested artifact set in markdown
- Writes output under `docs/generated/`
### Visual Suggestion
Left-to-right pipeline: repo context, clarification, generation, output
### Speaker Notes
Emphasize that the agent is not a generic writer. It uses repository evidence before making architecture claims.

## Slide 5: Supported Outputs
### Key Points
- BDD only
- Architecture only
- Full design
- Reusable template
- Broad requirement clarification
### Visual Suggestion
Four-quadrant output matrix
### Speaker Notes
Show that the agent is flexible, but still controlled by the output mode and guardrails.

## Slide 6: BDD Behavior
### Key Points
- Uses `storyCount` to control the number of stories
- Asks how many stories to create when `storyCount` is missing
- Uses 5 subtasks per story by default
- Includes epics, user stories, scenarios, tasks, dependencies, risks, NFRs, and estimation summary
### Visual Suggestion
Story block diagram with repeated sections
### Speaker Notes
This is the agent’s most structured workflow. The story count drives the report shape.

## Slide 7: Architecture Behavior
### Key Points
- Produces architecture overview, HLD, LLD, and diagrams
- Includes Mermaid diagrams where they improve clarity
- Grounds component and integration claims in visible repo evidence
- Keeps assumptions explicit when evidence is thin
### Visual Suggestion
Architecture stack diagram with flows and dependencies
### Speaker Notes
Explain that architecture output is evidence-driven, not speculative.

## Slide 8: Guardrails and Quality
### Key Points
- Do not invent repo context
- Do not hide assumptions
- Do not skip diagrams when architecture output is requested
- Do not return JSON when the contract is markdown
### Visual Suggestion
Checklist with pass/fail markers
### Speaker Notes
Highlight the controls that keep outputs usable in real engineering reviews.

## Slide 9: Example Prompts
### Key Points
- Using `feature.txt`, generate a full design report
- Using `feature.txt`, generate BDD stories and ask for `storyCount` if missing
- Using `feature.txt`, generate only the architecture section
- Using `feature.txt`, generate a reusable report template
### Visual Suggestion
Prompt examples in a compact callout panel
### Speaker Notes
Show the practical entry points users can use immediately.

## Slide 10: Closing Summary
### Key Points
- Converts feature briefs into structured engineering artifacts
- Keeps design output aligned to repository evidence
- Supports both execution planning and architecture communication
- Reduces manual drafting while improving consistency
### Visual Suggestion
Outcome summary with three benefit badges
### Speaker Notes
Close by positioning the agent as a repeatable design workflow, not just a document generator.
