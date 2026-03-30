# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
# Ensure the app listens on the port Render provides
ENV PORT=10000

# Set work directory
WORKDIR /app

# Install system dependencies
# These are often needed for Python packages that require compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy requirements and project config first to leverage Docker cache
COPY requirements.txt setup.py pyproject.toml* ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install the current package in editable mode if needed
# (Since requirements.txt has -e ., and we've copied the code, this should work)
RUN pip install -e .

# Expose the port (Render will use its own, but documenting it is good)
EXPOSE 10000

# Start the application using uvicorn
# We use the $PORT environment variable provided by Render. 
# 10000 is a common default for Render, but it usually overrides this.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"]