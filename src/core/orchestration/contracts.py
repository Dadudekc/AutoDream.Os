from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Protocol, Iterable, Mapping, Optional, Callable


@dataclass(frozen=True)
class OrchestrationContext:
    """SSOT: shared context object injected everywhere (DIP)."""

    config: Mapping[str, Any]
    emit: Callable[[str, Dict[str, Any]], None]  # event bus callback
    logger: Callable[[str], None]


@dataclass
class OrchestrationResult:
    ok: bool
    summary: str
    metrics: Dict[str, Any]


class Step(Protocol):
    """Unit of orchestration work."""

    def name(self) -> str: ...
    def run(
        self, ctx: OrchestrationContext, payload: Dict[str, Any]
    ) -> Dict[str, Any]: ...


class Orchestrator(Protocol):
    """Stable contract (LSP)."""

    def plan(
        self, ctx: OrchestrationContext, payload: Dict[str, Any]
    ) -> Iterable[Step]: ...
    def execute(
        self, ctx: OrchestrationContext, payload: Dict[str, Any]
    ) -> OrchestrationResult: ...
    def report(self, result: OrchestrationResult) -> str: ...
