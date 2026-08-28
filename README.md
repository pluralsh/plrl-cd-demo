# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural. It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test`, and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.

## Health endpoint

`GET /ping` is a stable health/ping endpoint. It always responds with HTTP 200 and `{"pong": true}`.
