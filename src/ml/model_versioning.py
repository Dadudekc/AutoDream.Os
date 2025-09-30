"""
ML Model Versioning System - V2 Compliant Refactored Version
===========================================================

Refactored into modular components for V2 compliance:
- Core functionality in model_versioning_core.py
- Advanced operations in model_versioning_advanced.py
- Main interface maintains backward compatibility

Author: Agent-5 (Coordinator)
License: MIT
"""

import logging
from typing import Any, Dict, List, Optional

from .model_versioning_core import ModelVersioningCore, ModelVersion, VersionStatus
from .model_versioning_advanced import ModelVersioningAdvanced


class ModelVersioning:
    """
    Main ML model versioning interface.
    Provides backward compatibility while using refactored components.
    """

    def __init__(self, model_path: str = "/app/models", registry_path: str = "/app/registry"):
        """Initialize the ModelVersioning system."""
        self.core = ModelVersioningCore(model_path, registry_path)
        self.advanced = ModelVersioningAdvanced(self.core)
        self.logger = logging.getLogger(__name__)

    # Core operations (delegated to core)
    def create_version(self, model_name: str, version: str, framework: str, 
                      file_path: str, created_by: str, description: str = None,
                      tags: list[str] = None, metrics: dict[str, Any] = None,
                      dependencies: dict[str, str] = None) -> ModelVersion:
        """Create a new model version."""
        return self.core.create_version(model_name, version, framework, file_path, 
                                      created_by, description, tags, metrics, dependencies)

    def get_version(self, model_name: str, version: str) -> ModelVersion | None:
        """Get a specific model version."""
        return self.core.get_version(model_name, version)

    def list_versions(self, model_name: str) -> list[ModelVersion]:
        """List all versions for a model."""
        return self.core.list_versions(model_name)

    def update_version_status(self, model_name: str, version: str, 
                            status: VersionStatus) -> bool:
        """Update the status of a model version."""
        return self.core.update_version_status(model_name, version, status)

    def delete_version(self, model_name: str, version: str) -> bool:
        """Delete a model version."""
        return self.core.delete_version(model_name, version)

    # Advanced operations (delegated to advanced)
    def promote_version(self, model_name: str, version: str, 
                       target_status: VersionStatus) -> bool:
        """Promote a model version to a new status."""
        return self.advanced.promote_version(model_name, version, target_status)

    def compare_versions(self, model_name: str, version1: str, version2: str) -> Dict[str, Any]:
        """Compare two model versions."""
        return self.advanced.compare_versions(model_name, version1, version2)

    def get_latest_version(self, model_name: str, status: Optional[VersionStatus] = None) -> Optional[ModelVersion]:
        """Get the latest version of a model, optionally filtered by status."""
        return self.advanced.get_latest_version(model_name, status)

    def get_production_versions(self) -> List[ModelVersion]:
        """Get all production versions across all models."""
        return self.advanced.get_production_versions()

    def archive_old_versions(self, model_name: str, keep_count: int = 5) -> int:
        """Archive old versions, keeping only the specified number of recent ones."""
        return self.advanced.archive_old_versions(model_name, keep_count)

    def validate_model_integrity(self, model_name: str, version: str) -> Dict[str, Any]:
        """Validate the integrity of a model version."""
        return self.advanced.validate_model_integrity(model_name, version)