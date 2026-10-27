# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint succeeds by default. For diagnostic testing only, set `PING_FAULT_INJECTION=true` exactly to make `/ping` return HTTP 500 deterministically. Any other value, including `True`, leaves fault injection disabled.

