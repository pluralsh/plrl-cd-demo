# Plural CD Demo Application

This is meant to be a simple demo microservice which can be managed by Plural.  It builds a single docker image, published to `ghcr.io/pluralsh/plrl-cd-test` and exposes a small flask api and prometheus metrics.

This can then be deployed easily within the context of a Plural Flow, or whatever other means you'd want to test against.


## Alerting and AI Driven fixes

This demo service still exposes `/ping`, but it now returns a stable success response instead of intentionally faulting. If you want to demo alert-driven remediation flows, use a dedicated fault injection change rather than relying on the default `/ping` behavior.

