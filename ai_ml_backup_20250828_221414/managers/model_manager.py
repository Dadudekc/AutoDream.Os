from typing import Any

from __future__ import annotations
from ai_ml.ai_ml_common import ModelStore


"""Utilities for managing the lifecycle of ML models."""




class ModelManager:
    """Handle saving and loading models.

    Parameters
    ----------
    logger:
        Logging interface used for status messages.
    store:
        Data access component used for persisting models.
    """

    def __init__(self, logger: Any, store: ModelStore) -> None:
        self._logger = logger
        self._store = store

    def save(self, model: Any, path: str) -> None:
        """Persist ``model`` to ``path`` using the injected store."""
        self._logger.info("Saving model to %s", path)
        self._store.save(model, path)

    def load(self, path: str) -> Any:
        """Load and return a model from ``path`` using the injected store."""
        self._logger.info("Loading model from %s", path)
        return self._store.load(path)
