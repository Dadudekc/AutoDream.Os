#!/usr/bin/env python3

from __future__ import annotations

import json

from src.core.constants.paths import AGENT_WORKSPACES_DIR
from src.services.status_embedding_indexer import refresh_status_embedding


def refresh_all_status_embeddings() -> None:
    """Re-index status.json for all agent workspaces."""
    for status_path in AGENT_WORKSPACES_DIR.glob("Agent-*/status.json"):
        with open(status_path, "r", encoding="utf-8") as f:
            status_data = json.load(f)
        refresh_status_embedding(status_path.parent.name, status_data)


if __name__ == "__main__":
    refresh_all_status_embeddings()
