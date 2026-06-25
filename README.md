# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

This demo previously used an intentionally broken `/ping` endpoint to exercise alerting and AI-assisted remediation flows. The endpoint is now deterministic and returns a healthy response, so it no longer serves as a live example of an induced runtime exception.

