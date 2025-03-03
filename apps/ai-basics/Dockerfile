FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN pip install uv

# Create virtual environment
RUN uv venv /app/.venv

# Copy requirements and config files first for better caching
COPY requirements.txt pytest.ini ./

# Install dependencies using UV
RUN . .venv/bin/activate && uv pip install --no-cache -r requirements.txt

# Install test dependencies
RUN . .venv/bin/activate && uv pip install --no-cache pytest pytest-cov pytest-asyncio

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

# Default command (can be overridden)
CMD ["python", "verify_environment.py"] 