# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

`/ping` is the reliable health endpoint and always returns `{"pong": true}`. For alerting and AI-driven RCA demonstrations, `/test-error` retains the former time-based error-injection behavior: it deliberately raises an internal error when the current Unix timestamp is divisible by three. Use `/test-error` for that fixture rather than probing `/ping`.

This changes the former fixture contract for `/ping`: callers now receive a consistent successful health response. Any test or alerting integration that depended on synthetic `/ping` failures must call `/test-error` instead.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).

