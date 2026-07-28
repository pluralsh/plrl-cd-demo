# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

This demo app previously included intentionally flaky `/ping` logic in `app/main.py` to simulate alert-driven debugging workflows. That demo behavior has been removed so `/ping` stays healthy by default in real environments.

Plural AI workflows can still be demonstrated by introducing and then fixing issues in a controlled environment, without keeping a random 500 in the default app behavior.
