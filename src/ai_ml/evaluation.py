from __future__ import annotations

"""Model evaluation built around dependency injection."""

from typing import Any, Dict, Protocol


class Framework(Protocol):
    """Protocol describing required evaluation behaviour."""

    def evaluate_model(self, model: Any, data: Any) -> Dict[str, float]:
        ...


class DataService(Protocol):
    """Protocol for providing evaluation data."""

    def fetch(self, query: Any) -> Any:
        """Return evaluation data for ``query``."""


class Evaluator:
    """Evaluate models using injected services."""

    def __init__(self, framework: Framework, data_service: DataService, logger: Any) -> None:
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
