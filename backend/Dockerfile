FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Remove any existing .venv directory and install dependencies
RUN rm -rf .venv && uv sync --frozen

# Copy the rest of the application
COPY . .

# Remove .venv again in case it was copied
RUN rm -rf .venv

# Expose port
EXPOSE 8000

# Run the app
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]