# [Feature Name]-design-bdd-breakdown

[Generate this report from a feature brief such as `feature.txt` or equivalent requirement text.]

## Story Count
[Set `storyCount` to the number of stories to generate. If it is missing, ask how many stories should be created before continuing. Repeat the story block below until it matches `storyCount`.]

## Architecture Overview
[Summarize the feature in 2-4 sentences. State the goal, user value, and where it fits in the current system.]

## High-Level Design (HLD)
[Describe the overall solution, major components, and how they interact at a high level.]

```mermaid
flowchart LR
  A[User] --> B[UI]
  B --> C[Controller]
  C --> D[Service]
  D --> E[Data Store]
```

## Low-Level Design (LLD)
### Components
- `[Component 1]`: [Responsibility]
- `[Component 2]`: [Responsibility]
- `[Component 3]`: [Responsibility]

### Data Model
`[table_or_entity_name]`
- `id`
- `[field_1]`
- `[field_2]`
- `[field_3]`

```mermaid
sequenceDiagram
  participant U as User
  participant UI as UI
  participant C as Controller
  participant S as Service
  participant D as Data Store

  U->>UI: interact
  UI->>C: request
  C->>S: process()
  S->>D: read/write
  D-->>S: result
  S-->>C: response
  C-->>UI: render data
```

## Architecture Diagrams
```mermaid
flowchart LR
  U[User] --> C[Controller]
  C --> S[Service]
  S --> D[Data Store]
  S --> L[External Service]
```

```mermaid
sequenceDiagram
  participant U as User
  participant C as Controller
  participant S as Service
  participant D as Data Store
  participant L as External Service

  U->>C: request
  C->>S: process()
  S->>D: read/write data
  S->>L: call external API
  L-->>S: response
  S-->>C: result
  C-->>U: response
```

## Epics
1. `[Epic 1 title]`
2. `[Epic 2 title]`
3. `[Epic 3 title]`
[Add one epic per story or feature slice as needed.]

## Story Block
[Repeat this block for each story in `storyCount`.]

### Story [n]
As a `[persona]`, I want `[goal]` so that `[value]`.

- Story Points: `[1/2/3/5/8/13/21]`
- Notes: `[optional implementation notes]`

### Story [n] Subtasks
1. `[Subtask 1]`
2. `[Subtask 2]`
3. `[Subtask 3]`
4. `[Subtask 4]`
5. `[Subtask 5]`

### Story [n] BDD Scenarios
```gherkin
Feature: [Feature name]
  Scenario: [scenario title]
    Given [precondition]
    When [action]
    Then [expected outcome]

  Scenario: [scenario title]
    Given [precondition]
    When [action]
    Then [expected outcome]

  Scenario: [scenario title]
    Given [precondition]
    When [action]
    Then [expected outcome]
```

### Story [n] Tasks
- `[story-specific task 1]`
- `[story-specific task 2]`
- `[story-specific task 3]`

### Story [n] Dependencies
- `[dependency 1]`
- `[dependency 2]`

## Test Data
### Positive
- `[example input 1]`
- `[example input 2]`

### Negative
- `[invalid input 1]`
- `[invalid input 2]`

### Boundary
- `[boundary case 1]`
- `[boundary case 2]`

### Edge
- `[edge case 1]`
- `[edge case 2]`

## Cross-Cutting Tasks
- `[cross-cutting task 1]`
- `[cross-cutting task 2]`
- `[cross-cutting task 3]`

## Execution Plan
1. `[step 1]`
2. `[step 2]`
3. `[step 3]`
4. `[step 4]`

## Risks
- `[risk 1]`
- `[risk 2]`

## Assumptions
- `[assumption 1]`
- `[assumption 2]`

## NFRs
- `[performance / security / logging / accessibility requirement 1]`
- `[performance / security / logging / accessibility requirement 2]`

## Estimation Summary
| Story | Points |
|---|---:|
| Story [n] | `[points]` |
[Add one row per story in `storyCount`.]
| Total | `[sum]` |
