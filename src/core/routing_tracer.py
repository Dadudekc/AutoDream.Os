#!/usr/bin/env python3
"""
ROUTING TRACER MODULE - DIAGNOSTIC PROTOCOL
==========================================

Tracks message paths and implements checksum verification for inter-agent communications.
Part of THEA's emergency routing patch implementation.

Author: Agent-4 (Strategic Oversight & Emergency Intervention Manager)
License: MIT
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .messaging_core import UnifiedMessage

logger = logging.getLogger(__name__)


@dataclass
class RoutingTrace:
    """Routing trace entry."""
    message_id: str
    timestamp: datetime
    sender: str
    recipient: str
    routing_path: List[str]
    checksum: str
    delivery_status: str
    verification_passed: bool
    error_message: Optional[str] = None
    processing_time_ms: float = 0.0


@dataclass
class ChecksumVerification:
    """Checksum verification result."""
    original_checksum: str
    calculated_checksum: str
    verification_passed: bool
    message_integrity: bool
    timestamp: datetime


class RoutingTracer:
    """Routing tracer for message path tracking and verification."""
    
    def __init__(self, trace_file: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.trace_file = trace_file or "routing_traces.json"
        self.traces: List[RoutingTrace] = []
        self.checksum_cache: Dict[str, str] = {}
        
        # Load existing traces
        self._load_traces()
    
    def _load_traces(self):
        """Load existing traces from file."""
        try:
            trace_path = Path(self.trace_file)
            if trace_path.exists():
                with open(trace_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.traces = [
                        RoutingTrace(
                            message_id=entry["message_id"],
                            timestamp=datetime.fromisoformat(entry["timestamp"]),
                            sender=entry["sender"],
                            recipient=entry["recipient"],
                            routing_path=entry["routing_path"],
                            checksum=entry["checksum"],
                            delivery_status=entry["delivery_status"],
                            verification_passed=entry["verification_passed"],
                            error_message=entry.get("error_message"),
                            processing_time_ms=entry.get("processing_time_ms", 0.0)
                        )
                        for entry in data.get("traces", [])
                    ]
                self.logger.info(f"Loaded {len(self.traces)} existing traces")
        except Exception as e:
            self.logger.error(f"Failed to load traces: {e}")
            self.traces = []
    
    def _save_traces(self):
        """Save traces to file."""
        try:
            trace_path = Path(self.trace_file)
            trace_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "traces": [
                    {
                        "message_id": trace.message_id,
                        "timestamp": trace.timestamp.isoformat(),
                        "sender": trace.sender,
                        "recipient": trace.recipient,
                        "routing_path": trace.routing_path,
                        "checksum": trace.checksum,
                        "delivery_status": trace.delivery_status,
                        "verification_passed": trace.verification_passed,
                        "error_message": trace.error_message,
                        "processing_time_ms": trace.processing_time_ms
                    }
                    for trace in self.traces
                ],
                "last_updated": datetime.now().isoformat(),
                "total_traces": len(self.traces)
            }
            
            with open(trace_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Failed to save traces: {e}")
    
    def generate_checksum(self, message: UnifiedMessage) -> str:
        """Generate checksum for message verification."""
        try:
            # Create checksum from message content and metadata
            checksum_data = {
                "content": message.content,
                "sender": message.sender,
                "recipient": message.recipient,
                "message_type": message.message_type.value,
                "priority": message.priority.value,
                "timestamp": message.timestamp.isoformat(),
                "message_id": message.message_id
            }
            
            # Convert to JSON string and hash
            json_str = json.dumps(checksum_data, sort_keys=True)
            checksum = hashlib.sha256(json_str.encode()).hexdigest()
            
            # Cache checksum
            self.checksum_cache[message.message_id] = checksum
            
            return checksum
            
        except Exception as e:
            self.logger.error(f"Failed to generate checksum: {e}")
            return ""
    
    def verify_checksum(self, message: UnifiedMessage, expected_checksum: str) -> ChecksumVerification:
        """Verify message checksum."""
        try:
            calculated_checksum = self.generate_checksum(message)
            verification_passed = calculated_checksum == expected_checksum
            
            return ChecksumVerification(
                original_checksum=expected_checksum,
                calculated_checksum=calculated_checksum,
                verification_passed=verification_passed,
                message_integrity=verification_passed,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Checksum verification failed: {e}")
            return ChecksumVerification(
                original_checksum=expected_checksum,
                calculated_checksum="",
                verification_passed=False,
                message_integrity=False,
                timestamp=datetime.now()
            )
    
    def start_trace(self, message: UnifiedMessage) -> str:
        """Start routing trace for message."""
        try:
            checksum = self.generate_checksum(message)
            routing_path = [message.sender]
            
            trace = RoutingTrace(
                message_id=message.message_id,
                timestamp=datetime.now(),
                sender=message.sender,
                recipient=message.recipient,
                routing_path=routing_path,
                checksum=checksum,
                delivery_status="in-progress",
                verification_passed=True,
                processing_time_ms=0.0
            )
            
            self.traces.append(trace)
            self.logger.debug(f"Started trace for message {message.message_id}")
            
            return message.message_id
            
        except Exception as e:
            self.logger.error(f"Failed to start trace: {e}")
            return ""
    
    def add_routing_hop(self, message_id: str, hop: str):
        """Add routing hop to trace."""
        try:
            for trace in self.traces:
                if trace.message_id == message_id:
                    trace.routing_path.append(hop)
                    self.logger.debug(f"Added routing hop {hop} to trace {message_id}")
                    break
        except Exception as e:
            self.logger.error(f"Failed to add routing hop: {e}")
    
    def complete_trace(self, message_id: str, delivery_status: str, 
                      verification_passed: bool = True, 
                      error_message: Optional[str] = None,
                      processing_time_ms: float = 0.0):
        """Complete routing trace."""
        try:
            for trace in self.traces:
                if trace.message_id == message_id:
                    trace.delivery_status = delivery_status
                    trace.verification_passed = verification_passed
                    trace.error_message = error_message
                    trace.processing_time_ms = processing_time_ms
                    
                    self.logger.debug(f"Completed trace for message {message_id}: {delivery_status}")
                    
                    # Save traces periodically
                    if len(self.traces) % 10 == 0:
                        self._save_traces()
                    
                    break
        except Exception as e:
            self.logger.error(f"Failed to complete trace: {e}")
    
    def get_trace(self, message_id: str) -> Optional[RoutingTrace]:
        """Get trace for specific message."""
        for trace in self.traces:
            if trace.message_id == message_id:
                return trace
        return None
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get routing statistics."""
        try:
            total_traces = len(self.traces)
            successful_deliveries = sum(1 for trace in self.traces if trace.delivery_status == "delivered")
            failed_deliveries = sum(1 for trace in self.traces if trace.delivery_status == "failed")
            verification_failures = sum(1 for trace in self.traces if not trace.verification_passed)
            
            # Calculate average processing time
            avg_processing_time = 0.0
            if total_traces > 0:
                total_time = sum(trace.processing_time_ms for trace in self.traces)
                avg_processing_time = total_time / total_traces
            
            # Get routing path statistics
            routing_paths = {}
            for trace in self.traces:
                path_key = " -> ".join(trace.routing_path)
                routing_paths[path_key] = routing_paths.get(path_key, 0) + 1
            
            return {
                "total_traces": total_traces,
                "successful_deliveries": successful_deliveries,
                "failed_deliveries": failed_deliveries,
                "verification_failures": verification_failures,
                "success_rate": successful_deliveries / total_traces if total_traces > 0 else 0.0,
                "verification_success_rate": (total_traces - verification_failures) / total_traces if total_traces > 0 else 0.0,
                "average_processing_time_ms": avg_processing_time,
                "routing_paths": routing_paths,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get routing statistics: {e}")
            return {}
    
    def get_agent_routing_analysis(self, agent_id: str) -> Dict[str, Any]:
        """Get routing analysis for specific agent."""
        try:
            agent_traces = [trace for trace in self.traces if trace.recipient == agent_id]
            
            if not agent_traces:
                return {"agent_id": agent_id, "message_count": 0, "analysis": "No messages found"}
            
            successful = sum(1 for trace in agent_traces if trace.delivery_status == "delivered")
            failed = sum(1 for trace in agent_traces if trace.delivery_status == "failed")
            verification_failures = sum(1 for trace in agent_traces if not trace.verification_passed)
            
            # Get common routing paths for this agent
            routing_paths = {}
            for trace in agent_traces:
                path_key = " -> ".join(trace.routing_path)
                routing_paths[path_key] = routing_paths.get(path_key, 0) + 1
            
            return {
                "agent_id": agent_id,
                "message_count": len(agent_traces),
                "successful_deliveries": successful,
                "failed_deliveries": failed,
                "verification_failures": verification_failures,
                "success_rate": successful / len(agent_traces),
                "verification_success_rate": (len(agent_traces) - verification_failures) / len(agent_traces),
                "common_routing_paths": routing_paths,
                "last_analysis": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get agent routing analysis: {e}")
            return {"agent_id": agent_id, "error": str(e)}
    
    def cleanup_old_traces(self, days_to_keep: int = 7):
        """Clean up old traces."""
        try:
            cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
            
            original_count = len(self.traces)
            self.traces = [
                trace for trace in self.traces 
                if trace.timestamp.timestamp() > cutoff_time
            ]
            
            removed_count = original_count - len(self.traces)
            if removed_count > 0:
                self.logger.info(f"Cleaned up {removed_count} old traces")
                self._save_traces()
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup old traces: {e}")


# Global routing tracer instance
_routing_tracer = None


def get_routing_tracer() -> RoutingTracer:
    """Get global routing tracer instance."""
    global _routing_tracer
    if _routing_tracer is None:
        _routing_tracer = RoutingTracer()
    return _routing_tracer


# Convenience functions
def start_message_trace(message: UnifiedMessage) -> str:
    """Start trace for message."""
    tracer = get_routing_tracer()
    return tracer.start_trace(message)


def complete_message_trace(message_id: str, delivery_status: str, 
                          verification_passed: bool = True,
                          error_message: Optional[str] = None,
                          processing_time_ms: float = 0.0):
    """Complete trace for message."""
    tracer = get_routing_tracer()
    tracer.complete_trace(message_id, delivery_status, verification_passed, error_message, processing_time_ms)


def get_routing_diagnostics() -> Dict[str, Any]:
    """Get comprehensive routing diagnostics."""
    tracer = get_routing_tracer()
    return {
        "routing_statistics": tracer.get_routing_statistics(),
        "agent_analyses": {
            f"Agent-{i}": tracer.get_agent_routing_analysis(f"Agent-{i}")
            for i in range(1, 9)
        }
    }