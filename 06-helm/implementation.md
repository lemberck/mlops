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

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Helm Chart Structure

When initializing a new Helm chart with `helm create <chart-name>`, 
Helm generates a set of default files and directories to provide a template for the application's deployment. 
However, not all files may be needed.

## Default Files and Directories:

### `templates/` Directory
- Contains the YAML templates for the Kubernetes resources.
- **`deployment.yaml`**: Template for creating a deployment. Modify as needed or delete it and use a customized manifest.
- **`service.yaml`**: Template for creating a service. Modify as needed or delete it and use a customized manifest..
- **`serviceaccount.yaml`**: Remove if the application doesn't require a Kubernetes ServiceAccount.
- **`hpa.yaml`**: For a Horizontal Pod Autoscaler, if required to enable automatic scaling. Remove if no autoscaling needed.
- **`ingress.yaml`**: For Ingress resources, if  setting up Ingress for the services. 
    --> An API object that manages external access to the services in a cluster. It provides HTTP routing based on defined rules and can act as a load balancer, SSL termination, and name-based virtual hosting.
### `tests/` Directory
- Contains tests to validate that the chart works as expected after installation.
### `values.yaml`
- Contains the default values for the chart's templates. Update with the application's configuration.
### `Chart.yaml`
- Metadata about the chart, like version, name, and description.
### `NOTES.txt`
- Instructions or information displayed post-installation.
### `_helpers.tpl`
- Template helpers for defining common labels and template functions.

### Development-Specific Files
- Any files prefixed with `dev_` are for development-specific configurations and aren't part of the default structure.

## Managing the Chart:

- **Keep Only What's Needed**: Delete default files that aren't applicable to your application, like `serviceaccount.yaml`, `hpa.yaml`, `ingress.yaml`, unless they're needed.
- **Lint the Chart**: Use `helm lint` to check for issues.
- **Test in Development**: Ensure thr configurations are correct by testing in a dev environment.

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


### Delete unnecessary files for the project form the chart
Ingress (ingress.yaml), Horizontal Pod Autoscaler (hpa.yaml), Connection Tests (test-connection.yaml), Service Account (serviceaccount.yaml), Generic Service Template (service.yaml), Template Helpers (_helpers.tpl).

### Move the manifests to the created chart
- Move `frontend-deployment.yaml` , `backend-deployment.yaml` , `frontend-loadbalancer-service.yaml` and `backend-clusterip-service.yaml` to **helm-sentiment-analysis-mlops/templates/**

### Remove 'namespace' fields from the manifests
When using Helm to manage the deployments, it's better not to hardcode the namespace in the manifest files. 

Helm has a built-in template function to handle namespaces, which allows to dynamically set the namespace during installation or upgrade of the chart.

- Delete the `create-namespace.yaml` (not needed anymore)
- Remove the `namespace` field from the metadata section in the YAML files moved in the previous section.

### Modify the Helm Chart Values
Inside `helm-sentiment-analysis-mlops`, there is a `values.yaml` file. This is where default values can be defined for the templates, which can be overridden during installation if necessary, allowing more flexibility and easy configuration for the chart when deploying into different environments or updates.

### Modify the templates in the Helm chart to use the defined values
Replace the static values in `frontend-deployment.yaml`, `backend-deployment.yaml`, `frontend-loadbalancer-service.yaml`, and `backend-clusterip-service.yaml` with template placeholders that reference the default values specified in `values.yaml`.

### Modify the NOTES.txt from the chart
Customize the NOTES.txt file in the Helm chart to provide specific instructions or messages that will be displayed to the user after deploying the chart. Since some default files were deleted and certain values have not been parameterized, the original NOTES.txt may reference resources or values that no longer exist or are relevant. Update the NOTES.txt to reflect the current state of the chart and provide any necessary post-installation steps or information relevant to the application.

### Pack the Helm Chart
- Navigate to the Helm chart is folder : `cd helm-sentiment-analysis-mlops`
- Lint the chart to check for issues : `helm install sentiment-analysis helm-sentiment-analysis-mlops/ --namespace sentiment-analysis-mlops --create-namespace`
    - Note : Linter is accusing error in comments at dev_ files. Added 'dev_*' to the .helmignore
- Go back one level : `cd ..`
- Run the following command to package the Helm chart: `helm package helm-sentiment-analysis-mlops`
    - This generates the '.tgz' file, the packaged chart.

### Deploy the Helm Chart
