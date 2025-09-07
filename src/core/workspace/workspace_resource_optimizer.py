#!/usr/bin/env python3
"""
Workspace Resource Optimizer - Agent Cellphone V2

Handles resource allocation, optimization, and monitoring for unified workspace system.
Provides intelligent resource management and optimization strategies.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3A - Workspace System Consolidation
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import logging
import time
import threading
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

# Core infrastructure imports
from src.core.managers.performance_manager import PerformanceManager


class ResourceType(Enum):
    """Resource types for workspace optimization"""
    MEMORY = "memory"
    CPU = "cpu"
    STORAGE = "storage"
    NETWORK = "network"
    AGENTS = "agents"


class OptimizationStrategy(Enum):
    """Resource optimization strategies"""
    BALANCED = "balanced"
    PERFORMANCE_FOCUSED = "performance_focused"
    RESOURCE_EFFICIENT = "resource_efficient"
    AGGRESSIVE = "aggressive"


@dataclass
class ResourceAllocation:
    """Resource allocation for a workspace"""
    workspace_id: str
    resource_type: ResourceType
    current_usage: float
    allocated_amount: float
    optimal_amount: float
    last_optimization: str = field(default_factory=lambda: datetime.now().isoformat())
    optimization_status: str = "pending"


@dataclass
class OptimizationResult:
    """Result of resource optimization"""
    workspace_id: str
    resource_type: ResourceType
    previous_allocation: float
    new_allocation: float
    optimization_gain: float
    optimization_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    strategy_used: OptimizationStrategy = OptimizationStrategy.BALANCED


class WorkspaceResourceOptimizer:
    """
    Workspace Resource Optimizer - TASK 3A

    Handles resource optimization for:
    - Memory allocation and management
    - CPU usage optimization
    - Storage allocation
    - Network resource management
    - Agent count optimization
    """

    def __init__(self, performance_manager: PerformanceManager):
        self.performance_manager = performance_manager
        self.logger = logging.getLogger(f"{__name__}.WorkspaceResourceOptimizer")

        # Resource tracking
        self.resource_allocations: Dict[str, List[ResourceAllocation]] = {}
        self.optimization_history: List[OptimizationResult] = []
        self.optimization_active = False
        self.optimization_thread = None
        self.optimization_lock = threading.Lock()

        # Optimization strategies
        self.current_strategy = OptimizationStrategy.BALANCED
        self.optimization_interval = 300  # 5 minutes
        self.last_optimization_run = None

        # Performance thresholds
        self.memory_threshold = 80.0  # 80% memory usage triggers optimization
        self.cpu_threshold = 75.0     # 75% CPU usage triggers optimization
        self.agent_threshold = 15     # More than 15 agents triggers optimization

        self.logger.info("Workspace Resource Optimizer initialized for TASK 3A")

    def start_optimization(self) -> bool:
        """Start resource optimization process"""
        try:
            with self.optimization_lock:
                if self.optimization_active:
                    self.logger.warning("Resource optimization already active")
                    return False

                self.optimization_active = True
                self.last_optimization_run = datetime.now()

                # Start optimization thread
                self.optimization_thread = threading.Thread(
                    target=self._optimization_worker,
                    daemon=True
                )
                self.optimization_thread.start()

                # Setup optimization monitoring
                self._setup_optimization_monitoring()

                self.logger.info("Resource optimization started successfully")
                return True

        except Exception as e:
            self.logger.error(f"Failed to start resource optimization: {e}")
            self.optimization_active = False
            return False

    def stop_optimization(self) -> bool:
        """Stop resource optimization process"""
        try:
            with self.optimization_lock:
                if not self.optimization_active:
                    self.logger.warning("Resource optimization not active")
                    return False

                self.optimization_active = False

                # Wait for optimization thread
                if self.optimization_thread and self.optimization_thread.is_alive():
                    self.optimization_thread.join(timeout=5.0)

                self.logger.info("Resource optimization stopped")
                return True

        except Exception as e:
            self.logger.error(f"Failed to stop resource optimization: {e}")
            return False

    def _setup_optimization_monitoring(self):
        """Setup optimization monitoring with performance manager"""
        try:
            # Add optimization metrics
            self.performance_manager.add_metric("resource_optimization_runs", 0, "count", "workspace")
            self.performance_manager.add_metric("resource_optimization_gains", 0.0, "percent", "workspace")
            self.performance_manager.add_metric("resource_allocation_efficiency", 100.0, "percent", "workspace")

            self.logger.info("Resource optimization monitoring setup completed")

        except Exception as e:
            self.logger.error(f"Failed to setup optimization monitoring: {e}")

    def _optimization_worker(self):
        """Main optimization worker thread"""
        try:
            self.logger.info("Resource optimization worker started")

            while self.optimization_active:
                try:
                    # Check if it's time for optimization
                    if self._should_run_optimization():
                        self._run_resource_optimization()
                        self.last_optimization_run = datetime.now()

                    # Sleep between checks
                    time.sleep(60)  # Check every minute

                except Exception as e:
                    self.logger.error(f"Error in optimization worker: {e}")
                    time.sleep(120)  # Longer sleep on error

            self.logger.info("Resource optimization worker stopped")

        except Exception as e:
            self.logger.error(f"Fatal error in optimization worker: {e}")

    def _should_run_optimization(self) -> bool:
        """Check if optimization should run"""
        if not self.last_optimization_run:
            return True

        time_since_last = (datetime.now() - self.last_optimization_run).total_seconds()
        return time_since_last >= self.optimization_interval

    def _run_resource_optimization(self):
        """Run comprehensive resource optimization"""
        try:
            self.logger.info("Running resource optimization cycle")

            optimization_results = []
            total_gain = 0.0

            # Optimize each workspace
            for workspace_id, allocations in self.resource_allocations.items():
                workspace_results = self._optimize_workspace_resources(workspace_id, allocations)
                optimization_results.extend(workspace_results)

                # Calculate total gain
                for result in workspace_results:
                    total_gain += result.optimization_gain

            # Update optimization history
            self.optimization_history.extend(optimization_results)

            # Update performance metrics
            self._update_optimization_metrics(len(optimization_results), total_gain)

            self.logger.info(f"Resource optimization completed: {len(optimization_results)} optimizations, {total_gain:.2f}% total gain")

        except Exception as e:
            self.logger.error(f"Failed to run resource optimization: {e}")

    def _optimize_workspace_resources(self, workspace_id: str, allocations: List[ResourceAllocation]) -> List[OptimizationResult]:
        """Optimize resources for a specific workspace"""
        try:
            optimization_results = []

            for allocation in allocations:
                if self._needs_optimization(allocation):
                    result = self._optimize_resource_allocation(allocation)
                    if result:
                        optimization_results.append(result)

            return optimization_results

        except Exception as e:
            self.logger.error(f"Failed to optimize workspace {workspace_id}: {e}")
            return []

    def _needs_optimization(self, allocation: ResourceAllocation) -> bool:
        """Check if resource allocation needs optimization"""
        try:
            if allocation.resource_type == ResourceType.MEMORY:
                return allocation.current_usage > self.memory_threshold
            elif allocation.resource_type == ResourceType.CPU:
                return allocation.current_usage > self.cpu_threshold
            elif allocation.resource_type == ResourceType.AGENTS:
                return allocation.current_usage > self.agent_threshold
            else:
                # For other resource types, check if usage is significantly different from optimal
                usage_ratio = allocation.current_usage / allocation.optimal_amount if allocation.optimal_amount > 0 else 1.0
                return usage_ratio > 1.2 or usage_ratio < 0.8

        except Exception as e:
            self.logger.error(f"Failed to check optimization need: {e}")
            return False

    def _optimize_resource_allocation(self, allocation: ResourceAllocation) -> Optional[OptimizationResult]:
        """Optimize a specific resource allocation"""
        try:
            previous_allocation = allocation.allocated_amount
            new_allocation = self._calculate_optimal_allocation(allocation)

            if new_allocation != previous_allocation:
                # Update allocation
                allocation.allocated_amount = new_allocation
                allocation.last_optimization = datetime.now().isoformat()
                allocation.optimization_status = "optimized"

                # Calculate optimization gain
                if previous_allocation > 0:
                    optimization_gain = ((previous_allocation - new_allocation) / previous_allocation) * 100.0
                else:
                    optimization_gain = 0.0

                # Create optimization result
                result = OptimizationResult(
                    workspace_id=allocation.workspace_id,
                    resource_type=allocation.resource_type,
                    previous_allocation=previous_allocation,
                    new_allocation=new_allocation,
                    optimization_gain=optimization_gain,
                    strategy_used=self.current_strategy
                )

                self.logger.info(f"Optimized {allocation.resource_type.value} for {allocation.workspace_id}: "
                               f"{previous_allocation:.2f} -> {new_allocation:.2f} ({optimization_gain:.2f}% gain)")

                return result

            return None

        except Exception as e:
            self.logger.error(f"Failed to optimize resource allocation: {e}")
            return None

    def _calculate_optimal_allocation(self, allocation: ResourceAllocation) -> float:
        """Calculate optimal resource allocation based on strategy"""
        try:
            if self.current_strategy == OptimizationStrategy.BALANCED:
                return self._balanced_allocation_strategy(allocation)
            elif self.current_strategy == OptimizationStrategy.PERFORMANCE_FOCUSED:
                return self._performance_focused_strategy(allocation)
            elif self.current_strategy == OptimizationStrategy.RESOURCE_EFFICIENT:
                return self._resource_efficient_strategy(allocation)
            elif self.current_strategy == OptimizationStrategy.AGGRESSIVE:
                return self._aggressive_strategy(allocation)
            else:
                return allocation.optimal_amount

        except Exception as e:
            self.logger.error(f"Failed to calculate optimal allocation: {e}")
            return allocation.allocated_amount

    def _balanced_allocation_strategy(self, allocation: ResourceAllocation) -> float:
        """Balanced resource allocation strategy"""
        try:
            # Balance between current usage and optimal amount
            if allocation.current_usage > allocation.optimal_amount:
                # Reduce allocation if usage is high
                return max(allocation.optimal_amount * 0.9, allocation.current_usage * 0.8)
            else:
                # Increase allocation if usage is low
                return min(allocation.optimal_amount * 1.1, allocation.current_usage * 1.2)

        except Exception as e:
            self.logger.error(f"Failed to apply balanced strategy: {e}")
            return allocation.allocated_amount

    def _performance_focused_strategy(self, allocation: ResourceAllocation) -> float:
        """Performance-focused resource allocation strategy"""
        try:
            # Prioritize performance over resource efficiency
            if allocation.current_usage > allocation.optimal_amount:
                # Increase allocation for better performance
                return max(allocation.optimal_amount * 1.2, allocation.current_usage * 1.1)
            else:
                # Maintain current allocation
                return allocation.allocated_amount

        except Exception as e:
            self.logger.error(f"Failed to apply performance-focused strategy: {e}")
            return allocation.allocated_amount

    def _resource_efficient_strategy(self, allocation: ResourceAllocation) -> float:
        """Resource-efficient allocation strategy"""
        try:
            # Prioritize resource efficiency over performance
            if allocation.current_usage < allocation.optimal_amount * 0.7:
                # Reduce allocation if usage is significantly low
                return allocation.current_usage * 1.1
            else:
                # Maintain current allocation
                return allocation.allocated_amount

        except Exception as e:
            self.logger.error(f"Failed to apply resource-efficient strategy: {e}")
            return allocation.allocated_amount

    def _aggressive_strategy(self, allocation: ResourceAllocation) -> float:
        """Aggressive resource allocation strategy"""
        try:
            # Aggressively optimize resources
            if allocation.current_usage > allocation.optimal_amount:
                # Significantly reduce allocation
                return allocation.optimal_amount * 0.8
            else:
                # Significantly increase allocation
                return allocation.optimal_amount * 1.3

        except Exception as e:
            self.logger.error(f"Failed to apply aggressive strategy: {e}")
            return allocation.allocated_amount

    def _update_optimization_metrics(self, optimizations_count: int, total_gain: float):
        """Update optimization performance metrics"""
        try:
            self.performance_manager.add_metric("resource_optimization_runs", optimizations_count, "count", "workspace")
            self.performance_manager.add_metric("resource_optimization_gains", total_gain, "percent", "workspace")

            # Calculate allocation efficiency
            if self.resource_allocations:
                total_allocations = sum(len(allocations) for allocations in self.resource_allocations.values())
                if total_allocations > 0:
                    efficiency = (total_allocations - len([a for a in self._get_all_allocations() if a.optimization_status == "pending"])) / total_allocations * 100.0
                    self.performance_manager.add_metric("resource_allocation_efficiency", efficiency, "percent", "workspace")

        except Exception as e:
            self.logger.error(f"Failed to update optimization metrics: {e}")

    def _get_all_allocations(self) -> List[ResourceAllocation]:
        """Get all resource allocations across all workspaces"""
        try:
            all_allocations = []
            for allocations in self.resource_allocations.values():
                all_allocations.extend(allocations)
            return all_allocations
        except Exception as e:
            self.logger.error(f"Failed to get all allocations: {e}")
            return []

    def register_workspace_resources(self, workspace_id: str, resource_info: Dict[str, Any]):
        """Register resources for a workspace"""
        try:
            allocations = []

            # Memory allocation
            if "memory_mb" in resource_info:
                allocations.append(ResourceAllocation(
                    workspace_id=workspace_id,
                    resource_type=ResourceType.MEMORY,
                    current_usage=resource_info.get("memory_mb", 0),
                    allocated_amount=resource_info.get("memory_mb", 0),
                    optimal_amount=resource_info.get("memory_mb", 0) * 0.8
                ))

            # CPU allocation
            if "cpu_percent" in resource_info:
                allocations.append(ResourceAllocation(
                    workspace_id=workspace_id,
                    resource_type=ResourceType.CPU,
                    current_usage=resource_info.get("cpu_percent", 0),
                    allocated_amount=resource_info.get("cpu_percent", 0),
                    optimal_amount=resource_info.get("cpu_percent", 0) * 0.8
                ))

            # Agent allocation
            if "agent_count" in resource_info:
                allocations.append(ResourceAllocation(
                    workspace_id=workspace_id,
                    resource_type=ResourceType.AGENTS,
                    current_usage=resource_info.get("agent_count", 0),
                    allocated_amount=resource_info.get("agent_count", 0),
                    optimal_amount=min(resource_info.get("agent_count", 0), 10)  # Optimal: max 10 agents
                ))

            self.resource_allocations[workspace_id] = allocations
            self.logger.info(f"Registered resources for workspace {workspace_id}: {len(allocations)} resource types")

        except Exception as e:
            self.logger.error(f"Failed to register resources for workspace {workspace_id}: {e}")

    def get_optimization_status(self) -> Dict[str, Any]:
        """Get resource optimization status"""
        try:
            total_allocations = sum(len(allocations) for allocations in self.resource_allocations.values())
            optimized_allocations = sum(
                len([a for a in allocations if a.optimization_status == "optimized"])
                for allocations in self.resource_allocations.values()
            )

            return {
                "optimization_active": self.optimization_active,
                "total_resource_allocations": total_allocations,
                "optimized_allocations": optimized_allocations,
                "optimization_efficiency": (optimized_allocations / total_allocations * 100.0) if total_allocations > 0 else 0.0,
                "current_strategy": self.current_strategy.value,
                "last_optimization_run": self.last_optimization_run.isoformat() if self.last_optimization_run else None,
                "optimization_history_count": len(self.optimization_history)
            }

        except Exception as e:
            self.logger.error(f"Failed to get optimization status: {e}")
            return {"error": str(e)}

    def set_optimization_strategy(self, strategy: OptimizationStrategy):
        """Set the optimization strategy"""
        try:
            self.current_strategy = strategy
            self.logger.info(f"Optimization strategy changed to: {strategy.value}")
        except Exception as e:
            self.logger.error(f"Failed to set optimization strategy: {e}")

    def set_optimization_interval(self, interval_seconds: int):
        """Set the optimization interval"""
        try:
            self.optimization_interval = max(60, interval_seconds)  # Minimum 1 minute
            self.logger.info(f"Optimization interval set to: {self.optimization_interval} seconds")
        except Exception as e:
            self.logger.error(f"Failed to set optimization interval: {e}")

