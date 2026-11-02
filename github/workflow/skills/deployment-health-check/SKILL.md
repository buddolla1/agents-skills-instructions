---
name: deployment-health-check
description: 'Evaluate CI/CD execution, artifact provenance, rollout state, canary signals, and microservice health before declaring a deployment successful.'
---

# Deployment Health Check

Use this skill to observe a deployment already placed in scope.

Tie the deployment identifier and artifact digest or version to the release commit. Evaluate pipeline status, rollout progress, replica or instance readiness, startup and readiness probes, error rate, latency, saturation, critical logs, dependency health, and configured canary comparison windows. Use service-specific thresholds when supplied; do not invent universal thresholds.

Return:

- `passed` when required pipeline, rollout, provenance, and health criteria pass
- `failed` when a required criterion fails or a confirmed regression appears
- `inconclusive` when the observation window or evidence is insufficient

Report the environment, observation window, metrics and logs consulted, thresholds, anomalies, and recommended next action. Monitoring does not authorize promotion, rollback, cancellation, or a Jira transition; those mutations require separate authorization.

