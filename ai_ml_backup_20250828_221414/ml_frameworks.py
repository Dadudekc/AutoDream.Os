"""Lightweight ML framework stubs for testing.

This module provides minimal placeholder implementations of the
:class:`~src.ai_ml.core.MLFramework` API so that the rest of the system
can be imported during tests without requiring heavy ML dependencies.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .core import MLFramework


class _BaseStubFramework(MLFramework):
    """Simple concrete implementation that performs no real ML work."""

    def __init__(self, name: str) -> None:
        super().__init__(name, version="stub")

    def initialize(self) -> bool:  # pragma: no cover - trivial
        self.is_initialized = True
        return True

    def create_model(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
        return {"config": model_config}

    def train_model(self, model: Dict[str, Any], data: Any, **kwargs) -> Dict[str, Any]:
        return {"model": model, "history": {}}

    def save_model(self, model: Dict[str, Any], path: str) -> bool:
        return True

    def load_model(self, path: str) -> Dict[str, Any]:
        return {"loaded_from": path}


class PyTorchFramework(_BaseStubFramework):
    def __init__(self) -> None:
        super().__init__("pytorch")


class TensorFlowFramework(_BaseStubFramework):
    def __init__(self) -> None:
        super().__init__("tensorflow")


class ScikitLearnFramework(_BaseStubFramework):
    def __init__(self) -> None:
        super().__init__("scikit-learn")


class JAXFramework(_BaseStubFramework):
    def __init__(self) -> None:
        super().__init__("jax")


class MLFrameworkManager:
    """Registry and factory for available frameworks."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.frameworks = {
            "pytorch": PyTorchFramework(),
            "tensorflow": TensorFlowFramework(),
            "scikit-learn": ScikitLearnFramework(),
            "jax": JAXFramework(),
        }

    def get_framework(self, name: str) -> Optional[MLFramework]:
        return self.frameworks.get(name)

    def list_frameworks(self) -> Dict[str, MLFramework]:  # pragma: no cover - trivial
        return self.frameworks


__all__ = [
    "MLFrameworkManager",
    "PyTorchFramework",
    "TensorFlowFramework",
    "ScikitLearnFramework",
    "JAXFramework",
]
