from __future__ import annotations
from typing import Dict, Any, Optional
import yaml

from .semantic_router import SemanticRouter
from .status_index import StatusIndex

def _load_cfg() -> Dict[str, Any]:
    with open("config/semantic_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

_router: Optional[SemanticRouter] = None
_status: Optional[StatusIndex] = None

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

def route_message(text: str) -> Dict[str, Any]:
    """Returns {priority, agent_suggestions[], context_hits[]}"""
    return _get_router().route(text, enrich_context=True)

def similar_status(payload_or_text: Any) -> Dict[str, Any]:
    """Returns {"results":[{id,score,meta}]} for status insights."""
    hits = _get_status_idx().similar(payload_or_text)
    return {"results": [{"id": i, "score": s, "meta": m} for (i, s, m) in hits]}
