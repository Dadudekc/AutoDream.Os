"""Factory for creating message delivery strategies."""

from typing import Callable

from .routing_models import Message


class StrategyFactory:
    """Return delivery strategy callables based on name."""

    def __init__(self, default_strategy: Callable[[Message], bool]) -> None:
        self.default_strategy = default_strategy

    def get_strategy(self, name: str) -> Callable[[Message], bool]:
        """Return a strategy implementation."""
        strategies = {
            "broadcast": self.default_strategy,
            "round_robin": self.default_strategy,
            "specific": self.default_strategy,
        }
        return strategies.get(name, self.default_strategy)
