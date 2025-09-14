# File: infra/docker/discord-agent-bot.Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates tini && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install -r requirements.txt

# App
COPY src ./src
COPY scripts ./scripts
COPY config ./config

# Non-root
RUN useradd -m botuser && chown -R botuser:botuser /app
USER botuser

ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["python","src/discord_commander/discord_agent_bot.py"]
