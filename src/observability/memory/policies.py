"""
Memory Policy Framework - V2_SWARM
==================================

Policy-driven memory management with tracemalloc integration.
Implements memory budgets, monitoring, and enforcement.

Author: Agent-5 (Coordinator)
License: MIT
"""

import logging
import tracemalloc
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


@dataclass
class MemoryBudget:
    """Memory budget configuration"""
    
    max_memory_mb: int
    warning_threshold_percent: int
    critical_threshold_percent: int
    
    @property
    def warning_mb(self) -> float:
        """Calculate warning threshold in MB"""
        return self.max_memory_mb * (self.warning_threshold_percent / 100)
    
    @property
    def critical_mb(self) -> float:
        """Calculate critical threshold in MB"""
        return self.max_memory_mb * (self.critical_threshold_percent / 100)


@dataclass
class MemorySnapshot:
    """Memory usage snapshot"""
    
    timestamp: float
    current_mb: float
    peak_mb: float
    object_count: int
    tracemalloc_stats: Optional[List] = None


class MemoryPolicyLoader:
    """Load memory policies from configuration"""
    
    def __init__(self, config_path: str = "config/memory_policy.yaml"):
        """Initialize policy loader"""
        self.config_path = config_path
        self.config = None
    
    def load(self) -> Dict[str, Any]:
        """Load policy configuration"""
        try:
            with open(self.config_path) as f:
                self.config = yaml.safe_load(f)
            logger.info(f"Memory policy loaded from {self.config_path}")
            return self.config
        except Exception as e:
            logger.error(f"Error loading memory policy: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'memory_budgets': {
                'global': {
                    'max_memory_mb': 512,
                    'warning_threshold_percent': 80,
                    'critical_threshold_percent': 95
                }
            },
            'leak_detection': {'enabled': True},
            'monitoring': {'tracemalloc': {'enabled': True}},
            'alerts': {'channels': ['logging']},
            'ledger': {'enabled': True},
            'enforcement': {'hard_limits': {'enabled': True}}
        }
    
    def get_budget(self, service_name: str) -> MemoryBudget:
        """Get budget for specific service"""
        if not self.config:
            self.load()
        
        budgets = self.config.get('memory_budgets', {})
        service_budget = budgets.get('services', {}).get(service_name)
        
        if service_budget:
            return MemoryBudget(**service_budget)
        
        # Fall back to global budget
        global_budget = budgets.get('global', {})
        return MemoryBudget(
            max_memory_mb=global_budget.get('max_memory_mb', 512),
            warning_threshold_percent=global_budget.get('warning_threshold_percent', 80),
            critical_threshold_percent=global_budget.get('critical_threshold_percent', 95)
        )


class TracemallocIntegration:
    """Tracemalloc integration for memory tracking"""
    
    def __init__(self, trace_limit: int = 25):
        """Initialize tracemalloc integration"""
        self.trace_limit = trace_limit
        self.is_tracing = False
    
    def start(self) -> bool:
        """Start memory tracing"""
        try:
            if not self.is_tracing:
                tracemalloc.start(self.trace_limit)
                self.is_tracing = True
                logger.info("Tracemalloc started successfully")
            return True
        except Exception as e:
            logger.error(f"Error starting tracemalloc: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop memory tracing"""
        try:
            if self.is_tracing:
                tracemalloc.stop()
                self.is_tracing = False
                logger.info("Tracemalloc stopped")
            return True
        except Exception as e:
            logger.error(f"Error stopping tracemalloc: {e}")
            return False
    
    def take_snapshot(self) -> MemorySnapshot:
        """Take memory snapshot"""
        import time
        import gc
        
        current, peak = tracemalloc.get_traced_memory()
        current_mb = current / 1024 / 1024
        peak_mb = peak / 1024 / 1024
        
        # Get object count
        gc.collect()
        object_count = len(gc.get_objects())
        
        # Get top memory allocations
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')[:10]
        
        return MemorySnapshot(
            timestamp=time.time(),
            current_mb=current_mb,
            peak_mb=peak_mb,
            object_count=object_count,
            tracemalloc_stats=[str(stat) for stat in top_stats]
        )


class MemoryPolicyEnforcer:
    """Enforce memory policies and budgets"""
    
    def __init__(self, policy_loader: MemoryPolicyLoader):
        """Initialize policy enforcer"""
        self.policy_loader = policy_loader
        self.config = policy_loader.config or policy_loader.load()
    
    def check_budget(self, service_name: str, current_mb: float) -> Dict[str, Any]:
        """Check if service is within budget"""
        budget = self.policy_loader.get_budget(service_name)
        
        status = "ok"
        if current_mb >= budget.critical_mb:
            status = "critical"
        elif current_mb >= budget.warning_mb:
            status = "warning"
        
        return {
            'service': service_name,
            'current_mb': current_mb,
            'budget_mb': budget.max_memory_mb,
            'warning_mb': budget.warning_mb,
            'critical_mb': budget.critical_mb,
            'status': status,
            'within_budget': status == "ok"
        }
    
    def enforce_limits(self, service_name: str, current_mb: float) -> Dict[str, Any]:
        """Enforce memory limits"""
        check_result = self.check_budget(service_name, current_mb)
        
        enforcement = self.config.get('enforcement', {})
        hard_limits = enforcement.get('hard_limits', {})
        
        if not hard_limits.get('enabled', True):
            return {'action': 'none', 'reason': 'enforcement disabled'}
        
        if check_result['status'] == 'critical':
            action = hard_limits.get('action', 'alert_only')
            return {
                'action': action,
                'reason': 'critical threshold exceeded',
                'check_result': check_result
            }
        
        return {'action': 'none', 'check_result': check_result}


class MemoryPolicyManager:
    """Main memory policy management class"""
    
    def __init__(self, config_path: str = "config/memory_policy.yaml"):
        """Initialize memory policy manager"""
        self.loader = MemoryPolicyLoader(config_path)
        self.tracer = None
        self.enforcer = None
        self.initialized = False
    
    def initialize(self) -> bool:
        """Initialize memory policy system"""
        try:
            # Load configuration
            self.loader.load()
            
            # Initialize tracemalloc if enabled
            if self.loader.config.get('monitoring', {}).get('tracemalloc', {}).get('enabled'):
                trace_limit = self.loader.config['monitoring']['tracemalloc'].get('trace_limit', 25)
                self.tracer = TracemallocIntegration(trace_limit)
                self.tracer.start()
            
            # Initialize enforcer
            self.enforcer = MemoryPolicyEnforcer(self.loader)
            
            self.initialized = True
            logger.info("Memory policy system initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing memory policy system: {e}")
            return False
    
    def get_snapshot(self) -> Optional[MemorySnapshot]:
        """Get current memory snapshot"""
        if not self.tracer or not self.tracer.is_tracing:
            return None
        return self.tracer.take_snapshot()
    
    def check_service(self, service_name: str, current_mb: float) -> Dict[str, Any]:
        """Check service memory status"""
        if not self.enforcer:
            return {'error': 'Policy system not initialized'}
        return self.enforcer.check_budget(service_name, current_mb)
    
    def shutdown(self) -> bool:
        """Shutdown memory policy system"""
        try:
            if self.tracer:
                self.tracer.stop()
            logger.info("Memory policy system shutdown complete")
            return True
        except Exception as e:
            logger.error(f"Error shutting down memory policy system: {e}")
            return False

