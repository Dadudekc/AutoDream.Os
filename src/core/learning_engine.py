#!/usr/bin/env python3
"""
Learning Engine - Agent Cellphone V2
===================================

Learning and adaptation engine for autonomous decision making.
Follows V2 standards: ≤200 LOC, single responsibility, OOP design.
"""

import threading
import time
import statistics
from collections import defaultdict, deque
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from .decision_types import LearningData, AgentCapability, IntelligenceLevel, LearningMode
from .persistent_data_storage import PersistentDataStorage, DataIntegrityLevel


class LearningEngine:
    """Learning and adaptation engine for continuous improvement"""
    
    def __init__(self, storage: Optional[PersistentDataStorage] = None):
        """Initialize the learning engine"""
        self.storage = storage or PersistentDataStorage()
        
        # Learning state
        self.learning_data: List[LearningData] = []
        self.agent_capabilities: Dict[str, AgentCapability] = {}
        self.performance_metrics: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=100)
        )
        self.decision_patterns: Dict[str, List[str]] = defaultdict(list)
        
        # Learning configuration
        self.intelligence_level = IntelligenceLevel.INTERMEDIATE
        self.learning_mode = LearningMode.REINFORCEMENT
        
        # Threading and synchronization
        self.learning_lock = threading.Lock()
        self.adaptation_thread = None
        
        # Initialize learning system
        self._initialize_learning_system()
        self._start_adaptation_loop()
    
    def _initialize_learning_system(self):
        """Initialize the learning system"""
        for dir_path in ["autonomous/learning", "autonomous/agents", "autonomous/patterns"]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        self.storage.store_data("learning_config", {"intelligence_level": self.intelligence_level.value, "learning_mode": self.learning_mode.value, "initialized_at": datetime.now().isoformat()}, "autonomous/learning", DataIntegrityLevel.ADVANCED)
    
    def _start_adaptation_loop(self):
        """Start the autonomous adaptation loop"""
        self.adaptation_thread = threading.Thread(
            target=self._adaptation_loop, daemon=True
        )
        self.adaptation_thread.start()
    
    def _adaptation_loop(self):
        """Autonomous adaptation loop for continuous learning"""
        while True:
            try:
                self._evaluate_performance()
                self._adapt_strategies()
                self._update_intelligence()
                time.sleep(300)
            except Exception as e:
                print(f"Adaptation loop error: {e}")
                time.sleep(600)
    
    def _evaluate_performance(self):
        """Evaluate overall system performance"""
        with self.learning_lock:
            if not self.performance_metrics:
                return
            
            total_performance = 0
            metric_count = 0
            
            for metric_name, values in self.performance_metrics.items():
                if values:
                    avg_value = statistics.mean(values)
                    total_performance += avg_value
                    metric_count += 1
            
            if metric_count > 0:
                overall_performance = total_performance / metric_count
                self.storage.store_data("performance_evaluation", {"overall_performance": overall_performance, "evaluated_at": datetime.now().isoformat()}, "autonomous/learning", DataIntegrityLevel.BASIC)
    
    def _adapt_strategies(self):
        """Adapt decision-making strategies based on performance"""
        with self.learning_lock:
            for decision_type, patterns in self.decision_patterns.items():
                if len(patterns) > 10:  # Need sufficient data
                    successful_patterns = self._identify_successful_patterns(decision_type)
                    self._update_strategy_weights(decision_type, successful_patterns)
    
    def _update_intelligence(self):
        """Update intelligence level based on performance"""
        with self.learning_lock:
            if self.intelligence_level == IntelligenceLevel.BASIC and self._should_upgrade_intelligence():
                self.intelligence_level = IntelligenceLevel.INTERMEDIATE
                print("🧠 Intelligence level upgraded to INTERMEDIATE")
            elif self.intelligence_level == IntelligenceLevel.INTERMEDIATE and self._should_upgrade_intelligence():
                self.intelligence_level = IntelligenceLevel.ADVANCED
                print("🧠 Intelligence level upgraded to ADVANCED")
            
            self.storage.store_data("intelligence_level", self.intelligence_level.value, "autonomous/learning", DataIntegrityLevel.BASIC)
    
    def _should_upgrade_intelligence(self) -> bool:
        """Determine if intelligence should be upgraded"""
        if not self.performance_metrics:
            return False
        
        improvement_count = 0
        total_checks = 0
        
        for metric_name, values in list(self.performance_metrics.values()):
            if len(values) >= 20:
                recent_values = list(values)[-10:]
                older_values = list(values)[-20:-10]
                
                if recent_values and older_values:
                    recent_avg = statistics.mean(recent_values)
                    older_avg = statistics.mean(older_values)
                    
                    if recent_avg > older_avg * 1.1:
                        improvement_count += 1
                    total_checks += 1
        
        return total_checks > 0 and (improvement_count / total_checks) > 0.7
    
    def _identify_successful_patterns(self, decision_type: str) -> List[str]:
        """Identify successful decision patterns for a given type"""
        return list(self.decision_patterns[decision_type])[:3]
    
    def _update_strategy_weights(self, decision_type: str, successful_patterns: List[str]):
        """Update strategy weights based on successful patterns"""
        self.storage.store_data(f"strategy_weights_{decision_type}", {"successful_patterns": successful_patterns, "updated_at": datetime.now().isoformat()}, "autonomous/patterns", DataIntegrityLevel.BASIC)
    
    def add_learning_data(self, learning_data: LearningData):
        """Add new learning data for continuous improvement"""
        with self.learning_lock:
            self.learning_data.append(learning_data)
            self.storage.store_data(f"learning_data_{int(time.time())}", learning_data.__dict__, "autonomous/learning", DataIntegrityLevel.BASIC)
    
    def update_agent_capability(self, agent_id: str, capability: AgentCapability):
        """Update agent capability information"""
        self.agent_capabilities[agent_id] = capability
        self.storage.store_data(f"agent_capability_{agent_id}", capability.__dict__, "autonomous/agents", DataIntegrityLevel.BASIC)
    
    def record_performance_metric(self, metric_name: str, value: float):
        """Record a performance metric for learning"""
        with self.learning_lock:
            self.performance_metrics[metric_name].append(value)
    
    def add_decision_pattern(self, decision_type: str, pattern: str):
        """Add a decision pattern for learning"""
        with self.learning_lock:
            self.decision_patterns[decision_type].append(pattern)
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get current learning system status"""
        with self.learning_lock:
            return {
                "intelligence_level": self.intelligence_level.value,
                "learning_mode": self.learning_mode.value,
                "total_learning_data": len(self.learning_data),
                "total_agents": len(self.agent_capabilities),
                "decision_patterns": dict(self.decision_patterns),
                "performance_metrics": {name: len(values) for name, values in self.performance_metrics.items()},
            }
    
    def shutdown(self):
        """Shutdown the learning engine"""
        self.storage.store_data("learning_final_state", self.get_learning_status(), "autonomous/learning", DataIntegrityLevel.ADVANCED)
        if self.adaptation_thread:
            self.adaptation_thread.join(timeout=5)


if __name__ == "__main__":
    # Smoke test for learning engine
    print("🧪 Testing Learning Engine Module...")
    
    class MockStorage:
        def store_data(self, key, data, path, integrity):
            pass
    
    engine = LearningEngine(MockStorage())
    assert engine.intelligence_level == IntelligenceLevel.INTERMEDIATE
    
    from .decision_types import create_learning_data
    learning_data = create_learning_data([0.1, 0.2], "success", "test")
    engine.add_learning_data(learning_data)
    assert len(engine.learning_data) == 1
    
    engine.record_performance_metric("test_metric", 0.85)
    assert len(engine.performance_metrics["test_metric"]) == 1
    
    print("✅ Learning Engine Module smoke test PASSED!")
