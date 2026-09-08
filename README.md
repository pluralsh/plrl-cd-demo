# Plural CD Demo Application

This is a simple FastAPI demo microservice that can be managed by Plural. It builds a single Docker image, published to `ghcr.io/pluralsh/plrl-cd-test`, and exposes a small API and Prometheus metrics.

It can be deployed within the context of a Plural Flow, or by any other means you want to test.

## Alerting and AI-driven fixes

`/ping` is safe to use for normal traffic and health monitoring: by default it always responds with `200 {"pong": true}`.

To deliberately exercise an HTTP 500 alert, explicitly set the `PING_FAULT_INJECTION` environment variable to `true` on the application container. While enabled, every `/ping` request raises `Exception("unknown internal error")` and returns 500. Leave this variable unset (the default) for normal deployments.

An example AI-generated fix PR is available at https://github.com/pluralsh/plrl-cd-demo/pull/5.
