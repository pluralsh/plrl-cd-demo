# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Health and error testing

`/ping` is a reliable health endpoint and always returns `{"pong": true}`. Do not use it to simulate failures.

For explicit test-only error simulation, `GET /test/error` returns a 500 response with `unknown internal error`.
