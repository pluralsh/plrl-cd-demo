# Plural CD Demo Application

This is a simple demo microservice that can be managed by Plural. It builds a single Docker image, published to `ghcr.io/pluralsh/plrl-cd-test`, and exposes a small FastAPI API and Prometheus metrics.

It can be deployed within a Plural Flow or by any other mechanism used for testing.

## `/ping` and synthetic fault injection

`GET /ping` normally returns:

```json
{"pong": true}
```

The endpoint is safe by default. The synthetic fault used for Flow and alerting demonstrations is disabled unless `PING_FAULT_INJECTION=true` is set (the value is parsed case-insensitively). With that explicit opt-in, `/ping` intentionally raises `unknown internal error` during Unix epoch seconds divisible by three, producing a 500 response; it succeeds during all other seconds. This is intended only for synthetic/demo alerting scenarios, not normal deployed availability testing.

The included Helm application chart exposes the same setting as `pingFaultInjection`, which defaults to `false` and renders `PING_FAULT_INJECTION=false`. Enable it only for a demo:

```yaml
pingFaultInjection: true
```

## Alerting and AI-driven fixes

The optional `/ping` fault injection can be used with log aggregation and, ideally, vector indexing of pull requests to connect a Prometheus or Datadog alert to a root cause using Plural AI. It can then spawn a pull request to fix the generated fault.

An example generated fix PR is available at https://github.com/pluralsh/plrl-cd-demo/pull/5. It was a one-shot; this can be verified in the repository pull request history.
