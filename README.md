<!-- Copyright Yahoo. Licensed under the terms of the Apache 2.0 license. See LICENSE in the project root.-->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://vespa.ai/assets/vespa-ai-logo-heather.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://vespa.ai/assets/vespa-ai-logo-rock.svg">
  <img alt="#Vespa" width="200" src="https://vespa.ai/assets/vespa-ai-logo-rock.svg" style="margin-bottom: 25px;">
</picture>

# Managed Vector Search using Vespa Cloud

There is a growing interest in AI-powered vector representations of unstructured multimodal data and searching efficiently over these representations. This repository describes how your organization can unlock the full potential of multimodal AI-powered vector representations using Vespa Cloud -- the industry-leading managed Vector Search Service. 

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
client for interacting with Vespa. Vespa-CLI works with both Vespa Cloud and self-serve on-premise Vespa deployments. 

```sh
brew install vespa-cli
```

You can also download [Vespa CLI](https://github.com/vespa-engine/vespa/releases) 
binaries for Windows, Linux and macOS.

## Configure Vespa-CLI 
Replace `<tenant-name>` with your Vespa Cloud tenant name. 
In this case, the application name used is `vector-search` and instance is `default`:

```sh
vespa config set target cloud && \
vespa config set --local application <tenant-name>.vector-search.default
```

## Security

Authorize access to the Vespa Cloud control plane: 
```sh
vespa auth login
```

Create a self-signed certificate for data plane (read and write) endpoint access:
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

* Change vector dimensionality (default `768`).
* Change vector [precision type](https://docs.vespa.ai/en/reference/tensor.html#tensor-type-spec)
  (default `float`) - choose between `int8`, `bfloat16`, `float` or `double`.
* Change [distance-metric](https://docs.vespa.ai/en/reference/schema-reference.html#distance-metric)
  (default `angular` useful for models trained with *cosine* similarity) -
  also supported `euclidean`, `innerproduct` and `hamming`.

Note that this sample application ships with CI/CD tests for production deployment that uses 768 dimensions. Changing
the schema requires changes of the CI/CD tests.

## Deploy to dev environment 
Vespa Cloud supports multiple different [environments](https://cloud.vespa.ai/en/reference/environments).
The following guides you through:
* Deploying to `dev` for developing and testing of your vector search use case
* Deploying to `perf` for performance validation and benchmarking
* Deploying to `prod` for high availability production serving

Vespa Cloud dev zone is where development happens, resources are downscaled to nodes with 2 v-cpu, 8GB of RAM and 50 GB of disk.
A single content node `dev` deployment can index about 1M 768 dimensional vectors. 

Deploy app to `dev`:
```sh
vespa deploy
```

The very first deployment to dev environment takes about 12 minutes for provisioning resources and 
signing endpoint certificates. Later deployments takes less than a minute. 

## Deploy to perf environment

The perf zone is used for [benchmarking](https://cloud.vespa.ai/en/benchmarking) and performance testing. 
It uses the same resource specification as in production, except
for redundancy. 

Deploy app to `perf` by using the `--zone` parameter:

```sh
vespa deploy --zone perf.aws-us-east-1c
```

## Deploy to production environment

This deploys the application to production via [automated deployment](https://cloud.vespa.ai/en/automated-deployments) 
pipeline which executes:

* System test [tests/system-test/feed-and-search-test.json](tests/system-test/feed-and-search-test.json)
* Staging setup test [tests/staging-setup/staging-feed-before-upgrade.json](tests/staging-setup/staging-feed-before-upgrade.json)
* Staging test [tests/staging-test/staging-after-upgrade.json](tests/staging-test/staging-after-upgrade.json)

The above tests also demonstrates Vespa vector search query and feed usage. 

Deploying to production require choosing which [production regions](https://cloud.vespa.ai/en/reference/zones.html) 
the app should be deployed to. The `deployment.xml` in this sample app uses [aws-us-east-1c](deployment.xml).

For high availability and low network latency, consider using multiple regions. Vespa Cloud
supports global query traffic routing so that query requests are served by the region which is
closest to the client. See [deployment.xml global endpoints](https://cloud.vespa.ai/en/reference/deployment#endpoints).

Currently available Vespa Cloud production zones is 
listed in [zones](https://cloud.vespa.ai/en/reference/zones.html). 
Request for new regions can be made by sending an email to [support@vespa.ai](mailto:support@vespa.ai).

The following deploys the application to the production regions specified in [deployment.xml](deployment.xml):
```sh
vespa prod deploy
```

Refer to [Production Deployment](https://cloud.vespa.ai/en/production-deployment)
to deploy to the production environment with CI/CD.


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

| Vectors | Dimensionality | Precision Type | Queries per second | Writes per second | Estimated cost per hour ($)         |
|---------|----------------|----------------|--------------------|-------------------|-------------------------------------|
| 5M      | 768            | float          | 2000               | 1000              | $ 3.36                              |
| 5M      | 768            | float          | 6000               | 1000              | $ 10.08                             |
| 10M     | 384            | float          | 2000               | 1000              | $ 3.36                              |
| 20M     | 384            | bfloat16       | 1500               | 750               | $ 3.36                              |

Lower number of vector dimensions and lower precision type (e.g, `bfloat16` instead of `float`), 
increases number of vectors which can be indexed per node (memory resource limits). Supported queries per second and
writes per second depends on [vector search parameters](https://docs.vespa.ai/en/approximate-nn-hnsw.html). 

Vespa Cloud sizing experts can assist in finding the most cost efficient resource specification matching your vector search 
use case. Sizing and cost estimation uses samples of your data in the `perf` environment. 

Vespa Cloud also supports [auto-scaling](https://cloud.vespa.ai/en/autoscaling) which lowers the cost of deployment
as resources can be scaled with query volume changes throughout the week. 

## Vespa Cloud endpoint testing
In the [security](#security) section above,
the `vespa auth cert` command downloads data-plane credentials:

```sh
vespa auth cert
Success: Certificate written to security/clients.pem
Success: Certificate written to ~/.vespa/<tenant-name>.vector-search.default/data-plane-public-cert.pem
Success: Private key written to ~/.vespa/<tenant-name>.vector-search.default/data-plane-private-key.pem
```

This is the certificate/key-pair used when feeding and querying documents.
The endpoint is found in the console and used in the commands below.

Before feeding or running queries, one can easily check the endpoint:

```sh
curl --verbose \
  --cert ~/.vespa/<tenant-name>.vector-search.default/data-plane-public-cert.pem \
  --key ~/.vespa/<tenant-name>.vector-search.default/data-plane-private-key.pem \
  https://vector-search.<tenant-name>.aws-us-east-1c.dev.z.vespa-app.cloud/
```

Expect a 200 OK with output like:

```json
{
  "handlers" : [ {
    "id" : "com.yahoo.container.usability.BindingsOverviewHandler",
    "class" : "com.yahoo.container.usability.BindingsOverviewHandler",
    "bundle" : "container-disc:8.89.6",
    "serverBindings" : [ "http://*/" ]
  } ...
```

Or simply use the vespa cli:  
```sh
vespa status query 
```

```sh
Container (query API) at https://vector-search.<tenant-name>.aws-us-east-1c.dev.z.vespa-app.cloud/ is ready
```


## Feeding example
[feed.py](feed.py) is a script to generate test documents based on the [schema](schemas/vector.sd).
Use this as a template for feeding your own vector data.
Example feed using `feed.py` to generate 20K test vectors with 768 dimensions:

```
vespa feed <(python3 feed.py 20000 768)
```


## Query examples 

Test the query API by querying for all documents - examples:

### Using the Vespa CLI
```sh
vespa query 'yql=select * from vectors where true' \
'ranking=unranked' \
'hits=1'
```
Using the configured `all` [document-summary](https://docs.vespa.ai/en/document-summaries.html),
which also returns the `vector` data, this is slower as more data is returned:

```sh
vespa query 'yql=select * from vectors where true' \
'ranking=unranked' \
'hits=1' \
'summary=all'
```

Same query, but with [different rendering](https://docs.vespa.ai/en/reference/query-api-reference.html#presentation) 
of the `vector` tensor field:

```sh
vespa query 'yql=select * from vectors where true' \
'ranking=unranked' \
'hits=1' \
'summary=all' \
'presentation.format.tensors=short-value'
```
Use `vespa query -v` to print the `curl` equivalent.

### Using HTTP GET 
Using GET, the request parameters must be url encoded. Here space is replaced with `+`:

```sh
curl \
 --cert ~/.vespa/<tenant-name>.vector-search.default/data-plane-public-cert.pem \
 --key ~/.vespa/<tenant-name>.vector-search.default/data-plane-private-key.pem \
 https://vector-search.<tenant-name>.aws-us-east-1c.dev.z.vespa-app.cloud/search/?yql=select+*+from+vector+where+true
```
### Using HTTP POST 
```sh
 curl \
 --cert ~/.vespa/<tenant-name>.vector-search.default/data-plane-public-cert.pem \
 --key ~/.vespa/<tenant-name>.vector-search.default/data-plane-private-key.pem \
 --json '
  {
   "yql": "select * from vectors where true",
   "ranking": "unranked",
   "hits":1
  }' \
  https://vector-search.<tenant-name>.aws-us-east-1c.dev.z.vespa-app.cloud/search/
```

Using `POST` is recommended for large request payloads. 

### Nearest neighbor queries
Approximate nearest neighbor search search, asking for ten nearest neighbors `{targetHits:10}`:
```sh
query=$(cat query-vector.json) && \
curl \
 --cert ~/.vespa/<tenant-name>.vector-search.default/data-plane-public-cert.pem \
 --key ~/.vespa/<tenant-name>.vector-search.default/data-plane-private-key.pem \
 --json "
  {
   'yql': 'select * from vectors where {targetHits:10}nearestNeighbor(vector, q)',
   'input.query(q)': '$query' 
  }" \
 https://vector-search.<tenant-name>.aws-us-east-1c.dev.z.vespa-app.cloud/search/
 ```

Exact nearest neighbor search search, asking for ten nearest neighbors:
```sh
query=$(cat query-vector.json) && \
curl \
 --cert ~/.vespa/<tenant-name>.vector-search.default/data-plane-public-cert.pem \
 --key ~/.vespa/<tenant-name>.vector-search.default/data-plane-private-key.pem \
 --json "
  {
   'yql': 'select * from vectors where {targetHits:10,approximate:false}nearestNeighbor(vector, q)',
   'input.query(q)': '$query' 
  }" \
 https://vector-search.<tenant-name>.aws-us-east-1c.dev.z.vespa-app.cloud/search/
 ```

Approximate nearest neighbor search combined with a filter on tags: 
```sh
query=$(cat query-vector.json) && \
curl \
 --cert ~/.vespa/<tenant-name>.vector-search.default/data-plane-public-cert.pem \
 --key ~/.vespa/<tenant-name>.vector-search.default/data-plane-private-key.pem \
 --json "
  {
   'yql': 'select * from vectors where {targetHits:10}nearestNeighbor(vector, q) and tags contains \"tag1\"',
   'input.query(q)': '$query' 
  }" \
 https://vector-search.<tenant-name>.aws-us-east-1c.dev.z.vespa-app.cloud/search/
 ```

See also [using Vespa Vector Search](#using-vespa-vector-search) for nearest neighbor search queries.

## Visit and exporting the data
Getting the vector data out of Vespa can be equally important as getting the vector data in, especially
when using [native embedders](https://blog.vespa.ai/text-embedding-made-simple/) that embeds text
into vector representation(s). Use the [Vespa visit](https://docs.vespa.ai/en/content/visiting.html)
functionality to export data. 

```sh
vespa visit --field-set vector:vector,id > ../vector-data.jsonl 
```
Will export all documents from the `vector` schema with only the `vector` and `id` field. 
Using `[all]` which exports both both schema and derived fields: 

```sh
vespa visit --field-set "[all]" > ../vector-data.jsonl 
```

Using [document selection](https://docs.vespa.ai/en/reference/document-select-language.html)
to limit what is returned. Note that the Vespa selection is not evaluated using index data structures
and is a linear scan operation. 

```sh
vespa visit --field-set "vector:vector" \
--selection "vector.tags != null" > ../vector-data.jsonl
```

## Documentation resources:

### Documentation 

* [Practical nearest neighbor search guide](https://docs.vespa.ai/en/nearest-neighbor-search-guide.html)
* [Nearest neighbor search](https://docs.vespa.ai/en/nearest-neighbor-search.html)
* [Approximate nearest neighbor search](https://docs.vespa.ai/en/approximate-nn-hnsw.html)

### Blog posts: 
* [Query Time Constrained Approximate Nearest Neighbor Search](https://blog.vespa.ai/constrained-approximate-nearest-neighbor-search/)
* [Billion-scale vector search with Vespa - part one](https://blog.vespa.ai/billion-scale-knn/)
* [Billion-scale vector search with Vespa - part two](https://blog.vespa.ai/billion-scale-knn-part-two/)
* [Billion-scale vector search using hybrid HNSW-IF](https://blog.vespa.ai/vespa-hybrid-billion-scale-vector-search/)


## Use Cases using Vespa Vector Search 

* [State-of-the-art text ranking](https://github.com/vespa-engine/sample-apps/blob/master/msmarco-ranking/passage-ranking.md)
* [State-of-the-art image search](https://github.com/vespa-engine/sample-apps/tree/master/text-image-search)
* [State-of-the-art open domain question answering](https://github.com/vespa-engine/sample-apps/tree/master/dense-passage-retrieval-with-ann)
* [Spotify using Vespa vector search](https://engineering.atspotify.com/2022/03/introducing-natural-language-search-for-podcast-episodes/)
