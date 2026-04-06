# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Endpoints

### `/ping` - Health Check
A stable health check endpoint that always returns HTTP 200. Use this for:
- Kubernetes liveness and readiness probes
- Load balancer health checks
- Monitoring and alerting

Example response:
```json
{"ok": true}
```

### `/ping-chaos` - Demo Chaos Endpoint
An intentionally unstable endpoint for demonstrating chaos engineering and AI-driven fixes. This endpoint will intermittently return 500 errors based on the `CHAOS_ENABLED` environment variable.

**Configuration:**
- `CHAOS_ENABLED=true` (default): Endpoint will fail ~33% of the time with 500 errors
- `CHAOS_ENABLED=false`: Endpoint behaves like `/ping` and always returns 200

Example response (when successful):
```json
{"ok": true, "chaos": true}
```

**Use cases:**
- Demonstrating AI-driven root cause analysis and automated fixes
- Testing alert configurations and escalation policies
- Chaos engineering experiments

## Alerting and AI Driven fixes

This service demonstrates Plural's AI-driven incident response capabilities. The `/ping-chaos` endpoint is deliberately unstable when `CHAOS_ENABLED=true`. If log aggregation and vector indexing of PRs are enabled, you can tie a Prometheus or Datadog alert directly to a full root cause analysis using Plural AI, which can even spawn a PR to fix broken code.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5. This was actually a one-shot (you can verify in the PR history of the repo).

**Note:** The `/ping` endpoint has been fixed to always return 200 OK to prevent production alerts from firing on the health check endpoint.

