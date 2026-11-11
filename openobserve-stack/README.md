# OpenObserve container-log testing

Flow: test-app stdout/stderr → Docker fluentd logging driver → Fluent Bit forward input → OpenObserve application_logs.

Designed for local Docker Desktop (Mac/Windows) or local Docker Engine on Linux. No application server or manual log-file copying is needed. Docker itself must be installed and running.

## Start

From this extracted directory:

```bash
cp .env.example .env
```

Edit `.env` with your email and a strong password, then run:

```bash
docker compose config --quiet
docker compose up -d
```

Open http://localhost:5080 and sign in with those credentials. Select Logs → application_logs and a recent time range. Allow time for image downloads, startup, and ingestion. The stream appears after first ingestion. The test container emits INFO every five seconds and a simulated ERROR to stderr every fifth iteration. These are test messages, not real failures.

## Inspect and stop

```bash
docker compose ps
docker compose logs --tail 50 fluent-bit
docker compose logs --tail 50 openobserve
docker compose stop test-app
docker compose down
```

Named volumes retain OpenObserve data and Fluent Bit buffered logs. Do not add `-v` unless you intend to delete that data. If reusing an existing OpenObserve volume, use its existing login credentials.

## Collect another application container

Copy the test-app `logging` block into that application's Compose service and recreate that container. The logging driver runs in the Docker daemon, so its address is the host-published 127.0.0.1:24224, not the Compose service name. This package collects only containers configured with that logging block; it does not discover all existing containers or backfill old logs. Remote Docker daemons require a reachable collector endpoint on that daemon host.

OpenObserve and Fluent Bit explicitly use local logging to prevent a logging feedback loop. Fluent Bit receives Docker metadata such as container_name, container_id, source, and log. Java stack traces require additional multiline processing.

The asynchronous Docker logging buffer can lose logs during prolonged collector outages or daemon restarts; this is a test configuration, not a guaranteed-delivery production pipeline. Images using latest are convenient for testing but should be pinned after validation.

## Validation

YAML parsed and configuration relationships checked. Docker is unavailable in the authoring environment, so container startup and end-to-end ingestion have not been runtime-tested.

## References

- https://docs.docker.com/engine/logging/drivers/fluentd/
- https://docs.fluentbit.io/manual/data-pipeline/inputs/forward
- https://openobserve.ai/docs/ingestion/logs/fluent-bit/



It starts three containers. OpenObserve, where the logs are stored and searched, using your env file for login and keeps its data in a volume; Fluent Bit, which receives logs and forwards them to OpenObserve; and test-app, which prints a test log every few seconds. Docker sends that test-app output to Fluent Bit, then Fluent Bit forwards it to the application logs stream. Compose starts OpenObserve first, then Fluent Bit, then the test container. If you want your real application later, we’ll add that same logging block to it.

https://github.com/openobserve/dashboards/blob/main/Docker_Metrics/Docker%20Container%20Metrics.dashboard.json











 