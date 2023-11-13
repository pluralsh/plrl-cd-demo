# Plural CD Demo Application

This is meant to be a simple demo of a plural cd application.  It covers a few common usecases:

* Set up a fullstack app with a deployment, service + ingress
* Update app on docker push
* Configure a release pipeline (coming soon!)

Going in order...

## Set up an app with external ingress

You can see the basic kubernetes manifests to make this work in `/kubernetes`.  We used the templated raw template approach since this is relatively trivial but you can also use kustomize or helm to manage your manifests as well (we prefer simplicity though).  It's worth pointing out a few things:

* in `kubernetes/deployment.yaml` we've parameterized the image tag - that will correspond to a service configuration variable
* in `kubernetes/ingress.yaml` we've parameterized the hostname - that will also correspond to a service configuration variable

## Update on Docker Push

To deploy a new image for this service, see the github action in [push.yaml](.github/workflows/push.yaml).  This implements a pretty common process for releasing a build artifact: unit test -> docker build -> deploy.

The first job in the workflow basically just sets up python and runs a trivial pytest for demo purposes.  You'll likely have a much more complex test harness for a more mature application.

The second job in the workflow uses the docker metadata action to generate a set of tags, then buildx to build, tag and push the image to ghcr.  You can see all the built images easily [here](https://github.com/pluralsh/plrl-cd-test/pkgs/container/plrl-cd-test).  We use ghcr for convenience but you can easily leverage any other docker registry, and most cloud's kubernetes distros natively integrate w/ their own registries so it's worth considering them as options.

The final job configures the `plural` cli using the `pluralsh/setup-plural` action then runs `plural cd services update` to reconfigure and redeploy the service.  In particular the syntax is:

```sh
plural cd services update @<cluster-handle>/<service-name> --conf <var>=<value> (...can add more configuration updates as needed)
```

This basically modifies the configuration (in our case for the variable `tag`) against the service, and eventually (usually <1m) its cluster's deploy agent will detect and deploy that change.

## Configure a release pipeline

You can create multiple stages of this service into a single release pipeline using our pipeline system. This allows you to sequentially release your code across dev, staging and production environments, with controlled promotion workflows along the way.  The spec for a pipeline can be seen in [pipeline.yaml](pipeline.yaml).

There are a few things to mention with the pipeline spec.  

First it's a DAG datastructure, the graph vertices are labeled stages, and you can configure edges between any pair of stages where promotions can occur.

Second, the exact details of what happens on promotion is configurable.  By default the subsequent stages will be configured to use the git `sha` of the service upon promotion.  But if you want, you can also have it copy secrets or perform other tasks to move state along the pipeline.  In our case, we're configuring it to copy the docker image tag, stored in the `tag` secret.

Third, stages can have many services.  In our case it's a trivial single service example, but you might have a more complex microservice architecture you'd like to have a single pipeline for and this helps simplify that process.

Once that pipeline has been configured, you'll be able to see promotions flow through on any event that updates the beginning services of the pipeline.