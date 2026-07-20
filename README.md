# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The service exposes a simple `/ping` endpoint that returns a healthy pong response for liveness-style checks. If log aggregation, and even better, vector indexing of PRs is enabled, you can still tie alerts to root cause analysis and Plural AI-generated fixes for real failures in the service.
