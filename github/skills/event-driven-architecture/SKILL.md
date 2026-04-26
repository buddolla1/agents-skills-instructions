---
name: event-driven-architecture
description: Design and review event-driven Java systems using Kafka or RabbitMQ patterns. Use when working on producers, consumers, message contracts, retries, idempotency, dead-letter handling, ordering, and asynchronous integration flows.
---

# Event-Driven Architecture

## When to Use This Skill

Use this skill when building or reviewing asynchronous integration between services or systems.

## Prerequisites

- The producer, consumer, and message contract being reviewed
- Any schema, broker, or topic and queue conventions already in use
- Knowledge of delivery expectations and retry behavior

## Goal

Apply event-driven patterns that preserve correctness, isolate failures, and keep message flow observable and reliable.

## Patterns to Evaluate

- Kafka publish/consume flows
- RabbitMQ queue and routing patterns
- Event schemas and backward compatibility
- Retry, dead-letter, and poison-message handling
- Consumer idempotency and duplicate delivery safety
- Ordering, partitioning, and reprocessing strategy

## Step-by-Step Workflows

1. Identify the event source, consumer, and business outcome.
2. Determine whether the flow is event, command, or integration message driven.
3. Check delivery semantics and duplicate handling assumptions.
4. Validate schema evolution and backward compatibility.
5. Confirm the operational path for retries, dead letters, and replay.

## Kafka Guidance

- Use partitions deliberately to balance ordering and parallelism.
- Keep key selection aligned with ordering requirements.
- Treat consumers as at-least-once unless the implementation proves otherwise.
- Ensure offset handling, rebalancing, and replay behavior are understood.

## RabbitMQ Guidance

- Choose exchange and queue topology based on routing needs.
- Make retry and dead-letter paths explicit.
- Avoid relying on implicit broker behavior for critical business flow.
- Tune prefetch and concurrency to match workload and processing cost.

## Guardrails

- Make consumers idempotent when duplicate delivery is possible.
- Do not embed business logic in message structure assumptions alone.
- Do not let retries create infinite poison-message loops.
- Prefer explicit schema/version handling for durable contracts.

## Output Standard

For each issue, provide:

- Flow or component
- Eventing concern
- Risk to delivery or correctness
- Recommended Kafka or RabbitMQ pattern
- Operational validation note

## Reporting Style

- Be specific about the delivery semantics being relied on.
- Prefer patterns that improve reliability without obscuring the business flow.
- Explain how the proposed change behaves during retries, failures, and reprocessing.

## Troubleshooting

- If duplicate delivery is possible, verify idempotency before recommending changes.
- If the retry path is unclear, define the dead-letter and replay behavior first.
- If ordering matters, confirm the partitioning or queueing model supports it.

## References

- Kafka or RabbitMQ platform conventions
- Related schema and consumer contract docs
