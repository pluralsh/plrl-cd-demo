# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The app exposes a stable `/ping` endpoint for basic health-style checks. If you want to demo alerting and AI-driven remediation flows, introduce an explicit failure scenario rather than relying on the default `/ping` behavior.

