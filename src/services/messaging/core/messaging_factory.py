#!/usr/bin/env python3
"""
Messaging Factory - V2 Compliant
================================

Factory functions for creating messaging service instances.
V2 COMPLIANT: Under 300 lines, single responsibility.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
from typing import Optional

from .messaging_coordinator import MessagingCoordinator

logger = logging.getLogger(__name__)

# Global instance cache
_global_messaging_service: Optional[MessagingCoordinator] = None


def get_consolidated_messaging_service(dry_run: bool = False) -> MessagingCoordinator:
    """Get or create the global consolidated messaging service instance.
    
    Args:
        dry_run: If True, operate in dry-run mode
        
    Returns:
        ConsolidatedMessagingService instance
    """
    global _global_messaging_service
    
    if _global_messaging_service is None:
        _global_messaging_service = MessagingCoordinator(dry_run=dry_run)
        logger.info("Created new consolidated messaging service instance")
    else:
        logger.debug("Returning existing consolidated messaging service instance")
    
    return _global_messaging_service


def get_messaging_service(dry_run: bool = False) -> MessagingCoordinator:
    """Get messaging service instance (alias).
    
    Args:
        dry_run: If True, operate in dry-run mode
        
    Returns:
        MessagingCoordinator instance
    """
    return get_consolidated_messaging_service(dry_run=dry_run)


def reset_global_service() -> None:
    """Reset the global service instance (useful for testing)."""
    global _global_messaging_service
    _global_messaging_service = None
    logger.info("Reset global messaging service instance")


def create_messaging_service(dry_run: bool = False) -> MessagingCoordinator:
    """Create a new messaging service instance (doesn't use global cache).
    
    Args:
        dry_run: If True, operate in dry-run mode
        
    Returns:
        New MessagingCoordinator instance
    """
    return MessagingCoordinator(dry_run=dry_run)

