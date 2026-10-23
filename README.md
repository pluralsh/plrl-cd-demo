# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Optional fault injection

`GET /ping` is healthy by default and returns `{"pong": true}`. Set
`PING_FAULT_INJECTION=true` only when intentionally demonstrating error alerting;
it makes `/ping` raise an unhandled error and return a 500 response.
