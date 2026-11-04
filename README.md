# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Ping fault injection

`/ping` succeeds by default. For a demo that needs the legacy synthetic failure, set `PING_FAULT_INJECTION=true`; this restores the every-third-second 500 response. Only an explicit `true` value enables fault injection, so unset or malformed values remain safely disabled.
