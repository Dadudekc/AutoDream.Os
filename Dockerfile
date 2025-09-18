# Multi-stage Dockerfile for V2_SWARM Agent Cellphone System
# Optimized for production deployment with security and performance

# Stage 1: Build stage
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILDPLATFORM
ARG TARGETPLATFORM

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt requirements-test.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim as production

# Create non-root user for security
RUN groupadd -r swarm && useradd -r -g swarm swarm

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/swarm/.local

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY tools/ ./tools/
COPY agent_workspaces/ ./agent_workspaces/
COPY devlogs/ ./devlogs/
COPY requirements.txt ./

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/temp

# Set ownership to swarm user
RUN chown -R swarm:swarm /app

# Switch to non-root user
USER swarm

# Add local Python packages to PATH
ENV PATH=/home/swarm/.local/bin:$PATH

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Expose port (if web interface is used)
EXPOSE 8000

# Default command
CMD ["python", "-m", "src.services.messaging", "--help"]
