# Kubernetes-Orchestrated Sentiment Analysis Microservices

## Project Overview

This repository contains a microservices-based sentiment analysis application deployed using Kubernetes. The project illustrates the application's distribution across a microservices architecture, encapsulating the backend and frontend into separate services.

This project uses the results of these other MLOps projects :
- [Sentiment Analysis Deployment via FastAPI](https://github.com/lemberck/mlops/tree/main/02-fastapi)
- [Containerization of Sentiment Analysis for MLOps - Backend + Frontend](https://github.com/lemberck/mlops/tree/main/04-docker)

## Architecture

The application is divided into two primary services:

- **Frontend Service**: A Streamlit user interface exposed to the public via a LoadBalancer. This service allows users to interact with the frontend pods directly.
  
- **Backend Service**: A FastAPI server accessible internally within the cluster through a ClusterIP. This service manages API requests from the frontend service, processing sentiment analysis tasks.

Each service is encapsulated within its deployment, ensuring modularity and independent scalability, following cloud-native application design principles.

## Project Structure
```bash
project/
├── backend/                                    # Backend service files
│   ├── auth.py                                 # Authentication handlers
│   ├── backend-clusterip-service.yaml          # Service definition for the backend
│   ├── backend-deployment.yaml                 # Deployment definition for the backend
│   ├── database.py                             # Database connection and operations
│   ├── dev_backend-clusterip-service.yaml      # Development version of the backend service definition
│   ├── dev_backend-deployment.yaml             # Development version of the backend deployment definition
│   ├── main.py                                 # FastAPI application entry point
│   ├── models.py                               # Data models and schema definitions
│   └── sentiment_analysis.py                   # Sentiment analysis logic
├── frontend/                                   # Frontend service files
│   ├── dev_frontend-deployment.yaml            # Development version of the frontend deployment definition
│   ├── dev_frontend-loadbalancer-service.yaml  # Development version of the frontend service definition
│   ├── frontend-deployment.yaml                # Deployment definition for the frontend
│   ├── frontend-loadbalancer-service.yaml      # Service definition for the frontend (exposed to internet)
│   └── streamlit_app.py                        # Streamlit application script
│── create-namespace.yaml                       # Namespace creation manifest
├── Dockerfile-backend                          # Dockerfile for building backend image
├── Dockerfile-frontend                         # Dockerfile for building frontend image
├── implementation.md                           # Documentation on implementation details
├── poetry.lock                                 # Lock file for Python dependencies
├── pyproject.toml                              # Python project and dependency file
└── README.md                                   # Project README with setup and usage instructions
```

## Implementation Steps

### 1. Project Setup
Separate the application into `frontend` and `backend` directories and organize Python dependencies using Poetry.

### 2. Dockerization
Create distinct Dockerfiles for the frontend and backend, ensuring only the necessary dependencies are included for each service.

### 3. Docker Hub Integration
Build Docker images for both services and push them to a Docker Hub repository.

### 4. Kubernetes Deployment
Craft Kubernetes manifests for deployments and services. Use `kubectl` commands to apply these manifests within a dedicated namespace in the cluster.

### 5. Service Exposure
Deploy the frontend service with a LoadBalancer to expose the Streamlit UI to end-users, and set up the backend service with a ClusterIP for internal cluster communications.

## Microservices Benefits

- **Decoupled Architecture**: The frontend and backend are developed and deployed independently, adhering to microservices best practices.
  
- **Scalability**: Each microservice can be scaled based on its resource requirements and load, promoting efficient resource usage.

- **Continuous Integration/Continuous Deployment (CI/CD)**: Each service can be updated and deployed individually without impacting the other, enabling smoother CI/CD pipelines.

## Kubernetes Advantages

- **Load Balancing**: Kubernetes manages traffic to the services, ensuring high availability and fault tolerance.
  
- **Service Discovery**: Services can interact with each other using DNS names, simplifying inter-service communications.

- **Self-healing**: Kubernetes restarts failing containers, replaces, reschedules, and scales them when nodes die.

- **Automated Rollouts/Rollbacks**: Kubernetes progressively rolls out changes to the application or its configuration, monitoring the application's health to prevent any downtime.

## Prerequisites

- Docker
- Kubernetes (Minikube for local development)
- kubectl CLI

## Usage

To deploy the application in your Kubernetes cluster:

```bash
minikube start
In another terminal : `minikube tunnel`
`kubectl apply -f create-namespace.yaml`
`kubectl apply -f backend/backend-deployment.yaml && kubectl apply -f frontend/frontend-deployment.yaml`
`kubectl apply -f backend/backend-clusterip-service.yaml && kubectl apply -f frontend/frontend-loadbalancer-service.yaml`
minikube service frontend-loadbalancer-service --url
```

This sets up the entire application, creating a namespace, deploying the frontend and backend, and exposing the frontend through a LoadBalancer service.
The last command shows the externalIP where the frontend application can be accessed.

![kub-01](https://github.com/lemberck/mlops/blob/main/05-kubernetes/img/kub-01.png)
![kub-02](https://github.com/lemberck/mlops/blob/main/05-kubernetes/img/kub-02.png)