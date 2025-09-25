#!/usr/bin/env python3
"""
Swarm Brain Configuration
========================

Configuration management for the swarm intelligence system.
V2 Compliance: ≤400 lines, focused configuration functionality.
"""

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class BrainConfig:
    """Configuration for the Swarm Brain system."""
    
    # Core paths
    root: Path = Path(os.getenv("SWARM_BRAIN_ROOT", ".swarm_brain")).resolve()
    sqlite_path: Path = root / "brain.sqlite3"
    index_path: Path = root / "index"
    
    # Embeddings configuration
    embeddings_backend: str = os.getenv("SWARM_BRAIN_EMBEDDINGS", "numpy")  # numpy|faiss|chroma|openai
    openai_model: str = os.getenv("SWARM_BRAIN_OPENAI_MODEL", "text-embedding-3-large")
    dim: int = int(os.getenv("SWARM_BRAIN_EMBED_DIM", "1536"))  # used by numpy/faiss
    
    # System configuration
    create_dirs: bool = True
    max_history_size: int = int(os.getenv("SWARM_BRAIN_MAX_HISTORY", "10000"))
    batch_size: int = int(os.getenv("SWARM_BRAIN_BATCH_SIZE", "100"))
    
    # Performance tuning
    enable_caching: bool = os.getenv("SWARM_BRAIN_CACHE", "true").lower() == "true"
    cache_size: int = int(os.getenv("SWARM_BRAIN_CACHE_SIZE", "1000"))
    
    # Logging
    log_level: str = os.getenv("SWARM_BRAIN_LOG_LEVEL", "INFO")
    enable_debug: bool = os.getenv("SWARM_BRAIN_DEBUG", "false").lower() == "true"


# Global configuration instance
CONFIG = BrainConfig()


def get_config() -> BrainConfig:
    """Get the global configuration instance."""
    return CONFIG


def update_config(**kwargs) -> BrainConfig:
    """Update configuration (creates new instance)."""
    global CONFIG
    current_dict = CONFIG.__dict__.copy()
    current_dict.update(kwargs)
    CONFIG = BrainConfig(**current_dict)
    return CONFIG




