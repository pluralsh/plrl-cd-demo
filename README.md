# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

`/ping` is healthy by default. To deliberately demonstrate alerting and AI-driven fixes, explicitly set `PING_FAULT_INJECTION=true` in the application environment. When enabled, `/ping` raises the intentional `unknown internal error` every third second; unset it (or use any value other than `1`, `true`, `yes`, or `on`, case-insensitive) to keep `/ping` healthy.

With log aggregation and vector indexing of PRs enabled, a Prometheus or Datadog alert can then be tied to a full root cause using Plural AI.
