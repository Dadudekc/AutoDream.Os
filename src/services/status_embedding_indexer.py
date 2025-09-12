#!/usr/bin/env python3
"""Status Embedding Indexer
===========================

Refresh agent status embeddings in the unified vector database.

EXAMPLE USAGE:
==============

# Import the service
from src.services.status_embedding_indexer import Status_Embedding_IndexerService

# Initialize service
service = Status_Embedding_IndexerService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Status_Embedding_IndexerService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

"""

from __future__ import annotations

import json
from typing import Any

from ..core.constants.paths import STATUS_EMBEDDINGS_FILE, ensure_path_exists


def refresh_status_embedding(agent_id: str, status_data: dict[str, Any]) -> None:
    """Refresh vector DB entry for an agent status."""
    ensure_path_exists(STATUS_EMBEDDINGS_FILE.parent)
    database: dict[str, Any] = {}
    if STATUS_EMBEDDINGS_FILE.exists():
        with open(STATUS_EMBEDDINGS_FILE, encoding="utf-8") as f:
            database = json.load(f)
    database[agent_id] = status_data
    with open(STATUS_EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=2)
