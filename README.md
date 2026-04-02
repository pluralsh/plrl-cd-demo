# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Endpoints

### `/ping` - Health Check Endpoint

The `/ping` endpoint provides a simple health check that returns `{"pong": true}` with HTTP 200.

**Default behavior:** Always returns HTTP 200 (no failures).

**Chaos mode:** Optionally enable random failures for testing alerting and resilience:

| Environment Variable | Type | Default | Description |
|---------------------|------|---------|-------------|
| `PING_FAIL_RATE` | float | `0.0` | Probability of failure (0.0-1.0). Values outside this range are clamped. Invalid values default to 0.0. |

**Examples:**
- `PING_FAIL_RATE=0.0` - Always succeed (default)
- `PING_FAIL_RATE=0.5` - 50% chance of failure
- `PING_FAIL_RATE=1.0` - Always fail

When a failure is triggered, the endpoint returns HTTP 500 with an informative error message:
```json
{
  "detail": "Chaos mode failure: PING_FAIL_RATE triggered simulated error"
}
```

### Other Endpoints

- `/` - Returns commit info and environment
- `/hello` - Returns `{"hello": "world!"}`
- `/world` - Returns `{"world": "hello!"}`


## Alerting and AI Driven fixes

The `/ping` endpoint with chaos mode enabled can be used to test alerting pipelines. If log aggregation, and even better, vector indexing of PRs is enabled, you can tie a prometheus or datadog alert directly to a full root cause using Plural AI, and it will even spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).

