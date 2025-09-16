"""
Coordinates Module

This module provides service functionality for the swarm system.

Component Type: Service
Priority: High
Dependencies: src.core.coordinate_loader


EXAMPLE USAGE:
==============

# Import the service
from src.services.messaging.coordinates import CoordinatesService

# Initialize service
service = CoordinatesService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(CoordinatesService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def get_coordinate_loader():
    try:
        from src.core.coordinate_loader import get_coordinate_loader as _core

        return _core()
    except Exception as e:
        logger.warning(f"[coord] fallback loader: {e}")

        class Mock:
            def get_all_agents(self):
                return [f"Agent-{i}" for i in range(1, 9)]

            def is_agent_active(self, a):
                return True

            def get_chat_coordinates(self, a):
                return (100, 100)

        return Mock()


def list_agents() -> list[str]:
    loader = get_coordinate_loader()
    return [a for a in loader.get_all_agents() if loader.is_agent_active(a)]


def get_agent_coordinates(agent_id: str) -> tuple[int, int] | None:
    try:
        return get_coordinate_loader().get_chat_coordinates(agent_id)
    except Exception as e:
        logger.error(f"[coord] failed for {agent_id}: {e}")
        return None


def load_all_active_coords() -> dict[str, tuple[int, int]]:
    loader = get_coordinate_loader()
    out: dict[str, tuple[int, int]] = {}
    for a in loader.get_all_agents():
        if loader.is_agent_active(a):
            try:
                out[a] = loader.get_chat_coordinates(a)
            except Exception:
                pass
    return out
