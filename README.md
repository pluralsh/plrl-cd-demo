# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

This demo service includes a lightweight `/ping` endpoint that is suitable for health and monitoring checks. If alerts fire for a real regression, log aggregation and PR context can still be used with Plural AI to trace the root cause and propose a targeted fix.

