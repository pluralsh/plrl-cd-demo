# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint succeeds by default. To intentionally exercise the alerting and AI-driven remediation workflow, set `PING_FAILURE_ENABLED=true`. With this explicitly opt-in setting, `/ping` returns an internal error for roughly one out of every three seconds; leave it unset in normal deployments.

If log aggregation and vector indexing of PRs are enabled, you can tie a Prometheus or Datadog alert directly to a full root cause using Plural AI, which can then spawn a remediation PR.

