from __future__ import annotations

"""Utilities for managing the lifecycle of ML models."""

from typing import Any, Protocol


class ModelStore(Protocol):
    """Protocol defining how models are persisted."""

    def save(self, model: Any, path: str) -> None:
        """Persist a model at ``path``."""

    def load(self, path: str) -> Any:
        """Retrieve a model from ``path``."""


class ModelLifecycle:
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
