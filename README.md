# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Health and alert demonstrations

`GET /ping` is safe for health checks and synthetic polling. It always returns HTTP 200 with `{"pong": true}`.

For controlled alert demonstrations, call `GET /test/error`. This test/demo-only endpoint intentionally returns HTTP 500 and is excluded from the normal OpenAPI schema.

If log aggregation, and even better, vector indexing of PRs is enabled, you can tie a Prometheus or Datadog alert directly to a full root cause using Plural AI, and it will even spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5. This was actually a one-shot (you can verify in the PR history of the repo).

