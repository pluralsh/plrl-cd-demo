# Plural CD Demo Application

This is a simple demo microservice that can be managed by Plural. It builds a single Docker image, published to `ghcr.io/pluralsh/plrl-cd-test`, and exposes a small FastAPI API and Prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or by any other means you'd want to test against.

## Alerting and AI Driven Fixes

The `/ping` endpoint normally returns `200 {"pong": true}`. Its deterministic one-in-three failure is retained solely as an opt-in alerting and AI-fix demonstration.

Enable the fault only for a designated demo or non-production deployment by setting:

```sh
PING_FAULT_INJECTION_ENABLED=true
```

The conventional truthy values `1`, `true`, `yes`, and `on` (case-insensitive) enable it. With the flag enabled, `/ping` returns HTTP 500 with a diagnostic response once every three epoch seconds. Production deployments should leave this variable unset or set it to `false`; absent, false, and malformed values do not inject faults.

If log aggregation, and even better vector indexing of PRs, is enabled, you can tie a Prometheus or Datadog alert directly to a full root cause using Plural AI, and it can spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5. This was actually a one-shot (you can verify in the PR history of the repo).
