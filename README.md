# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint is now stable by default so it can be used safely for operational health checks. For demo scenarios, the old intermittent failure can still be enabled explicitly by setting `PING_FAULT_INJECTION=true`, which restores the time-based exception behavior.

This keeps the alert investigation demo available without generating constant alert noise in environments that curl `/ping` continuously.

