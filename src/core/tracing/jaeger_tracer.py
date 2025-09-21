# V3-004: Distributed Tracing Implementation - Jaeger Tracer
# Agent-1: Architecture Foundation Specialist
# 
# Jaeger distributed tracing integration for V2_SWARM system

import os
import time
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from contextlib import contextmanager
from functools import wraps

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor


@dataclass
class TraceConfig:
    """Jaeger tracing configuration."""
    service_name: str
    jaeger_endpoint: str
    environment: str
    version: str
    sampling_rate: float = 0.1
    max_tag_value_length: int = 256
    batch_size: int = 512
    export_timeout: int = 30


class JaegerTracer:
    """Jaeger distributed tracing implementation for V2_SWARM."""
    
    def __init__(self, config: TraceConfig):
        self.config = config
        self.tracer = None
        self._setup_tracer()
        self._instrument_libraries()
    
    def _setup_tracer(self) -> None:
        """Setup Jaeger tracer with OpenTelemetry."""
        # Create resource
        resource = Resource.create({
            "service.name": self.config.service_name,
            "service.version": self.config.version,
            "deployment.environment": self.config.environment
        })
        
        # Create tracer provider
        trace.set_tracer_provider(TracerProvider(resource=resource))
        
        # Create Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name=os.getenv("JAEGER_AGENT_HOST", "jaeger-agent"),
            agent_port=int(os.getenv("JAEGER_AGENT_PORT", "6831")),
            udp_split_oversized_batches=True
        )
        
        # Create span processor
        span_processor = BatchSpanProcessor(
            jaeger_exporter,
            max_export_batch_size=self.config.batch_size,
            export_timeout_millis=self.config.export_timeout * 1000
        )
        
        # Add span processor to tracer provider
        trace.get_tracer_provider().add_span_processor(span_processor)
        
        # Get tracer
        self.tracer = trace.get_tracer(__name__)
        
        logging.info(f"Jaeger tracer initialized for service: {self.config.service_name}")
    
    def _instrument_libraries(self) -> None:
        """Instrument common libraries for automatic tracing."""
        try:
            # Instrument HTTP requests
            RequestsInstrumentor().instrument()
            
            # Instrument PostgreSQL
            Psycopg2Instrumentor().instrument()
            
            # Instrument Redis
            RedisInstrumentor().instrument()
            
            logging.info("Library instrumentation completed")
        except Exception as e:
            logging.warning(f"Library instrumentation failed: {e}")
    
    @contextmanager
    def trace_span(self, operation_name: str, tags: Dict[str, Any] = None):
        """Context manager for creating spans."""
        if tags is None:
            tags = {}
        
        with self.tracer.start_as_current_span(operation_name) as span:
            # Add tags to span
            for key, value in tags.items():
                if isinstance(value, (str, int, float, bool)):
                    span.set_attribute(key, value)
                else:
                    span.set_attribute(key, str(value))
            
            try:
                yield span
            except Exception as e:
                # Record exception
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                raise
    
    def trace_function(self, operation_name: str = None, tags: Dict[str, Any] = None):
        """Decorator for tracing functions."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                name = operation_name or f"{func.__module__}.{func.__name__}"
                func_tags = tags or {}
                
                with self.trace_span(name, func_tags) as span:
                    # Add function arguments as tags
                    span.set_attribute("function.name", func.__name__)
                    span.set_attribute("function.module", func.__module__)
                    
                    start_time = time.time()
                    try:
                        result = func(*args, **kwargs)
                        span.set_attribute("function.success", True)
                        return result
                    except Exception as e:
                        span.set_attribute("function.success", False)
                        span.set_attribute("function.error", str(e))
                        raise
                    finally:
                        duration = time.time() - start_time
                        span.set_attribute("function.duration", duration)
            
            return wrapper
        return decorator
    
    def trace_async_function(self, operation_name: str = None, tags: Dict[str, Any] = None):
        """Decorator for tracing async functions."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                name = operation_name or f"{func.__module__}.{func.__name__}"
                func_tags = tags or {}
                
                with self.trace_span(name, func_tags) as span:
                    # Add function arguments as tags
                    span.set_attribute("function.name", func.__name__)
                    span.set_attribute("function.module", func.__module__)
                    span.set_attribute("function.async", True)
                    
                    start_time = time.time()
                    try:
                        result = await func(*args, **kwargs)
                        span.set_attribute("function.success", True)
                        return result
                    except Exception as e:
                        span.set_attribute("function.success", False)
                        span.set_attribute("function.error", str(e))
                        raise
                    finally:
                        duration = time.time() - start_time
                        span.set_attribute("function.duration", duration)
            
            return wrapper
        return decorator
    
    def add_span_tags(self, tags: Dict[str, Any]) -> None:
        """Add tags to current span."""
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            for key, value in tags.items():
                if isinstance(value, (str, int, float, bool)):
                    current_span.set_attribute(key, value)
                else:
                    current_span.set_attribute(key, str(value))
    
    def record_event(self, name: str, attributes: Dict[str, Any] = None) -> None:
        """Record an event in the current span."""
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            current_span.add_event(name, attributes or {})
    
    def set_span_status(self, status_code: str, description: str = None) -> None:
        """Set status of current span."""
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            current_span.set_status(trace.Status(status_code, description))
    
    def get_trace_id(self) -> Optional[str]:
        """Get current trace ID."""
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            return format(current_span.get_span_context().trace_id, '032x')
        return None
    
    def get_span_id(self) -> Optional[str]:
        """Get current span ID."""
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            return format(current_span.get_span_context().span_id, '016x')
        return None
    
    def create_child_span(self, operation_name: str, tags: Dict[str, Any] = None):
        """Create a child span."""
        return self.trace_span(operation_name, tags)
    
    def shutdown(self) -> None:
        """Shutdown tracer and flush remaining spans."""
        try:
            # Force flush remaining spans
            trace.get_tracer_provider().shutdown()
            logging.info("Jaeger tracer shutdown completed")
        except Exception as e:
            logging.error(f"Error during tracer shutdown: {e}")


class TraceManager:
    """Trace management for V2_SWARM system."""
    
    def __init__(self):
        self.tracers: Dict[str, JaegerTracer] = {}
        self._initialize_default_tracer()
    
    def _initialize_default_tracer(self) -> None:
        """Initialize default tracer for the system."""
        config = TraceConfig(
            service_name=os.getenv("SERVICE_NAME", "swarm-v3"),
            jaeger_endpoint=os.getenv("JAEGER_ENDPOINT", "http://jaeger-collector:14268"),
            environment=os.getenv("ENVIRONMENT", "dev"),
            version=os.getenv("SERVICE_VERSION", "1.0.0"),
            sampling_rate=float(os.getenv("TRACE_SAMPLING_RATE", "0.1"))
        )
        
        self.tracers["default"] = JaegerTracer(config)
    
    def get_tracer(self, service_name: str = "default") -> JaegerTracer:
        """Get tracer for service."""
        return self.tracers.get(service_name, self.tracers["default"])
    
    def create_service_tracer(self, service_name: str, config: TraceConfig) -> JaegerTracer:
        """Create tracer for specific service."""
        tracer = JaegerTracer(config)
        self.tracers[service_name] = tracer
        return tracer
    
    def shutdown_all(self) -> None:
        """Shutdown all tracers."""
        for tracer in self.tracers.values():
            tracer.shutdown()
        self.tracers.clear()


# Global trace manager instance
trace_manager = TraceManager()
