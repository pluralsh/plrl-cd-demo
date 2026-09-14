# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural. It builds a single Docker image, published to `ghcr.io/pluralsh/plrl-cd-test`, and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.

## Alerting and AI-driven fixes

`/ping` normally returns `200 {"pong": true}`. Its deterministic one-in-three failure is retained only as an opt-in alerting and AI-fix demonstration.

Enable the failure behavior only for a designated demo or non-production deployment:

```sh
PING_FAULT_INJECTION_ENABLED=true
```

The conventional truthy values `1`, `true`, `yes`, and `on` (case-insensitive) enable it. When enabled, `/ping` returns HTTP 500 with a diagnostic response once every three epoch seconds. Production deployments should leave this variable unset or set it to `false`; absent, false, and unrecognized values do not inject failures.

If log aggregation, and even better vector indexing of PRs, is enabled, you can tie a Prometheus or Datadog alert directly to a full root cause using Plural AI, and it can spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5. This was actually a one-shot (you can verify in the PR history of the repo).
