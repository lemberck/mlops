# Implementation


# CI Pipeline
Responsible for linters, unit tests, integration tests, building the docker image of services and take them to registry service.

## Add linters to poetry
- Start poetry env : `poetry shell`
- Add linters to dev env only : `poetry add --group dev pylint flake8`
- Install dependecies to the env : `poetry install --no-root`

### Run the linters for the python scripts
- **Flake8** : Returns a list of issues that it finds according to its rules. 
It is considered easier to integrate into a CI/CD pipeline due to its speed and simplicity.
    - Run for specific script : `poetry run flake8 path/to/python/scripts`
    - Run for all script in the project : `poetry run flake8 .`

> To **automate code checks with flake8 in a CI pipeline**, simply add it as a step in your workflow configuration. If flake8 reports any errors, the CI pipeline will fail, as it exits with a non-zero status upon finding linting violations.

> You can also configure flake8 using a **.flake8** file in your repository to customize the rules to fit the  project's guidelines. For example, you could ignore certain warnings or errors, exclude files, or adjust the maximum line length.

-----------------------------------------

- **Pylint** : It also provides a numerical score (up to 10) . pIt can be slower because it performs a full static analysis of the code, but has more checks than flake8. 
    - Run for specific script : `poetry run pylint path/to/python/scripts`
    - Run for all script in the project : `poetry run pylint folder_name/`
> The score can be used to **automate the linting process in the CI pipeline**, by setting a minimun score that must be met for the build to pass.

> You can add a **.pylintrc** file to customize the rules to fit the project's guidelines

NOTE : If facing an error `[Errno 13] Permission denied: b'/var/lib/docker/overlay2/b23cb536bf8b0ccc4a0f6570ea820a95d6d22a6ca1212b1f104b0fd58077c487/diff/opt/kafka_2.12-2.3.0/bin/...` , run `poetry update`

#### --- After running the linters, solve the issues manually.


## Add unit tests [Not working yet, skip]
- Add test package to dev env only : `poetry add --group dev pytest pytest-asyncio`
- Create a test directory : `mkdir -p tests/backend tests/frontend`
- Create 'pytest.ini' at the root of the project, to show pytest to look for modules inside backend/ and frontend/ : `touch pyproject.ini`
  - https://pytest-with-eric.com/introduction/pytest-pythonpath/ 
```bash
[pytest]  
pythonpath = backend frontend
```

- Create tests for all scrips (the must start with 'test_') : `touch tests/backend/test_auth.py tests/backend/test_database.py tests/backend/test_models.py tests/backend/test_sentiment_analysis.py tests/frontend/test_streamlit_app.py`


## Add pre-commit (for future commits) [Not working yet, skip] 
Pre-commit is used to automate the enforcement of code style instead of just reporting. The framework can be set up to run the chosen linters automatically on every commit. With this, every time there is a commit, pre-commit will run the linters on the changed files. If there are any issues detected by the linters, the commit will be blocked until those issues are resolved. This helps to ensure that you maintain a high code quality.
- Add pre-commit as a Development Dependency: `poetry add --group dev pre-commit`
- Create the pre-commit Configuration File: 
    - Create a file named .pre-commit-config.yaml with the following content to configure pre-commit to run flake8 and pylint: 
    ```bash 
    repos:
  - repo: https://github.com/pycqa/flake8
    rev: ''  # Use the desired version of flake8
    hooks:
      - id: flake8

  - repo: https://github.com/pycqa/pylint
    rev: ''  # Use the desired version of pylint
    hooks:
      - id: pylint
        additional_dependencies: ['pylint']
    ```
    **Note** : To check the installed versions of flake8 and pylint : `poetry show | grep -E "flake8|pylint"`

- Install the pre-commit Hook: `poetry run pre-commit install`
- Run pre-commit Against All Files (Optional - Recommended): `poetry run pre-commit run --all-files`
- Commit The Changes:
    - Add the .pre-commit-config.yaml and any changes to pyproject.toml to your repository and commit them:
    ```bash
    git add .pre-commit-config.yaml pyproject.toml
    git commit -m "Add pre-commit hooks for flake8 and pylint"
    ```

