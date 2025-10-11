# Vector Database Package
# Updated: 2025-10-11 - Consolidated middleware (Agent-7)

from . import (
    analytics_utils,
    collection_utils,
    document_utils,
    middleware,
    models,
    routes,
    search_utils,
    unified_middleware,
    utils,
)

# Backward compatibility - import middleware classes
from .unified_middleware import (
    ErrorHandlerMiddleware,
    RequestHandlerMiddleware,
    ResponseHandlerMiddleware,
    UnifiedVectorMiddleware,
    ValidationMiddleware,
)

__all__ = [
    "analytics_utils",
    "collection_utils",
    "document_utils",
    "middleware",
    "models",
    "routes",
    "search_utils",
    "unified_middleware",
    "utils",
    # Middleware classes
    "UnifiedVectorMiddleware",
    "ErrorHandlerMiddleware",
    "RequestHandlerMiddleware",
    "ResponseHandlerMiddleware",
    "ValidationMiddleware",
]
