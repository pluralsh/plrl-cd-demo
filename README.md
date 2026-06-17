# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural. It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.

## Alerting and AI Driven fixes

The original `/ping` implementation in `app/main.py` intentionally raised `Exception("unknown internal error")` whenever `int(time.time()) % 3 == 0`, which created synthetic 500s about one-third of the time. That made the endpoint useful for demoing root-cause analysis, but confusing for normal deployments because Kubernetes probes only hit `/`, so pods stay healthy while `/ping` alerts fire.

`/ping` is now healthy by default so the demo app behaves deterministically in normal environments. If you still want to simulate the original flaky behavior for alerting demos, set `ENABLE_FLAKY_PING=true` in the app environment to re-enable the time-based failures explicitly.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5. This was actually a one-shot (you can verify in the PR history of the repo).
