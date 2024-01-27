# Use a lightweight Python image
FROM python:3.10-slim

# Install system dependencies required for downloading and installing binaries
RUN apt-get update && apt-get install -y --no-install-recommends curl gnupg \
    && rm -rf /var/lib/apt/lists/*

# Add the MPR repository key and install just
RUN curl -fsSL https://repo.makedeb.org/archive-key.asc | apt-key add - \
    && echo "deb https://repo.makedeb.org/ stable mpm" | tee /etc/apt/sources.list.d/makedeb.list \
    && apt-get update \
    && apt-get install -y just

# Set the working directory to the root of the project
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the Poetry configuration files and the Python scripts to the /app directory
COPY pyproject.toml poetry.lock ./
COPY prd-scripts ./

# Configure Poetry for non-interactive installation of CPU-only packages
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI application using Uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
