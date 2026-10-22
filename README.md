# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Ping fault injection

`GET /ping` returns `{"pong": true}` by default. To deliberately exercise the synthetic error path in a demo, set `PING_FAULT_INJECTION=true`. Only the case-insensitive value `true` (surrounding whitespace is ignored) enables injection; unset, empty, and all other values leave `/ping` successful. When enabled, the endpoint retains its original intermittent failure behavior (one request in every three seconds).

