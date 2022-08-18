# Pod Chaos Monkey
Deletes a randomly chosen pod from a kubernetes cluster's namespace

## Pre-requisites
* a Kubernetes cluster
  * Alternately install KinD (https://kind.sigs.k8s.io/docs/user/quick-start#installation) and `kind create cluster`
* Helm
  * Install Helm (https://helm.sh/docs/intro/install/)
* A reliable application in **workloads** namespace
  * start a **nginx** deployment with `kubectl -n workloads create deployment nginx --image=nginx --port=80 --replicas=2`

## Installation
* Build image with `docker build -t pod-chaos-monkey:latest .`

* Push it to your registry, or if you're using KinD, load image into the cluster with
`kind load docker-image pod-chaos-monkey:latest`

* Now you're ready to deploy with
`helm upgrade -i pod-chaos-monkey chart/. -f helm-values.yaml`
(change the `.image.repository` value if using a remote registry)

To change helm release values, check the available values [here](./chart/README.md) 

Here's the main application options:

| Key | Type | Default | Description                      |
|-----|------|---------|----------------------------------|
| args.loglevel | string | `"info"` | log verbosity                    |
| args.namespace | string | `"workloads"` | watched namespace                |
| args.sleep | string | `"30"` | sleep time between pod deletions |

# Run tests

* Install **pytest** in your virtualenv with `pip install pytest`
* Run tests with `PYTHONPATH=./app pytest` 