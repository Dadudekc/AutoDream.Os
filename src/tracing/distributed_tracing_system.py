#!/usr/bin/env python3
"""
Distributed Tracing System - V3-004 Implementation
==================================================

Comprehensive distributed tracing system for V3 implementation.
Provides observability across all microservices and agent operations.

Features:
- OpenTelemetry integration
- Jaeger tracing backend
- Custom span creation and management
- Agent operation tracing
- Performance monitoring
- Error tracking and correlation

Usage:
    from src.tracing.distributed_tracing_system import DistributedTracingSystem
    
    tracer = DistributedTracingSystem()
    with tracer.start_span("agent_operation") as span:
        # Your code here
        span.set_attribute("agent_id", "Agent-1")
"""

import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
from contextlib import contextmanager
from dataclasses import dataclass

# OpenTelemetry imports
try:
    from opentelemetry import trace
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.trace import Status, StatusCode
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    print("⚠️ OpenTelemetry not available - using fallback tracing")

logger = logging.getLogger(__name__)


@dataclass
class TraceConfig:
    """Configuration for distributed tracing."""
    service_name: str = "dream-os-v3"
    jaeger_endpoint: str = "http://localhost:14268/api/traces"
    sample_rate: float = 1.0
    max_attributes: int = 128
    max_events: int = 128
    max_links: int = 128


class DistributedTracingSystem:
    """Comprehensive distributed tracing system for V3 operations."""
    
    def __init__(self, config: Optional[TraceConfig] = None):
        """
        Initialize the distributed tracing system.
        
        Args:
            config: Tracing configuration
        """
        self.config = config or TraceConfig()
        self.tracer = None
        self.tracer_provider = None
        self.is_initialized = False
        
        # Fallback tracing data
        self.fallback_spans: List[Dict[str, Any]] = []
        
        # Initialize tracing
        self._initialize_tracing()
    
    def _initialize_tracing(self):
        """Initialize the OpenTelemetry tracing system."""
        if not OPENTELEMETRY_AVAILABLE:
            logger.warning("OpenTelemetry not available - using fallback tracing")
            return
        
        try:
            # Create resource
            resource = Resource.create({
                "service.name": self.config.service_name,
                "service.version": "v3.0.0",
                "deployment.environment": "production"
            })
            
            # Create tracer provider
            self.tracer_provider = TracerProvider(
                resource=resource,
                sampler=trace.sampling.TraceIdRatioBased(self.config.sample_rate)
            )
            
            # Create Jaeger exporter
            jaeger_exporter = JaegerExporter(
                agent_host_name="localhost",
                agent_port=6831,
                collector_endpoint=self.config.jaeger_endpoint
            )
            
            # Create span processor
            span_processor = BatchSpanProcessor(jaeger_exporter)
            self.tracer_provider.add_span_processor(span_processor)
            
            # Set global tracer provider
            trace.set_tracer_provider(self.tracer_provider)
            
            # Get tracer
            self.tracer = trace.get_tracer(__name__)
            
            # Instrument libraries
            RequestsInstrumentor().instrument()
            URLLib3Instrumentor().instrument()
            
            self.is_initialized = True
            logger.info("✅ Distributed tracing system initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize tracing system: {e}")
            self.is_initialized = False
    
    @contextmanager
    def start_span(self, 
                   name: str, 
                   attributes: Optional[Dict[str, Any]] = None,
                   parent_span: Optional[Any] = None):
        """
        Start a new span for tracing.
        
        Args:
            name: Span name
            attributes: Span attributes
            parent_span: Parent span context
            
        Yields:
            Span object for adding attributes and events
        """
        if self.is_initialized and self.tracer:
            # Use OpenTelemetry tracing
            with self.tracer.start_as_current_span(
                name, 
                context=parent_span,
                attributes=attributes or {}
            ) as span:
                yield span
        else:
            # Use fallback tracing
            span_data = {
                "name": name,
                "start_time": datetime.now().isoformat(),
                "attributes": attributes or {},
                "events": [],
                "status": "active"
            }
            self.fallback_spans.append(span_data)
            
            try:
                yield span_data
            finally:
                span_data["end_time"] = datetime.now().isoformat()
                span_data["status"] = "completed"
    
    def add_span_attribute(self, span: Any, key: str, value: Any):
        """Add an attribute to a span."""
        if self.is_initialized and hasattr(span, 'set_attribute'):
            span.set_attribute(key, value)
        elif isinstance(span, dict):
            span["attributes"][key] = value
    
    def add_span_event(self, span: Any, name: str, attributes: Optional[Dict[str, Any]] = None):
        """Add an event to a span."""
        if self.is_initialized and hasattr(span, 'add_event'):
            span.add_event(name, attributes or {})
        elif isinstance(span, dict):
            event = {
                "name": name,
                "timestamp": datetime.now().isoformat(),
                "attributes": attributes or {}
            }
            span["events"].append(event)
    
    def set_span_status(self, span: Any, status: str, description: Optional[str] = None):
        """Set the status of a span."""
        if self.is_initialized and hasattr(span, 'set_status'):
            if status == "error":
                span.set_status(Status(StatusCode.ERROR, description))
            elif status == "ok":
                span.set_status(Status(StatusCode.OK, description))
        elif isinstance(span, dict):
            span["status"] = status
            if description:
                span["status_description"] = description
    
    def trace_agent_operation(self, 
                            agent_id: str, 
                            operation: str, 
                            attributes: Optional[Dict[str, Any]] = None):
        """
        Trace an agent operation.
        
        Args:
            agent_id: ID of the agent performing the operation
            operation: Operation being performed
            attributes: Additional attributes
            
        Returns:
            Context manager for the span
        """
        span_attributes = {
            "agent.id": agent_id,
            "operation.type": operation,
            "system.component": "agent",
            **(attributes or {})
        }
        
        return self.start_span(f"agent.{agent_id}.{operation}", span_attributes)
    
    def trace_messaging_operation(self, 
                                from_agent: str, 
                                to_agent: str, 
                                message_type: str,
                                attributes: Optional[Dict[str, Any]] = None):
        """
        Trace a messaging operation.
        
        Args:
            from_agent: Source agent ID
            to_agent: Target agent ID
            message_type: Type of message
            attributes: Additional attributes
            
        Returns:
            Context manager for the span
        """
        span_attributes = {
            "messaging.from": from_agent,
            "messaging.to": to_agent,
            "messaging.type": message_type,
            "system.component": "messaging",
            **(attributes or {})
        }
        
        return self.start_span(f"messaging.{from_agent}.{to_agent}.{message_type}", span_attributes)
    
    def trace_fsm_transition(self, 
                           agent_id: str, 
                           from_state: str, 
                           to_state: str,
                           attributes: Optional[Dict[str, Any]] = None):
        """
        Trace an FSM state transition.
        
        Args:
            agent_id: Agent ID
            from_state: Source state
            to_state: Target state
            attributes: Additional attributes
            
        Returns:
            Context manager for the span
        """
        span_attributes = {
            "fsm.agent_id": agent_id,
            "fsm.from_state": from_state,
            "fsm.to_state": to_state,
            "system.component": "fsm",
            **(attributes or {})
        }
        
        return self.start_span(f"fsm.{agent_id}.{from_state}.{to_state}", span_attributes)
    
    def trace_v3_contract(self, 
                        contract_id: str, 
                        agent_id: str, 
                        operation: str,
                        attributes: Optional[Dict[str, Any]] = None):
        """
        Trace a V3 contract execution.
        
        Args:
            contract_id: V3 contract ID
            agent_id: Agent executing the contract
            operation: Operation being performed
            attributes: Additional attributes
            
        Returns:
            Context manager for the span
        """
        span_attributes = {
            "v3.contract_id": contract_id,
            "v3.agent_id": agent_id,
            "v3.operation": operation,
            "system.component": "v3_contract",
            **(attributes or {})
        }
        
        return self.start_span(f"v3.{contract_id}.{operation}", span_attributes)
    
    def get_trace_summary(self) -> Dict[str, Any]:
        """Get a summary of current tracing data."""
        if self.is_initialized:
            return {
                "tracing_backend": "opentelemetry",
                "jaeger_endpoint": self.config.jaeger_endpoint,
                "service_name": self.config.service_name,
                "sample_rate": self.config.sample_rate,
                "status": "active"
            }
        else:
            return {
                "tracing_backend": "fallback",
                "total_spans": len(self.fallback_spans),
                "recent_spans": self.fallback_spans[-10:] if self.fallback_spans else [],
                "status": "fallback_mode"
            }
    
    def export_traces(self, output_file: Optional[str] = None) -> str:
        """Export trace data to a file."""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"traces_export_{timestamp}.json"
        
        import json
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "config": {
                "service_name": self.config.service_name,
                "jaeger_endpoint": self.config.jaeger_endpoint,
                "sample_rate": self.config.sample_rate
            },
            "tracing_summary": self.get_trace_summary(),
            "fallback_spans": self.fallback_spans if not self.is_initialized else []
        }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"📊 Trace data exported to {output_file}")
        return output_file
    
    def cleanup(self):
        """Clean up tracing resources."""
        if self.is_initialized and self.tracer_provider:
            try:
                self.tracer_provider.shutdown()
                logger.info("✅ Tracing system cleaned up")
            except Exception as e:
                logger.error(f"❌ Error cleaning up tracing system: {e}")


