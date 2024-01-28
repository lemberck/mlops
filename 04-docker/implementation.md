### Add Dependency

Add the dependency 'requests', and 'streamlit':

```poetry add requests streamlit```


### Develop scripts (streamlit app only)
- **streamlit_app.py** - Interacts with a FastAPI application, allowing users to test API endpoints for user management and sentiment analysis through a simple command-line interface.

### Create the Dockerfile
- **Dockerfile** : The Dockerfile defines a containerized environment for a FastAPI application using Python 3.10. It sets up an environment for running a Python-based web application, utilizing FastAPI and Streamlit. It starts with a Python 3.10 slim image as the base and sets /app as the working directory. Poetry, a Python dependency manager, is installed to manage project dependencies. The Dockerfile then copies the pyproject.toml and poetry.lock files, along with all Python scripts from the prd-scripts directory, into the container. Dependencies are installed in a non-interactive mode. The container is configured to expose two ports, 8000 for FastAPI and 8501 for Streamlit, facilitating external access to the services. The final command in the Dockerfile runs the FastAPI and the Streamlit apps, making them the default services when the container starts.

- **Dockerfile_no_streamlit** : The Dockerfile defines a containerized environment for a FastAPI application using Python 3.10. 
It sets up the working directory, installs Poetry for dependency management, and copies necessary files into the container. 
Dependencies are installed non-interactively, ensuring only necessary packages are included. The container exposes port 8000 for the 
application, and uses Uvicorn to run the FastAPI app, configured to listen on all interfaces to facilitate external access. 
This setup provides a lightweight, isolated environment for running and testing the FastAPI application.

### Build the Docker Image
1. With streamlit

```docker build -t fastapi-poetry-streamlit .```

2. No streamlit

```docker build -f Dockerfile_no_streamlit -t fastapi-poetry .```

> Builds a Docker image from a Dockerfile in the current directory (denoted by '.') . The '-t fastapi-poetry' option assigns the tag fastapi-poetry-streamlit (or fastapi-poetry)  to the built image, which can be used to reference the image later, for example, when running a container.
Note: Run this command where the Dockerfile is  located.

### Start the container
1. With streamlit

```docker run -p 8080:8000 -p 8501:8501 fastapi-poetry-streamlit:latest```
> Starts a container from the 'fastapi-poetry-streamlit:latest' Docker image. The -p 8080:8000 option maps port 8080 on the host to port 8000 inside the container, allowing external access to the FastAPI application running on port 8000 in the container through port 8080 on the host machine. Following the same logig, streamlit 8501 container port is mapped to the host port 8501. This means you can access the FastAPI app from your browser or other tools using http://localhost:8080/docs and streamlit using http://localhost:8501 . The latest tag refers to the most recent version of the fastapi-poetry-streamlit image. Change the host port as needed.

**Note:** Wait for both services to be finished with the set up after running this command (streamlit is faster than FastAPI application)

2. No streamlit

```docker run -p 8080:8000 fastapi-poetry:latest```
> Starts a container from the 'fastapi-poetry:latest' Docker image. The -p 8080:8000 option maps port 8080 on the host to port 8000 inside the container, allowing external access to the FastAPI application running on port 8000 in the container through port 8080 on the host machine. This means you can access the FastAPI app from your browser using http://localhost:8080. The latest tag refers to the most recent version of the fastapi-poetry image. Change the host port as needed.

#### Test the API

1. With Streamlit
> In your browser, access http://localhost:8501 to use the streamlit application.

2. No Streamlit
> In your browser, access http://localhost:8080/docs to use the generated documentation with testing features from FastAPI.

### Stop the container

- Get the container ID
```docker ps```

- Stop the container
```docker stop <containerID>```



