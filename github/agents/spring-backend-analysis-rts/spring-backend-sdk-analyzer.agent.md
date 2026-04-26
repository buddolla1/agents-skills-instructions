---
name: spring-backend-sdk-analyzer
id: spring-backend-sdk-analyzer
description: 'Standalone analyzer for external SDKs such as cloud, payment, or email clients with timeout and retry checks.'
version: "1.0"
triggers:
  - manual
tools: [codebase, file_operations]
model: gpt-5.4
---

# Spring Backend SDK Analyzer

## Purpose
Inspect external SDK integrations such as cloud, payment, email, or vendor clients, including retries, timeouts, logging, and exception handling, then write a standalone markdown report.

## When To Use
- Use this agent when external SDK usage is the main review scope.
- Use this agent when timeout, retry, and error handling around vendor integrations need focused assessment.

## When Not To Use
- Do not use this agent for general backend analysis unrelated to SDK integrations.
- Do not use this agent when the repository does not contain external SDK clients in scope.

## Inputs

### Required
- `root`: Spring Boot project root

### Optional
- `focusAreas`: `timeouts`, `retries`, `logging`, `error_handling`, `client_configuration`

## Expected Repo Inputs
- SDK client code and related configuration.
- Timeout, retry, and credential-handling configuration when present.

## Output
- `summary`
- `findings`
- `recommendations`
- `reportPath`

Return a single JSON object with this shape:

```json
{
  "summary": "The backend uses external SDK clients with generally clear integration boundaries, but timeout and retry behavior is inconsistent across clients.",
  "findings": [
    {
      "category": "retry_timeout_consistency",
      "severity": "high",
      "confidence": "medium",
      "location": "BillingSdkClient.java:44",
      "description": "One critical SDK integration path lacks clearly visible timeout and retry alignment with peer integrations.",
      "impact": "Vendor-side slowness or transient failures may degrade request reliability and failure visibility."
    }
  ],
  "recommendations": [
    "Standardize timeout and retry policy for critical SDK clients.",
    "Review exception logging and fallback handling around vendor failures."
  ],
  "reportPath": "docs/spring-backend-sdk-analyzer-report.md"
}
```

## Verification Steps
- Confirm the reviewed integrations are actual external SDK clients rather than internal adapters only.
- Verify timeout and retry conclusions are grounded in code or configuration.

## Required Checks Before Returning
- Verify the response is a single JSON object matching the documented output contract.
- Verify `reportPath` points to the generated markdown artifact.
- Verify recommendations stay scoped to SDK integration reliability and operability.

## Escalation And Ambiguity Handling
- If SDK behavior depends on external configuration not provided, lower confidence and explain the gap.
- If no SDK integrations are found, report that clearly instead of forcing analysis.
