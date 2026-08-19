# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint is healthy by default and returns `{"pong": true}`.  The historical synthetic failure used for alerting and AI root-cause demos is retained, but is disabled unless `ENABLE_CHAOS_TESTING=true` is set.  When explicitly enabled, `/ping` raises an intentional internal error whenever the current Unix timestamp is divisible by three.

This opt-in behavior lets log aggregation, vector indexing of PRs, and Plural AI demonstrate the path from a Prometheus or Datadog alert to a root cause and generated fix without permanently emitting demo 500s in normal deployments.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).
