# {ProjectName} Architecture

## Architecture Overview

`{ProjectName}` is a {project_type} application.

The system has two core responsibilities:
- {core_responsibility_1}
- {core_responsibility_2}

The codebase is intentionally scoped to {architecture_scope_statement}.

## Technology Stack Summary

- {tech_stack_item_1}
- {tech_stack_item_2}
- {tech_stack_item_3}
- {tech_stack_item_4}

## System Context & External Integrations

`{ProjectName}` runs as a {deployment_model}.

External integrations:
- {external_integration_1}
- {external_integration_2}
- {external_integration_3}

## High-Level Design (HLD)

```mermaid
flowchart LR
    {hld_diagram}
```

The architecture follows a {architecture_pattern} model:
- {hld_point_1}
- {hld_point_2}
- {hld_point_3}

## Low-Level Design (LLD)

### `{component_1}`

{component_1_description}

Observed behavior:
- {component_1_observation_1}
- {component_1_observation_2}
- {component_1_observation_3}

### `{component_2}`

{component_2_description}

Responsibilities:
- {component_2_responsibility_1}
- {component_2_responsibility_2}
- {component_2_responsibility_3}

### `{component_3}`

{component_3_description}

It is not part of the runtime application path.

## Architecture Diagrams

### Runtime Bootstrap

```mermaid
flowchart TD
    {runtime_bootstrap_diagram}
```

### Data Layer

```mermaid
flowchart LR
    {data_layer_diagram}
```

## Flow Diagrams

### Deployment Flow

```mermaid
flowchart LR
    {deployment_flow_diagram}
```

{deployment_flow_notes}

### Startup Flow

1. {startup_step_1}
2. {startup_step_2}
3. {startup_step_3}
4. {startup_step_4}
5. {startup_step_5}

### Query Flow

```mermaid
sequenceDiagram
    {query_sequence_diagram}
```

1. {query_step_1}
2. {query_step_2}
3. {query_step_3}
4. {query_step_4}
5. {query_step_5}
6. {query_step_6}

## Component Responsibilities

### `{component_1}`

- {component_1_resp_1}
- {component_1_resp_2}
- {component_1_resp_3}

### `{component_2}`

- {component_2_resp_1}
- {component_2_resp_2}
- {component_2_resp_3}
- {component_2_resp_4}

### `{component_3}`

- {component_3_resp_1}
- {component_3_resp_2}
- {component_3_resp_3}

## Dependency Mapping

### Runtime Dependencies

- `{component_1}` depends on {runtime_dep_1}.
- `{component_2}` depends on {runtime_dep_2}.
- {runtime_dependency_3}
- {runtime_dependency_4}

### Build and Configuration Dependencies

- `{build_file_1}` defines {build_dependency_1}.
- `{config_file_1}` defines {build_dependency_2}.
- `{config_file_2}` defines {build_dependency_3}.
- `{config_file_3}` provides the local runtime container or environment.

## Data Model

The schema is defined in `{schema_file}`.

```sql
{schema_sql}
```

The table uses:
- {schema_point_1}
- {schema_point_2}
- {schema_point_3}
- {schema_point_4}

## Configuration

Runtime configuration is in `{config_file}`.

Important settings:
- {config_setting_1}
- {config_setting_2}
- {config_setting_3}
- {config_setting_4}
- {config_setting_5}
- {config_setting_6}
- {config_setting_7}

## External Dependencies

### {external_dependency_1}

{external_dependency_1_description}

### {external_dependency_2}

{external_dependency_2_description}

## Findings

- {finding_1}
- {finding_2}
- {finding_3}
- {finding_4}
- {finding_5}
- {finding_6}
- {finding_7}

## Risks

- {risk_1}
- {risk_2}
- {risk_3}
- {risk_4}
- {risk_5}

## Recommendations

1. {recommendation_1}
2. {recommendation_2}
3. {recommendation_3}
4. {recommendation_4}
5. {recommendation_5}
6. {recommendation_6}
7. {recommendation_7}

## Summary

{summary_text}
