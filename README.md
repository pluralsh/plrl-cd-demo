# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

`/ping` is a deterministic health endpoint and returns `{"pong": true}` by default. This makes it suitable for continuous monitoring, including the demo deployment's pinger sidecar.

To intentionally inject the original error behavior for alerting demonstrations, set `PING_FAILURE_INJECTION=true`. With that explicit opt-in setting, `/ping` raises an error every third Unix-epoch second; when unset or set to any other value, it remains successful.
