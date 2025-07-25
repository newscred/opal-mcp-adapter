FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install uv

# Copy pyproject.toml and uv.lock for dependency management
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy application code
COPY . .

# Install dependencies using uv
RUN uv sync --frozen


# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "python", "main.py"]