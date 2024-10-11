# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install PostgreSQL client libraries, Redis, and other dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    redis-server

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Make ports for FastAPI, Flower, and Redis available
EXPOSE 8000 5555 6379

# Start Redis server
RUN service redis-server start

# Run Alembic migrations


# Define environment variable for FastAPI
ENV ENVIRONMENT=production

# Define the entrypoint for the app, running Uvicorn for FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
