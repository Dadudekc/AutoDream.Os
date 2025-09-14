from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class OrchestrationContext:
    """SSOT: shared context object injected everywhere (DIP)."""

    config: Mapping[str, Any]
    emit: Callable[[str, dict[str, Any]], None]  # event bus callback
    logger: Callable[[str], None]


@dataclass
class OrchestrationResult:
    ok: bool
    summary: str
    metrics: dict[str, Any]


class Step(Protocol):
    """Unit of orchestration work."""

    def name(self) -> str: ...
    def run(self, ctx: OrchestrationContext, payload: dict[str, Any]) -> dict[str, Any]: ...


class Orchestrator(Protocol):
    """Stable contract (LSP)."""

    def plan(self, ctx: OrchestrationContext, payload: dict[str, Any]) -> Iterable[Step]: ...
    def execute(
        self, ctx: OrchestrationContext, payload: dict[str, Any]
    ) -> OrchestrationResult: ...
    def report(self, result: OrchestrationResult) -> str: ...
