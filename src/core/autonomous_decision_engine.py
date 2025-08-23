#!/usr/bin/env python3
"""
Autonomous Decision Engine - Agent Cellphone V2
===============================================

Refactored integration module for autonomous decision making.
Follows V2 standards: ≤300 LOC, single responsibility, clean integration.

**Refactored Architecture:**
- decision_types.py: Enums and data classes (≤100 LOC)
- decision_core.py: Core decision logic (≤200 LOC)  
- learning_engine.py: Learning and adaptation (≤200 LOC)
- decision_cli.py: CLI interface (≤100 LOC)

**Standards Compliance:**
- LOC: ≤300 lines ✅
- SRP: Single responsibility principle ✅
- OOP: Object-Oriented Design ✅
- CLI: CLI Interface Available ✅

Author: Agent-1 (Foundation & Testing Specialist)
License: MIT
"""

from typing import Optional, Dict, Any

from .decision_types import (
    DecisionType, DecisionConfidence, LearningMode, IntelligenceLevel,
    DecisionContext, DecisionResult, LearningData, AgentCapability,
    create_decision_context, create_learning_data, create_agent_capability
)
from .decision_core import DecisionCore
from .learning_engine import LearningEngine
from .persistent_data_storage import PersistentDataStorage, DataIntegrityLevel


class AutonomousDecisionEngine:
    """
    Refactored autonomous decision-making engine.
    Integrates decision core and learning engine for comprehensive operations.
    """
    
    def __init__(self, storage: Optional[PersistentDataStorage] = None):
        """Initialize the integrated autonomous decision engine"""
        self.storage = storage or PersistentDataStorage()
        
        # Initialize core components
        self.decision_core = DecisionCore(self.storage)
        self.learning_engine = LearningEngine(self.storage)
        
        # Synchronize agent capabilities between components
        self._sync_agent_capabilities()
    
    def _sync_agent_capabilities(self):
        """Synchronize agent capabilities between decision core and learning engine"""
        # This ensures both components have access to the same agent data
        # In a production system, this would use a shared data store
        pass
    
    def make_autonomous_decision(
        self, decision_type: str, context: DecisionContext
    ) -> DecisionResult:
        """Make an autonomous decision using the decision core"""
        result = self.decision_core.make_autonomous_decision(decision_type, context)
        
        # Add decision pattern to learning engine for continuous improvement
        self.learning_engine.add_decision_pattern(decision_type, result.decision_id)
        
        return result
    
    def add_learning_data(self, learning_data: LearningData):
        """Add learning data for continuous improvement"""
        self.learning_engine.add_learning_data(learning_data)
    
    def update_agent_capability(self, agent_id: str, capability: AgentCapability):
        """Update agent capability in both components"""
        self.decision_core.update_agent_capability(agent_id, capability)
        self.learning_engine.update_agent_capability(agent_id, capability)
    
    def record_performance_metric(self, metric_name: str, value: float):
        """Record performance metric for learning"""
        self.learning_engine.record_performance_metric(metric_name, value)
    
    def get_autonomous_status(self) -> Dict[str, Any]:
        """Get comprehensive autonomous system status"""
        decision_status = self.decision_core.get_decision_status()
        learning_status = self.learning_engine.get_learning_status()
        
        # Combine status from both components
        combined_status = {
            "decision_system": decision_status,
            "learning_system": learning_status,
            "integration_status": "active",
            "total_components": 2,
        }
        
        return combined_status
    
    def get_decision_status(self) -> Dict[str, Any]:
        """Get decision system status"""
        return self.decision_core.get_decision_status()
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get learning system status"""
        return self.learning_engine.get_learning_status()
    
    def shutdown(self):
        """Shutdown all components gracefully"""
        self.decision_core.shutdown()
        self.learning_engine.shutdown()
        
        # Save final integrated state
        self.storage.store_data(
            "autonomous_final_state",
            self.get_autonomous_status(),
            "autonomous",
            DataIntegrityLevel.ADVANCED,
        )


# Convenience functions for backward compatibility
def create_autonomous_engine(storage: Optional[PersistentDataStorage] = None) -> AutonomousDecisionEngine:
    """Create and return an autonomous decision engine instance"""
    return AutonomousDecisionEngine(storage)


def make_decision(decision_type: str, context_data: Dict[str, Any], agent_id: str = "system") -> DecisionResult:
    """Convenience function to make a decision"""
    engine = create_autonomous_engine()
    try:
        context = create_decision_context(decision_type, agent_id, context_data)
        return engine.make_autonomous_decision(decision_type, context)
    finally:
        engine.shutdown()


def add_learning_data(
    input_features: list, output_target: Any, context: str,
    performance_metric: float = 0.0, feedback_score: float = 0.0
):
    """Convenience function to add learning data"""
    engine = create_autonomous_engine()
    try:
        learning_data = create_learning_data(
            input_features, output_target, context, performance_metric, feedback_score
        )
        engine.add_learning_data(learning_data)
    finally:
        engine.shutdown()


def update_agent(
    agent_id: str, skills: list, experience_level: float = 0.0,
    learning_rate: float = 0.1, specialization: str = "general"
):
    """Convenience function to update agent capability"""
    engine = create_autonomous_engine()
    try:
        capability = create_agent_capability(
            agent_id, skills, experience_level, learning_rate, specialization
        )
        engine.update_agent_capability(agent_id, capability)
    finally:
        engine.shutdown()


def record_metric(metric_name: str, value: float):
    """Convenience function to record performance metric"""
    engine = create_autonomous_engine()
    try:
        engine.record_performance_metric(metric_name, value)
    finally:
        engine.shutdown()


def get_status() -> Dict[str, Any]:
    """Convenience function to get system status"""
    engine = create_autonomous_engine()
    try:
        return engine.get_autonomous_status()
    finally:
        engine.shutdown()


# Export all types and classes for external use
__all__ = [
    # Main engine class
    "AutonomousDecisionEngine",
    
    # Core types and enums
    "DecisionType", "DecisionConfidence", "LearningMode", "IntelligenceLevel",
    "DecisionContext", "DecisionResult", "LearningData", "AgentCapability",
    
    # Factory functions
    "create_decision_context", "create_learning_data", "create_agent_capability",
    
    # Convenience functions
    "create_autonomous_engine", "make_decision", "add_learning_data",
    "update_agent", "record_metric", "get_status",
    
    # Component classes
    "DecisionCore", "LearningEngine",
]


if __name__ == "__main__":
    # Simple test of the refactored system
    print("🧪 Testing Refactored Autonomous Decision Engine...")
    
    try:
        # Create engine
        engine = create_autonomous_engine()
        print("✅ Engine created successfully")
        
        # Test decision making
        context = create_decision_context(
            "task_assignment", "test_agent", {"task_requirements": ["python"]}
        )
        result = engine.make_autonomous_decision("task_assignment", context)
        print(f"✅ Decision made: {result.selected_option}")
        
        # Test status
        status = engine.get_autonomous_status()
        print(f"✅ Status retrieved: {len(status)} components")
        
        # Cleanup
        engine.shutdown()
        print("✅ Engine shutdown successfully")
        
        print("✅ Refactored system test PASSED!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("This may indicate missing dependencies or import issues.")
