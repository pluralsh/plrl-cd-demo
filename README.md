# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Environment Variables

The application supports the following environment variables for fault injection testing:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `FAULT_INJECT_RATE` | Float (0-1) | `0.0` | Rate at which faults are injected (0 = never, 1 = always). Values outside [0,1] are clamped. |
| `FAULT_INJECT_PING` | Boolean | `true` | Enable/disable fault injection on `/ping` endpoint. Accepts: `true/false`, `1/0`, `yes/no`, `on/off` (case-insensitive). |
| `GIT_COMMIT` | String | - | Git commit SHA (set during Docker build). |
| `ENV` | String | `DEFAULT_ENV` | Environment name. |

**Note:** Invalid environment variable values will not crash the application. A warning will be logged and the default value will be used.


## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Returns git commit and environment info |
| `/ping` | GET | Ping endpoint with optional fault injection |
| `/hello` | GET | Returns `{"hello": "world!"}` |
| `/world` | GET | Returns `{"world": "hello!"}` |
| `/healthz` | GET | Health check endpoint (see below) |

### Health Check Endpoint (`/healthz`)

The `/healthz` endpoint returns a JSON response with the current application health status and configuration:

```json
{
  "status": "ok",
  "faultInjection": {
    "rate": 0.0,
    "ping": true
  },
  "uptimeSeconds": 123.45
}
```

This endpoint is useful for:
- Kubernetes liveness/readiness probes
- Monitoring fault injection configuration
- Verifying application uptime


## Alerting and AI Driven fixes

Within `app/main.py` we've created a deliberately configurable fault injection on the `/ping` endpoint. If log aggregation, and even better, vector indexing of PRs is enabled, you can tie a prometheus or datadog alert directly to a full root cause using Plural AI, and it will even spawn a PR to fix the broken code change.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).

