# Plural CD Demo Application

This is a simple demo microservice which can be managed by Plural. It builds one Docker image, published to `ghcr.io/pluralsh/plrl-cd-test`, and exposes a small FastAPI and Prometheus metrics endpoint.

## `/ping` failure fixture

`/ping` is reliable by default and returns `{"pong": true}`. Its former periodic 500 response is preserved only as an explicitly enabled alerting/test fixture:

```yaml
env:
  - name: PING_FAILURE_INJECTION
    value: "true"
```

With `PING_FAILURE_INJECTION=true`, `/ping` raises `Exception("unknown internal error")` when the current epoch second is divisible by three. Any other value, including an unset variable or `false`, disables injection. Do not set this variable in production.

### demo-prod rollout

This repository does not contain a demo-prod Flow or `flow-test/stateless` deployment manifest, so there is no demo-prod-specific GitOps file to change here. After CI publishes an immutable image for the merge commit, a follow-up deployment PR must update the external demo-prod `flow-test/stateless` image from `ghcr.io/pluralsh/plrl-cd-test:0.1.2` to that published immutable tag. Leave `PING_FAILURE_INJECTION` unset (or set it explicitly to `"false"`); no production failure-fixture override is required for the new default.

## Build and release

`.github/workflows/push.yaml` runs `pytest` for pull requests, `main` pushes, and version tags. It then builds the root `Dockerfile` for `linux/amd64` and `linux/arm64` and pushes `ghcr.io/pluralsh/plrl-cd-test`. Pushing a `vX.Y.Z` tag publishes the corresponding semver image tag `X.Y.Z`; for example, the incident image tag `0.1.2` is produced by the `v0.1.2` release tag. The `release` recipe in `Justfile` creates and pushes those version tags.
