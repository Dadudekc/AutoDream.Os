#!/usr/bin/env python3
"""
Analytics Interfaces - V2 Compliant Module
=========================================

Abstract interfaces for unified analytics system.
V2 COMPLIANT: Focused interfaces under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from ..models.analytics_enums import (
    AnalyticsStatus,
    AnalyticsType,
    IntelligenceType,
    ProcessingMode,
)
from ..models.analytics_models import (
    AnalyticsData,
    AnalyticsInfo,
    AnalyticsMetrics,
    AnalyticsResult,
)


class AnalyticsEngine(ABC):
    """Base analytics engine interface."""

    def __init__(self, analytics_id: str, name: str, analytics_type: AnalyticsType):
        self.analytics_id = analytics_id
        self.name = name
        self.analytics_type = analytics_type
        self.status = AnalyticsStatus.INITIALIZING
        self.logger = logging.getLogger(f"analytics.{name}")
        self.metrics = AnalyticsMetrics(analytics_id=analytics_id)

    @abstractmethod
    def start(self) -> bool:
        """Start the analytics engine."""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Stop the analytics engine."""
        pass

    @abstractmethod
    def process_data(self, data: AnalyticsData) -> AnalyticsResult:
        """Process analytics data."""
        pass

    @abstractmethod
    def get_capabilities(self) -> list[str]:
        """Get analytics capabilities."""
        pass

    def update_metrics(self, processing_time: float, success: bool) -> None:
        """Update analytics metrics."""
        self.metrics.total_processed += 1
        if success:
            self.metrics.successful_processed += 1
        else:
            self.metrics.failed_processed += 1

        # Update average processing time
        total_time = self.metrics.average_processing_time * (self.metrics.total_processed - 1)
        self.metrics.average_processing_time = (
            total_time + processing_time
        ) / self.metrics.total_processed
        self.metrics.last_updated = datetime.now()


class IntelligenceEngine(AnalyticsEngine):
    """Intelligence analytics engine interface."""

    def __init__(self, analytics_id: str, name: str, intelligence_type: IntelligenceType):
        super().__init__(analytics_id, name, AnalyticsType.INTELLIGENCE)
        self.intelligence_type = intelligence_type

    @abstractmethod
    def analyze_patterns(self, data: AnalyticsData) -> AnalyticsResult:
        """Analyze patterns in data."""
        pass

    @abstractmethod
    def detect_anomalies(self, data: AnalyticsData) -> AnalyticsResult:
        """Detect anomalies in data."""
        pass

    @abstractmethod
    def generate_insights(self, data: AnalyticsData) -> AnalyticsResult:
        """Generate insights from data."""
        pass


class ProcessingEngine(AnalyticsEngine):
    """Data processing analytics engine interface."""

    def __init__(self, analytics_id: str, name: str, processing_mode: ProcessingMode):
        super().__init__(analytics_id, name, AnalyticsType.PROCESSING)
        self.processing_mode = processing_mode

    @abstractmethod
    def validate_data(self, data: AnalyticsData) -> bool:
        """Validate input data."""
        pass

    @abstractmethod
    def transform_data(self, data: AnalyticsData) -> AnalyticsData:
        """Transform data for processing."""
        pass

    @abstractmethod
    def aggregate_results(self, results: list[AnalyticsResult]) -> AnalyticsResult:
        """Aggregate multiple results."""
        pass


# Export all interfaces for easy import
__all__ = [
    "AnalyticsEngine",
    "IntelligenceEngine",
    "ProcessingEngine",
]
