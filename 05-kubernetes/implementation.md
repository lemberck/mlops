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

### Build the backend and frontend images : 
`docker build -f Dockerfile-backend -t backend-img .`

`docker build -f Dockerfile-frontend -t frontend-img .`

