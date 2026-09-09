# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint normally returns a successful response. To deliberately simulate the error path for alerting and AI-driven-fix demonstrations, set `PING_FAIL_ENABLED=true`; with that explicit opt-in it raises `unknown internal error` every third epoch second. This keeps normal health checks and production traffic reliable while preserving the demo scenario.

With log aggregation and vector indexing of PRs enabled, a Prometheus or Datadog alert can be tied directly to a root cause using Plural AI, which can spawn a PR to fix the broken code change. An example generated fix PR is available in the repository history.

