# Helm in Kubernetes Orchestration for Sentiment Analysis MLOps project 

This repository serves as a hands-on project to utilizing Helm, the Kubernetes package manager, which plays the role in deploying and managing applications in a Kubernetes environment. Helm enhances Kubernetes' capabilities by introducing the concept of charts, which are pre-configured resource templates that make application deployment more efficient, reliable, and manageable.

This project uses the results of these other MLOps projects :
- [Sentiment Analysis Deployment via FastAPI](https://github.com/lemberck/mlops/tree/main/02-fastapi)
- [Containerization of Sentiment Analysis for MLOps - Backend + Frontend](https://github.com/lemberck/mlops/tree/main/04-docker)
- [Microservice Architecture for Sentiment Analysis in Kubernetes](https://github.com/lemberck/mlops/tree/main/05-kubernetes)

## Why Helm?

- **Simplicity**: Helm's chart system simplifies the deployment process, allowing complex applications to be packaged into easy-to-understand units.
- **Reusability**: Charts are reusable, version-controlled packages, which means it can be defineed once and deployed anywhere, multiple times.
- **Scalability**: With Helm, scaling the application horizontally or upgrading the deployment becomes a matter of changing a few configurations.
- **Rollbacks**: Helm makes it easy to roll back to previous versions of the deployment if something goes wrong, providing a safety net for reliable operations.
- **Dependency Management**: Helm charts can manage dependencies between Kubernetes objects, making it straightforward to deploy complex applications.

## Helm in Action

In this project, Helm is utilized to orchestrate the deployment of a pre-existing Dockerized sentiment analysis application. The focus here is not on the application itself but on demonstrating Helm's powerful features for Kubernetes orchestration. 

Through practical application, this project aims to highlight the facilitation of MLOps practices by leveraging Helm, emphasizing the significance of efficient resource management, and configuration templating in modern-day deployment strategies.


## Project Structure
```bash
project
├── backend                         # Backend application source code
│   ├── auth.py                     # Authentication module
│   ├── database.py                 # Database operations module
│   ├── main.py                     # Main application entry point for FastAPI
│   ├── models.py                   # Data models
│   └── sentiment_analysis.py       # Sentiment analysis logic
├── frontend                        # Frontend application source code
│   └── streamlit_app.py            # Streamlit application script
├── helm-sentiment-analysis-mlops   # Helm chart for the project
│   ├── templates                   # Template files for Kubernetes objects
│   │   ├── backend-clusterip-service.yaml       # Service definition for backend
│   │   ├── backend-deployment.yaml              # Deployment definition for backend
│   │   ├── frontend-deployment.yaml             # Deployment definition for frontend
│   │   └── frontend-loadbalancer-service.yaml   # Service definition for frontend with LoadBalancer
│   ├── .helmignore                 # Files and patterns to ignore when packaging
│   ├── Chart.yaml                  # Chart metadata file
│   ├── values.yaml                 # Default configuration values for the chart
│   └── NOTES.txt                   # Notes and instructions displayed after chart installation
├── img                             # Directory for images used in documentation or app
├── Dockerfile-backend              # Dockerfile for building the backend image
├── Dockerfile-frontend             # Dockerfile for building the frontend image
├── helm-sentiment-analysis-mlops-0.1.0.tgz # Packaged Helm chart archive
├── implementation.md               # Documentation on implementing the Helm chart
├── poetry.lock                     # Lock file for Python dependencies (Poetry)
├── pyproject.toml                  # Project metadata and dependencies (Poetry)
└── README.md                       # Project README file
```

## Deploying with Helm
To deploy this application:

1. Start your Kubernetes cluster (e.g., Minikube).
2. Install Helm on your machine.
3. Deploy the application using Helm:

   ``` helm install sentiment-analysis helm-sentiment-analysis-mlops/ --namespace sentiment-analysis-mlops --create-namespace```

4. Access the application through the frontend service exposed by Kubernetes.

## Cleanup with Helm
To remove the application from your cluster, use Helm to uninstall:

``` helm uninstall sentiment-analysis -n sentiment-analysis-mlops```

Optionally, delete the namespace:

``` kubectl delete ns sentiment-analysis-mlops```

## Future Directions
**CI/CD Integration**: Future implementations will introduce continuous integration and deployment pipelines for automated testing and deployment workflows.

![Application](https://github.com/lemberck/mlops/blob/main/06-helm/img/helm-dep.png)