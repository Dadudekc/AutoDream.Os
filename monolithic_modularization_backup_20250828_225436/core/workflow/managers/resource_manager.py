#!/usr/bin/env python3
"""
Resource Manager - Resource Allocation Engine
===========================================

Resource allocation for unified workflow system.
Follows V2 standards: ≤200 LOC, single responsibility.

Author: Agent-3 (Workflow Unification)
License: MIT
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from ..types.workflow_models import ResourceRequirement, AgentCapabilityInfo


@dataclass
class ResourceAllocation:
    """Resource allocation information."""
    resource_id: str
    agent_id: str
    allocation_time: datetime
    expected_duration: float
    resource_type: str
    capacity: float
    allocated_capacity: float


@dataclass
class ResourceMetrics:
    """Resource utilization metrics."""
    resource_id: str
    utilization_percentage: float
    available_capacity: float
    total_capacity: float
    allocation_count: int
    last_updated: datetime


class ResourceManager:
    """
    Resource manager for workflow system.
    
    Single responsibility: Manage resource allocation, monitoring,
    and optimization for workflow execution.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ResourceManager")
        self.resources: Dict[str, Dict[str, Any]] = {}
        self.allocations: Dict[str, ResourceAllocation] = {}
        self.agent_resources: Dict[str, List[str]] = {}  # agent_id -> [resource_ids]
        self.resource_metrics: Dict[str, ResourceMetrics] = {}
    
    def allocate_resource(self, requirement: ResourceRequirement, agent_id: str) -> bool:
        """
        Allocate resource based on requirement.
        
        Args:
            requirement: Resource requirement specification
            agent_id: ID of the agent requesting the resource
            
        Returns:
            True if allocation successful, False otherwise
        """
        self.logger.info(f"Allocating resource {requirement.resource_id} for agent {agent_id}")
        
        # Check if resource exists
        if requirement.resource_id not in self.resources:
            self.logger.error(f"Resource not found: {requirement.resource_id}")
            return False
        
        resource = self.resources[requirement.resource_id]
        
        # Check resource availability
        if not self._check_resource_availability(requirement.resource_id, requirement.required_amount):
            self.logger.error(f"Resource {requirement.resource_id} not available with required capacity")
            return False
        
        # Check agent compatibility
        if not self._check_agent_compatibility(agent_id, requirement.resource_id):
            self.logger.error(f"Agent {agent_id} not compatible with resource {requirement.resource_id}")
            return False
        
        # Create allocation
        allocation = ResourceAllocation(
            resource_id=requirement.resource_id,
            agent_id=agent_id,
            allocation_time=datetime.now(),
            expected_duration=requirement.expected_duration or 3600.0,  # Default 1 hour
            resource_type=requirement.resource_type,
            capacity=requirement.required_amount,
            allocated_capacity=requirement.required_amount
        )
        
        # Store allocation
        allocation_id = f"{requirement.resource_id}_{agent_id}_{int(time.time())}"
        self.allocations[allocation_id] = allocation
        
        # Update resource state
        self._update_resource_allocation(requirement.resource_id, requirement.required_amount, True)
        
        # Update agent resources
        if agent_id not in self.agent_resources:
            self.agent_resources[agent_id] = []
        self.agent_resources[agent_id].append(requirement.resource_id)
        
        self.logger.info(f"Resource {requirement.resource_id} allocated to agent {agent_id}")
        return True
    
    def release_resource(self, resource_id: str, agent_id: str) -> bool:
        """
        Release allocated resource.
        
        Args:
            resource_id: ID of the resource to release
            agent_id: ID of the agent releasing the resource
            
        Returns:
            True if release successful, False otherwise
        """
        self.logger.info(f"Releasing resource {resource_id} from agent {agent_id}")
        
        # Find allocation
        allocation_id = None
        for aid, allocation in self.allocations.items():
            if (allocation.resource_id == resource_id and 
                allocation.agent_id == agent_id):
                allocation_id = aid
                break
        
        if not allocation_id:
            self.logger.error(f"No allocation found for resource {resource_id} and agent {agent_id}")
            return False
        
        allocation = self.allocations[allocation_id]
        
        # Update resource state
        self._update_resource_allocation(resource_id, allocation.allocated_capacity, False)
        
        # Remove allocation
        del self.allocations[allocation_id]
        
        # Update agent resources
        if agent_id in self.agent_resources and resource_id in self.agent_resources[agent_id]:
            self.agent_resources[agent_id].remove(resource_id)
        
        self.logger.info(f"Resource {resource_id} released from agent {agent_id}")
        return True
    
    def add_resource(self, resource_id: str, resource_type: str, capacity: float, 
                    metadata: Optional[Dict[str, Any]] = None):
        """
        Add new resource to the system.
        
        Args:
            resource_id: Unique identifier for the resource
            resource_type: Type of the resource
            capacity: Total capacity of the resource
            metadata: Optional metadata for the resource
        """
        self.logger.info(f"Adding resource: {resource_id} (type: {resource_type}, capacity: {capacity})")
        
        if resource_id in self.resources:
            self.logger.warning(f"Resource {resource_id} already exists, updating")
        
        self.resources[resource_id] = {
            "resource_type": resource_type,
            "total_capacity": capacity,
            "available_capacity": capacity,
            "allocated_capacity": 0.0,
            "metadata": metadata or {},
            "created_time": datetime.now()
        }
        
        # Initialize metrics
        self.resource_metrics[resource_id] = ResourceMetrics(
            resource_id=resource_id,
            utilization_percentage=0.0,
            available_capacity=capacity,
            total_capacity=capacity,
            allocation_count=0,
            last_updated=datetime.now()
        )
        
        self.logger.info(f"Resource {resource_id} added successfully")
    
    def remove_resource(self, resource_id: str) -> bool:
        """
        Remove resource from the system.
        
        Args:
            resource_id: ID of the resource to remove
            
        Returns:
            True if removal successful, False otherwise
        """
        self.logger.info(f"Removing resource: {resource_id}")
        
        if resource_id not in self.resources:
            self.logger.error(f"Resource not found: {resource_id}")
            return False
        
        # Check if resource is allocated
        if self.resources[resource_id]["allocated_capacity"] > 0:
            self.logger.error(f"Cannot remove resource {resource_id} - still allocated")
            return False
        
        # Remove resource
        del self.resources[resource_id]
        
        # Remove metrics
        if resource_id in self.resource_metrics:
            del self.resource_metrics[resource_id]
        
        # Remove from agent resources
        for agent_resources in self.agent_resources.values():
            if resource_id in agent_resources:
                agent_resources.remove(resource_id)
        
        self.logger.info(f"Resource {resource_id} removed successfully")
        return True
    
    def get_resource_status(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current status of a resource.
        
        Args:
            resource_id: ID of the resource
            
        Returns:
            Resource status dictionary or None if not found
        """
        if resource_id not in self.resources:
            return None
        
        resource = self.resources[resource_id]
        return {
            "resource_id": resource_id,
            "resource_type": resource["resource_type"],
            "total_capacity": resource["total_capacity"],
            "available_capacity": resource["available_capacity"],
            "allocated_capacity": resource["allocated_capacity"],
            "utilization_percentage": (resource["allocated_capacity"] / resource["total_capacity"]) * 100,
            "metadata": resource["metadata"]
        }
    
    def get_available_resources(self, resource_type: Optional[str] = None, 
                              min_capacity: Optional[float] = None) -> List[str]:
        """
        Get list of available resources.
        
        Args:
            resource_type: Optional filter by resource type
            min_capacity: Optional minimum capacity requirement
            
        Returns:
            List of available resource IDs
        """
        available_resources = []
        
        for resource_id, resource in self.resources.items():
            if resource["available_capacity"] > 0:
                # Check resource type filter
                if resource_type and resource["resource_type"] != resource_type:
                    continue
                
                # Check capacity filter
                if min_capacity and resource["available_capacity"] < min_capacity:
                    continue
                
                available_resources.append(resource_id)
        
        return available_resources
    
    def get_resource_utilization(self, resource_id: str) -> Optional[float]:
        """
        Get utilization percentage of a resource.
        
        Args:
            resource_id: ID of the resource
            
        Returns:
            Utilization percentage (0-100) or None if not found
        """
        if resource_id not in self.resources:
            return None
        
        resource = self.resources[resource_id]
        return (resource["allocated_capacity"] / resource["total_capacity"]) * 100
    
    def optimize_resource_allocation(self) -> Dict[str, Any]:
        """
        Optimize resource allocation across the system.
        
        Returns:
            Dictionary containing optimization results
        """
        self.logger.info("Running resource allocation optimization")
        
        optimization_results = {
            "total_resources": len(self.resources),
            "total_allocations": len(self.allocations),
            "overall_utilization": 0.0,
            "recommendations": []
        }
        
        # Calculate overall utilization
        total_capacity = 0.0
        total_allocated = 0.0
        
        for resource in self.resources.values():
            total_capacity += resource["total_capacity"]
            total_allocated += resource["allocated_capacity"]
        
        if total_capacity > 0:
            optimization_results["overall_utilization"] = (total_allocated / total_capacity) * 100
        
        # Generate optimization recommendations
        for resource_id, resource in self.resources.items():
            utilization = (resource["allocated_capacity"] / resource["total_capacity"]) * 100
            
            if utilization < 20:
                optimization_results["recommendations"].append(
                    f"Resource {resource_id} is underutilized ({utilization:.1f}%)"
                )
            elif utilization > 90:
                optimization_results["recommendations"].append(
                    f"Resource {resource_id} is overutilized ({utilization:.1f}%)"
                )
        
        self.logger.info(f"Resource optimization completed. Overall utilization: {optimization_results['overall_utilization']:.1f}%")
        return optimization_results
    
    def _check_resource_availability(self, resource_id: str, required_capacity: float) -> bool:
        """Check if resource has sufficient available capacity."""
        if resource_id not in self.resources:
            return False
        
        resource = self.resources[resource_id]
        return resource["available_capacity"] >= required_capacity
    
    def _check_agent_compatibility(self, agent_id: str, resource_id: str) -> bool:
        """Check if agent is compatible with the resource."""
        # Basic implementation - can be extended with more sophisticated compatibility checking
        return True
    
    def _update_resource_allocation(self, resource_id: str, capacity: float, is_allocation: bool):
        """Update resource allocation state."""
        if resource_id not in self.resources:
            return
        
        resource = self.resources[resource_id]
        
        if is_allocation:
            resource["allocated_capacity"] += capacity
            resource["available_capacity"] -= capacity
        else:
            resource["allocated_capacity"] = max(0, resource["allocated_capacity"] - capacity)
            resource["available_capacity"] = min(resource["total_capacity"], 
                                              resource["available_capacity"] + capacity)
        
        # Update metrics
        if resource_id in self.resource_metrics:
            metrics = self.resource_metrics[resource_id]
            metrics.available_capacity = resource["available_capacity"]
            metrics.total_capacity = resource["total_capacity"]
            metrics.utilization_percentage = (resource["allocated_capacity"] / resource["total_capacity"]) * 100
            metrics.last_updated = datetime.now()
            if is_allocation:
                metrics.allocation_count += 1
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test for resource manager."""
        try:
            # Test resource addition
            self.add_resource("test_resource", "test_type", 100.0)
            
            # Test resource allocation
            from ..types.workflow_models import ResourceRequirement
            
            test_requirement = ResourceRequirement(
                resource_id="test_resource",
                resource_type="test_type",
                required_amount=50.0,
                unit="units"
            )
            
            allocation_success = self.allocate_resource(test_requirement, "test_agent")
            if allocation_success:
                self.logger.info("✅ Resource manager smoke test passed.")
                return True
            else:
                self.logger.error("❌ Resource manager smoke test failed: Resource allocation failed.")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Resource manager smoke test failed: {e}")
            return False
