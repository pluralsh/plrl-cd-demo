# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural. It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.

## Alerting and AI Driven fixes

This repo previously included a deliberately broken `/ping` endpoint to demonstrate alerting-driven remediation flows. The production `flow-test-stateless` service depends on `/ping` as a continuously polled health endpoint, so `/ping` should now stay healthy and return `200 {"pong": true}` consistently.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5. This was actually a one-shot (you can verify in the PR history of the repo).
