#!/usr/bin/env python3
"""
Distributed Tracing Core - Core Logic Module
============================================

Core logic for distributed tracing system.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: distributed_tracing_system.py (412 lines) - Core module
"""

import logging
from datetime import datetime
from typing import Any

# OpenTelemetry imports
try:
    from opentelemetry import trace
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    print("⚠️ OpenTelemetry not available - using fallback tracing")

logger = logging.getLogger(__name__)


class TraceConfig:
    """Configuration for distributed tracing"""

    def __init__(self):
        self.service_name = "agent-swarm"
        self.jaeger_endpoint = "http://localhost:14268/api/traces"
        self.sampling_rate = 1.0


class DistributedTracingCore:
    """Core distributed tracing functionality"""

    def __init__(self, config: TraceConfig = None):
        """Initialize distributed tracing core"""
        self.config = config or TraceConfig()
        self.tracer_provider = None
        self.tracer = None
        self._initialize_tracing()

    def manage_tracing(self, action: str, **kwargs) -> Any:
        """Consolidated tracing operations"""
        if action == "start_span":
            name = kwargs["name"]
            attributes = kwargs.get("attributes", {})

            if OPENTELEMETRY_AVAILABLE:
                span = self.tracer.start_span(name)
                if attributes:
                    for key, value in attributes.items():
                        span.set_attribute(key, value)
                return span
            else:
                return self.tracer.start_span(name)

        elif action == "set_attribute":
            span = kwargs.get("span")
            if span:
                span.set_attribute(kwargs["key"], kwargs["value"])
                return True
            return False

        elif action == "set_status":
            span = kwargs.get("span")
            if span:
                span.set_status(kwargs["status"], kwargs.get("description"))
                return True
            return False

        elif action == "add_event":
            span = kwargs.get("span")
            if span:
                span.add_event(kwargs["name"], kwargs.get("attributes", {}))
                return True
            return False

        elif action == "get_tracer":
            return self.tracer

        elif action == "get_status":
            return {
                "opentelemetry_available": OPENTELEMETRY_AVAILABLE,
                "tracer_provider_initialized": self.tracer_provider is not None,
                "tracer_available": self.tracer is not None,
                "service_name": self.config.service_name,
                "sampling_rate": self.config.sampling_rate,
            }

        return None

    def _initialize_tracing(self) -> None:
        """Initialize tracing system"""
        if OPENTELEMETRY_AVAILABLE:
            try:
                resource = Resource.create(
                    {
                        "service.name": self.config.service_name,
                        "service.version": "1.0.0",
                        "deployment.environment": "development",
                    }
                )

                self.tracer_provider = TracerProvider(resource=resource)
                jaeger_exporter = JaegerExporter(
                    agent_host_name="localhost",
                    agent_port=6831,
                    collector_endpoint=self.config.jaeger_endpoint,
                )

                span_processor = BatchSpanProcessor(jaeger_exporter)
                self.tracer_provider.add_span_processor(span_processor)
                trace.set_tracer_provider(self.tracer_provider)
                self.tracer = trace.get_tracer(__name__)

                logger.info("OpenTelemetry tracing initialized successfully")

            except Exception as e:
                logger.error(f"Failed to initialize OpenTelemetry: {e}")
                self._setup_fallback()
        else:
            self._setup_fallback()

    def _setup_fallback(self) -> None:
        """Setup fallback tracing"""
        logger.warning("Using fallback tracing system")

        class FallbackTracer:
            def __init__(self):
                self.spans = []

            def start_span(self, name: str):
                return FallbackSpan(name, self.spans)

        class FallbackSpan:
            def __init__(self, name: str, spans: list):
                self.name = name
                self.spans = spans
                self.attributes = {}
                self.events = []
                self.start_time = datetime.now()

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.end_time = datetime.now()
                self.spans.append(self)

            def set_attribute(self, key: str, value: Any) -> None:
                self.attributes[key] = value

            def set_status(self, status: str, description: str = None) -> None:
                self.status = status
                self.description = description

            def add_event(self, name: str, attributes: dict[str, Any] = None) -> None:
                self.events.append(
                    {"name": name, "attributes": attributes or {}, "timestamp": datetime.now()}
                )

        self.tracer = FallbackTracer()
