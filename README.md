# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

`/ping` is the reliable health/test endpoint and returns `200 {"pong": true}` by default. This is safe for the pinger sidecar and monitoring checks.

To deliberately reproduce the legacy alerting demo, set `PING_FAILURE_ENABLED=true` in the application's environment. While enabled, `/ping` returns a 500 with the legacy `unknown internal error` once every three Unix seconds; omit the variable (or use any value other than `true`) to disable this failure injection. Do not enable it on a workload monitored for availability.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).
