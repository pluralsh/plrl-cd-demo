# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

Within `app/main.py` we've created a `/ping` endpoint with optional chaos behavior for testing and demonstration purposes. By default, the endpoint returns a stable 200 response. To enable intermittent failures (approximately 33% of requests), set the `ENABLE_PING_CHAOS` environment variable to `true`.

**Configuration:**
- `ENABLE_PING_CHAOS=false` (default): `/ping` always returns 200 OK (production-safe)
- `ENABLE_PING_CHAOS=true`: `/ping` raises an exception ~33% of the time (demo/testing only)

This chaos mode can be used to demonstrate alert-driven workflows. If log aggregation, and even better, vector indexing of PRs is enabled, you can tie a prometheus or datadog alert directly to a full root cause using Plural AI, and it will even spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).

**Helm Configuration:**
To enable chaos mode in your helm deployment, set the environment variable in `values.yaml`:
```yaml
env:
  ENABLE_PING_CHAOS: "true"
```

