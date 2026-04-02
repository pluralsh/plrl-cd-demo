# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Returns commit and environment info |
| `GET /ping` | Health check endpoint (see Chaos Mode below) |
| `GET /hello` | Returns `{"hello": "world!"}` |
| `GET /world` | Returns `{"world": "hello!"}` |


## Chaos Mode

The `/ping` endpoint supports a chaos mode for testing alerting and failure scenarios.

### Environment Variable

| Variable | Default | Description |
|----------|---------|-------------|
| `CHAOS_MODE` | `false` | When `true`, `/ping` will intermittently return HTTP 500 errors |

**Accepted values for `CHAOS_MODE`:** `true`, `1`, `yes` (case-insensitive) to enable; `false`, `0`, `no` to disable.

### Behavior

- **`CHAOS_MODE=false` (default):** `/ping` always returns HTTP 200 with `{"status": "ok"}`. Safe for production health checks and monitoring.
- **`CHAOS_MODE=true`:** `/ping` intermittently returns HTTP 500 errors (~33% of requests) to simulate failures for chaos testing.

### Helm Configuration

In `values.yaml`:

```yaml
# Enable chaos mode for testing (default: false)
chaosMode: false
```

This sets the `CHAOS_MODE` environment variable in the deployment.

### Enabling Chaos for Testing

To enable chaos mode for testing alerts:

```bash
# Via Helm
helm upgrade my-release ./helm --set chaosMode=true

# Or directly via environment variable
export CHAOS_MODE=true
```

**Warning:** Do not enable chaos mode in production unless intentionally testing failure scenarios and alerting.


## Alerting and AI Driven fixes

The `/ping` endpoint with chaos mode enabled can be used to test AI-driven alerting. If log aggregation and vector indexing of PRs is enabled, you can tie a prometheus or datadog alert directly to a full root cause using Plural AI, and it will even spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).

