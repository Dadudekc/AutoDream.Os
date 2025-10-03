#!/usr/bin/env python3
"""
Distributed Tracing Operations - Operations Module
==================================================

Operations and utilities for distributed tracing system.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: distributed_tracing_system.py (412 lines) - Operations module
"""

import logging
from datetime import datetime
from typing import Any

from src.tracing.distributed_tracing_core import DistributedTracingCore, TraceConfig

logger = logging.getLogger(__name__)


class TracingMetricsCollector:
    """Collects and manages tracing metrics"""

    def __init__(self):
        """Initialize metrics collector"""
        self.metrics: dict[str, Any] = {}
        self.span_counts: dict[str, int] = {}
        self.error_counts: dict[str, int] = {}

    def manage_metrics(self, action: str, **kwargs) -> Any:
        """Consolidated metrics management"""
        if action == "record_span":
            span_name = kwargs["span_name"]
            self.span_counts[span_name] = self.span_counts.get(span_name, 0) + 1
            return True

        elif action == "record_error":
            error_type = kwargs["error_type"]
            self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
            return True

        elif action == "get_metrics":
            return {
                "total_spans": sum(self.span_counts.values()),
                "span_counts": dict(self.span_counts),
                "total_errors": sum(self.error_counts.values()),
                "error_counts": dict(self.error_counts),
                "timestamp": datetime.now().isoformat(),
            }

        elif action == "reset_metrics":
            self.span_counts.clear()
            self.error_counts.clear()
            return True

        return None


class TracingSpanManager:
    """Manages tracing spans and their lifecycle"""

    def __init__(self):
        """Initialize span manager"""
        self.active_spans: dict[str, Any] = {}
        self.span_history: list[dict[str, Any]] = []
        self.max_history_size = 1000

    def manage_spans(self, action: str, **kwargs) -> Any:
        """Consolidated span management"""
        if action == "register_span":
            span_id = kwargs["span_id"]
            span_info = {
                "name": kwargs["name"],
                "start_time": datetime.now(),
                "attributes": kwargs.get("attributes", {}),
                "status": "active",
            }
            self.active_spans[span_id] = span_info
            return True

        elif action == "complete_span":
            span_id = kwargs["span_id"]
            if span_id in self.active_spans:
                span_info = self.active_spans[span_id]
                span_info["end_time"] = datetime.now()
                span_info["status"] = "completed"

                # Move to history
                self.span_history.append(span_info)

                # Keep history size manageable
                if len(self.span_history) > self.max_history_size:
                    self.span_history = self.span_history[-self.max_history_size :]

                del self.active_spans[span_id]
                return True
            return False

        elif action == "get_active_spans":
            return dict(self.active_spans)

        elif action == "get_span_history":
            return self.span_history.copy()

        elif action == "get_span_stats":
            return {
                "active_spans": len(self.active_spans),
                "total_history": len(self.span_history),
                "span_names": list(set(span["name"] for span in self.span_history)),
            }

        return None


class DistributedTracingService:
    """Main service for distributed tracing operations"""

    def __init__(self, config: TraceConfig = None):
        """Initialize distributed tracing service"""
        self.core = DistributedTracingCore(config)
        self.metrics_collector = TracingMetricsCollector()
        self.span_manager = TracingSpanManager()

    def manage_tracing_operations(self, action: str, **kwargs) -> Any:
        """Consolidated tracing operations"""
        if action == "start_traced_operation":
            span_name = kwargs["name"]
            span_id = f"{span_name}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

            # Start span
            span = self.core.manage_tracing(
                "start_span", name=span_name, attributes=kwargs.get("attributes", {})
            )

            # Register with span manager
            self.span_manager.manage_spans(
                "register_span",
                span_id=span_id,
                name=span_name,
                attributes=kwargs.get("attributes", {}),
            )

            # Record metrics
            self.metrics_collector.manage_metrics("record_span", span_name=span_name)

            return {"span": span, "span_id": span_id}

        elif action == "complete_traced_operation":
            span_id = kwargs["span_id"]
            span = kwargs.get("span")

            # Complete span
            if span:
                self.core.manage_tracing("set_status", span=span, status="OK")

            # Complete in span manager
            self.span_manager.manage_spans("complete_span", span_id=span_id)

            return True

        elif action == "trace_error":
            span_id = kwargs["span_id"]
            span = kwargs.get("span")
            error_type = kwargs["error_type"]
            error_message = kwargs.get("error_message", "")

            # Set error status
            if span:
                self.core.manage_tracing(
                    "set_status", span=span, status="ERROR", description=error_message
                )
                self.core.manage_tracing(
                    "add_event", span=span, name="error", attributes={"error_type": error_type}
                )

            # Record error metrics
            self.metrics_collector.manage_metrics("record_error", error_type=error_type)

            return True

        elif action == "get_tracing_summary":
            core_status = self.core.get_tracing_status()
            metrics = self.metrics_collector.manage_metrics("get_metrics")
            span_stats = self.span_manager.manage_spans("get_span_stats")

            return {**core_status, "metrics": metrics, "span_stats": span_stats}

        return None

    def cleanup_old_data(self, days: int = 7) -> int:
        """Cleanup old tracing data and return count removed"""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)

        initial_count = len(self.span_manager.span_history)

        self.span_manager.span_history = [
            span
            for span in self.span_manager.span_history
            if span.get("start_time", datetime.now()).timestamp() > cutoff_date
        ]

        removed_count = initial_count - len(self.span_manager.span_history)

        logger.info(f"Cleaned up {removed_count} old tracing records")
        return removed_count
