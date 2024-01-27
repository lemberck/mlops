# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory to the root of the project
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the necessary Poetry configuration files
COPY pyproject.toml poetry.lock /app/

# Configure Poetry for non-interactive installation of CPU-only packages
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root

# Copy the application scripts directory
COPY prd-scripts /app/prd-scripts

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI application using Uvicorn from within the scripts directory
CMD ["poetry", "run", "uvicorn", "prd-scripts.main:app", "--host", "0.0.0.0", "--port", "8000"]
