# Base image for Python
FROM python:3.10-slim AS base

# Set working directory inside the container
WORKDIR /code

# Copy only requirements.txt to leverage caching
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code, excluding files defined in .dockerignore
COPY . .

# Environment variables for Uvicorn configuration
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000

# Expose application port
EXPOSE 8000

# Default command to run the app
CMD ["uvicorn", "apps.weather_service.main:app", "--host", "${UVICORN_HOST}", "--port", "${UVICORN_PORT}", "--reload"]
