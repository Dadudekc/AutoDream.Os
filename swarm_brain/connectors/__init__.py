"""
Swarm Brain Connectors
======================

Integration connectors for existing agent systems.
"""

from .project_scanner import ingest_scan
from .devlogs import ingest_devlog
from .discord import ingest_discord
from .performance import ingest_performance

__all__ = [
    "ingest_scan",
    "ingest_devlog", 
    "ingest_discord",
    "ingest_performance"
]




