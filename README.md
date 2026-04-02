# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

Within `app/main.py` we've created a deliberately broken endpoint `/ping` for chaos testing. The chaos behavior is now **configurable** and **disabled by default** to prevent alert noise in production.

### Chaos Configuration

The `/ping` endpoint's chaos/failure injection is controlled by the `CHAOS_ENABLED` environment variable:

| Value | Behavior |
|-------|----------|
| `false`, `0`, `no`, unset (default) | `/ping` always returns 200 OK |
| `true`, `1`, `yes`, `on` | `/ping` randomly returns 500 errors (~33% of requests) |

**Note:** Values are case-insensitive and whitespace is trimmed.

### Helm Configuration

To enable chaos testing via Helm, set `chaos.enabled` in your values:

```yaml
chaos:
  enabled: true  # Default: false
```

Or via command line:
```bash
helm install my-release ./helm --set chaos.enabled=true
```

### Use Case

If log aggregation and vector indexing of PRs is enabled, you can tie a prometheus or datadog alert directly to a full root cause using Plural AI, and it will even spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5. This was actually a one-shot (you can verify in the PR history of the repo).

