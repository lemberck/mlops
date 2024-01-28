# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory to the root of the project
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the Poetry configuration files to the /app directory
COPY pyproject.toml poetry.lock ./

# Copy the Python scripts to the /app/prd-scripts directory
COPY prd-scripts ./

# Configure Poetry for non-interactive installation of CPU-only packages
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Expose the ports the apps run on (FastAPI and Streamlit respectively)
EXPOSE 8000 
EXPOSE 8501  

# Run both FastAPI and Streamlit applications (container ports)
CMD poetry run uvicorn main:app --host 0.0.0.0 --port 8000 & \
    poetry run streamlit run streamlit_app.py --server.port 8501
