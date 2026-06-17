# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

Earlier demo versions intentionally broke the `/ping` endpoint in `app/main.py`.  If log aggregation, and even better, vector indexing of PRs is enabled, you can tie a prometheus or datadog alert directly to a full root cause using Plural AI, and it will even spawn a PR to fix the broken code change.

This repository now keeps `/ping` healthy so the service can be used as a stable demo application without intentional 500s.

