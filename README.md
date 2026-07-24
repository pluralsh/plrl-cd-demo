# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The service exposes a simple `/ping` endpoint that returns a stable success response for health or synthetic checks. If log aggregation and vector indexing of PRs are enabled, you can still tie real alerts to root-cause analysis and have Plural AI propose a fix PR for genuine application issues.

