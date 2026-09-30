# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

`/ping` is a reliable health endpoint and returns `200 {"pong": true}` by default. To reproduce the historical one-in-three failure for isolated alerting demonstrations, set `PING_FAILURE_INJECTION=true`; do not enable it in monitored deployments.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).
