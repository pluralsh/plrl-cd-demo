# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

Within `app/main.py` we've created a demo fault path for `/ping`. By default `/ping` now returns success consistently, and the old intermittent failure mode is only enabled when `ENABLE_PING_FAULT` is set to `1`, `true`, `yes`, or `on`. If log aggregation, and even better, vector indexing of PRs is enabled, you can still opt into that behavior to tie a prometheus or datadog alert directly to a full root cause using Plural AI, and it will even spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).

