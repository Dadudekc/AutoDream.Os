# V3-004: Distributed Tracing Implementation - Error Tracker
# Agent-1: Architecture Foundation Specialist
# 
# Error tracking and visualization for V2_SWARM distributed tracing

import traceback
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
from enum import Enum

from .jaeger_tracer import trace_manager


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories."""
    SYSTEM = "system"
    DATABASE = "database"
    NETWORK = "network"
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    BUSINESS_LOGIC = "business_logic"
    EXTERNAL_API = "external_api"
    UNKNOWN = "unknown"


@dataclass
class ErrorInfo:
    """Error information structure."""
    error_id: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    category: ErrorCategory
    stack_trace: str
    context: Dict[str, Any]
    user_id: Optional[str]
    agent_id: Optional[str]
    request_id: Optional[str]
    trace_id: Optional[str]
    span_id: Optional[str]
    timestamp: datetime
    resolved: bool = False
    resolution_notes: Optional[str] = None


@dataclass
class ErrorStats:
    """Error statistics structure."""
    total_errors: int
    errors_by_severity: Dict[str, int]
    errors_by_category: Dict[str, int]
    errors_by_hour: Dict[str, int]
    top_errors: List[Dict[str, Any]]
    timestamp: datetime


class ErrorTracker:
    """Error tracking and visualization for distributed tracing."""
    
    def __init__(self, max_errors: int = 10000):
        self.max_errors = max_errors
        self.errors: deque = deque(maxlen=max_errors)
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.severity_counts: Dict[ErrorSeverity, int] = defaultdict(int)
        self.category_counts: Dict[ErrorCategory, int] = defaultdict(int)
        self.tracer = trace_manager.get_tracer()
        self.logger = logging.getLogger(__name__)
    
    def track_error(self, error: Exception, severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                   category: ErrorCategory = ErrorCategory.UNKNOWN,
                   context: Dict[str, Any] = None, user_id: str = None,
                   agent_id: str = None, request_id: str = None) -> str:
        """Track an error occurrence."""
        error_id = f"err_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{id(error)}"
        
        # Get current trace information
        trace_id = self.tracer.get_trace_id()
        span_id = self.tracer.get_span_id()
        
        # Create error info
        error_info = ErrorInfo(
            error_id=error_id,
            error_type=type(error).__name__,
            error_message=str(error),
            severity=severity,
            category=category,
            stack_trace=traceback.format_exc(),
            context=context or {},
            user_id=user_id,
            agent_id=agent_id,
            request_id=request_id,
            trace_id=trace_id,
            span_id=span_id,
            timestamp=datetime.utcnow()
        )
        
        # Store error
        self.errors.append(error_info)
        
        # Update counters
        self.error_counts[error_info.error_type] += 1
        self.severity_counts[severity] += 1
        self.category_counts[category] += 1
        
        # Record in trace
        with self.tracer.trace_span("error_occurrence") as span:
            self.tracer.add_span_tags({
                "error.id": error_id,
                "error.type": error_info.error_type,
                "error.message": error_info.error_message,
                "error.severity": severity.value,
                "error.category": category.value,
                "user.id": user_id or "",
                "agent.id": agent_id or "",
                "request.id": request_id or ""
            })
            
            # Record exception in span
            self.tracer.record_event("error", {
                "error_type": error_info.error_type,
                "error_message": error_info.error_message,
                "severity": severity.value
            })
        
        # Log error
        self.logger.error(f"Error tracked: {error_id} - {error_info.error_type}: {error_info.error_message}")
        
        return error_id
    
    def track_custom_error(self, error_type: str, error_message: str,
                          severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                          category: ErrorCategory = ErrorCategory.UNKNOWN,
                          context: Dict[str, Any] = None, user_id: str = None,
                          agent_id: str = None, request_id: str = None) -> str:
        """Track a custom error."""
        error_id = f"custom_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{len(self.errors)}"
        
        # Get current trace information
        trace_id = self.tracer.get_trace_id()
        span_id = self.tracer.get_span_id()
        
        # Create error info
        error_info = ErrorInfo(
            error_id=error_id,
            error_type=error_type,
            error_message=error_message,
            severity=severity,
            category=category,
            stack_trace="Custom error - no stack trace available",
            context=context or {},
            user_id=user_id,
            agent_id=agent_id,
            request_id=request_id,
            trace_id=trace_id,
            span_id=span_id,
            timestamp=datetime.utcnow()
        )
        
        # Store error
        self.errors.append(error_info)
        
        # Update counters
        self.error_counts[error_type] += 1
        self.severity_counts[severity] += 1
        self.category_counts[category] += 1
        
        # Record in trace
        with self.tracer.trace_span("custom_error") as span:
            self.tracer.add_span_tags({
                "error.id": error_id,
                "error.type": error_type,
                "error.message": error_message,
                "error.severity": severity.value,
                "error.category": category.value,
                "user.id": user_id or "",
                "agent.id": agent_id or "",
                "request.id": request_id or ""
            })
        
        self.logger.warning(f"Custom error tracked: {error_id} - {error_type}: {error_message}")
        
        return error_id
    
    def resolve_error(self, error_id: str, resolution_notes: str = None) -> bool:
        """Mark an error as resolved."""
        for error in self.errors:
            if error.error_id == error_id:
                error.resolved = True
                error.resolution_notes = resolution_notes
                
                # Record resolution in trace
                with self.tracer.trace_span("error_resolution") as span:
                    self.tracer.add_span_tags({
                        "error.id": error_id,
                        "error.resolved": True,
                        "resolution.notes": resolution_notes or ""
                    })
                
                self.logger.info(f"Error resolved: {error_id}")
                return True
        
        return False
    
    def get_error(self, error_id: str) -> Optional[ErrorInfo]:
        """Get error by ID."""
        for error in self.errors:
            if error.error_id == error_id:
                return error
        return None
    
    def get_errors_by_severity(self, severity: ErrorSeverity) -> List[ErrorInfo]:
        """Get errors by severity."""
        return [error for error in self.errors if error.severity == severity]
    
    def get_errors_by_category(self, category: ErrorCategory) -> List[ErrorInfo]:
        """Get errors by category."""
        return [error for error in self.errors if error.category == category]
    
    def get_errors_by_user(self, user_id: str) -> List[ErrorInfo]:
        """Get errors by user ID."""
        return [error for error in self.errors if error.user_id == user_id]
    
    def get_errors_by_agent(self, agent_id: str) -> List[ErrorInfo]:
        """Get errors by agent ID."""
        return [error for error in self.errors if error.agent_id == agent_id]
    
    def get_recent_errors(self, hours: int = 24) -> List[ErrorInfo]:
        """Get recent errors."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return [error for error in self.errors if error.timestamp >= cutoff_time]
    
    def get_error_statistics(self) -> ErrorStats:
        """Get error statistics."""
        # Calculate errors by hour (last 24 hours)
        errors_by_hour = defaultdict(int)
        for error in self.errors:
            hour_key = error.timestamp.strftime("%Y-%m-%d %H:00")
            errors_by_hour[hour_key] += 1
        
        # Get top errors
        top_errors = sorted(
            self.error_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        top_errors_list = [
            {"error_type": error_type, "count": count}
            for error_type, count in top_errors
        ]
        
        return ErrorStats(
            total_errors=len(self.errors),
            errors_by_severity={s.value: c for s, c in self.severity_counts.items()},
            errors_by_category={c.value: count for c, count in self.category_counts.items()},
            errors_by_hour=dict(errors_by_hour),
            top_errors=top_errors_list,
            timestamp=datetime.utcnow()
        )
    
    def get_error_trends(self, days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """Get error trends over time."""
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        recent_errors = [error for error in self.errors if error.timestamp >= cutoff_time]
        
        # Group by day
        daily_errors = defaultdict(list)
        for error in recent_errors:
            day_key = error.timestamp.strftime("%Y-%m-%d")
            daily_errors[day_key].append(error)
        
        # Calculate trends
        trends = {}
        for day, day_errors in daily_errors.items():
            severity_counts = defaultdict(int)
            category_counts = defaultdict(int)
            
            for error in day_errors:
                severity_counts[error.severity.value] += 1
                category_counts[error.category.value] += 1
            
            trends[day] = {
                "total": len(day_errors),
                "by_severity": dict(severity_counts),
                "by_category": dict(category_counts)
            }
        
        return trends
    
    def export_errors(self) -> List[Dict[str, Any]]:
        """Export errors for analysis."""
        return [asdict(error) for error in self.errors]
    
    def clear_resolved_errors(self, max_age_days: int = 30) -> int:
        """Clear resolved errors older than specified days."""
        cutoff_time = datetime.utcnow() - timedelta(days=max_age_days)
        
        original_count = len(self.errors)
        self.errors = deque(
            [error for error in self.errors if not (error.resolved and error.timestamp < cutoff_time)],
            maxlen=self.max_errors
        )
        
        cleared_count = original_count - len(self.errors)
        
        if cleared_count > 0:
            self.logger.info(f"Cleared {cleared_count} resolved errors")
        
        return cleared_count


class ErrorHandler:
    """Error handler for automatic error tracking."""
    
    def __init__(self, error_tracker: ErrorTracker):
        self.error_tracker = error_tracker
        self.logger = logging.getLogger(__name__)
    
    def handle_exception(self, error: Exception, context: Dict[str, Any] = None,
                        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                        category: ErrorCategory = ErrorCategory.UNKNOWN) -> str:
        """Handle an exception with automatic tracking."""
        error_id = self.error_tracker.track_error(
            error=error,
            severity=severity,
            category=category,
            context=context
        )
        
        # Log the error
        self.logger.error(f"Exception handled: {error_id}", exc_info=True)
        
        return error_id
    
    def handle_database_error(self, error: Exception, query: str = None,
                            context: Dict[str, Any] = None) -> str:
        """Handle database errors."""
        db_context = context or {}
        if query:
            db_context["query"] = query
        
        return self.handle_exception(
            error=error,
            context=db_context,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.DATABASE
        )
    
    def handle_network_error(self, error: Exception, url: str = None,
                           context: Dict[str, Any] = None) -> str:
        """Handle network errors."""
        network_context = context or {}
        if url:
            network_context["url"] = url
        
        return self.handle_exception(
            error=error,
            context=network_context,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.NETWORK
        )
    
    def handle_auth_error(self, error: Exception, user_id: str = None,
                         context: Dict[str, Any] = None) -> str:
        """Handle authentication errors."""
        auth_context = context or {}
        if user_id:
            auth_context["user_id"] = user_id
        
        return self.handle_exception(
            error=error,
            context=auth_context,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.AUTHENTICATION
        )



