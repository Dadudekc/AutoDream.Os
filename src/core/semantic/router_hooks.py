from __future__ import annotations

from typing import Any

import yaml

from .semantic_router import SemanticRouter
from .status_index import StatusIndex


def _load_cfg() -> dict[str, Any]:
    with open("config/semantic_config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


_router: SemanticRouter | None = None
_status: StatusIndex | None = None


def _get_router() -> SemanticRouter:
    global _router
    if _router is None:
        _router = SemanticRouter(_load_cfg())
    return _router


def _get_status_idx() -> StatusIndex:
    global _status
    if _status is None:
        _status = StatusIndex(_load_cfg())
        seed_dir = (_load_cfg().get("status_index") or {}).get("seed_dir")
        if seed_dir:
            _status.ingest_dir(seed_dir)
    return _status


def route_message(text: str) -> dict[str, Any]:
    """Returns {priority, agent_suggestions[], context_hits[]}"""
    return _get_router().route(text, enrich_context=True)


def similar_status(payload_or_text: Any) -> dict[str, Any]:

EXAMPLE USAGE:
==============

# Import the core component
from src.core.semantic.router_hooks import Router_Hooks

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Router_Hooks(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

    """Returns {"results":[{id,score,meta}]} for status insights."""
    hits = _get_status_idx().similar(payload_or_text)
    return {"results": [{"id": i, "score": s, "meta": m} for (i, s, m) in hits]}
