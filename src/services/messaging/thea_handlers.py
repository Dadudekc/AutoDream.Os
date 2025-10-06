"""
Thea_Handlers Module

This module provides service functionality for the swarm system.

Component Type: Service
Priority: High
Dependencies: None


EXAMPLE USAGE:
==============

# Import the service
from src.services.messaging.thea_handlers import Thea_HandlersService

# Initialize service
service = Thea_HandlersService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Thea_HandlersService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

"""
from __future__ import annotations


def send_to_thea(
    message: str,
    *,
    username: str | None = None,
    # SECURITY: Password placeholder - replace with environment variable
    headless: bool = True,
    thread_url: str | None = None,
    resume_last: bool = False,
    attach_file: str | None = None,
):
    # Thin wrapper around your SimpleTheaCommunication module
    import os
    import sys

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    sys.path.append(project_root)
    from simple_thea_communication import SimpleTheaCommunication

    thea = SimpleTheaCommunication(
        username=username,
        # SECURITY: Password placeholder - replace with environment variable
        use_selenium=True,
        headless=headless,
    )
    ok = thea.run_communication_cycle(message)
    thea.cleanup()
    return ok
