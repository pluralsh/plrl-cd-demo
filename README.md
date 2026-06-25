# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural. It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.

## Alerting and AI Driven fixes

The app previously shipped with a deliberately broken `/ping` endpoint in `app/main.py` that raised deterministic 500s roughly one third of the time. That behavior was useful for demoing AI-assisted root cause analysis, but it is now disabled by default so normal deployments get a reliable health response.

If you still want to demonstrate the old failure mode intentionally, set `PING_FAULT_INJECTION=true` (or `1`, `yes`, `on`) to opt in to the same time-based `/ping` exceptions.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5. This was actually a one-shot (you can verify in the PR history of the repo).
