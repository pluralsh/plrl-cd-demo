# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint is healthy by default and returns a `200` response. To intentionally exercise an alerting workflow in a non-production environment, set `SIMULATE_PING_FAILURE=true`; this explicitly enables the prior simulated unhandled error behavior.

If log aggregation and vector indexing of PRs are enabled, a Prometheus or Datadog alert can then be tied directly to a full root cause using Plural AI, which can spawn a corrective PR.

