# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## `/ping` fault injection

`GET /ping` returns `{"pong": true}` by default. It does not generate synthetic failures during normal operation.

For controlled fault testing only, set `PING_FAULT_INJECTION=true`. This exact, case-sensitive value makes `/ping` return a 500 response; unset or any other value leaves the endpoint healthy.
