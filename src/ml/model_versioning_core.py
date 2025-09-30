import hashlib
import json
import logging
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any


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
    description: str | None = None
    tags: list[str] | None = None
    metrics: dict[str, Any] | None = None
    dependencies: dict[str, str] | None = None


class ModelVersioningCore:
    """
    Core ML model versioning functionality.
    Manages model metadata tracking and basic lifecycle operations.
    """

    def __init__(self, model_path: str = "/app/models", registry_path: str = "/app/registry"):
        """Initialize the ModelVersioningCore system."""
        self.model_path = model_path
        self.registry_path = registry_path
        self.logger = logging.getLogger(__name__)
        
        # Ensure directories exist
        os.makedirs(self.model_path, exist_ok=True)
        os.makedirs(self.registry_path, exist_ok=True)

    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""

    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            self.logger.error(f"Error getting file size for {file_path}: {e}")
            return 0

    def create_version(self, model_name: str, version: str, framework: str, 
                      file_path: str, created_by: str, description: str = None,
                      tags: list[str] = None, metrics: dict[str, Any] = None,
                      dependencies: dict[str, str] = None) -> ModelVersion:
        """Create a new model version."""
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Model file not found: {file_path}")
            
            # Calculate metadata
            file_hash = self.calculate_file_hash(file_path)
            file_size = self.get_file_size(file_path)
            
            # Create version object
            version_obj = ModelVersion(
                model_name=model_name,
                version=version,
                framework=framework,
                file_path=file_path,
                file_hash=file_hash,
                file_size=file_size,
                created_at=datetime.now(),
                created_by=created_by,
                status=VersionStatus.DRAFT,
                description=description,
                tags=tags or [],
                metrics=metrics or {},
                dependencies=dependencies or {}
            )
            
            # Save to registry
            self._save_version_to_registry(version_obj)
            
            self.logger.info(f"Created version {version} for model {model_name}")
            return version_obj
            
        except Exception as e:
            self.logger.error(f"Error creating version: {e}")
            raise

    def get_version(self, model_name: str, version: str) -> ModelVersion | None:
        """Get a specific model version."""
        try:
            registry_file = os.path.join(self.registry_path, f"{model_name}_{version}.json")
            if not os.path.exists(registry_file):
                return None
                
            with open(registry_file, 'r') as f:
                data = json.load(f)
                
            # Convert datetime string back to datetime object
            data['created_at'] = datetime.fromisoformat(data['created_at'])
            data['status'] = VersionStatus(data['status'])
            
            return ModelVersion(**data)
            
        except Exception as e:
            self.logger.error(f"Error getting version: {e}")
            return None

    def list_versions(self, model_name: str) -> list[ModelVersion]:
        """List all versions for a model."""
        try:
            versions = []
            for filename in os.listdir(self.registry_path):
                if filename.startswith(f"{model_name}_") and filename.endswith('.json'):
                    version_str = filename.replace(f"{model_name}_", "").replace('.json', '')
                    version = self.get_version(model_name, version_str)
                    if version:
                        versions.append(version)
            
            # Sort by creation date (newest first)
            versions.sort(key=lambda v: v.created_at, reverse=True)
            return versions
            
        except Exception as e:
            self.logger.error(f"Error listing versions: {e}")
            return []

    def update_version_status(self, model_name: str, version: str, 
                            status: VersionStatus) -> bool:
        """Update the status of a model version."""
        try:
            version_obj = self.get_version(model_name, version)
            if not version_obj:
                return False
                
            version_obj.status = status
            self._save_version_to_registry(version_obj)
            
            self.logger.info(f"Updated status for {model_name} v{version} to {status.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating version status: {e}")
            return False

    def delete_version(self, model_name: str, version: str) -> bool:
        """Delete a model version."""
        try:
            registry_file = os.path.join(self.registry_path, f"{model_name}_{version}.json")
            if os.path.exists(registry_file):
                os.remove(registry_file)
                self.logger.info(f"Deleted version {version} for model {model_name}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error deleting version: {e}")
            return False

    def _save_version_to_registry(self, version: ModelVersion) -> None:
        """Save version to registry file."""
        try:
            registry_file = os.path.join(self.registry_path, f"{version.model_name}_{version.version}.json")
            
            # Convert to dict for JSON serialization
            data = asdict(version)
            data['created_at'] = version.created_at.isoformat()
            data['status'] = version.status.value
            
            with open(registry_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving version to registry: {e}")
            raise
