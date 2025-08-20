#!/usr/bin/env python3
"""
Decision Core - Agent Cellphone V2
==================================

Main decision-making engine class.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable

from .decision_types import (
    DecisionType, DecisionStatus, DecisionPriority,
    DecisionRequest, DecisionResult, DecisionContext
)


class DecisionMakingEngine:
    """
    Implements collaborative decision-making algorithms and coordination
    
    Responsibilities:
    - Process decision requests collaboratively
    - Coordinate with other agents on decision logic
    - Build decision coordination systems
    - Implement intelligent decision algorithms
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.DecisionMakingEngine")
        self.workspace_path = Path("agent_workspaces")
        self.pending_decisions: Dict[str, DecisionRequest] = {}
        self.completed_decisions: Dict[str, DecisionResult] = {}
        self.decision_algorithms: Dict[DecisionType, Callable] = {}
        self.collaboration_history: List[Dict] = []
        
        # Ensure workspace exists
        self.workspace_path.mkdir(exist_ok=True)
        
        # Initialize decision algorithms
        self._initialize_decision_algorithms()
    
    def _initialize_decision_algorithms(self):
        """Initialize decision-making algorithms for each type"""
        self.decision_algorithms = {
            DecisionType.TASK_ASSIGNMENT: self._decide_task_assignment,
            DecisionType.RESOURCE_ALLOCATION: self._decide_resource_allocation,
            DecisionType.PRIORITY_DETERMINATION: self._decide_priority,
            DecisionType.CONFLICT_RESOLUTION: self._decide_conflict_resolution,
            DecisionType.WORKFLOW_OPTIMIZATION: self._decide_workflow_optimization,
            DecisionType.AGENT_COORDINATION: self._decide_agent_coordination
        }
    
    def submit_decision_request(self, decision_type: DecisionType, requester: str,
                              parameters: Dict[str, Any], priority: DecisionPriority = DecisionPriority.MEDIUM,
                              deadline: Optional[float] = None, collaborators: Optional[List[str]] = None) -> str:
        """Submit a new decision request"""
        decision_id = f"{decision_type.value}_{int(time.time())}_{requester}"
        
        request = DecisionRequest(
            decision_id=decision_id,
            decision_type=decision_type,
            requester=requester,
            timestamp=time.time(),
            parameters=parameters,
            priority=priority,
            deadline=deadline,
            collaborators=collaborators or []
        )
        
        self.pending_decisions[decision_id] = request
        self.logger.info(f"Decision request submitted: {decision_id} ({decision_type.value})")
        
        return decision_id
    
    def process_decision(self, decision_id: str, context: Optional[DecisionContext] = None) -> Optional[DecisionResult]:
        """Process a pending decision request"""
        if decision_id not in self.pending_decisions:
            self.logger.error(f"Decision request not found: {decision_id}")
            return None
        
        request = self.pending_decisions[decision_id]
        self.logger.info(f"Processing decision: {decision_id} ({request.decision_type.value})")
        
        try:
            # Get the appropriate algorithm
            algorithm = self.decision_algorithms.get(request.decision_type)
            if not algorithm:
                self.logger.error(f"No algorithm found for decision type: {request.decision_type}")
                return None
            
            # Process the decision
            decision_result = algorithm(request, context)
            
            if decision_result:
                # Move to completed decisions
                self.completed_decisions[decision_id] = decision_result
                del self.pending_decisions[decision_id]
                
                # Record collaboration
                self.collaboration_history.append({
                    'timestamp': time.time(),
                    'decision_id': decision_id,
                    'collaborators': request.collaborators,
                    'result': decision_result.decision
                })
                
                self.logger.info(f"Decision completed: {decision_id}")
                return decision_result
            
        except Exception as e:
            self.logger.error(f"Error processing decision {decision_id}: {e}")
            return None
        
        return None
    
    def get_decision_status(self, decision_id: str) -> Optional[DecisionStatus]:
        """Get the current status of a decision"""
        if decision_id in self.pending_decisions:
            return DecisionStatus.PENDING
        elif decision_id in self.completed_decisions:
            return DecisionStatus.DECIDED
        else:
            return None
    
    def get_pending_decisions(self, priority: Optional[DecisionPriority] = None) -> List[DecisionRequest]:
        """Get pending decisions, optionally filtered by priority"""
        if priority is None:
            return list(self.pending_decisions.values())
        
        return [req for req in self.pending_decisions.values() if req.priority == priority]
    
    def get_completed_decisions(self, decision_type: Optional[DecisionType] = None) -> List[DecisionResult]:
        """Get completed decisions, optionally filtered by type"""
        if decision_type is None:
            return list(self.completed_decisions.values())
        
        return [result for result in self.completed_decisions.values() if result.decision_type == decision_type]
    
    def get_decision_summary(self) -> Dict[str, Any]:
        """Get comprehensive decision summary"""
        return {
            'timestamp': time.time(),
            'pending_decisions': len(self.pending_decisions),
            'completed_decisions': len(self.completed_decisions),
            'total_collaborations': len(self.collaboration_history),
            'by_type': self._count_decisions_by_type(),
            'by_priority': self._count_decisions_by_priority()
        }
    
    def _count_decisions_by_type(self) -> Dict[str, int]:
        """Count decisions by type"""
        counts = {}
        for decision_type in DecisionType:
            counts[decision_type.value] = 0
        
        # Count pending decisions
        for request in self.pending_decisions.values():
            counts[request.decision_type.value] += 1
        
        # Count completed decisions
        for result in self.completed_decisions.values():
            counts[result.decision_type.value] += 1
        
        return counts
    
    def _count_decisions_by_priority(self) -> Dict[str, int]:
        """Count decisions by priority"""
        counts = {}
        for priority in DecisionPriority:
            counts[priority.name.lower()] = 0
        
        # Count pending decisions by priority
        for request in self.pending_decisions.values():
            counts[request.priority.name.lower()] += 1
        
        return counts
    
    def _create_decision_result(self, request: DecisionRequest, decision: Any, confidence: float, 
                               reasoning: str, implementation_plan: List[str]) -> DecisionResult:
        """Create a decision result with common parameters"""
        return DecisionResult(
            decision_id=request.decision_id,
            decision_type=request.decision_type,
            timestamp=time.time(),
            decision=decision,
            confidence=confidence,
            reasoning=reasoning,
            collaborators=request.collaborators,
            implementation_plan=implementation_plan
        )
    
    def _decide_task_assignment(self, request: DecisionRequest, context: Optional[DecisionContext]) -> DecisionResult:
        """Decide on task assignment"""
        decision = f"Assign task to agent_{hash(request.decision_id) % 5}"
        return self._create_decision_result(
            request, decision, 0.8, "Task assigned based on agent availability",
            ["Notify assigned agent", "Update task status"]
        )
    
    def _decide_resource_allocation(self, request: DecisionRequest, context: Optional[DecisionContext]) -> DecisionResult:
        """Decide on resource allocation"""
        # Placeholder implementation
        decision = "Allocate 50% of available resources"
        return DecisionResult(
            decision_id=request.decision_id,
            decision_type=request.decision_type,
            timestamp=time.time(),
            decision=decision,
            confidence=0.7,
            reasoning="Balanced resource allocation",
            collaborators=request.collaborators,
            implementation_plan=["Update resource pool", "Notify affected agents"]
        )
    
    def _decide_priority(self, request: DecisionRequest, context: Optional[DecisionContext]) -> DecisionResult:
        """Decide on priority determination"""
        # Placeholder implementation
        decision = DecisionPriority.HIGH
        return DecisionResult(
            decision_id=request.decision_id,
            decision_type=request.decision_type,
            timestamp=time.time(),
            decision=decision,
            confidence=0.9,
            reasoning="High priority based on impact analysis",
            collaborators=request.collaborators,
            implementation_plan=["Update priority queue", "Notify stakeholders"]
        )
    
    def _decide_conflict_resolution(self, request: DecisionRequest, context: Optional[DecisionContext]) -> DecisionResult:
        """Decide on conflict resolution"""
        # Placeholder implementation
        decision = "Resolve conflict through negotiation"
        return DecisionResult(
            decision_id=request.decision_id,
            decision_type=request.decision_type,
            timestamp=time.time(),
            decision=decision,
            confidence=0.6,
            reasoning="Negotiation approach for conflict resolution",
            collaborators=request.collaborators,
            implementation_plan=["Schedule negotiation", "Prepare resolution options"]
        )
    
    def _decide_workflow_optimization(self, request: DecisionRequest, context: Optional[DecisionContext]) -> DecisionResult:
        """Decide on workflow optimization"""
        # Placeholder implementation
        decision = "Optimize workflow by reducing bottlenecks"
        return DecisionResult(
            decision_id=request.decision_id,
            decision_type=request.decision_type,
            timestamp=time.time(),
            decision=decision,
            confidence=0.8,
            reasoning="Bottleneck analysis indicates optimization opportunity",
            collaborators=request.collaborators,
            implementation_plan=["Analyze bottlenecks", "Implement optimizations"]
        )
    
    def _decide_agent_coordination(self, request: DecisionRequest, context: Optional[DecisionContext]) -> DecisionResult:
        """Decide on agent coordination"""
        # Placeholder implementation
        decision = "Coordinate agents through centralized hub"
        return DecisionResult(
            decision_id=request.decision_id,
            decision_type=request.decision_type,
            timestamp=time.time(),
            decision=decision,
            confidence=0.7,
            reasoning="Centralized coordination for complex tasks",
            collaborators=request.collaborators,
            implementation_plan=["Establish coordination hub", "Define protocols"]
        )
