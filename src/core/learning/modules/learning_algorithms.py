#!/usr/bin/env python3
"""
Learning Algorithms Module - Agent Cellphone V2
==============================================

Extracted from unified_learning_engine.py to provide focused learning algorithm functionality.
Follows V2 standards: modular design, SRP, clean interfaces.

**Author:** Captain Agent-3 (MODULAR-007 Contract)
**Created:** Current Sprint
**Status:** ACTIVE - MODULARIZATION IN PROGRESS
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from ..models import (
    LearningMode, LearningStrategy, LearningData, LearningMetrics
)
from ..decision_models import (
    DecisionAlgorithm, DecisionType, DecisionResult, DecisionContext
)


class LearningAlgorithmsModule:
    """
    Focused module for learning algorithm management and execution
    
    This module handles:
    - Learning strategy execution
    - Algorithm performance tracking
    - Adaptive learning mechanisms
    - Algorithm optimization
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.algorithms: Dict[str, LearningStrategy] = {}
        self.performance_history: Dict[str, List[float]] = {}
        self.algorithm_metrics: Dict[str, LearningMetrics] = {}
        
        self.logger.info("LearningAlgorithmsModule initialized")
    
    def register_learning_strategy(self, strategy: LearningStrategy) -> bool:
        """Register a new learning strategy"""
        try:
            if strategy.strategy_id in self.algorithms:
                self.logger.warning(f"Strategy {strategy.strategy_id} already exists, updating")
            
            self.algorithms[strategy.strategy_id] = strategy
            self.performance_history[strategy.strategy_id] = []
            self.algorithm_metrics[strategy.strategy_id] = LearningMetrics(
                metric_id=f"algo_{strategy.strategy_id}",
                agent_id="system",
                metric_name=f"algorithm_performance_{strategy.strategy_id}",
                metric_type="algorithm_performance",
                average_value=0.0,
                trend="stable",
                last_updated=datetime.now()
            )
            
            self.logger.info(f"Registered learning strategy: {strategy.strategy_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register learning strategy: {e}")
            return False
    
    def execute_learning_strategy(
        self,
        strategy_id: str,
        input_data: Dict[str, Any],
        context: str = "general"
    ) -> Optional[Dict[str, Any]]:
        """Execute a specific learning strategy"""
        try:
            if strategy_id not in self.algorithms:
                raise ValueError(f"Strategy {strategy_id} not found")
            
            strategy = self.algorithms[strategy_id]
            self.logger.info(f"Executing learning strategy: {strategy_id}")
            
            # Execute strategy based on type
            if strategy.learning_modes and LearningMode.ADAPTIVE in strategy.learning_modes:
                result = self._execute_adaptive_strategy(strategy, input_data, context)
            elif strategy.learning_modes and LearningMode.COLLABORATIVE in strategy.learning_modes:
                result = self._execute_collaborative_strategy(strategy, input_data, context)
            elif strategy.learning_modes and LearningMode.REINFORCEMENT in strategy.learning_modes:
                result = self._execute_reinforcement_strategy(strategy, input_data, context)
            else:
                result = self._execute_general_strategy(strategy, input_data, context)
            
            # Update performance metrics
            if result and "performance_score" in result:
                self._update_algorithm_performance(strategy_id, result["performance_score"])
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to execute learning strategy {strategy_id}: {e}")
            return None
    
    def _execute_adaptive_strategy(
        self,
        strategy: LearningStrategy,
        input_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """Execute adaptive learning strategy"""
        adaptation_rate = strategy.parameters.get("adaptation_rate", 0.1)
        performance_threshold = strategy.parameters.get("performance_threshold", 0.8)
        
        # Simulate adaptive learning execution
        base_performance = 0.7  # Base performance score
        context_boost = 0.1 if context == "specialized" else 0.0
        adaptation_boost = adaptation_rate * (1.0 - base_performance)
        
        final_performance = min(1.0, base_performance + context_boost + adaptation_boost)
        
        return {
            "strategy_id": strategy.strategy_id,
            "execution_mode": "adaptive",
            "performance_score": final_performance,
            "adaptation_applied": adaptation_boost,
            "context_boost": context_boost,
            "execution_timestamp": datetime.now().isoformat()
        }
    
    def _execute_collaborative_strategy(
        self,
        strategy: LearningStrategy,
        input_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """Execute collaborative learning strategy"""
        collaboration_threshold = strategy.parameters.get("collaboration_threshold", 0.6)
        max_collaborators = strategy.parameters.get("max_collaborators", 5)
        
        # Simulate collaborative learning execution
        base_performance = 0.75
        collaboration_boost = min(0.2, collaboration_threshold * 0.3)
        collaborator_count = min(max_collaborators, len(input_data.get("collaborators", [])))
        
        final_performance = min(1.0, base_performance + collaboration_boost + (collaborator_count * 0.02))
        
        return {
            "strategy_id": strategy.strategy_id,
            "execution_mode": "collaborative",
            "performance_score": final_performance,
            "collaboration_boost": collaboration_boost,
            "collaborator_count": collaborator_count,
            "execution_timestamp": datetime.now().isoformat()
        }
    
    def _execute_reinforcement_strategy(
        self,
        strategy: LearningStrategy,
        input_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """Execute reinforcement learning strategy"""
        exploration_rate = strategy.parameters.get("exploration_rate", 0.2)
        learning_rate = strategy.parameters.get("learning_rate", 0.1)
        
        # Simulate reinforcement learning execution
        base_performance = 0.65
        exploration_boost = exploration_rate * 0.15
        learning_boost = learning_rate * (1.0 - base_performance)
        
        final_performance = min(1.0, base_performance + exploration_boost + learning_boost)
        
        return {
            "strategy_id": strategy.strategy_id,
            "execution_mode": "reinforcement",
            "performance_score": final_performance,
            "exploration_boost": exploration_boost,
            "learning_boost": learning_boost,
            "execution_timestamp": datetime.now().isoformat()
        }
    
    def _execute_general_strategy(
        self,
        strategy: LearningStrategy,
        input_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """Execute general learning strategy"""
        # Simulate general strategy execution
        base_performance = 0.6
        context_boost = 0.1 if context == "optimized" else 0.0
        
        final_performance = min(1.0, base_performance + context_boost)
        
        return {
            "strategy_id": strategy.strategy_id,
            "execution_mode": "general",
            "performance_score": final_performance,
            "context_boost": context_boost,
            "execution_timestamp": datetime.now().isoformat()
        }
    
    def _update_algorithm_performance(self, strategy_id: str, performance_score: float):
        """Update performance metrics for an algorithm"""
        try:
            if strategy_id in self.performance_history:
                self.performance_history[strategy_id].append(performance_score)
                
                # Keep only last 100 performance scores
                if len(self.performance_history[strategy_id]) > 100:
                    self.performance_history[strategy_id] = self.performance_history[strategy_id][-100:]
                
                # Update metrics
                if strategy_id in self.algorithm_metrics:
                    metrics = self.algorithm_metrics[strategy_id]
                    scores = self.performance_history[strategy_id]
                    metrics.average_value = sum(scores) / len(scores)
                    
                    # Calculate trend
                    if len(scores) >= 2:
                        recent_avg = sum(scores[-10:]) / min(10, len(scores))
                        overall_avg = sum(scores[:-10]) / max(1, len(scores) - 10)
                        
                        if recent_avg > overall_avg * 1.05:
                            metrics.trend = "improving"
                        elif recent_avg < overall_avg * 0.95:
                            metrics.trend = "declining"
                        else:
                            metrics.trend = "stable"
                    
                    metrics.last_updated = datetime.now()
                    
        except Exception as e:
            self.logger.error(f"Failed to update algorithm performance: {e}")
    
    def get_algorithm_performance(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """Get performance metrics for a specific algorithm"""
        try:
            if strategy_id not in self.algorithms:
                return None
            
            metrics = self.algorithm_metrics.get(strategy_id)
            performance_history = self.performance_history.get(strategy_id, [])
            
            if not metrics:
                return None
            
            return {
                "strategy_id": strategy_id,
                "average_performance": metrics.average_value,
                "trend": metrics.trend,
                "total_executions": len(performance_history),
                "recent_performance": performance_history[-10:] if performance_history else [],
                "last_updated": metrics.last_updated.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get algorithm performance: {e}")
            return None
    
    def get_all_algorithm_performance(self) -> Dict[str, Dict[str, Any]]:
        """Get performance metrics for all algorithms"""
        try:
            performance_summary = {}
            
            for strategy_id in self.algorithms:
                performance_data = self.get_algorithm_performance(strategy_id)
                if performance_data:
                    performance_summary[strategy_id] = performance_data
            
            return performance_summary
            
        except Exception as e:
            self.logger.error(f"Failed to get all algorithm performance: {e}")
            return {}
    
    def optimize_algorithm_parameters(self, strategy_id: str) -> bool:
        """Optimize algorithm parameters based on performance history"""
        try:
            if strategy_id not in self.algorithms:
                return False
            
            strategy = self.algorithms[strategy_id]
            performance_history = self.performance_history.get(strategy_id, [])
            
            if len(performance_history) < 10:
                self.logger.info(f"Insufficient performance data for optimization: {strategy_id}")
                return False
            
            # Simple optimization: adjust parameters based on recent performance
            recent_avg = sum(performance_history[-10:]) / 10
            overall_avg = sum(performance_history) / len(performance_history)
            
            if recent_avg < overall_avg * 0.9:  # Performance declining
                # Increase exploration/adaptation
                if "adaptation_rate" in strategy.parameters:
                    strategy.parameters["adaptation_rate"] = min(0.3, strategy.parameters["adaptation_rate"] * 1.2)
                if "exploration_rate" in strategy.parameters:
                    strategy.parameters["exploration_rate"] = min(0.4, strategy.parameters["exploration_rate"] * 1.2)
                
                self.logger.info(f"Optimized parameters for {strategy_id} due to declining performance")
            
            elif recent_avg > overall_avg * 1.1:  # Performance improving
                # Fine-tune parameters
                if "adaptation_rate" in strategy.parameters:
                    strategy.parameters["adaptation_rate"] = max(0.05, strategy.parameters["adaptation_rate"] * 0.95)
                if "exploration_rate" in strategy.parameters:
                    strategy.parameters["exploration_rate"] = max(0.1, strategy.parameters["exploration_rate"] * 0.95)
                
                self.logger.info(f"Fine-tuned parameters for {strategy_id} due to improving performance")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to optimize algorithm parameters: {e}")
            return False
    
    def run_module_test(self) -> bool:
        """Run basic functionality test for the learning algorithms module"""
        try:
            # Test strategy registration
            test_strategy = LearningStrategy(
                strategy_id="test_strategy",
                name="Test Strategy",
                description="Test learning strategy for module validation",
                learning_modes=[LearningMode.ADAPTIVE],
                parameters={"adaptation_rate": 0.15, "performance_threshold": 0.85}
            )
            
            if not self.register_learning_strategy(test_strategy):
                return False
            
            # Test strategy execution
            result = self.execute_learning_strategy(
                "test_strategy",
                {"test_input": "test_value"},
                "test_context"
            )
            
            if not result:
                return False
            
            # Test performance tracking
            performance = self.get_algorithm_performance("test_strategy")
            if not performance:
                return False
            
            # Test optimization
            if not self.optimize_algorithm_parameters("test_strategy"):
                return False
            
            # Clean up test data
            self.algorithms.pop("test_strategy", None)
            self.performance_history.pop("test_strategy", None)
            self.algorithm_metrics.pop("test_strategy", None)
            
            self.logger.info("✅ Learning algorithms module test passed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Learning algorithms module test failed: {e}")
            return False
