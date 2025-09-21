"""
Broadcast Module

This module provides service functionality for the swarm system.

Component Type: Service
Priority: High
Dependencies: None


EXAMPLE USAGE:
==============

# Import the service
from src.services.messaging.broadcast import BroadcastService

# Initialize service
service = BroadcastService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(BroadcastService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

"""
from __future__ import annotations

from .coordinates import list_agents
from .service import MessagingService


def broadcast(content: str, sender: str = "ConsolidatedMessagingService") -> dict[str, bool]:
    svc = MessagingService()
    results = {}
    for a in list_agents():
        results[a] = svc.send(a, content)
    return results
