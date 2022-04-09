[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7031472&assignment_repo_type=AssignmentRepo)

# CMPT756 Term Project - Raccoon Fury

This is the project repo for CMPT756, Spring 2022 maintained by team Raccoon Fury.

## Structure

Below is the top-level folder structure of this repo.

```
.
├── ci
├── cluster
├── db
├── gatling
├── loader
├── logs
├── mcli
├── s1
├── s2
├── s3
├── s3li
└── tools
```

- `ci`: files for continuous integration
- `cluster`: files for configuring the cluster
- `db`: the database writer service
- `gatling`: files for `gatling` to simulate load
- `loader`: files to load DynamoDB with fixtures
- `logs`: all the logs generated
- `mcli`: CLI for the music service
- `s1`: the user service
- `s2`: the music service
- `s3`: the playlist service
- `s3li`: ::TODO::
- `tools`: convenient scripts to quick start the services

## Prerequisites

You will need at least the following:
- [docker](https://docs.docker.com/get-docker/)
- [aws-cli](https://github.com/aws/aws-cli)
- [istioctl](https://github.com/istio/istio/blob/master/istioctl)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [helm](https://github.com/helm/helm)

## Deployment

You will need to instantiate `tpl-vars.txt` in the `cluster` directory using the template `tpl-vars-blank.txt`. Make sure the region matches the one in your local profile.

We will cover some useful commands in the next section. A detailed guide for deployment can be found [here](https://scp756-221.github.io/course-site/#/a4/page?embedded=true&hidegitlink=true).

## Useful commands
### Generating the templates
```shell
> make -f k8s-tpl.mak templates
```

### Starting cloud cluster
```shell
/home/k8s# make -f eks.mak start
```

### Setting up`kubeconfig`
```shell
/home/k8s# kubectl config use-context aws756
/home/k8s# kubectl create ns c756ns
/home/k8s# kubectl config set-context aws756 --namespace=c756ns
/home/k8s# make -f eks.mak cd
```

### Installing the service mesh Istio

```shell
/home/k8s# kubectl config use-context aws756
/home/k8s# istioctl install -y --set profile=demo --set hub=gcr.io/istio-release
/home/k8s# kubectl label namespace c756ns istio-injection=enabled
```

You will find a list of services in the namespace by:

```shell
/home/k8s# kubectl get svc --all-namespaces | cut -c -140
```

You can find the external IPs using:

```shell
/home/k8s# kubectl -n istio-system get service istio-ingressgateway | cut -c -140
```

### Building the images
```shell
/home/k8s# make -f k8s.mak cri
```

### Deploying the services
```shell
/home/k8s# make -f k8s.mak gw db s2 s3
```

### Checking service logs
```shell
/home/k8s# kubectl logs --selector app=cmpt756s2 --container cmpt756s2 --tail=-1
/home/k8s# kubectl logs --selector app=cmpt756s3 --container cmpt756s3 --tail=-1
```

The testing URL: `http://<PUBLIC_IP>/api/v1/<SERVICE>/health`

### Running CI test locally
```shell
# update ci/v1/compose.yaml and instantiate the templates again

/home/k8s# cd ci
/home/k8s# ./runci-local.sh v1
```

### Spinning down the EKS cluster
```
make -f eks.mak stop
```

### Configuring K8S autoscaler

#### Creating an autoscaler
```shell
##optional## kubectl delete -n kube-system deployments.apps metrics-server
kubectl apply -f metrics-server.yaml

kubectl set resources deployment cmpt756s1 -c=cmpt756s1 --limits=cpu=100m,memory=64Mi
kubectl set resources deployment cmpt756s2-v2 -c=cmpt756s2 --limits=cpu=100m,memory=64Mi
kubectl set resources deployment cmpt756db -c=cmpt756db --limits=cpu=100m,memory=64Mi

make -f k8s.mak s1 db
tools/s2ver.sh v2

kubectl autoscale deployment cmpt756s1 --min=2 --max=100
kubectl autoscale deployment cmpt756s2-v2 --min=2 --max=100
kubectl autoscale deployment cmpt756db --min=2 --max=100
```

#### Viewing autoscaler
```shell
kubectl get hpa
```

#### Deleting autoscaler
```shell
kubectl delete hpa cmpt756s1 cmpt756s2-v2 cmpt756db
```

### Monitoring using Grafana

Provision your cluster by:

```shell
make -f k8s.mak provision
```

You can find the dashboard URL by calling:

```shell
make -f k8s.mak grafana-url
```

### Simulating load with Gatling

To simulate loads:

```shell
./tools/gatling-n-<SERVICE>.sh <NUM_OF_USERS>
```

To stop Gatling:
```
./tools/kill-gatling.sh
```