"""Utility helpers for vector configuration (SSOT)."""

from typing import Any, Dict, Optional


def load_simple_config(
    agent_id: str, config_path: Optional[str] = None
) -> Dict[str, Any]:
    """Return simplified configuration for vector integration.

    Parameters
    ----------
    agent_id: str
        Identifier for the agent using the vector integration.
    config_path: Optional[str]
        Optional path to a configuration file (currently unused).
    """
    return {
        "collection_name": f"agent_{agent_id}",
        "embedding_model": "default",
        "max_results": 10,
    }
