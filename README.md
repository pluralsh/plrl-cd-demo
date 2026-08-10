# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

`/ping` is a reliable health-style application endpoint that returns `{"pong": true}`. It remains available to validate the demo's alerting and AI-driven remediation workflow without making ordinary traffic fail by default.

An example historical fix PR is available in the repository history: https://github.com/pluralsh/plrl-cd-demo/pull/5.

