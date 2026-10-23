# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint succeeds by default. For alerting demos only, set `PING_FAULT_INJECTION=true` (exact lowercase value) to enable its intentional intermittent failures. If log aggregation, and even better, vector indexing of PRs is enabled, you can tie a Prometheus or Datadog alert directly to a full root cause using Plural AI.

