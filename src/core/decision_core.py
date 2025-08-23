#!/usr/bin/env python3
"""
Decision Core - Agent Cellphone V2
==================================

Core decision-making engine for autonomous operations.
Follows V2 standards: ≤200 LOC, single responsibility, OOP design.
"""

import threading
import time
import random
from collections import defaultdict
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from .decision_types import (
    DecisionType, DecisionConfidence, IntelligenceLevel,
    DecisionContext, DecisionResult, AgentCapability
)
from .persistent_data_storage import PersistentDataStorage, DataIntegrityLevel


class DecisionCore:
    """Core decision-making engine for autonomous operations"""
    
    def __init__(self, storage: Optional[PersistentDataStorage] = None):
        """Initialize the decision core"""
        self.storage = storage or PersistentDataStorage()
        self.decision_history: List[DecisionResult] = []
        self.agent_capabilities: Dict[str, AgentCapability] = {}
        self.decision_patterns: Dict[str, List[str]] = defaultdict(list)
        self.intelligence_level = IntelligenceLevel.INTERMEDIATE
        self.decision_lock = threading.Lock()
        self._initialize_decision_system()
    
    def _initialize_decision_system(self):
        """Initialize the decision system"""
        for dir_path in ["autonomous/decisions", "autonomous/patterns"]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        self.storage.store_data("decision_config", {"intelligence_level": self.intelligence_level.value, "initialized_at": datetime.now().isoformat()}, "autonomous/decisions", DataIntegrityLevel.ADVANCED)
    
    def make_autonomous_decision(
        self, decision_type: str, context: DecisionContext
    ) -> DecisionResult:
        """Make an autonomous decision based on type and context"""
        with self.decision_lock:
            decision_id = f"decision_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # Apply intelligence-based decision making
            if self.intelligence_level == IntelligenceLevel.BASIC:
                decision = self._basic_decision(decision_type, context)
            elif self.intelligence_level == IntelligenceLevel.INTERMEDIATE:
                decision = self._intermediate_decision(decision_type, context)
            else:
                decision = self._advanced_decision(decision_type, context)
            
            # Create and store decision result
            result = DecisionResult(decision_id=decision_id, decision_type=decision_type, selected_option=decision["option"], confidence=decision["confidence"], reasoning=decision["reasoning"], alternatives=decision["alternatives"], expected_outcome=decision["expected_outcome"], risk_assessment=decision["risk_assessment"], timestamp=datetime.now().isoformat())
            
            self.decision_history.append(result)
            self.storage.store_data(f"decision_{decision_id}", result.__dict__, "autonomous/decisions", DataIntegrityLevel.ADVANCED)
            
            self.decision_patterns[decision_type].append(decision["pattern"])
            return result
    
    def _basic_decision(self, decision_type: str, context: DecisionContext) -> Dict[str, Any]:
        """Basic rule-based decision making"""
        if decision_type == DecisionType.TASK_ASSIGNMENT.value:
            available_agents = [
                aid for aid, cap in self.agent_capabilities.items() if cap.availability
            ]
            selected_agent = available_agents[0] if available_agents else "system"
            pattern = "round_robin_basic" if available_agents else "fallback_basic"
            
            return {"option": selected_agent, "confidence": DecisionConfidence.MEDIUM.value, "reasoning": f"Basic assignment to {selected_agent}", "alternatives": available_agents[:3], "expected_outcome": f"Task assigned to {selected_agent}", "risk_assessment": "Low - basic assignment", "pattern": pattern}
        
        elif decision_type == DecisionType.RESOURCE_ALLOCATION.value:
            resources = context.context_data.get("resources", [])
            agents = list(self.agent_capabilities.keys())
            
            if resources and agents:
                allocation = {agent: len(resources) // len(agents) for agent in agents}
                pattern = "equal_distribution_basic"
            else:
                allocation = {"system": 1}
                pattern = "fallback_basic"
            
            return {"option": str(allocation), "confidence": DecisionConfidence.MEDIUM.value, "reasoning": "Basic equal distribution of resources", "alternatives": [str(allocation)], "expected_outcome": "Resources distributed equally", "risk_assessment": "Low - simple distribution", "pattern": pattern}
        
        else:
            return {"option": "default_action", "confidence": DecisionConfidence.LOW.value, "reasoning": "Basic rule-based decision", "alternatives": ["default_action"], "expected_outcome": "Standard outcome", "risk_assessment": "Medium - generic decision", "pattern": "generic_basic"}
    
    def _intermediate_decision(self, decision_type: str, context: DecisionContext) -> Dict[str, Any]:
        """Intermediate pattern-based decision making"""
        if decision_type == DecisionType.TASK_ASSIGNMENT.value:
            task_requirements = context.context_data.get("task_requirements", [])
            available_agents = []
            
            for agent_id, capability in self.agent_capabilities.items():
                if capability.availability and all(skill in capability.skills for skill in task_requirements):
                    score = capability.experience_level * capability.learning_rate
                    available_agents.append((agent_id, score))
            
            if available_agents:
                selected_agent = max(available_agents, key=lambda x: x[1])[0]
                pattern = "capability_based_intermediate"
            else:
                selected_agent = "system"
                pattern = "fallback_intermediate"
            
            return {"option": selected_agent, "confidence": DecisionConfidence.MEDIUM.value, "reasoning": f"Capability-based assignment to {selected_agent}", "alternatives": [aid for aid, _ in available_agents[:3]], "expected_outcome": f"Task assigned to best qualified agent: {selected_agent}", "risk_assessment": "Medium - capability-based", "pattern": pattern}
        
        else:
            decision_type_name = context.decision_type
            if decision_type_name in self.decision_patterns and self.decision_patterns[decision_type_name]:
                pattern = max(set(self.decision_patterns[decision_type_name]), key=self.decision_patterns[decision_type_name].count)
                option = f"pattern_based_{pattern}"
            else:
                option = "default_action"
                pattern = "generic_intermediate"
            
            return {"option": option, "confidence": DecisionConfidence.MEDIUM.value, "reasoning": "Pattern-based decision making", "alternatives": [option], "expected_outcome": "Pattern-based outcome", "risk_assessment": "Medium - pattern-based", "pattern": pattern}
    
    def _advanced_decision(self, decision_type: str, context: DecisionContext) -> Dict[str, Any]:
        """Advanced predictive decision making"""
        if decision_type == DecisionType.TASK_ASSIGNMENT.value:
            task_requirements = context.context_data.get("task_requirements", [])
            available_agents = []
            
            for agent_id, capability in self.agent_capabilities.items():
                if capability.availability and all(skill in capability.skills for skill in task_requirements):
                    score = capability.experience_level * capability.learning_rate
                    available_agents.append((agent_id, score))
            
            if available_agents:
                selected_agent = max(available_agents, key=lambda x: x[1])[0]
                pattern = "predictive_advanced"
            else:
                selected_agent = "system"
                pattern = "fallback_advanced"
            
            return {"option": selected_agent, "confidence": DecisionConfidence.HIGH.value, "reasoning": f"Predictive assignment to {selected_agent}", "alternatives": [aid for aid, _ in available_agents[:3]], "expected_outcome": f"Task assigned to agent with best predicted performance: {selected_agent}", "risk_assessment": "Low - predictive modeling", "pattern": pattern}
        
        else:
            decision_type_name = context.decision_type
            if decision_type_name in self.decision_patterns and self.decision_patterns[decision_type_name]:
                patterns = self.decision_patterns[decision_type_name]
                pattern_counts = defaultdict(int)
                for pattern in patterns:
                    pattern_counts[pattern] += 1
                
                if pattern_counts:
                    best_pattern = max(pattern_counts.items(), key=lambda x: x[1])[0]
                    option = f"successful_pattern_{best_pattern}"
                    pattern = best_pattern
                else:
                    option = "default_action"
                    pattern = "generic_advanced"
            else:
                option = "default_action"
                pattern = "generic_advanced"
            
            return {"option": option, "confidence": DecisionConfidence.HIGH.value, "reasoning": "Advanced pattern-based decision making", "alternatives": [option], "expected_outcome": "Advanced pattern-based outcome", "risk_assessment": "Low - advanced analysis", "pattern": pattern}
    
    def update_agent_capability(self, agent_id: str, capability: AgentCapability):
        """Update agent capability information"""
        self.agent_capabilities[agent_id] = capability
        self.storage.store_data(f"agent_capability_{agent_id}", capability.__dict__, "autonomous/agents", DataIntegrityLevel.BASIC)
    
    def get_decision_status(self) -> Dict[str, Any]:
        """Get current decision system status"""
        with self.decision_lock:
            return {"intelligence_level": self.intelligence_level.value, "total_decisions": len(self.decision_history), "total_agents": len(self.agent_capabilities), "decision_patterns": dict(self.decision_patterns), "last_decision": self.decision_history[-1].timestamp if self.decision_history else None}
    
    def shutdown(self):
        """Shutdown the decision core"""
        self.storage.store_data("decision_final_state", self.get_decision_status(), "autonomous/decisions", DataIntegrityLevel.ADVANCED)


if __name__ == "__main__":
    print("🧪 Testing Decision Core Module...")
    
    class MockStorage:
        def store_data(self, key, data, path, integrity): pass
    
    core = DecisionCore(MockStorage())
    assert core.intelligence_level == IntelligenceLevel.INTERMEDIATE
    
    from .decision_types import create_decision_context
    context = create_decision_context("task_assignment", "test_agent", {"task_requirements": ["python"]})
    
    result = core.make_autonomous_decision("task_assignment", context)
    assert result.decision_type == "task_assignment"
    assert result.confidence in ["low", "medium", "high"]
    
    status = core.get_decision_status()
    assert "intelligence_level" in status
    
    print("✅ Decision Core Module smoke test PASSED!")
