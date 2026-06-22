# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint now returns `{"pong": true}` deterministically by default so continuous health checks do not generate noisy 500s in normal deployments.

For demos or testing, you can still opt into the original intermittent failure behavior by setting `ENABLE_PING_FAULT_INJECTION=true` in the application environment. When that flag is enabled, `/ping` resumes occasionally raising an internal error based on the current time so alerting and automated remediation flows can still be exercised intentionally.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).