## CI Workflow with GitHub Actions
  1 - Create the workflow directory at the root of the  project : `mkdir -p .github/workflows`

  2 - Create Workflow File for the linters : `touch .github/workflows/ci_python-lint.yml`

  3 - Edit the yml file : `code .github/workflows/ci_python-lint.yml` [VSCode]
  ```bash
  name: CI - Lint, Build, and Push Docker Images

# Triggers the workflow on push to the main branch and pull requests to the main branch,
# but ignores changes that only affect markdown files to prevent unnecessary runs.
on:
  push:
    branches: [ main ]
    paths-ignore:
      - '**/*.md'
  pull_request:
    branches: [ main ]
    paths-ignore:
      - '**/*.md'
  workflow_dispatch:  # Allows the workflow to be manually triggered.

jobs:
  CI_lint-build-push:
    runs-on: ubuntu-latest  # The job will run on the latest Ubuntu virtual environment provided by GitHub.

    steps:
      # Retrieves the code from the repository so that it can be built and tested.
      - name: Check out repository code
        uses: actions/checkout@v2

      # Python is set up for the job since the project is Python-based,
      # and linting tools Flake8 and Pylint require a Python environment.
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'

      # Poetry is used for dependency management to ensure consistent environments,
      # which is essential for reproducible builds and tests.
      - name: Install dependencies with Poetry
        run: |
          pip install poetry
          poetry install --no-root

      # Runs Flake8 for style guide enforcement, catching errors like missing imports or undeclared variables.
      - name: Run Flake8
        run: poetry run flake8 .

      # Runs Pylint to assess code quality, using a score to fail the workflow if the code doesn't meet quality thresholds (>=9.0)
      # This ensures that only high-quality code is integrated and deployed.
      - name: Run Pylint
        run: |
          score=$(poetry run pylint **/*.py --exit-zero --fail-under=9 | grep "Your code has been rated at" | awk '{print substr($7, 1, index($7, "/") - 1)}')
          echo "Pylint score: $score"
          python -c "import sys; sys.exit(0 if float('$score') >= 9 else 1)"

      # Docker images for the backend and frontend services are built with the current commit SHA as a tag.
      # Using the SHA ensures that each image is uniquely tagged with the state of the code that produced it,
      # which is crucial for traceability and rollback in case issues are discovered in production.
      - name: Build backend Docker image
        run: docker build -t ${{ secrets.DOCKER_HUB_USERNAME }}/${{ vars.PROJECT_NAME }}-backend:${{ github.sha }} -f Dockerfile-backend .

      - name: Build frontend Docker image
        run: docker build -t ${{ secrets.DOCKER_HUB_USERNAME }}/${{ vars.PROJECT_NAME }}-frontend:${{ github.sha }} -f Dockerfile-frontend .

      # Docker Hub credentials are stored as GH secrets to securely log in to the Docker Hub registry
      # so that the images can be pushed without exposing sensitive information.
      - name: Log in to Docker Hub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}

      # Pushes the uniquely tagged images to Docker Hub, ready to be pulled down and deployed.
      # This step is critical for the Continuous Deployment (CD) process that follows.
      - name: Push backend Docker image to Docker Hub
        run: docker push ${{ secrets.DOCKER_HUB_USERNAME }}/${{ vars.PROJECT_NAME }}-backend:${{ github.sha }}

      - name: Push frontend Docker image to Docker Hub
        run: docker push ${{ secrets.DOCKER_HUB_USERNAME }}/${{ vars.PROJECT_NAME }}-frontend:${{ github.sha }}

  ```
  4- [DockerHub] Create a DockerHub Access Token : **DockerHub > My Account >Security > New Access Token**
  -  Copy the access token that is generated. This token will be used as a password in GitHub Actions. It is shown only once.

  5 - [For sensitive data] Add Secrets to the Project's GitHub Repository to store he DH credentials : **Settings > Secrets and variables > Actions > New Repository Secret**
  - Add a new secret `DOCKER_HUB_USERNAME` with value equals to your DH username.
  - Add a new secret `DOCKER_HUB_ACCESS_TOKEN` with value equals to the DH access token created on step 4

  6 - [For NOT sensitive data] Add Variables to the Project's GitHub Repository to store the Project name for the image tagging: **Settings > Secrets and variables > Actions > Variables tab > New Repository variable**
  - Add a new variable `PROJECT_NAME` with value equals to 'mlops-sentiment_analysis'

  7 - Commit the CI workflow creation
  > NOTE: In order to GitHub Actions recognize workflow files, they must be located in the .github/workflows directory at the root of the project. 
  To enable testing, the **07-cicd/ directory has been committed to its own separate remote repository**. The workflow file within 07-cicd/ inside the mlops remote repository will not trigger GitHub Actions workflows; it serves purely to consolidate related mlops project materials.

  8 - Go to GH repo > Actions . The workflow must be at the Workflow section on the left. It is possible to trigger it manually (it was configured as such) and it will triggers automatically everytime there is a push or pull request to the main branch.

  # CD pipeline
  Responsible for pulling the images from registry and deploying the services, if CI pipeline succeeds.

  ## CD Workflow with Github Actions
  1 - Create Workflow File for the cd pipeline : `touch .github/workflows/cd_pull-deploy.yml`
  2 - Edit the yml file : `code .github/workflows/cd_pull-deploy.yml` [VSCode]
  ```bash

  ```
