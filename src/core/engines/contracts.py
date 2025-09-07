from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Protocol, Optional, List
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class EngineContext:
    """SSOT: shared context object for all engines (DIP)."""

    config: Dict[str, Any]
    logger: Any
    metrics: Dict[str, Any]


@dataclass
class EngineResult:
    """Standard result format for all engines."""

    success: bool
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    error: Optional[str] = None


class Engine(Protocol):
    """Base engine protocol - all engines must implement this."""

    def initialize(self, context: EngineContext) -> bool: ...
    def execute(
        self, context: EngineContext, payload: Dict[str, Any]
    ) -> EngineResult: ...
    def cleanup(self, context: EngineContext) -> bool: ...
    def get_status(self) -> Dict[str, Any]: ...


class MLEngine(Engine):
    """ML operations engine protocol."""

    def train_model(
        self, context: EngineContext, data: Dict[str, Any]
    ) -> EngineResult: ...
    def predict(
        self, context: EngineContext, input_data: Dict[str, Any]
    ) -> EngineResult: ...
    def optimize(
        self, context: EngineContext, config: Dict[str, Any]
    ) -> EngineResult: ...


class AnalysisEngine(Engine):
    """Analysis operations engine protocol."""

    def analyze(self, context: EngineContext, data: Dict[str, Any]) -> EngineResult: ...
    def extract_patterns(
        self, context: EngineContext, data: Dict[str, Any]
    ) -> EngineResult: ...
    def detect_violations(
        self, context: EngineContext, data: Dict[str, Any]
    ) -> EngineResult: ...


class IntegrationEngine(Engine):
    """Integration operations engine protocol."""

    def connect(
        self, context: EngineContext, config: Dict[str, Any]
    ) -> EngineResult: ...
    def sync(self, context: EngineContext, data: Dict[str, Any]) -> EngineResult: ...
    def transform(
        self, context: EngineContext, data: Dict[str, Any]
    ) -> EngineResult: ...


class CoordinationEngine(Engine):
    """Coordination operations engine protocol."""

    def coordinate(
        self, context: EngineContext, tasks: List[Dict[str, Any]]
    ) -> EngineResult: ...
    def schedule(
        self, context: EngineContext, schedule: Dict[str, Any]
    ) -> EngineResult: ...
    def monitor(self, context: EngineContext, targets: List[str]) -> EngineResult: ...


class UtilityEngine(Engine):
    """Utility operations engine protocol."""

    def process(self, context: EngineContext, data: Dict[str, Any]) -> EngineResult: ...
    def validate(
        self, context: EngineContext, data: Dict[str, Any]
    ) -> EngineResult: ...
    def transform(
        self, context: EngineContext, data: Dict[str, Any]
    ) -> EngineResult: ...
