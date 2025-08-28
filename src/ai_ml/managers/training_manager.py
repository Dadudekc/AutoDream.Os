from __future__ import annotations

"""Training orchestration built around dependency injection."""

from typing import Any, Dict

from ai_ml.ai_ml_common import DataService, TrainingFramework


class TrainingManager:
    """Coordinate data retrieval and model training.

    Parameters
    ----------
    framework:
        Underlying machine-learning framework implementation.
    data_service:
        Service used to retrieve training data.
    logger:
        Logging interface for status messages.
    """

    def __init__(
        self, framework: TrainingFramework, data_service: DataService, logger: Any
    ) -> None:
        self._framework = framework
        self._data_service = data_service
        self._logger = logger

    def run(self, model_config: Dict[str, Any], data_query: Any) -> Dict[str, Any]:
        """Train a model and return training metadata."""
        self._logger.info("Fetching training data")
        data = self._data_service.fetch(data_query)
        self._logger.info("Creating model")
        model = self._framework.create_model(model_config)
        self._logger.info("Training model")
        result = self._framework.train_model(model, data)
        return result
