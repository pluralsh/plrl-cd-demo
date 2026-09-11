# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Health endpoint

`GET /ping` is a stable application health endpoint and returns `{"pong": true}` with HTTP 200. It must not be used for default fault injection because it is monitored in Flow deployments.

