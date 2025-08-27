"""Model registry operations for ModelManager."""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional


class RegistryMixin:
    """Mixin handling model registry persistence and operations."""

    storage_path: any
    models: Dict[str, Dict[str, Any]]
    model_operations: List[Dict[str, Any]]

    def _load_model_registry(self) -> None:
        """Load the model registry from disk."""
        try:
            registry_path = self.storage_path / "model_registry.json"
            if registry_path.exists():
                with open(registry_path, "r") as f:
                    self.models = json.load(f)
                self.record_operation("load_model_registry", True, 0.0)
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error loading model registry: {e}")
            self.record_operation("load_model_registry", False, 0.0)

    def _save_model_registry(self) -> None:
        """Save the model registry to disk."""
        try:
            registry_path = self.storage_path / "model_registry.json"
            with open(registry_path, "w") as f:
                json.dump(self.models, f, indent=2)
            self.record_operation("save_model_registry", True, 0.0)
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error saving model registry: {e}")
            self.record_operation("save_model_registry", False, 0.0)

    def register_model(self, model_id: str, model_info: Dict[str, Any]) -> bool:
        """Register a new model."""
        try:
            start_time = datetime.now()
            self.models[model_id] = {
                **model_info,
                "registered_at": datetime.now().isoformat(),
                "status": "registered",
            }
            self._save_model_registry()
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "register",
                "model_id": model_id,
                "model_info": model_info,
            }
            self.model_operations.append(operation_record)
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("register_model", True, operation_time)
            self.logger.info(f"Registered model: {model_id}")
            return True
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error registering model {model_id}: {e}")
            self.record_operation("register_model", False, 0.0)
            return False

    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a registered model."""
        try:
            model_info = self.models.get(model_id)
            self.record_operation("get_model_info", True, 0.0)
            return model_info
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error getting model info for {model_id}: {e}")
            self.record_operation("get_model_info", False, 0.0)
            return None

    def update_model_status(self, model_id: str, status: str) -> bool:
        """Update the status of a model."""
        try:
            start_time = datetime.now()
            if model_id in self.models:
                self.models[model_id]["status"] = status
                self.models[model_id]["updated_at"] = datetime.now().isoformat()
                self._save_model_registry()
                operation_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "update_status",
                    "model_id": model_id,
                    "new_status": status,
                }
                self.model_operations.append(operation_record)
                operation_time = (datetime.now() - start_time).total_seconds()
                self.record_operation("update_model_status", True, operation_time)
                return True
            self.record_operation("update_model_status", False, 0.0)
            return False
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error updating model status for {model_id}: {e}")
            self.record_operation("update_model_status", False, 0.0)
            return False

    def list_models(self, status_filter: Optional[str] = None) -> List[str]:
        """List models, optionally filtered by status."""
        try:
            if status_filter:
                model_ids = [
                    mid
                    for mid, info in self.models.items()
                    if info.get("status") == status_filter
                ]
            else:
                model_ids = list(self.models.keys())
            self.record_operation("list_models", True, 0.0)
            return model_ids
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error listing models: {e}")
            self.record_operation("list_models", False, 0.0)
            return []

    def delete_model(self, model_id: str) -> bool:
        """Delete a model registration."""
        try:
            start_time = datetime.now()
            if model_id in self.models:
                del self.models[model_id]
                self._save_model_registry()
                operation_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "delete",
                    "model_id": model_id,
                }
                self.model_operations.append(operation_record)
                operation_time = (datetime.now() - start_time).total_seconds()
                self.record_operation("delete_model", True, operation_time)
                self.logger.info(f"Deleted model registration: {model_id}")
                return True
            self.record_operation("delete_model", False, 0.0)
            return False
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error deleting model {model_id}: {e}")
            self.record_operation("delete_model", False, 0.0)
            return False
