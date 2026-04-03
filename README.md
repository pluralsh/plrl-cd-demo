# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

Within `app/main.py` we've created endpoints that can simulate failures for testing alerting and AI-driven fixes.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SIMULATE_FAILURES` | `false` | When set to `true`, enables intentional failure simulation on `/ping` and `/fail` endpoints |

### Endpoints

- **`/ping`** - Health check endpoint. Always returns 200 by default. When `SIMULATE_FAILURES=true`, will fail with 500 error when `time.time() % 3 == 0`.
- **`/fail`** - Dedicated failure simulation endpoint. Returns 200 by default. When `SIMULATE_FAILURES=true`, behaves like `/ping` and can fail deterministically.
- **`/hello`** - Returns `{"hello": "world!"}`
- **`/world`** - Returns `{"world": "hello!"}`
- **`/`** - Returns environment info (commit, env)

### Testing Alert Integration

To test alerting and AI-driven fixes without causing noisy production alerts:

1. Deploy with `SIMULATE_FAILURES=false` (default) for production
2. Set `SIMULATE_FAILURES=true` only in test/staging environments where you want to trigger alerts

This prevents the "Flow 500s" alert from firing in environments where failures are not expected.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).

