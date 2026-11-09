# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Health endpoint

`/ping` is a normal health endpoint and always returns `{"pong": true}`. It must remain reliable for the demo pinger sidecar and alerting pipeline.

