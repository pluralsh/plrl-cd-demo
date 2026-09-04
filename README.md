# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural. It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test`, and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.

## Alerting and AI Driven fixes

`GET /ping` returns `{"pong": true}` with a 200 response by default. The alerting demo's deliberate failure behavior is disabled unless `PING_FAULT_INJECTION=true` is explicitly set (case-insensitive). When enabled, `/ping` raises `Exception("unknown internal error")` whenever the current Unix timestamp is divisible by three.

This opt-in behavior lets a Prometheus or Datadog alert, especially with log aggregation and vector indexing of PRs enabled, be tied directly to a full root cause using Plural AI. It can then spawn a PR to fix the broken code change while production remains safe by leaving `PING_FAULT_INJECTION` unset.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5. This was actually a one-shot (you can verify in the PR history of the repo).
