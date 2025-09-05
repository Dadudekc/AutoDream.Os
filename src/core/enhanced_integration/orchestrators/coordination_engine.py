"""
Coordination Engine - V2 Compliant Module
========================================

Handles coordination strategy and resource allocation.
Extracted from enhanced_integration_orchestrator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

from ..integration_models import (
    CoordinationStrategy, ResourceAllocationStrategy, IntegrationStatus,
    IntegrationType, OptimizationLevel
)


class CoordinationEngine:
    """
    Engine for coordination strategy and resource management.
    
    Handles coordination decisions, resource allocation, and optimization strategies.
    """
    
    def __init__(self, config):
        """Initialize coordination engine."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Coordination state
        self.current_strategy = config.coordination_strategy
        self.resource_allocation = config.resource_allocation
        self.optimization_level = config.optimization_level
        
        # Resource tracking
        self.allocated_resources: Dict[str, Any] = {}
        self.resource_limits: Dict[str, int] = {
            "cpu_cores": config.max_concurrent_operations,
            "memory_mb": 1024,
            "network_connections": 100
        }
    
    def determine_coordination_strategy(self, task_type: str, priority: str) -> CoordinationStrategy:
        """Determine optimal coordination strategy for task."""
        try:
            # High priority tasks use aggressive coordination
            if priority == "high" or priority == "critical":
                return CoordinationStrategy.AGGRESSIVE
            
            # Performance optimization tasks use balanced coordination
            if task_type == "performance_optimization":
                return CoordinationStrategy.BALANCED
            
            # Vector database tasks use conservative coordination
            if task_type == "vector_database":
                return CoordinationStrategy.CONSERVATIVE
            
            # Default to balanced strategy
            return CoordinationStrategy.BALANCED
            
        except Exception as e:
            self.logger.error(f"Error determining coordination strategy: {e}")
            return CoordinationStrategy.BALANCED
    
    def allocate_resources(self, task_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Allocate resources for task execution."""
        try:
            allocation = {}
            
            # CPU allocation
            cpu_required = task_requirements.get("cpu_cores", 1)
            if self._can_allocate_cpu(cpu_required):
                allocation["cpu_cores"] = cpu_required
                self.allocated_resources["cpu_cores"] = (
                    self.allocated_resources.get("cpu_cores", 0) + cpu_required
                )
            
            # Memory allocation
            memory_required = task_requirements.get("memory_mb", 128)
            if self._can_allocate_memory(memory_required):
                allocation["memory_mb"] = memory_required
                self.allocated_resources["memory_mb"] = (
                    self.allocated_resources.get("memory_mb", 0) + memory_required
                )
            
            # Network allocation
            network_required = task_requirements.get("network_connections", 1)
            if self._can_allocate_network(network_required):
                allocation["network_connections"] = network_required
                self.allocated_resources["network_connections"] = (
                    self.allocated_resources.get("network_connections", 0) + network_required
                )
            
            self.logger.debug(f"Resource allocation: {allocation}")
            return allocation
            
        except Exception as e:
            self.logger.error(f"Error allocating resources: {e}")
            return {}
    
    def _can_allocate_cpu(self, required: int) -> bool:
        """Check if CPU cores can be allocated."""
        current = self.allocated_resources.get("cpu_cores", 0)
        return (current + required) <= self.resource_limits["cpu_cores"]
    
    def _can_allocate_memory(self, required: int) -> bool:
        """Check if memory can be allocated."""
        current = self.allocated_resources.get("memory_mb", 0)
        return (current + required) <= self.resource_limits["memory_mb"]
    
    def _can_allocate_network(self, required: int) -> bool:
        """Check if network connections can be allocated."""
        current = self.allocated_resources.get("network_connections", 0)
        return (current + required) <= self.resource_limits["network_connections"]
    
    def deallocate_resources(self, allocation: Dict[str, Any]):
        """Deallocate resources after task completion."""
        try:
            for resource_type, amount in allocation.items():
                if resource_type in self.allocated_resources:
                    self.allocated_resources[resource_type] = max(
                        0, self.allocated_resources[resource_type] - amount
                    )
            
            self.logger.debug(f"Resources deallocated: {allocation}")
            
        except Exception as e:
            self.logger.error(f"Error deallocating resources: {e}")
    
    def get_resource_utilization(self) -> Dict[str, float]:
        """Get current resource utilization."""
        utilization = {}
        
        for resource_type, allocated in self.allocated_resources.items():
            limit = self.resource_limits.get(resource_type, 1)
            utilization[resource_type] = (allocated / limit) * 100 if limit > 0 else 0
        
        return utilization
    
    def optimize_resource_allocation(self) -> Dict[str, Any]:
        """Optimize resource allocation based on current usage."""
        try:
            utilization = self.get_resource_utilization()
            optimizations = {}
            
            # CPU optimization
            if utilization.get("cpu_cores", 0) > 80:
                optimizations["cpu_cores"] = "high_utilization"
            elif utilization.get("cpu_cores", 0) < 20:
                optimizations["cpu_cores"] = "underutilized"
            
            # Memory optimization
            if utilization.get("memory_mb", 0) > 90:
                optimizations["memory_mb"] = "high_utilization"
            elif utilization.get("memory_mb", 0) < 10:
                optimizations["memory_mb"] = "underutilized"
            
            # Network optimization
            if utilization.get("network_connections", 0) > 85:
                optimizations["network_connections"] = "high_utilization"
            elif utilization.get("network_connections", 0) < 15:
                optimizations["network_connections"] = "underutilized"
            
            return {
                "utilization": utilization,
                "optimizations": optimizations,
                "recommendations": self._generate_recommendations(optimizations)
            }
            
        except Exception as e:
            self.logger.error(f"Error optimizing resource allocation: {e}")
            return {"error": str(e)}
    
    def _generate_recommendations(self, optimizations: Dict[str, str]) -> List[str]:
        """Generate resource allocation recommendations."""
        recommendations = []
        
        for resource, status in optimizations.items():
            if status == "high_utilization":
                recommendations.append(f"Consider increasing {resource} limit")
            elif status == "underutilized":
                recommendations.append(f"Consider reducing {resource} allocation")
        
        if not recommendations:
            recommendations.append("Resource allocation is optimal")
        
        return recommendations
    
    def get_coordination_summary(self) -> Dict[str, Any]:
        """Get coordination engine summary."""
        return {
            "strategy": self.current_strategy.value,
            "resource_allocation": self.resource_allocation.value,
            "optimization_level": self.optimization_level.value,
            "allocated_resources": self.allocated_resources.copy(),
            "resource_limits": self.resource_limits.copy(),
            "utilization": self.get_resource_utilization()
        }
    
    def update_coordination_strategy(self, strategy: CoordinationStrategy):
        """Update coordination strategy."""
        self.current_strategy = strategy
        self.logger.info(f"Coordination strategy updated to: {strategy.value}")
    
    def update_resource_allocation_strategy(self, strategy: ResourceAllocationStrategy):
        """Update resource allocation strategy."""
        self.resource_allocation = strategy
        self.logger.info(f"Resource allocation strategy updated to: {strategy.value}")
    
    def update_optimization_level(self, level: OptimizationLevel):
        """Update optimization level."""
        self.optimization_level = level
        self.logger.info(f"Optimization level updated to: {level.value}")
    
    def reset_resource_allocation(self):
        """Reset all resource allocations."""
        self.allocated_resources.clear()
        self.logger.info("Resource allocation reset")
    
    def get_available_resources(self) -> Dict[str, int]:
        """Get currently available resources."""
        available = {}
        
        for resource_type, limit in self.resource_limits.items():
            allocated = self.allocated_resources.get(resource_type, 0)
            available[resource_type] = max(0, limit - allocated)
        
        return available
