# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

This application was previously configured with a deliberately broken endpoint `/ping` to demonstrate Plural AI's ability to detect issues through log aggregation and prometheus alerts, then automatically generate fix PRs. With log aggregation and vector indexing of PRs enabled, Plural AI can tie a prometheus or datadog alert directly to a full root cause and spawn a PR to fix broken code.

The `/ping` endpoint has now been fixed to return 200 status consistently. Example AI-generated fix PRs can be found in the repository's PR history, including: https://github.com/pluralsh/plrl-cd-demo/pull/5.

