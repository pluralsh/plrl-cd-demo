# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint supports configurable failure injection for chaos testing and AI-driven alerting demos. By default, `/ping` returns a stable `200 OK` response.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PING_FAIL_ENABLED` | `false` | Set to `true` to enable intentional 500 errors on `/ping` |
| `PING_FAIL_RATE` | `33` | Failure rate as percentage (0-100). Only applies when `PING_FAIL_ENABLED=true` |

### Usage Examples

**Stable mode (default):**
```bash
# /ping always returns 200 OK
curl http://localhost/ping
# {"pong": true, "status": "ok"}
```

**Enable failure injection for demo/testing:**
```bash
# Enable failures with default 33% rate
export PING_FAIL_ENABLED=true

# Or customize the failure rate (e.g., 50%)
export PING_FAIL_ENABLED=true
export PING_FAIL_RATE=50
```

**Helm deployment:**
```yaml
# In values.yaml or via --set
env:
  - name: PING_FAIL_ENABLED
    value: "true"
  - name: PING_FAIL_RATE
    value: "50"
```

### AI-Driven Fixes Demo

If log aggregation, and even better, vector indexing of PRs is enabled, you can tie a prometheus or datadog alert directly to a full root cause using Plural AI, and it will even spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5. This was actually a one-shot (you can verify in the PR history of the repo).

