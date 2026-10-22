# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small FastAPI service and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Ping health and synthetic faults

`GET /ping` is healthy by default and returns `{"pong": true}`. This is the endpoint used by the demo pinger, so ordinary deployments do not generate intentional 5xx responses.

For a deliberate alerting demonstration only, set `SYNTHETIC_PING_FAILURE=true`. The value is exact and case-sensitive: only `true` makes `/ping` return a 500; the variable being unset or set to any other value keeps it healthy.
