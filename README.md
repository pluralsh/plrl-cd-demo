# Plural CD Demo Application

This is a simple FastAPI demo microservice that can be managed by Plural. It builds a single Docker image published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small API and Prometheus metrics.

It can be deployed within a Plural Flow or by other means for testing.

## Endpoints

- `GET /ping` is a reliable ping endpoint. It always returns HTTP 200 with `{"pong": true}`.
- `GET /test/faults/ping` is an explicit fault-injection endpoint for alerting and RCA demonstrations. When the integer Unix timestamp is divisible by three, it intentionally raises an error and returns HTTP 500; at all other timestamps it returns HTTP 200 with `{"pong": true}`. This produces a deterministic failure during one out of every three one-second intervals. Do not use this endpoint for health checks or ordinary pingers.

## Alerting and AI-driven fixes

The explicit fault-injection endpoint supports demonstrations in which log aggregation, vector indexing of PRs, and Prometheus or Datadog alerts can be tied to a root-cause analysis using Plural AI. It is intentionally isolated from the ordinary `/ping` endpoint so application health and routine Flow pingers remain reliable.
