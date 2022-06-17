<!-- Copyright Yahoo. Licensed under the terms of the Apache 2.0 license. See LICENSE in the project root.-->
![Vespa Cloud logo](https://cloud.vespa.ai/assets/logos/vespa-cloud-logo-full-black.png)

# Managed Vector Search using Vespa Cloud

## Create your tenant in the Vespa Cloud

If you don't already have a Vespa Cloud tenant, 
create one at [console.vespa-cloud.com](https://console.vespa-cloud.com/). 
Onboarding the Vespa Cloud requires a Google or GitHub account. 
Onboarding Vespa Cloud will start your [free trial](https://cloud.vespa.ai/pricing#free-trial) period, 
no credit card required. 

## Clone this repo 
```sh
git clone --depth 1 https://github.com/vespa-cloud/vector-search.git && cd vector-search
```

## Install Vespa-CLI
Install the [Vespa-CLI](https://docs.vespa.ai/en/vespa-cli.html) which is the official command-line
client for interacting with Vespa:

```sh
brew install vespa-cli 
```

You can also download [Vespa CLI](https://github.com/vespa-engine/vespa/releases) 
for Windows, Linux and macOS.

## Configure Vespa-CLI 
Replace `<tenant-name>` with your Vespa Cloud tenant name. 
In this case, the application name used is `vector-search` and instance is `default`:

```sh
vespa config set target cloud && \
 vespa config set --local application <tenant-name>.vector-search.default
```

## Security

Authorize access to Vespa Cloud control plane: 
```sh
vespa auth login
```

Create a self-signed certificate for data plane (read and write) access:
```sh
vespa auth cert
```

Read more about how Vespa Cloud keeps your data safe and private at rest and in transit 
in the [Vespa Cloud Security Guide](https://cloud.vespa.ai/en/security/guide).

## Configure Vector Schema 
Now the app is ready to be deployed. The [vector schema](schemas/vector.sd)
is configured with `768` dimensions using `float` precision. 

The [vector schema](schemas/vector.sd) could be changed before deploying 
to match your vector data:

* Change vector dimensionality (Default `768`)
* Change vector precision type (Default `float`) - Choose between `int8`, `bfloat16` or `float`.
* Change [distance-metric](https://docs.vespa.ai/en/reference/schema-reference.html#distance-metric) 
(Default `euclidean`) - Also supported `angular`, `innerproduct` and `hamming`.


## Deploy to dev environment 
Vespa Cloud supports multiple different [environments](https://cloud.vespa.ai/en/reference/environments).
The following guides you through:
* Deploying to `dev` for developing and testing of your vector search use case
* Deploying to `perf` for performance validation and benchmarking
* Deploying to `prod` for high availability production serving

Dev zone is where development happens, resources are downscaled to nodes with 2 v-cpu, 8GB of RAM and 50 GB of disk.
A single node `dev` deployment can index up to about 1M 768 dimensional vectors. 

Deploy app to `dev`:
```sh
vespa deploy  
```

The first deployment to dev environment takes about 12 minutes for provisioning resources and 
setting up certificates. 

## Deploy to perf environment

The perf zone is used for [benchmarking](https://cloud.vespa.ai/en/benchmarking) and performance testing. 
It uses the same resource specification as in production, except
for redundancy. 

Deploy app to `perf` by using the `--zone` parameter:

```sh
vespa deploy --zone perf.aws-us-east-1c
```


## Deploy to production environment

This submits the application to production via [automated deployment](https://cloud.vespa.ai/en/automated-deployments) 
pipeline which executes:

* System test [tests/system-test/feed-and-search-test.json](tests/system-test/feed-and-search-test.json)
* Staging setup test [tests/staging-setup/staging-feed-before-upgrade.json](tests/staging-setup/staging-feed-before-upgrade.json)
* Staging test [tests/staging-test/staging-after-upgrade.json](tests/staging-test/staging-after-upgrade.json)

The above tests also demonstrates query and feed usage. 

Deploying to production require choosing which production region the app should be
deployed to. The `deployment.xml` in this sample app uses [aws-us-east-1c](deployment.xml).

For high availability and low network latency, consider using multiple regions. Vespa Cloud
supports global query traffic routing so that query requests are served by the region which is
closest to the client. See [deployment.xml global endpoints](https://cloud.vespa.ai/en/reference/deployment#endpoints).

Currently available Vespa Cloud production zones is 
listed in [zones](https://cloud.vespa.ai/en/reference/zones.html). 
Request for new regions can be made by sending an email to [support@vespa.ai](mailto:support@vespa.ai).

The following deploys the application to the production regions specified in [deployment.xml](deployment.xml):
```sh
vespa prod submit 
```

We recommend deploying using CI/CD, for example deploying to Vespa Cloud using GitHub Actions.  

## Vespa Cloud - Vector Search Price Examples

[Vespa Cloud pricing](https://cloud.vespa.ai/pricing) is simple and transparent. 
All customers receive all features and services, and is charged a fee proportional to the resources the application uses. 

The production env configuration in [services.xml](services.xml) specifies the following resources:
```xml
<nodes deploy:environment="prod" count="2" groups="2">
      <resources memory="32GB" vcpu="8" disk="300GB" storage-type="local" />
</nodes>
```

Above specifies a redundant high availability deployment 
using [grouped data distribution](https://docs.vespa.ai/en/performance/sizing-search.html ) with
one node per group and 2 groups for redundancy.   

| Vectors | Dimensionality | Precision Type | Queries per second | Writes per second | Estimated cost per month (720 hours) |
|---------|----------------|----------------|--------------------|-------------------|--------------------------------------|
| 5M      | 768            | float          | 2000               | 1000              | $ 1,581                              |
| 5M      | 768            | float          | 6000               | 1000              | $ 3,162                              |
| 10M     | 384            | float          | 2000               | 1000              | $ 1,581                              |
| 20M     | 384            | bfloat16       | 1500               | 750               | $ 1,581                              |

Lower number of vector dimensions and lower precision type (e.g, `bfloat16` instead of `float`), 
increases number of vectors which can be indexed per node (memory resource limits). Supported queries per second and
writes per second depends on [vector search parameters](https://docs.vespa.ai/en/approximate-nn-hnsw.html).

Vespa Cloud sizing experts can assist in finding the most cost efficient resource specification matching your vector search 
use case. Sizing and cost estimation uses samples of your data using the `perf` environment. 

Vespa Cloud also supports [auto-scaling](https://cloud.vespa.ai/en/autoscaling), in this example scaling 
number of groups (replicas) to handle query traffic changes.

```xml
<nodes deploy:environment="prod" count="[2,4]" groups="[2,4]">
      <resources memory="512GB" vcpu="64" disk="2400GB" storage-type="local" />
</nodes>
```


## Using Vespa Vector Search 

Documentation:

* [Practical nearest neighbor search guide](https://docs.vespa.ai/en/nearest-neighbor-search-guide.html)
* [Nearest neighbor search](https://docs.vespa.ai/en/nearest-neighbor-search.html)
* [Approximate nearest neighbor search](https://docs.vespa.ai/en/approximate-nn-hnsw.html)

Blog posts: 

* [Billion-scale vector search with Vespa - part one](https://blog.vespa.ai/billion-scale-knn/)
* [Billion-scale vector search with Vespa - part two](https://blog.vespa.ai/billion-scale-knn-part-two/)
* [Query Time Constrained Approximate Nearest Neighbor Search](https://blog.vespa.ai/constrained-approximate-nearest-neighbor-search/)

Use Cases using Vespa Vector Search 

* [State-of-the-art text ranking](https://github.com/vespa-engine/sample-apps/blob/master/msmarco-ranking/passage-ranking.md)
* [State-of-the-art image search](https://github.com/vespa-engine/sample-apps/tree/master/text-image-search)
* [State-of-the-art open domain question answering](https://github.com/vespa-engine/sample-apps/tree/master/dense-passage-retrieval-with-ann)
* [Spotify using Vespa vector search](https://engineering.atspotify.com/2022/03/introducing-natural-language-search-for-podcast-episodes/)
