## Implementation

### Install HELM (if not done yet)
```
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null

sudo apt-get install apt-transport-https --yes

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list

sudo apt-get update

sudo apt-get install helm

helm version
```

### Get the repository from previous project
- https://github.com/lemberck/mlops/tree/main/05-kubernetes

### Create the Helm Chart
---> A Helm chart is a collection of files that describe a related set of Kubernetes resources. 

`helm create helm-sentiment-analysis-mlops`

> This will create a directory called 'helm-sentiment-analysis-mlops' with the structure needed for a chart.

### Move the manifests to the created chart
- Move `frontend-deployment.yaml` , `backend-deployment.yaml` , `frontend-loadbalancer-service.yaml` and `backend-clusterip-service.yaml` to **helm-sentiment-analysis-mlops/templates/**

### Remove 'namespace' fields from the manifests
When using Helm to manage the deployments, it's better not to hardcode the namespace in the manifest files. 

Helm has a built-in template function to handle namespaces, which allows to dynamically set the namespace during installation or upgrade of the chart.

- Delete the `create-namespace.yaml` (not needed anymore)
- Remove the `namespace` field from the metadata section in the YAML files moved in the previous section.

### Modify the Helm Chart Values
Inside `helm-sentiment-analysis-mlops`, there is a `values.yaml` file. This is where default values can be defined for the templates, which can be overridden during installation if necessary, allowing more flexibility and easy configuration for the chart when deploying into different environments or updates.