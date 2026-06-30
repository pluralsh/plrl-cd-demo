# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint now returns a normal health response by default so the demo service does not intermittently 500 in regular use. If you want to intentionally simulate the historical failure mode for alerting demos, set `PING_FAILURE_INJECTION=true` and `/ping` will raise an internal error whenever `int(time.time()) % 3 == 0`.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).

