#!/usr/bin/env python3
"""
Consolidated Debate Service V2 - V2 Compliant
=============================================

Unified debate coordination service consolidating all debate components.
V2 COMPLIANT: Under 100 lines, focused orchestration responsibility.

Author: Agent-4 (Quality Assurance Specialist - CAPTAIN)
License: MIT
"""

import logging
from typing import Any, Dict, List, Optional

# Import core debate components
from .debate.core import DebateCoordinator, DebateResponse, DebateTopic

logger = logging.getLogger(__name__)


class ConsolidatedDebateService(DebateCoordinator):
    """Main consolidated debate service coordinating all debate components.
    
    This class extends DebateCoordinator to maintain backward compatibility.
    """
    
    def __init__(self):
        super().__init__()
        logger.info("Consolidated Debate Service V2 initialized")


# Create global instance for backward compatibility
_global_debate_service: Optional[ConsolidatedDebateService] = None


def get_debate_service() -> ConsolidatedDebateService:
    """Get or create the global debate service instance."""
    global _global_debate_service
    
    if _global_debate_service is None:
        _global_debate_service = ConsolidatedDebateService()
        logger.info("Created new consolidated debate service instance")
    
    return _global_debate_service


def reset_debate_service() -> None:
    """Reset the global debate service instance (useful for testing)."""
    global _global_debate_service
    _global_debate_service = None
    logger.info("Reset global debate service instance")


# Export key classes for backward compatibility
__all__ = [
    "ConsolidatedDebateService",
    "DebateCoordinator",
    "DebateResponse",
    "DebateTopic",
    "get_debate_service",
    "reset_debate_service"
]
