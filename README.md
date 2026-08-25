# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural. It builds a single Docker image, published to `ghcr.io/pluralsh/plrl-cd-test`, and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.

## Health endpoint

`GET /ping` is the service health endpoint and consistently returns `{"pong": true}`. It is suitable for probes and alerting checks.
