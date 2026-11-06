# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

`/ping` succeeds by default. To deliberately simulate a `/ping` 500 for alerting demos or tests, set `PING_FAULT_INJECTION=true`. This setting is an exact opt-in: any other value (or an unset variable) keeps `/ping` healthy.

