# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

# Consolidated configuration management (Phase 2 Batch 2A)
from .consolidated_config_management import (
    ConfigurationConsolidator,  # Backwards compatibility
    UnifiedConfigurationManager,
    scan_and_consolidate_config,
    validate_configuration_setup,
)

# Note: Individual config modules removed in favor of consolidation
# Import them directly when needed for backwards compatibility

__all__ = [
    "UnifiedConfigurationManager",
    "scan_and_consolidate_config",
    "validate_configuration_setup",
    "ConfigurationConsolidator",  # Backwards compatibility
]
