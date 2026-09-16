# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural. It builds a single Docker image, published to `ghcr.io/pluralsh/plrl-cd-test`, and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.

## Health checking

`GET /ping` is the service health endpoint and always returns `200 OK` with `{ "pong": true }`. It is safe for continuous probes, including the pinger sidecar used in Flow deployments.

## Alerting and AI Driven fixes

Plural alerting and AI-driven fixes can correlate application errors with their root cause and generate a remediation PR. The health endpoint remains reliable so it can distinguish real application failures from synthetic test behavior.
