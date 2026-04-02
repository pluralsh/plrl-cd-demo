# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

Within `app/main.py` we've created a `/ping` endpoint that can exhibit chaotic behavior for testing purposes.  If log aggregation, and even better, vector indexing of PRs is enabled, you can tie a prometheus or datadog alert directly to a full root cause using Plural AI, and it will even spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).

## CHAOS_MODE Configuration

The `/ping` endpoint behavior is controlled by the `CHAOS_MODE` environment variable:

| Value | Behavior |
|-------|----------|
| Unset (default) | `/ping` always returns 200 OK with `{"pong": true}` |
| `"false"` or `"0"` | Same as unset - stable, always returns 200 |
| `"true"` or `"1"` | Chaos mode enabled - `/ping` intermittently returns 5xx errors (every ~3 seconds) |

### Helm Configuration

To enable chaos mode in a Helm deployment, set the following in your values:

```yaml
env:
  CHAOS_MODE: "true"
```

By default, `CHAOS_MODE` is set to `"false"` in the Helm chart for stable production deployments.

