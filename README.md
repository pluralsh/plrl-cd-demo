# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural. It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.

## Alerting and AI Driven fixes

Historically `app/main.py` included a deliberately broken `/ping` endpoint. That was useful for demoing alert-driven root cause analysis, but `demo-prod/flow-test` also uses `/ping` as a once-per-second synthetic health signal via a sidecar. The old default behavior created misleading 5xx alerts that looked like real service instability.

To keep the demo low-risk in normal operation, `/ping` now returns `200` with `{ "pong": true }` by default. If you still want to demonstrate failure injection, opt in by setting `PING_FAULT_INJECTION=true`; with that environment variable enabled, `/ping` restores the prior behavior of throwing an `unknown internal error` roughly one third of the time.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5. This was actually a one-shot (you can verify in the PR history of the repo).
