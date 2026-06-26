# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The service exposes a lightweight `/ping` endpoint that always returns `{"pong": true}` with HTTP 200 for external health checks and alert validation workflows.

Plural AI can still be used to trace production alerts back to the relevant code or configuration changes and generate candidate fixes when issues are detected.

