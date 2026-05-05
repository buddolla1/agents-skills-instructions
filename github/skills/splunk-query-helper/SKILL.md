---
name: splunk-query-helper
description: 'Help write, explain, refine, and troubleshoot Splunk SPL queries. Use when building searches, filtering noisy events, parsing fields, creating stats or timecharts, and improving query clarity or performance.'
---

# Splunk Query Helper

## When to Use This Skill

Use this skill when working with Splunk SPL for log analysis, dashboards, alerts, or incident investigation.

Typical cases:

- Build a new SPL query from an investigation goal
- Refine a noisy search into something actionable
- Parse fields from semi-structured log lines
- Aggregate events with `stats`, `timechart`, or `chart`
- Troubleshoot why a query returns too much, too little, or nothing
- Improve readability and performance of an existing query

## Prerequisites

- The investigation goal or question being answered
- Known indexes, source types, hosts, apps, or data domains when available
- Sample log lines or field names if parsing is required
- Time range and expected result shape

## Goal

Produce correct, readable, and efficient SPL that matches the user’s intent and is practical to run in Splunk.

## Working Approach

1. Clarify the target dataset first: `index`, `sourcetype`, `source`, `host`, or known fields.
2. Narrow the time range and base search before adding transformations.
3. Prefer existing indexed fields over expensive late parsing.
4. Extract, normalize, and rename fields only when needed for the analysis.
5. Use the smallest aggregation that answers the question.
6. Return the final SPL with a short explanation of what each stage does.

## Query Construction Rules

- Start with the narrowest reliable base search.
- Filter early on stable fields before using transforming commands.
- Prefer `stats` over `transaction` unless session reconstruction is truly required.
- Use `where` for expression logic and field comparisons.
- Use `search` for simple term and field filtering.
- Use `eval` for derived fields and normalization.
- Use `rex` only when fields are not already extracted.
- Use `table` or `fields` near the end to control output shape.

## Performance Guidance

- Restrict index and time range as early as possible.
- Avoid leading wildcards unless there is no better option.
- Avoid unnecessary `join`, `append`, and `map` commands.
- Be careful with high-cardinality `stats by` dimensions.
- Prefer summary or accelerated data models when the use case already supports them.
- If performance is poor, simplify the search and verify each stage incrementally.

## Common Patterns

### Error Count by Service

```spl
index=app_logs sourcetype=service_logs level=ERROR
| stats count by service
| sort - count
```

### Time Trend

```spl
index=app_logs sourcetype=service_logs status=500
| timechart span=5m count by service
```

### Field Extraction

```spl
index=app_logs sourcetype=service_logs "requestId="
| rex "requestId=(?<request_id>[A-Za-z0-9-]+)"
| stats count by request_id
```

### Slow Requests

```spl
index=app_logs sourcetype=service_logs duration_ms=*
| eval duration_ms=tonumber(duration_ms)
| where duration_ms > 2000
| table _time service endpoint duration_ms request_id
```

### Top Endpoints by Volume

```spl
index=app_logs sourcetype=service_logs endpoint=*
| stats count by endpoint
| sort - count
| head 20
```

### Unique Users by Service

```spl
index=app_logs sourcetype=service_logs user_id=* service=*
| stats dc(user_id) as unique_users by service
| sort - unique_users
```

### P95 Latency by Endpoint

```spl
index=app_logs sourcetype=service_logs duration_ms=* endpoint=*
| eval duration_ms=tonumber(duration_ms)
| stats perc95(duration_ms) as p95_ms avg(duration_ms) as avg_ms by endpoint
| sort - p95_ms
```

### Error Rate by Service

```spl
index=app_logs sourcetype=service_logs service=* status=*
| eval is_error=if(status>=500,1,0)
| stats count as total sum(is_error) as errors by service
| eval error_rate=round((errors/total)*100,2)
| sort - error_rate
```

### Latest Event per Request

```spl
index=app_logs sourcetype=service_logs request_id=*
| sort 0 - _time
| dedup request_id
| table _time request_id service status message
```

### Missing Field Detection

```spl
index=app_logs sourcetype=service_logs
| eval missing_request_id=if(isnull(request_id) OR request_id="", "yes", "no")
| stats count by missing_request_id service
```

### Login Failures by User and Source IP

```spl
index=security sourcetype=auth_logs action=login outcome=failure
| stats count by user src_ip
| sort - count
```

### Rare Errors

```spl
index=app_logs sourcetype=service_logs level=ERROR error_code=*
| stats count by error_code
| where count < 5
| sort count
```

### Compare Current Hour to Previous Hour

```spl
index=app_logs sourcetype=service_logs
| bin _time span=1h
| stats count by _time service
| streamstats current=f window=1 last(count) as previous_count by service
| eval delta=count-previous_count
| table _time service count previous_count delta
```

### Correlate by Request ID

```spl
index=app_logs sourcetype=service_logs request_id=*
| stats values(service) as services values(status) as statuses values(message) as messages min(_time) as first_seen max(_time) as last_seen by request_id
| eval duration_sec=last_seen-first_seen
| sort - duration_sec
```

### Detect Traffic Spikes

```spl
index=app_logs sourcetype=service_logs
| timechart span=5m count by service
```

Use `anomalydetection` or compare against a baseline only when the dataset and operational need justify the extra complexity.

## Guardrails

- Do not invent field names, indexes, or source types; mark assumptions clearly.
- Do not use expensive commands when a simpler pattern will do.
- Do not over-parse raw text if structured fields already exist.
- Do not return SPL without explaining assumptions when the data model is incomplete.
- Do not broaden the search scope just to force results.

## Output Standard

For each answer, provide:

- Final SPL query
- Assumptions made
- Short explanation of major pipeline stages
- Any validation or performance notes

## Troubleshooting

- If there are no results, verify time range, index, and base filters first.
- If there are too many results, tighten the base search before adding transforms.
- If fields are missing, inspect raw events and confirm extraction timing.
- If counts look wrong, check whether multi-value fields, duplicates, or event granularity affect the result.
- If the query is slow, remove later pipeline steps until the expensive stage is obvious.

## Reporting Style

- Keep SPL readable and formatted line by line.
- State assumptions explicitly.
- Prefer small iterative refinements over a single opaque query.