# Convenience functions
def create_tracing_system(config: Optional[TraceConfig] = None) -> DistributedTracingSystem:
    """Create a distributed tracing system with default settings."""
    return DistributedTracingSystem(config)


def trace_agent_operation(agent_id: str, operation: str, **kwargs):
    """Convenience function for tracing agent operations."""
    tracer = create_tracing_system()
    return tracer.trace_agent_operation(agent_id, operation, kwargs)


if __name__ == "__main__":
    # Example usage
    print("🔍 V2_SWARM Distributed Tracing System")
    print("=" * 45)
    
    # Create tracing system
    tracer = create_tracing_system()
    print("✅ Distributed tracing system created")
    
    # Test agent operation tracing
    with tracer.trace_agent_operation("Agent-1", "v3_004_execution") as span:
        tracer.add_span_attribute(span, "contract.id", "V3-004")
        tracer.add_span_attribute(span, "operation.duration", 120)
        tracer.add_span_event(span, "tracing_initialized")
        tracer.set_span_status(span, "ok", "Tracing system operational")
    
    # Test messaging tracing
    with tracer.trace_messaging_operation("Agent-1", "Agent-4", "status_update") as span:
        tracer.add_span_attribute(span, "message.priority", "NORMAL")
        tracer.add_span_event(span, "message_sent")
    
    # Get summary
    summary = tracer.get_trace_summary()
    print("📊 Tracing Summary:", summary)
    
    # Export traces
    export_file = tracer.export_traces()
    print(f"📊 Traces exported to: {export_file}")
    
    # Cleanup
    tracer.cleanup()
    print("✅ Tracing system test completed")
