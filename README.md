[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7031472&assignment_repo_type=AssignmentRepo)
# tprj
Term Project repo


## Deploy to AWS [here](https://scp756-221.github.io/course-site/#/a4/page?embedded=true&hidegitlink=true)
### Generate the templates
```
> make -f k8s-tpl.mak templates
```

### Start cloud cluster
```
/home/k8s# make -f eks.mak start
```

### Setup kubeconfig
```
/home/k8s# kubectl config use-context aws756
/home/k8s# kubectl create ns c756ns
/home/k8s# kubectl config set-context aws756 --namespace=c756ns
/home/k8s# make -f eks.mak cd

```

### Installing the service mesh istio
```
/home/k8s# kubectl config use-context aws756
/home/k8s# istioctl install -y --set profile=demo --set hub=gcr.io/istio-release
/home/k8s# kubectl label namespace c756ns istio-injection=enabled
```

```
/home/k8s# kubectl get svc --all-namespaces | cut -c -140
```

```
/home/k8s# kubectl -n istio-system get service istio-ingressgateway | cut -c -140
```

### Building images
```
/home/k8s# make -f k8s.mak cri
```

### Deploying the services
```
/home/k8s# make -f k8s.mak gw db s2 s3
```

### Check service logs
```
/home/k8s# kubectl logs --selector app=cmpt756s2 --container cmpt756s2 --tail=-1
/home/k8s# kubectl logs --selector app=cmpt756s3 --container cmpt756s3 --tail=-1
```

Testing URL: `http://<PUBLIC_IP>/api/v1/playlist/health`

### Run CI test locally
```
# update ci/v1.1/compose.yaml
$ make -f k8s-tpl.mak templates

/home/k8s# cd ci
/home/k8s# ./runci-local.sh v1.1
```