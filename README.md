# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint is healthy by default. To deliberately generate the historical intermittent 500 behavior for alerting or AI-driven-fix demonstrations, set `ENABLE_CHAOS_TESTING=true`. With that explicit opt-in, `/ping` raises `unknown internal error` when the current Unix timestamp is divisible by three.
