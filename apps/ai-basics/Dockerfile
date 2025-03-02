FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and config files first for better caching
COPY requirements.txt pytest.ini ./
RUN pip install --no-cache-dir -r requirements.txt

# Install test dependencies
RUN pip install pytest pytest-cov pytest-asyncio

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command (can be overridden)
CMD ["python", "verify_environment.py"] 