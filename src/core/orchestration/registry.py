from __future__ import annotations
from typing import Dict, Callable, List
from .contracts import Step


class StepRegistry:
    """DIP registry: high-level depends on abstraction, not concretion."""

    def __init__(self) -> None:
        self._steps: Dict[str, Callable[[], Step]] = {}

    def register(self, key: str, factory: Callable[[], Step]) -> None:
        if key in self._steps:
            raise ValueError(f"duplicate step key: {key}")
        self._steps[key] = factory

    def build(self, keys: List[str]) -> List[Step]:
        return [self._steps[k]() for k in keys if k in self._steps]
