# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

This demo app still works well for experimenting with observability and AI-assisted remediation flows, but `/ping` now behaves like a normal health endpoint and returns a stable success response for health checks and sidecars.

