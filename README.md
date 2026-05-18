# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

Within `app/main.py` we've created a deliberately broken endpoint `/ping` with **configurable failure injection** for demo purposes.

### Demo Failure Behavior

The `/ping` endpoint can be configured to fail ~33% of the time (when `time.time() % 3 == 0`) to demonstrate Plural AI's remediation capabilities. This behavior is:

- **Disabled by default** - `/ping` returns 200 OK in normal operation
- **Configurable via environment variable** - Set `ENABLE_DEMO_FAILURES=true` to enable time-based failures

#### Enabling Demo Failures

To enable the demo failure injection for AI remediation testing:

```bash
# Set the environment variable
export ENABLE_DEMO_FAILURES=true

# Or in Kubernetes/Helm deployment
env:
  - name: ENABLE_DEMO_FAILURES
    value: "true"
```

When enabled, if log aggregation and vector indexing of PRs are configured, you can tie a Prometheus or Datadog alert directly to a full root cause using Plural AI, which can even spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).

