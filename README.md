# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## `/ping` behavior

`GET /ping` returns `200 {"pong": true}` by default and is safe for continuous health checking.

For deterministic test-only failure simulation, set `PING_FAULT_INJECTION=true`. With that exact value, every `/ping` request returns HTTP 500 with a synthetic-fault response. Unset or any other value leaves fault injection disabled.
