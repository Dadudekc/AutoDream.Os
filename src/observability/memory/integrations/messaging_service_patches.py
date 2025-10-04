"""
Messaging Service Integration Patches
=====================================

Integration patches for consolidated_messaging_service_core.py
to add Phase 3 memory leak prevention capabilities.

Author: Agent-7 (Web Development Expert)
License: MIT
V2 Compliance: ≤400 lines, KISS principle
"""

import logging
from typing import Any

from .messaging_checks import (
    CoordinationRequestPurger,
    MessageSizeValidator,
    MessagingInstrumentation,
    get_messaging_integration,
)

logger = logging.getLogger(__name__)


# ============================================================
# INTEGRATION PATCH FOR CONSOLIDATED MESSAGING SERVICE
# ============================================================


class MessagingServiceMemoryPatch:
    """
    Memory leak prevention patch for ConsolidatedMessagingServiceCore.
    Adds Phase 3 capabilities to existing messaging service.
    """

    def __init__(self, messaging_service):
        """Initialize messaging service memory patch"""
        self.messaging_service = messaging_service
        self.validator = MessageSizeValidator(max_size_mb=1.0)
        self.instrumentation = MessagingInstrumentation()
        self.purger = CoordinationRequestPurger(max_age_seconds=3600, max_count=1000)
        self.integration = get_messaging_integration()
        logger.info("MessagingServiceMemoryPatch initialized")

    def validate_message_before_send(self, message: str) -> dict[str, Any]:
        """Validate message before sending"""
        validation_result = self.validator.validate(message)

        if not validation_result.is_valid:
            logger.warning(f"Message validation failed: {validation_result.reason}")
            return {
                "valid": False,
                "reason": validation_result.reason,
                "size_bytes": validation_result.message_size_bytes,
            }

        return {
            "valid": True,
            "size_bytes": validation_result.message_size_bytes,
            "metadata": validation_result.metadata,
        }

    def instrument_send_operation(self, message: str, operation: str = "send_message"):
        """Get instrumentation context manager for send operation"""
        message_size = len(message.encode("utf-8"))
        return self.instrumentation.instrument_operation(operation, message_size)

    def purge_coordination_requests(self) -> dict[str, Any]:
        """Purge old coordination requests"""
        if not hasattr(self.messaging_service, "coordination_requests"):
            return {"error": "No coordination_requests attribute found"}

        purge_result = self.purger.purge_old_requests(self.messaging_service.coordination_requests)

        # Update messaging service coordination requests
        self.messaging_service.coordination_requests = purge_result["remaining_requests"]

        logger.info(f"Purged {purge_result['purged_count']} coordination requests")

        return purge_result

    def get_patch_status(self) -> dict[str, Any]:
        """Get patch status and metrics"""
        return {
            "patch_active": True,
            "validator": {"max_size_mb": self.validator.max_size_bytes / (1024 * 1024)},
            "instrumentation": self.instrumentation.get_metrics_summary(),
            "purger": {
                "max_age_seconds": self.purger.max_age_seconds,
                "max_count": self.purger.max_count,
                "current_request_count": len(
                    getattr(self.messaging_service, "coordination_requests", {})
                ),
            },
        }


# ============================================================
# HELPER FUNCTIONS FOR INTEGRATION
# ============================================================


def patch_messaging_service(messaging_service) -> MessagingServiceMemoryPatch:
    """
        Apply memory leak prevention patch to messaging service.

        Usage:
    from src.services.messaging_service_core import ConsolidatedMessagingServiceCore
            from src.observability.memory.integrations.messaging_service_patches import patch_messaging_service

            messaging_service = ConsolidatedMessagingServiceCore()
            patch = patch_messaging_service(messaging_service)

            # Validate message before sending
            validation = patch.validate_message_before_send(message)
            if validation['valid']:
                with patch.instrument_send_operation(message):
                    # Send message
                    pass

            # Periodically purge old requests
            patch.purge_coordination_requests()
    """
    return MessagingServiceMemoryPatch(messaging_service)


def create_enhanced_messaging_service(messaging_service_class, *args, **kwargs):
    """
        Create messaging service with memory leak prevention enabled.

        Usage:
    from src.services.messaging_service_core import ConsolidatedMessagingServiceCore
            from src.observability.memory.integrations.messaging_service_patches import create_enhanced_messaging_service

            messaging_service = create_enhanced_messaging_service(
                ConsolidatedMessagingServiceCore,
                coord_path="config/coordinates.json"
            )

            # Service now has .memory_patch attribute
            patch_status = messaging_service.memory_patch.get_patch_status()
    """
    # Create messaging service instance
    service = messaging_service_class(*args, **kwargs)

    # Apply memory patch
    service.memory_patch = patch_messaging_service(service)

    logger.info("Enhanced messaging service created with memory leak prevention")

    return service


# ============================================================
# INTEGRATION GUIDE DOCUMENTATION
# ============================================================

"""
INTEGRATION GUIDE
=================

### Option 1: Patch Existing Service

```python
from src.services.messaging_service_core import ConsolidatedMessagingServiceCore
from src.observability.memory.integrations.messaging_service_patches import patch_messaging_service

# Create standard messaging service
messaging_service = ConsolidatedMessagingServiceCore()

# Apply memory leak prevention patch
patch = patch_messaging_service(messaging_service)

# Use patch for validation and instrumentation
def send_message(message: str):
    # Validate message size
    validation = patch.validate_message_before_send(message)
    if not validation['valid']:
        raise ValueError(f"Message validation failed: {validation['reason']}")

    # Instrument send operation
    with patch.instrument_send_operation(message, "send_message"):
        # Existing send logic here
        pass

# Periodic cleanup (run every hour or after N operations)
def cleanup_old_requests():
    result = patch.purge_coordination_requests()
    print(f"Purged {result['purged_count']} old requests")
```

### Option 2: Create Enhanced Service

```python
from src.services.messaging_service_core import ConsolidatedMessagingServiceCore
from src.observability.memory.integrations.messaging_service_patches import create_enhanced_messaging_service

# Create enhanced messaging service with built-in memory leak prevention
messaging_service = create_enhanced_messaging_service(
    ConsolidatedMessagingServiceCore,
    coord_path="config/coordinates.json"
)

# Access patch directly
validation = messaging_service.memory_patch.validate_message_before_send(message)
with messaging_service.memory_patch.instrument_send_operation(message):
    # Send message
    pass

# Periodic cleanup
messaging_service.memory_patch.purge_coordination_requests()

# Get patch status
status = messaging_service.memory_patch.get_patch_status()
```

### Integration with Phase 1 Detectors

The messaging patches automatically integrate with Phase 1 memory policy framework:

```python
from src.observability.memory.policies import MemoryPolicyManager
from src.observability.memory.integrations import get_messaging_integration

# Initialize Phase 1 policy manager
policy_manager = MemoryPolicyManager()
policy_manager.initialize()

# Get messaging integration with Phase 1 connection
integration = get_messaging_integration(policy_manager)

# Integration provides unified status
status = integration.get_system_status()
```
"""


# Export all public classes and functions
__all__ = [
    "MessagingServiceMemoryPatch",
    "patch_messaging_service",
    "create_enhanced_messaging_service",
]
