import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from .model_versioning_core import ModelVersioningCore, ModelVersion, VersionStatus


class ModelVersioningAdvanced:
    """
    Advanced ML model versioning operations.
    Provides semantic versioning, model comparison, and lifecycle management.
    """

    def __init__(self, core: ModelVersioningCore):
        """Initialize advanced versioning with core instance."""
        self.core = core
        self.logger = logging.getLogger(__name__)

    def promote_version(self, model_name: str, version: str, 
                       target_status: VersionStatus) -> bool:
        """Promote a model version to a new status."""
        try:
            # Validate promotion path
            current_version = self.core.get_version(model_name, version)
            if not current_version:
                self.logger.error(f"Version {version} not found for model {model_name}")
                return False
            
            # Check promotion validity
            if not self._is_valid_promotion(current_version.status, target_status):
                self.logger.error(f"Invalid promotion from {current_version.status.value} to {target_status.value}")
                return False
            
            # Update status
            success = self.core.update_version_status(model_name, version, target_status)
            if success:
                self.logger.info(f"Promoted {model_name} v{version} to {target_status.value}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error promoting version: {e}")
            return False

    def compare_versions(self, model_name: str, version1: str, version2: str) -> Dict[str, Any]:
        """Compare two model versions."""
        try:
            v1 = self.core.get_version(model_name, version1)
            v2 = self.core.get_version(model_name, version2)
            
            if not v1 or not v2:
                return {"error": "One or both versions not found"}
            
            comparison = {
                "model_name": model_name,
                "version1": version1,
                "version2": version2,
                "file_size_diff": v2.file_size - v1.file_size,
                "framework_changed": v1.framework != v2.framework,
                "status_changed": v1.status != v2.status,
                "metrics_changed": v1.metrics != v2.metrics,
                "dependencies_changed": v1.dependencies != v2.dependencies,
                "created_time_diff": (v2.created_at - v1.created_at).total_seconds()
            }
            
            return comparison
            
        except Exception as e:
            self.logger.error(f"Error comparing versions: {e}")
            return {"error": str(e)}

    def get_latest_version(self, model_name: str, status: Optional[VersionStatus] = None) -> Optional[ModelVersion]:
        """Get the latest version of a model, optionally filtered by status."""
        try:
            versions = self.core.list_versions(model_name)
            
            if not versions:
                return None
            
            # Filter by status if specified
            if status:
                versions = [v for v in versions if v.status == status]
            
            # Return the most recent version
            return versions[0] if versions else None
            
        except Exception as e:
            self.logger.error(f"Error getting latest version: {e}")
            return None

    def get_production_versions(self) -> List[ModelVersion]:
        """Get all production versions across all models."""
        try:
            production_versions = []
            
            # Get all registry files
            for filename in self.core.registry_path:
                if filename.endswith('.json'):
                    # Extract model name and version from filename
                    parts = filename.replace('.json', '').split('_')
                    if len(parts) >= 2:
                        model_name = '_'.join(parts[:-1])
                        version = parts[-1]
                        
                        version_obj = self.core.get_version(model_name, version)
                        if version_obj and version_obj.status == VersionStatus.PRODUCTION:
                            production_versions.append(version_obj)
            
            return production_versions
            
        except Exception as e:
            self.logger.error(f"Error getting production versions: {e}")
            return []

    def archive_old_versions(self, model_name: str, keep_count: int = 5) -> int:
        """Archive old versions, keeping only the specified number of recent ones."""
        try:
            versions = self.core.list_versions(model_name)
            
            if len(versions) <= keep_count:
                return 0
            
            archived_count = 0
            versions_to_archive = versions[keep_count:]
            
            for version in versions_to_archive:
                if version.status != VersionStatus.ARCHIVED:
                    success = self.core.update_version_status(
                        model_name, version.version, VersionStatus.ARCHIVED
                    )
                    if success:
                        archived_count += 1
            
            self.logger.info(f"Archived {archived_count} old versions for model {model_name}")
            return archived_count
            
        except Exception as e:
            self.logger.error(f"Error archiving old versions: {e}")
            return 0

    def validate_model_integrity(self, model_name: str, version: str) -> Dict[str, Any]:
        """Validate the integrity of a model version."""
        try:
            version_obj = self.core.get_version(model_name, version)
            if not version_obj:
                return {"valid": False, "error": "Version not found"}
            
            # Check if file still exists
            if not os.path.exists(version_obj.file_path):
                return {"valid": False, "error": "Model file not found"}
            
            # Verify file hash
            current_hash = self.core.calculate_file_hash(version_obj.file_path)
            if current_hash != version_obj.file_hash:
                return {"valid": False, "error": "File hash mismatch"}
            
            # Verify file size
            current_size = self.core.get_file_size(version_obj.file_path)
            if current_size != version_obj.file_size:
                return {"valid": False, "error": "File size mismatch"}
            
            return {"valid": True, "message": "Model integrity verified"}
            
        except Exception as e:
            self.logger.error(f"Error validating model integrity: {e}")
            return {"valid": False, "error": str(e)}

    def _is_valid_promotion(self, current_status: VersionStatus, target_status: VersionStatus) -> bool:
        """Check if a promotion is valid based on status hierarchy."""
        promotion_paths = {
            VersionStatus.DRAFT: [VersionStatus.STAGING, VersionStatus.ARCHIVED],
            VersionStatus.STAGING: [VersionStatus.PRODUCTION, VersionStatus.DRAFT],
            VersionStatus.PRODUCTION: [VersionStatus.DEPRECATED, VersionStatus.ARCHIVED],
            VersionStatus.DEPRECATED: [VersionStatus.ARCHIVED],
            VersionStatus.ARCHIVED: []  # Cannot promote from archived
        }
        
        return target_status in promotion_paths.get(current_status, [])
