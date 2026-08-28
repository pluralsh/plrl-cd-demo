# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint is healthy by default. To deliberately demonstrate periodic failures for alerting and AI-driven fixes, set `PING_FAULT_INJECTION_EVERY_N_REQUESTS` to a positive integer (for example, `3`). This enables a 500 response on every Nth `/ping` request in each application process; the request count is synchronized within that process but is not shared across replicas. Leave the variable unset (or set it to `0`) to disable fault injection.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).
