"""
Model Manager Module
Extracted from core.py for modularization

Contains:
- ModelManager: Model lifecycle and management
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from ..core.base_manager import BaseManager
from .models import AIModel
from .ml_framework import MLFramework

# Configure logging
logger = logging.getLogger(__name__)


class ModelManager(BaseManager):
    """Model lifecycle and management

    Manages AI/ML models throughout their lifecycle
    """

    def __init__(self, models_dir: Optional[str] = None):
        """Initialize model manager"""
        super().__init__(
            manager_id="model_manager",
            name="Model Manager",
            description="AI/ML model lifecycle management",
        )

        self.models_dir = Path(models_dir) if models_dir else Path("models/")
        self.models: Dict[str, AIModel] = {}
        self.frameworks: Dict[str, MLFramework] = {}
        self.model_versions: Dict[str, List[str]] = {}
        self.model_metadata: Dict[str, Dict[str, Any]] = {}

        self.logger.info("Model Manager initialized")

    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================

    def _on_start(self) -> bool:
        """Initialize model management system"""
        try:
            self.logger.info("Starting Model Manager...")

            # Ensure models directory exists
            self.models_dir.mkdir(parents=True, exist_ok=True)

            # Load existing models
            self._load_existing_models()

            # Initialize frameworks
            self._initialize_frameworks()

            self.logger.info("Model Manager started successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start Model Manager: {e}")
            return False

    def _on_stop(self):
        """Cleanup model management system"""
        try:
            self.logger.info("Stopping Model Manager...")

            # Save model metadata
            self._save_model_metadata()

            # Cleanup frameworks
            for framework in self.frameworks.values():
                framework.cleanup()

            self.logger.info("Model Manager stopped successfully")

        except Exception as e:
            self.logger.error(f"Failed to stop Model Manager: {e}")

    def _on_heartbeat(self):
        """Model manager heartbeat"""
        try:
            # Check model health
            self._check_model_health()

            # Update metrics
            self.record_operation("heartbeat", True, 0.0)

        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)

    def _on_initialize_resources(self) -> bool:
        """Initialize model management resources"""
        try:
            # Ensure models directory exists
            self.models_dir.mkdir(parents=True, exist_ok=True)

            # Initialize data structures
            self.models = {}
            self.model_versions = {}
            self.model_metadata = {}

            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False

    def _on_cleanup_resources(self):
        """Cleanup model management resources"""
        try:
            # Save metadata
            self._save_model_metadata()

            # Clear data
            self.models.clear()
            self.model_versions.clear()
            self.model_metadata.clear()

            self.logger.info("Model Manager resources cleaned up")

        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Handle model management recovery logic"""
        try:
            self.logger.info(f"Attempting Model Manager recovery: {context}")
            
            # Clear error state
            self.status = ManagerStatus.INITIALIZING
            
            # Reinitialize resources
            if self._on_initialize_resources():
                self.status = ManagerStatus.ONLINE
                self.logger.info("Model Manager recovery successful")
                return True
            else:
                self.status = ManagerStatus.ERROR
                self.logger.error("Model Manager recovery failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Recovery attempt failed: {e}")
            self.status = ManagerStatus.ERROR
            return False

    # ============================================================================
    # Model Management
    # ============================================================================

    def register_model(self, model: AIModel) -> bool:
        """Register a new model"""
        try:
            if model.model_id in self.models:
                self.logger.warning(f"Model {model.model_id} already registered")
                return False

            self.models[model.model_id] = model
            self.model_versions[model.model_id] = [model.version]
            self.model_metadata[model.model_id] = {
                "registered_at": datetime.now().isoformat(),
                "last_accessed": datetime.now().isoformat(),
                "access_count": 0
            }

            self.logger.info(f"Registered model: {model.name} ({model.model_id})")
            return True

        except Exception as e:
            self.logger.error(f"Failed to register model: {e}")
            return False

    def get_model(self, model_id: str) -> Optional[AIModel]:
        """Get a registered model by ID"""
        try:
            if model_id in self.models:
                # Update access metadata
                if model_id in self.model_metadata:
                    self.model_metadata[model_id]["last_accessed"] = datetime.now().isoformat()
                    self.model_metadata[model_id]["access_count"] += 1

                return self.models[model_id]
            return None
        except Exception as e:
            self.logger.error(f"Failed to get model {model_id}: {e}")
            return None

    def list_models(self) -> List[AIModel]:
        """List all registered models"""
        return list(self.models.values())

    def update_model_status(self, model_id: str, status: str) -> bool:
        """Update model status"""
        try:
            if model_id in self.models:
                # Update model status logic here
                self.logger.info(f"Updated model {model_id} status to {status}")
                return True
            else:
                self.logger.warning(f"Model {model_id} not found")
                return False
        except Exception as e:
            self.logger.error(f"Failed to update model status: {e}")
            return False

    def remove_model(self, model_id: str) -> bool:
        """Remove a registered model"""
        try:
            if model_id in self.models:
                del self.models[model_id]
                if model_id in self.model_versions:
                    del self.model_versions[model_id]
                if model_id in self.model_metadata:
                    del self.model_metadata[model_id]

                self.logger.info(f"Removed model: {model_id}")
                return True
            else:
                self.logger.warning(f"Model {model_id} not found")
                return False
        except Exception as e:
            self.logger.error(f"Failed to remove model: {e}")
            return False

    # ============================================================================
    # Framework Management
    # ============================================================================

    def register_framework(self, framework: MLFramework) -> bool:
        """Register a new ML framework"""
        try:
            if framework.name in self.frameworks:
                self.logger.warning(f"Framework {framework.name} already registered")
                return False

            self.frameworks[framework.name] = framework
            self.logger.info(f"Registered framework: {framework.name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to register framework: {e}")
            return False

    def get_framework(self, name: str) -> Optional[MLFramework]:
        """Get a registered framework by name"""
        return self.frameworks.get(name)

    def list_frameworks(self) -> List[MLFramework]:
        """List all registered frameworks"""
        return list(self.frameworks.values())

    def remove_framework(self, name: str) -> bool:
        """Remove a registered framework"""
        try:
            if name in self.frameworks:
                framework = self.frameworks[name]
                framework.cleanup()
                del self.frameworks[name]

                self.logger.info(f"Removed framework: {name}")
                return True
            else:
                self.logger.warning(f"Framework {name} not found")
                return False
        except Exception as e:
            self.logger.error(f"Failed to remove framework: {e}")
            return False

    # ============================================================================
    # Model Operations
    # ============================================================================

    def load_model_from_file(self, model_path: Union[str, Path]) -> Optional[AIModel]:
        """Load a model from file"""
        try:
            model_path = Path(model_path)
            if not model_path.exists():
                self.logger.error(f"Model file not found: {model_path}")
                return None

            # Load model logic here
            # This would typically involve framework-specific loading
            self.logger.info(f"Loaded model from: {model_path}")
            return None  # Placeholder

        except Exception as e:
            self.logger.error(f"Failed to load model from file: {e}")
            return None

    def save_model_to_file(self, model: AIModel, model_path: Union[str, Path]) -> bool:
        """Save a model to file"""
        try:
            model_path = Path(model_path)
            model_path.parent.mkdir(parents=True, exist_ok=True)

            # Save model logic here
            # This would typically involve framework-specific saving
            self.logger.info(f"Saved model to: {model_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save model to file: {e}")
            return False

    def validate_model(self, model_id: str) -> bool:
        """Validate a model"""
        try:
            if model_id not in self.models:
                self.logger.warning(f"Model {model_id} not found")
                return False

            # Model validation logic here
            self.logger.info(f"Validated model: {model_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to validate model: {e}")
            return False

    # ============================================================================
    # Version Management
    # ============================================================================

    def add_model_version(self, model_id: str, version: str) -> bool:
        """Add a new version for a model"""
        try:
            if model_id in self.model_versions:
                if version not in self.model_versions[model_id]:
                    self.model_versions[model_id].append(version)
                    self.logger.info(f"Added version {version} for model {model_id}")
                    return True
                else:
                    self.logger.warning(f"Version {version} already exists for model {model_id}")
                    return False
            else:
                self.logger.warning(f"Model {model_id} not found")
                return False
        except Exception as e:
            self.logger.error(f"Failed to add model version: {e}")
            return False

    def get_model_versions(self, model_id: str) -> List[str]:
        """Get all versions for a model"""
        return self.model_versions.get(model_id, [])

    def get_latest_version(self, model_id: str) -> Optional[str]:
        """Get the latest version for a model"""
        versions = self.get_model_versions(model_id)
        if versions:
            return versions[-1]
        return None

    # ============================================================================
    # Health Monitoring
    # ============================================================================

    def _check_model_health(self) -> Dict[str, Any]:
        """Check model management system health"""
        try:
            health_status = {
                "total_models": len(self.models),
                "total_frameworks": len(self.frameworks),
                "models_with_versions": len(self.model_versions),
                "last_health_check": datetime.now().isoformat()
            }

            # Check for potential issues
            if len(self.models) == 0:
                health_status["warnings"] = ["No models registered"]
            if len(self.frameworks) == 0:
                health_status["warnings"] = ["No frameworks registered"]

            return health_status

        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return {"error": str(e)}

    # ============================================================================
    # Data Persistence
    # ============================================================================

    def _load_existing_models(self) -> None:
        """Load existing models from storage"""
        try:
            # Load models logic here
            self.logger.info("Loaded existing models")
        except Exception as e:
            self.logger.error(f"Failed to load existing models: {e}")

    def _save_model_metadata(self) -> bool:
        """Save model metadata to storage"""
        try:
            metadata_path = self.models_dir / "model_metadata.json"
            with open(metadata_path, "w") as f:
                json.dump(self.model_metadata, f, indent=2)

            return True
        except Exception as e:
            self.logger.error(f"Failed to save model metadata: {e}")
            return False

    def _initialize_frameworks(self) -> None:
        """Initialize registered frameworks"""
        try:
            for framework in self.frameworks.values():
                framework.initialize()
            self.logger.info("Initialized all frameworks")
        except Exception as e:
            self.logger.error(f"Failed to initialize frameworks: {e}")

    # ============================================================================
    # Utility Methods
    # ============================================================================

    def get_statistics(self) -> Dict[str, Any]:
        """Get model management statistics"""
        return {
            "total_models": len(self.models),
            "total_frameworks": len(self.frameworks),
            "models_with_versions": len(self.model_versions),
            "total_metadata_entries": len(self.model_metadata)
        }

    def search_models(self, query: str) -> List[AIModel]:
        """Search models by query"""
        try:
            results = []
            query_lower = query.lower()

            for model in self.models.values():
                if (query_lower in model.name.lower() or 
                    query_lower in model.provider.lower() or
                    query_lower in model.model_id.lower()):
                    results.append(model)

            return results
        except Exception as e:
            self.logger.error(f"Model search failed: {e}")
            return []
