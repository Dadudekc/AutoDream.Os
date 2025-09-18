import os
import json
import shutil
import hashlib
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
# import semver  # Removed dependency for V2 compliance

class VersionStatus(Enum):
    """Status enumeration for model versions."""
    DRAFT = "draft"
    STAGING = "staging"
    PRODUCTION = "production"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

@dataclass
class ModelVersion:
    """Data class for model version information."""
    model_name: str
    version: str
    framework: str
    file_path: str
    file_hash: str
    file_size: int
    created_at: datetime
    created_by: str
    status: VersionStatus
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None
    dependencies: Optional[Dict[str, str]] = None

class ModelVersioning:
    """
    Manages ML model versioning, metadata tracking, and lifecycle management.
    Provides semantic versioning and model registry capabilities.
    """

    def __init__(self, model_path: str = "/app/models", registry_path: str = "/app/registry"):
        """
        Initializes the ModelVersioning system.

        Args:
            model_path: Path to store model files.
            registry_path: Path to store version registry.
        """
        if not model_path:
            raise ValueError("Model path cannot be empty.")
        if not registry_path:
            raise ValueError("Registry path cannot be empty.")

        self.model_path = model_path
        self.registry_path = registry_path
        self.logger = logging.getLogger(__name__)
        
        # Version registry
        self.versions: Dict[str, Dict[str, ModelVersion]] = {}  # {model_name: {version: ModelVersion}}
        self.registry_file = os.path.join(registry_path, "model_registry.json")

        # Ensure directories exist
        os.makedirs(model_path, exist_ok=True)
        os.makedirs(registry_path, exist_ok=True)

        # Load existing registry
        self._load_registry()

    def _load_registry(self) -> None:
        """Loads the model version registry from disk."""
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r') as f:
                    data = json.load(f)
                
                for model_name, versions in data.items():
                    self.versions[model_name] = {}
                    for version, version_data in versions.items():
                        # Convert datetime strings back to datetime objects
                        version_data['created_at'] = datetime.fromisoformat(version_data['created_at'])
                        # Convert status string back to enum
                        version_data['status'] = VersionStatus(version_data['status'])
                        self.versions[model_name][version] = ModelVersion(**version_data)
                
                self.logger.info(f"Loaded registry with {len(self.versions)} models")
            except Exception as e:
                self.logger.error(f"Failed to load registry: {e}")
                self.versions = {}

    def _save_registry(self) -> None:
        """Saves the model version registry to disk."""
        try:
            # Convert to serializable format
            data = {}
            for model_name, versions in self.versions.items():
                data[model_name] = {}
                for version, version_obj in versions.items():
                    version_dict = asdict(version_obj)
                    # Convert datetime to string
                    version_dict['created_at'] = version_obj.created_at.isoformat()
                    # Convert enum to string
                    version_dict['status'] = version_obj.status.value
                    data[model_name][version] = version_dict

            with open(self.registry_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.logger.info("Registry saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save registry: {e}")

    def _calculate_file_hash(self, file_path: str) -> str:
        """
        Calculates SHA-256 hash of a file.

        Args:
            file_path: Path to the file.

        Returns:
            SHA-256 hash of the file.
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def register_model_version(self, model_name: str, version: str, framework: str,
                             file_path: str, created_by: str, description: Optional[str] = None,
                             tags: Optional[List[str]] = None, 
                             metrics: Optional[Dict[str, Any]] = None,
                             dependencies: Optional[Dict[str, str]] = None) -> ModelVersion:
        """
        Registers a new model version.

        Args:
            model_name: Name of the model.
            version: Semantic version string.
            framework: ML framework used.
            file_path: Path to the model file.
            created_by: User who created this version.
            description: Optional description of the version.
            tags: Optional list of tags.
            metrics: Optional model metrics.
            dependencies: Optional dependency information.

        Returns:
            ModelVersion object.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if not version:
            raise ValueError("Version cannot be empty.")
        if not framework:
            raise ValueError("Framework cannot be empty.")
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"Model file not found: {file_path}")
        if not created_by:
            raise ValueError("Created by cannot be empty.")

        # Validate version format (simple validation for V2 compliance)
        if not version or not isinstance(version, str):
            raise ValueError(f"Invalid version format: {version}")

        # Check if version already exists
        if model_name in self.versions and version in self.versions[model_name]:
            raise ValueError(f"Version {version} already exists for model {model_name}")

        # Calculate file properties
        file_hash = self._calculate_file_hash(file_path)
        file_size = os.path.getsize(file_path)

        # Create model version
        model_version = ModelVersion(
            model_name=model_name,
            version=version,
            framework=framework,
            file_path=file_path,
            file_hash=file_hash,
            file_size=file_size,
            created_at=datetime.utcnow(),
            created_by=created_by,
            status=VersionStatus.DRAFT,
            description=description,
            tags=tags or [],
            metrics=metrics,
            dependencies=dependencies
        )

        # Add to registry
        if model_name not in self.versions:
            self.versions[model_name] = {}
        self.versions[model_name][version] = model_version

        # Save registry
        self._save_registry()

        self.logger.info(f"Registered model version: {model_name} v{version}")
        return model_version

    def get_model_versions(self, model_name: str) -> List[ModelVersion]:
        """
        Gets all versions of a model.

        Args:
            model_name: Name of the model.

        Returns:
            List of ModelVersion objects sorted by version.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        
        if model_name not in self.versions:
            return []

        versions = list(self.versions[model_name].values())
        # Sort by version string (simple sorting for V2 compliance)
        versions.sort(key=lambda v: v.version, reverse=True)
        return versions

    def get_latest_version(self, model_name: str, status_filter: Optional[VersionStatus] = None) -> Optional[ModelVersion]:
        """
        Gets the latest version of a model.

        Args:
            model_name: Name of the model.
            status_filter: Optional status filter.

        Returns:
            Latest ModelVersion or None if not found.
        """
        versions = self.get_model_versions(model_name)
        if not versions:
            return None

        if status_filter:
            versions = [v for v in versions if v.status == status_filter]

        return versions[0] if versions else None

    def update_version_status(self, model_name: str, version: str, status: VersionStatus) -> bool:
        """
        Updates the status of a model version.

        Args:
            model_name: Name of the model.
            version: Version string.
            status: New status.

        Returns:
            True if successfully updated, False otherwise.
        """
        if not model_name or not version:
            return False
        
        if model_name not in self.versions or version not in self.versions[model_name]:
            return False

        self.versions[model_name][version].status = status
        self._save_registry()
        
        self.logger.info(f"Updated status for {model_name} v{version}: {status.value}")
        return True

    def promote_version(self, model_name: str, version: str, target_status: VersionStatus) -> bool:
        """
        Promotes a model version to a new status.

        Args:
            model_name: Name of the model.
            version: Version string.
            target_status: Target status for promotion.

        Returns:
            True if successfully promoted, False otherwise.
        """
        if not model_name or not version:
            return False
        
        if model_name not in self.versions or version not in self.versions[model_name]:
            return False

        current_version = self.versions[model_name][version]
        
        # Validate promotion path
        if target_status == VersionStatus.PRODUCTION:
            # Can only promote from staging to production
            if current_version.status != VersionStatus.STAGING:
                self.logger.warning(f"Cannot promote {model_name} v{version} from {current_version.status.value} to production")
                return False
        elif target_status == VersionStatus.STAGING:
            # Can promote from draft to staging
            if current_version.status != VersionStatus.DRAFT:
                self.logger.warning(f"Cannot promote {model_name} v{version} from {current_version.status.value} to staging")
                return False

        return self.update_version_status(model_name, version, target_status)

    def deprecate_version(self, model_name: str, version: str, reason: Optional[str] = None) -> bool:
        """
        Deprecates a model version.

        Args:
            model_name: Name of the model.
            version: Version string.
            reason: Optional reason for deprecation.

        Returns:
            True if successfully deprecated, False otherwise.
        """
        if not model_name or not version:
            return False
        
        if model_name not in self.versions or version not in self.versions[model_name]:
            return False

        success = self.update_version_status(model_name, version, VersionStatus.DEPRECATED)
        if success and reason:
            # Add deprecation reason to description
            version_obj = self.versions[model_name][version]
            if version_obj.description:
                version_obj.description += f"\n\nDeprecated: {reason}"
            else:
                version_obj.description = f"Deprecated: {reason}"
            self._save_registry()

        return success

    def compare_versions(self, model_name: str, version1: str, version2: str) -> Dict[str, Any]:
        """
        Compares two versions of a model.

        Args:
            model_name: Name of the model.
            version1: First version to compare.
            version2: Second version to compare.

        Returns:
            Comparison results dictionary.
        """
        if not model_name or not version1 or not version2:
            raise ValueError("Model name and both versions are required.")

        if (model_name not in self.versions or 
            version1 not in self.versions[model_name] or 
            version2 not in self.versions[model_name]):
            raise ValueError("One or both versions not found.")

        v1 = self.versions[model_name][version1]
        v2 = self.versions[model_name][version2]

        return {
            "model_name": model_name,
            "version1": {
                "version": version1,
                "created_at": v1.created_at.isoformat(),
                "status": v1.status.value,
                "file_size": v1.file_size,
                "metrics": v1.metrics
            },
            "version2": {
                "version": version2,
                "created_at": v2.created_at.isoformat(),
                "status": v2.status.value,
                "file_size": v2.file_size,
                "metrics": v2.metrics
            },
            "comparison": {
                "file_size_diff": v2.file_size - v1.file_size,
                "created_time_diff": (v2.created_at - v1.created_at).total_seconds(),
                "same_framework": v1.framework == v2.framework,
                "same_creator": v1.created_by == v2.created_by
            }
        }

    def get_registry_summary(self) -> Dict[str, Any]:
        """
        Gets a summary of the model registry.

        Returns:
            Registry summary dictionary.
        """
        total_models = len(self.versions)
        total_versions = sum(len(versions) for versions in self.versions.values())
        
        status_counts = {}
        for versions in self.versions.values():
            for version in versions.values():
                status = version.status.value
                status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "total_models": total_models,
            "total_versions": total_versions,
            "status_distribution": status_counts,
            "registry_file": self.registry_file,
            "last_updated": datetime.utcnow().isoformat()
        }
