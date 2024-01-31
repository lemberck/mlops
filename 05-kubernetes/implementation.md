## Implementation

### Separate the scripts into frontend and backend folders
Backend : main.py,auth.py,database.py,models.py,sentiment_analysis.py
Frontend : streamlit_app.py

### Reorganize poetry '.toml' file to separate in groups : frontend and backend dependencies
- Remove the all dependencies from the main dependencies except python.
- Create two groups, frontend and backend.
- Move all dependencies except streamlit and requests to the backend group.
- Add streamlit and requests to the frontend group.

### Update project to reflect the changes in the pyproject.toml
- Update the Lock File: `poetry update`
- Reinstall Dependencies: To assure the installation of dependencies for each group to ensure everything is working as expected.
    - backend : `poetry install --no-root --only backend --sync`
    - frontend : `poetry install --no-root --only frontend --sync`

> Note : To install the dependencies only, use `poetry install --no-root --only backend` and `poetry install --no-root --only frontend`

### Create separated dockerfiles for front and backend
--> Separation of Concerns : Building loosely coupled services - microservices architecture.
--> Make sure to install only the dependecies of the correct poetry group
- Docker-backend
- Docker-frontend

### Update streamlit_app.py
- Replace the base URL that points to localhost:8000 with what will be the name of the Kubernetes service for the backend.

### Build the backend and frontend images : 
`docker build -f Dockerfile-backend -t backend-img .`

`docker build -f Dockerfile-frontend -t frontend-img .`

### Take images to Repository - Docker Hub
- Create DockerHub account (if not created yet)
- Create a repository to store the images in DockerHub
- Login to dockerhub using the terminal : `docker login` , then username and password
- Tag the images
    - Format : `docker tag local-image  your-docker-username/repository-name:image` . The create tag will be `your-docker-username/repository-name:image`
        - `docker tag backend-img lemberck/sentiment-analysis-mlops:backend-latest`
        - `docker tag frontend-img lemberck/sentiment-analysis-mlops:frontend-latest`

### Push the tagged images to Dockerhub repository (takes 5-10 min)
- Format : `docker push created-tag`
    - `docker push lemberck/sentiment-analysis-mlops:backend-latest`
    - `docker push lemberck/sentiment-analysis-mlops:frontend-latest`

### Create deployment manifests (YAML file) for both frontend and backend, and also the namespace.
- create-namespace.yaml
- frontend-deployment.yaml 
- backend-deployment.yaml
- dev_... are just the commented ones

### Create services manifests
- backend-clusterip-service.yaml
- frontend-loadbalancer.yaml
- dev_... are just the commented ones

### Create the namespace
`kubectl apply -f sentiment-analysis-namespace.yaml`

### Apply the Namespace and Deployments
- Start minikube : `minikube start`
- Create the namespace : `kubectl apply -f create-namespace.yaml`
- Apply the Deployments : `kubectl apply -f backend/backend-deployment.yaml && kubectl apply -f frontend/frontend-deployment.yaml`
    - Note: Takes about 30 secs to 1 minute for the pods to be ready.
- Check the deployments : `kubectl get deployments -n sentiment-analysis-mlops`

### Apply the Services
- Apply the Services : `kubectl apply -f backend/backend-clusterip-service.yaml && kubectl apply -f frontend/frontend-loadbalancer-service.yaml`
- Enable LoadBalancer in local env (minikube) : `minikube tunnel`
- Check : `kubectl get services -n sentiment-analysis-mlops`

