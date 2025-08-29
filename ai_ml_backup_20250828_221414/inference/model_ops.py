"""Model registry operations for AIManager."""

from datetime import datetime
from typing import List, Optional

from ..models import AIModel


class ModelOpsMixin:
    """Mixin providing model registry operations."""

    models: dict
    model_registrations: list

    def register_model(self, model: AIModel) -> bool:
        """Register an AI model."""
        try:
            start_time = datetime.now()
            self.models[model.name] = model
            registration_record = {
                "timestamp": datetime.now().isoformat(),
                "model_name": model.name,
                "provider": model.provider,
                "model_id": model.model_id,
                "version": model.version,
            }
            self.model_registrations.append(registration_record)
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("register_model", True, operation_time)
            self.logger.info(f"Registered model: {model.name}")
            return True
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error registering model {model.name}: {e}")
            self.record_operation("register_model", False, 0.0)
            return False

    def get_model(self, model_name: str) -> Optional[AIModel]:
        """Get a registered model by name."""
        try:
            model = self.models.get(model_name)
            self.record_operation("get_model", True, 0.0)
            return model
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error getting model {model_name}: {e}")
            self.record_operation("get_model", False, 0.0)
            return None

    def list_models(self) -> List[str]:
        """List all registered model names."""
        try:
            model_names = list(self.models.keys())
            self.record_operation("list_models", True, 0.0)
            return model_names
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error listing models: {e}")
            self.record_operation("list_models", False, 0.0)
            return []
