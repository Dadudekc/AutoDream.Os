from typing import Any, Dict

from __future__ import annotations
from ai_ml.ai_ml_common import DataService, EvaluationFramework


"""Model evaluation built around dependency injection."""




class EvaluationManager:
    """Evaluate models using injected services."""

    def __init__(
        self, framework: EvaluationFramework, data_service: DataService, logger: Any
    ) -> None:
        self._framework = framework
        self._data_service = data_service
        self._logger = logger

    def run(self, model: Any, data_query: Any) -> Dict[str, float]:
        """Evaluate ``model`` and return metrics."""
        self._logger.info("Fetching evaluation data")
        data = self._data_service.fetch(data_query)
        self._logger.info("Evaluating model")
        metrics = self._framework.evaluate_model(model, data)
        return metrics
