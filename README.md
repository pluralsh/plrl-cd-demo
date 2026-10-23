# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

The `/ping` endpoint succeeds by default so it is safe for production health checks. To deliberately demonstrate an alert-to-remediation workflow, set `PING_FAULT_INJECTION` to exactly `true`; this makes every `/ping` request return a synthetic HTTP 500. Any other value, including an unset variable, leaves `/ping` healthy.

An example fix PR we generated is here: https://github.com/pluralsh/plrl-cd-demo/pull/5.  This was actually a one-shot (you can verify in the PR history of the repo).
