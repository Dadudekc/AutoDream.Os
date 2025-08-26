"""Backward-compatible wrapper for the refactored middleware package.

The original monolithic module has been split into smaller modules under
``src.services.middleware`` to improve maintainability and adhere to the
repository's coding standards. This wrapper exposes the primary classes so
that existing imports continue to function.
"""

from src.services.middleware import (
    BaseMiddlewareComponent,
    DataFlowDirection,
    DataPacket,
    MiddlewareChain,
    MiddlewareOrchestrator,
    MiddlewareType,
    RoutingMiddleware,
    DataTransformationMiddleware,
    ValidationMiddleware,
)

__all__ = [
    "BaseMiddlewareComponent",
    "DataFlowDirection",
    "DataPacket",
    "MiddlewareChain",
    "MiddlewareOrchestrator",
    "MiddlewareType",
    "RoutingMiddleware",
    "DataTransformationMiddleware",
    "ValidationMiddleware",
]
