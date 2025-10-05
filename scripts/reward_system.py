#!/usr/bin/env python3
"""
Reward System for Autonomous Development Tasks
============================================

This module implements a comprehensive reward system for training autonomous development
agents. It provides both immediate and long-term rewards based on code quality, task
completion, architectural compliance, and autonomous decision-making capabilities.

The reward system is designed to:
- Encourage high-quality code production
- Promote V2 compliance and architectural patterns
- Reward efficient problem-solving and decision-making
- Provide feedback for continuous learning and improvement
- Balance immediate gratification with long-term project health

Usage:
    python scripts/reward_system.py --evaluate-task task.json --agent-output output.json
    python scripts/reward_system.py --train-reward-model --data-path data/training
    python scripts/reward_system.py --optimize-rewards --config configs/reward_config.yaml
"""

import os
import sys
import json
import argparse
import logging
import numpy as np
import torch
import torch.nn as nn
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import math

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.shared_logging import setup_logging
from validation.quality_gates_validator import QualityGatesValidator
from validation.v3_directives_validator import V3DirectivesValidator

class RewardType(Enum):
    """Types of rewards in the system."""
    IMMEDIATE = "immediate"          # Instant feedback for actions
    DELAYED = "delayed"              # Feedback after task completion
    CUMULATIVE = "cumulative"        # Accumulated rewards over time
    PENALTY = "penalty"              # Negative rewards for poor performance
    BONUS = "bonus"                  # Extra rewards for exceptional performance

class RewardCategory(Enum):
    """Categories of rewards."""
    CODE_QUALITY = "code_quality"
    FUNCTIONALITY = "functionality"
    ARCHITECTURE = "architecture"
    AUTONOMY = "autonomy"
    LEARNING = "learning"
    EFFICIENCY = "efficiency"
    COMPLIANCE = "compliance"
    INNOVATION = "innovation"

@dataclass
class RewardComponent:
    """A single component of the reward system."""
    name: str
    category: RewardCategory
    reward_type: RewardType
    weight: float
    min_value: float = 0.0
    max_value: float = 1.0
    description: str = ""
    
    def calculate(self, input_data: Dict[str, Any]) -> float:
        """Calculate reward value for this component."""
        # This will be implemented by specific reward components
        return 0.0

@dataclass
class RewardResult:
    """Result of reward calculation."""
    total_reward: float
    component_rewards: Dict[str, float]
    breakdown: Dict[str, Any]
    timestamp: datetime
    task_id: str
    agent_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        return result

class CodeQualityReward(RewardComponent):
    """Reward component for code quality metrics."""
    
    def __init__(self, weight: float = 0.25):
        super().__init__(
            name="code_quality",
            category=RewardCategory.CODE_QUALITY,
            reward_type=RewardType.IMMEDIATE,
            weight=weight,
            description="Rewards based on code quality metrics"
        )
    
    def calculate(self, input_data: Dict[str, Any]) -> float:
        """Calculate code quality reward."""
        code_metrics = input_data.get("code_metrics", {})
        
        # Syntax correctness (0-1)
        syntax_score = code_metrics.get("syntax_correctness", 0.0)
        
        # Style compliance (0-1)
        style_score = code_metrics.get("style_compliance", 0.0)
        
        # Complexity score (0-1, higher is better)
        complexity_score = code_metrics.get("complexity_score", 0.0)
        
        # Maintainability score (0-1)
        maintainability_score = code_metrics.get("maintainability_score", 0.0)
        
        # Test coverage (0-1)
        test_coverage = code_metrics.get("test_coverage", 0.0)
        
        # Calculate weighted average
        weights = [0.2, 0.2, 0.2, 0.2, 0.2]
        scores = [syntax_score, style_score, complexity_score, maintainability_score, test_coverage]
        
        return np.average(scores, weights=weights)

class FunctionalityReward(RewardComponent):
    """Reward component for functionality and correctness."""
    
    def __init__(self, weight: float = 0.2):
        super().__init__(
            name="functionality",
            category=RewardCategory.FUNCTIONALITY,
            reward_type=RewardType.DELAYED,
            weight=weight,
            description="Rewards based on functional correctness"
        )
    
    def calculate(self, input_data: Dict[str, Any]) -> float:
        """Calculate functionality reward."""
        test_results = input_data.get("test_results", {})
        
        # Test pass rate (0-1)
        total_tests = test_results.get("total_tests", 0)
        passed_tests = test_results.get("passed_tests", 0)
        test_pass_rate = passed_tests / total_tests if total_tests > 0 else 0.0
        
        # Edge case handling (0-1)
        edge_cases_tested = test_results.get("edge_cases_tested", 0)
        total_edge_cases = test_results.get("total_edge_cases", 5)  # Assume 5 edge cases
        edge_case_score = min(1.0, edge_cases_tested / total_edge_cases)
        
        # Error handling (0-1)
        error_tests_passed = test_results.get("error_tests_passed", 0)
        total_error_tests = test_results.get("total_error_tests", 0)
        error_handling_score = error_tests_passed / total_error_tests if total_error_tests > 0 else 0.0
        
        # Performance requirements (0-1)
        performance_met = test_results.get("performance_requirements_met", False)
        performance_score = 1.0 if performance_met else 0.0
        
        # Calculate weighted average
        weights = [0.4, 0.2, 0.2, 0.2]
        scores = [test_pass_rate, edge_case_score, error_handling_score, performance_score]
        
        return np.average(scores, weights=weights)

class ArchitectureReward(RewardComponent):
    """Reward component for architectural compliance."""
    
    def __init__(self, weight: float = 0.2):
        super().__init__(
            name="architecture",
            category=RewardCategory.ARCHITECTURE,
            reward_type=RewardType.DELAYED,
            weight=weight,
            description="Rewards based on architectural compliance"
        )
    
    def calculate(self, input_data: Dict[str, Any]) -> float:
        """Calculate architecture reward."""
        v2_compliance = input_data.get("v2_compliance", {})
        
        # V2 compliance score (0-1)
        compliance_score = v2_compliance.get("overall_score", 0.0)
        
        # Design pattern usage (0-1)
        design_patterns = v2_compliance.get("design_patterns_used", [])
        pattern_score = min(1.0, len(design_patterns) / 3.0)  # 3 patterns is good
        
        # Modularity score (0-1)
        modularity_score = v2_compliance.get("modularity_score", 0.0)
        
        # Dependency management (0-1)
        dependency_score = v2_compliance.get("dependency_management_score", 0.0)
        
        # Code organization (0-1)
        organization_score = v2_compliance.get("code_organization_score", 0.0)
        
        # Calculate weighted average
        weights = [0.3, 0.2, 0.2, 0.15, 0.15]
        scores = [compliance_score, pattern_score, modularity_score, dependency_score, organization_score]
        
        return np.average(scores, weights=weights)

class AutonomyReward(RewardComponent):
    """Reward component for autonomous decision-making."""
    
    def __init__(self, weight: float = 0.15):
        super().__init__(
            name="autonomy",
            category=RewardCategory.AUTONOMY,
            reward_type=RewardType.CUMULATIVE,
            weight=weight,
            description="Rewards based on autonomous decision-making"
        )
    
    def calculate(self, input_data: Dict[str, Any]) -> float:
        """Calculate autonomy reward."""
        autonomy_metrics = input_data.get("autonomy_metrics", {})
        
        # Decision quality (0-1)
        decision_quality = autonomy_metrics.get("decision_quality", 0.0)
        
        # Problem-solving efficiency (0-1)
        problem_solving = autonomy_metrics.get("problem_solving_efficiency", 0.0)
        
        # Self-correction ability (0-1)
        self_corrections = autonomy_metrics.get("self_corrections_made", 0)
        self_correction_score = min(1.0, self_corrections / 3.0)  # 3 corrections is good
        
        # Initiative score (0-1)
        initiatives_taken = autonomy_metrics.get("initiatives_taken", 0)
        initiative_score = min(1.0, initiatives_taken / 2.0)  # 2 initiatives is good
        
        # Calculate weighted average
        weights = [0.3, 0.3, 0.2, 0.2]
        scores = [decision_quality, problem_solving, self_correction_score, initiative_score]
        
        return np.average(scores, weights=weights)

class LearningReward(RewardComponent):
    """Reward component for learning and adaptation."""
    
    def __init__(self, weight: float = 0.1):
        super().__init__(
            name="learning",
            category=RewardCategory.LEARNING,
            reward_type=RewardType.CUMULATIVE,
            weight=weight,
            description="Rewards based on learning and adaptation"
        )
    
    def calculate(self, input_data: Dict[str, Any]) -> float:
        """Calculate learning reward."""
        learning_metrics = input_data.get("learning_metrics", {})
        
        # Adaptation score (0-1)
        adaptation_score = learning_metrics.get("adaptation_score", 0.0)
        
        # Knowledge application (0-1)
        knowledge_applied = learning_metrics.get("knowledge_applied", 0)
        knowledge_score = min(1.0, knowledge_applied / 5.0)  # 5 applications is good
        
        # Pattern recognition (0-1)
        patterns_recognized = learning_metrics.get("patterns_recognized", 0)
        pattern_recognition_score = min(1.0, patterns_recognized / 3.0)  # 3 patterns is good
        
        # Improvement over time (0-1)
        improvement_rate = learning_metrics.get("improvement_rate", 0.0)
        
        # Calculate weighted average
        weights = [0.3, 0.25, 0.25, 0.2]
        scores = [adaptation_score, knowledge_score, pattern_recognition_score, improvement_rate]
        
        return np.average(scores, weights=weights)

class EfficiencyReward(RewardComponent):
    """Reward component for efficiency and performance."""
    
    def __init__(self, weight: float = 0.1):
        super().__init__(
            name="efficiency",
            category=RewardCategory.EFFICIENCY,
            reward_type=RewardType.IMMEDIATE,
            weight=weight,
            description="Rewards based on efficiency and performance"
        )
    
    def calculate(self, input_data: Dict[str, Any]) -> float:
        """Calculate efficiency reward."""
        efficiency_metrics = input_data.get("efficiency_metrics", {})
        
        # Time efficiency (0-1)
        expected_time = efficiency_metrics.get("expected_time", 60)  # minutes
        actual_time = efficiency_metrics.get("actual_time", 60)
        time_efficiency = max(0.0, 1.0 - (actual_time - expected_time) / expected_time)
        
        # Resource efficiency (0-1)
        resource_usage = efficiency_metrics.get("resource_usage", 0.5)
        resource_efficiency = 1.0 - resource_usage  # Lower usage is better
        
        # Code efficiency (0-1)
        code_efficiency = efficiency_metrics.get("code_efficiency_score", 0.0)
        
        # Memory efficiency (0-1)
        memory_efficiency = efficiency_metrics.get("memory_efficiency_score", 0.0)
        
        # Calculate weighted average
        weights = [0.3, 0.2, 0.3, 0.2]
        scores = [time_efficiency, resource_efficiency, code_efficiency, memory_efficiency]
        
        return np.average(scores, weights=weights)

class InnovationReward(RewardComponent):
    """Reward component for innovation and creativity."""
    
    def __init__(self, weight: float = 0.05):
        super().__init__(
            name="innovation",
            category=RewardCategory.INNOVATION,
            reward_type=RewardType.BONUS,
            weight=weight,
            description="Rewards based on innovation and creativity"
        )
    
    def calculate(self, input_data: Dict[str, Any]) -> float:
        """Calculate innovation reward."""
        innovation_metrics = input_data.get("innovation_metrics", {})
        
        # Novel solutions (0-1)
        novel_solutions = innovation_metrics.get("novel_solutions", 0)
        novelty_score = min(1.0, novel_solutions / 2.0)  # 2 novel solutions is good
        
        # Creative problem solving (0-1)
        creative_solutions = innovation_metrics.get("creative_solutions", 0)
        creativity_score = min(1.0, creative_solutions / 1.0)  # 1 creative solution is good
        
        # Optimization improvements (0-1)
        optimizations = innovation_metrics.get("optimizations_made", 0)
        optimization_score = min(1.0, optimizations / 2.0)  # 2 optimizations is good
        
        # Best practices adoption (0-1)
        best_practices = innovation_metrics.get("best_practices_adopted", 0)
        best_practice_score = min(1.0, best_practices / 3.0)  # 3 practices is good
        
        # Calculate weighted average
        weights = [0.3, 0.3, 0.2, 0.2]
        scores = [novelty_score, creativity_score, optimization_score, best_practice_score]
        
        return np.average(scores, weights=weights)

class RewardSystem:
    """Main reward system for autonomous development agents."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.logger = setup_logging("reward_system")
        self.config = config or self._load_default_config()
        
        # Initialize reward components
        self.components = self._initialize_components()
        
        # Reward history for learning
        self.reward_history: List[RewardResult] = []
        
        # Performance tracking
        self.performance_metrics = {
            "total_rewards": 0.0,
            "average_reward": 0.0,
            "reward_trend": 0.0,
            "best_performance": 0.0
        }
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "reward_components": {
                "code_quality": 0.25,
                "functionality": 0.2,
                "architecture": 0.2,
                "autonomy": 0.15,
                "learning": 0.1,
                "efficiency": 0.1,
                "innovation": 0.05
            },
            "penalty_multiplier": 0.5,
            "bonus_threshold": 0.8,
            "learning_rate": 0.01,
            "decay_factor": 0.95
        }
    
    def _initialize_components(self) -> List[RewardComponent]:
        """Initialize reward components."""
        components = []
        
        # Get component weights from config
        weights = self.config["reward_components"]
        
        # Add all reward components
        components.append(CodeQualityReward(weights["code_quality"]))
        components.append(FunctionalityReward(weights["functionality"]))
        components.append(ArchitectureReward(weights["architecture"]))
        components.append(AutonomyReward(weights["autonomy"]))
        components.append(LearningReward(weights["learning"]))
        components.append(EfficiencyReward(weights["efficiency"]))
        components.append(InnovationReward(weights["innovation"]))
        
        return components
    
    def calculate_reward(self, task_data: Dict[str, Any], agent_output: Dict[str, Any], 
                        task_id: str, agent_id: str) -> RewardResult:
        """Calculate total reward for agent performance."""
        # Prepare input data
        input_data = {
            "code_metrics": agent_output.get("code_metrics", {}),
            "test_results": agent_output.get("test_results", {}),
            "v2_compliance": agent_output.get("v2_compliance", {}),
            "autonomy_metrics": agent_output.get("autonomy_metrics", {}),
            "learning_metrics": agent_output.get("learning_metrics", {}),
            "efficiency_metrics": agent_output.get("efficiency_metrics", {}),
            "innovation_metrics": agent_output.get("innovation_metrics", {}),
            "task_data": task_data
        }
        
        # Calculate component rewards
        component_rewards = {}
        total_reward = 0.0
        
        for component in self.components:
            try:
                reward_value = component.calculate(input_data)
                component_rewards[component.name] = reward_value
                total_reward += reward_value * component.weight
            except Exception as e:
                self.logger.warning(f"Error calculating reward for {component.name}: {e}")
                component_rewards[component.name] = 0.0
        
        # Apply penalties and bonuses
        total_reward = self._apply_penalties_and_bonuses(total_reward, input_data)
        
        # Create reward result
        result = RewardResult(
            total_reward=total_reward,
            component_rewards=component_rewards,
            breakdown=self._create_breakdown(input_data, component_rewards),
            timestamp=datetime.now(),
            task_id=task_id,
            agent_id=agent_id
        )
        
        # Update performance metrics
        self._update_performance_metrics(result)
        
        # Store in history
        self.reward_history.append(result)
        
        return result
    
    def _apply_penalties_and_bonuses(self, base_reward: float, input_data: Dict[str, Any]) -> float:
        """Apply penalties and bonuses to base reward."""
        reward = base_reward
        
        # Apply penalties
        penalty_multiplier = self.config["penalty_multiplier"]
        
        # Penalty for syntax errors
        code_metrics = input_data.get("code_metrics", {})
        if code_metrics.get("syntax_correctness", 1.0) < 0.5:
            reward *= penalty_multiplier
        
        # Penalty for test failures
        test_results = input_data.get("test_results", {})
        if test_results.get("passed_tests", 0) < test_results.get("total_tests", 1) * 0.8:
            reward *= penalty_multiplier
        
        # Penalty for V2 compliance violations
        v2_compliance = input_data.get("v2_compliance", {})
        if v2_compliance.get("overall_score", 1.0) < 0.7:
            reward *= penalty_multiplier
        
        # Apply bonuses
        bonus_threshold = self.config["bonus_threshold"]
        
        # Bonus for exceptional performance
        if base_reward > bonus_threshold:
            reward *= 1.2  # 20% bonus
        
        # Bonus for innovation
        innovation_metrics = input_data.get("innovation_metrics", {})
        if innovation_metrics.get("novel_solutions", 0) > 0:
            reward *= 1.1  # 10% bonus
        
        # Bonus for learning
        learning_metrics = input_data.get("learning_metrics", {})
        if learning_metrics.get("adaptation_score", 0) > 0.8:
            reward *= 1.05  # 5% bonus
        
        return min(1.0, max(0.0, reward))  # Clamp to [0, 1]
    
    def _create_breakdown(self, input_data: Dict[str, Any], component_rewards: Dict[str, float]) -> Dict[str, Any]:
        """Create detailed breakdown of reward calculation."""
        breakdown = {
            "input_summary": {
                "code_quality_available": bool(input_data.get("code_metrics")),
                "test_results_available": bool(input_data.get("test_results")),
                "v2_compliance_available": bool(input_data.get("v2_compliance")),
                "autonomy_metrics_available": bool(input_data.get("autonomy_metrics")),
                "learning_metrics_available": bool(input_data.get("learning_metrics")),
                "efficiency_metrics_available": bool(input_data.get("efficiency_metrics")),
                "innovation_metrics_available": bool(input_data.get("innovation_metrics"))
            },
            "component_weights": {comp.name: comp.weight for comp in self.components},
            "component_scores": component_rewards,
            "penalties_applied": [],
            "bonuses_applied": []
        }
        
        # Add penalty information
        code_metrics = input_data.get("code_metrics", {})
        if code_metrics.get("syntax_correctness", 1.0) < 0.5:
            breakdown["penalties_applied"].append("syntax_errors")
        
        test_results = input_data.get("test_results", {})
        if test_results.get("passed_tests", 0) < test_results.get("total_tests", 1) * 0.8:
            breakdown["penalties_applied"].append("test_failures")
        
        v2_compliance = input_data.get("v2_compliance", {})
        if v2_compliance.get("overall_score", 1.0) < 0.7:
            breakdown["penalties_applied"].append("v2_compliance_violations")
        
        # Add bonus information
        if sum(component_rewards.values()) / len(component_rewards) > self.config["bonus_threshold"]:
            breakdown["bonuses_applied"].append("exceptional_performance")
        
        innovation_metrics = input_data.get("innovation_metrics", {})
        if innovation_metrics.get("novel_solutions", 0) > 0:
            breakdown["bonuses_applied"].append("innovation")
        
        return breakdown
    
    def _update_performance_metrics(self, result: RewardResult):
        """Update performance metrics."""
        self.performance_metrics["total_rewards"] += result.total_reward
        
        # Calculate average reward
        if len(self.reward_history) > 0:
            self.performance_metrics["average_reward"] = (
                self.performance_metrics["total_rewards"] / len(self.reward_history)
            )
        
        # Calculate reward trend
        if len(self.reward_history) >= 10:
            recent_rewards = [r.total_reward for r in self.reward_history[-10:]]
            older_rewards = [r.total_reward for r in self.reward_history[-20:-10]] if len(self.reward_history) >= 20 else recent_rewards
            self.performance_metrics["reward_trend"] = np.mean(recent_rewards) - np.mean(older_rewards)
        
        # Update best performance
        if result.total_reward > self.performance_metrics["best_performance"]:
            self.performance_metrics["best_performance"] = result.total_reward
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        return {
            "total_tasks": len(self.reward_history),
            "average_reward": self.performance_metrics["average_reward"],
            "reward_trend": self.performance_metrics["reward_trend"],
            "best_performance": self.performance_metrics["best_performance"],
            "component_averages": self._get_component_averages(),
            "recent_performance": self._get_recent_performance()
        }
    
    def _get_component_averages(self) -> Dict[str, float]:
        """Get average scores for each component."""
        if not self.reward_history:
            return {}
        
        component_averages = {}
        for component in self.components:
            scores = [result.component_rewards.get(component.name, 0.0) for result in self.reward_history]
            component_averages[component.name] = np.mean(scores)
        
        return component_averages
    
    def _get_recent_performance(self, window: int = 10) -> Dict[str, float]:
        """Get recent performance metrics."""
        if len(self.reward_history) < window:
            return {}
        
        recent_results = self.reward_history[-window:]
        return {
            "average_reward": np.mean([r.total_reward for r in recent_results]),
            "reward_std": np.std([r.total_reward for r in recent_results]),
            "improvement_rate": self._calculate_improvement_rate(recent_results)
        }
    
    def _calculate_improvement_rate(self, results: List[RewardResult]) -> float:
        """Calculate improvement rate over recent results."""
        if len(results) < 2:
            return 0.0
        
        rewards = [r.total_reward for r in results]
        return (rewards[-1] - rewards[0]) / len(rewards)
    
    def save_reward_history(self, filepath: str):
        """Save reward history to file."""
        with open(filepath, 'w') as f:
            json.dump([result.to_dict() for result in self.reward_history], f, indent=2)
    
    def load_reward_history(self, filepath: str):
        """Load reward history from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.reward_history = []
        for item in data:
            result = RewardResult(
                total_reward=item["total_reward"],
                component_rewards=item["component_rewards"],
                breakdown=item["breakdown"],
                timestamp=datetime.fromisoformat(item["timestamp"]),
                task_id=item["task_id"],
                agent_id=item["agent_id"]
            )
            self.reward_history.append(result)

class RewardOptimizer:
    """Optimizes reward system parameters based on performance."""
    
    def __init__(self, reward_system: RewardSystem):
        self.reward_system = reward_system
        self.logger = setup_logging("reward_optimizer")
    
    def optimize_weights(self, optimization_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Optimize component weights based on performance data."""
        # This is a simplified optimization - in practice, you'd use more sophisticated methods
        # like gradient descent or evolutionary algorithms
        
        current_weights = {comp.name: comp.weight for comp in self.reward_system.components}
        optimized_weights = current_weights.copy()
        
        # Analyze correlation between component scores and overall performance
        for component in self.reward_system.components:
            component_scores = []
            overall_scores = []
            
            for data in optimization_data:
                if component.name in data.get("component_rewards", {}):
                    component_scores.append(data["component_rewards"][component.name])
                    overall_scores.append(data.get("overall_performance", 0.0))
            
            if len(component_scores) > 5:  # Need sufficient data
                correlation = np.corrcoef(component_scores, overall_scores)[0, 1]
                
                # Adjust weight based on correlation
                if correlation > 0.3:  # Strong positive correlation
                    optimized_weights[component.name] = min(0.5, current_weights[component.name] * 1.1)
                elif correlation < -0.3:  # Strong negative correlation
                    optimized_weights[component.name] = max(0.05, current_weights[component.name] * 0.9)
        
        return optimized_weights

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Reward System for Autonomous Development")
    parser.add_argument("--evaluate-task", action="store_true", help="Evaluate a single task")
    parser.add_argument("--task-file", type=str, help="Path to task JSON file")
    parser.add_argument("--agent-output", type=str, help="Path to agent output JSON file")
    parser.add_argument("--train-reward-model", action="store_true", help="Train reward model")
    parser.add_argument("--data-path", type=str, help="Path to training data")
    parser.add_argument("--optimize-rewards", action="store_true", help="Optimize reward parameters")
    parser.add_argument("--config", type=str, help="Path to config file")
    parser.add_argument("--output", type=str, default="output", help="Output directory")
    
    args = parser.parse_args()
    
    # Setup output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize reward system
    config = {}
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    reward_system = RewardSystem(config)
    
    if args.evaluate_task:
        # Evaluate a single task
        if not args.task_file or not args.agent_output:
            print("Error: --task-file and --agent-output are required for evaluation")
            return
        
        with open(args.task_file, 'r') as f:
            task_data = json.load(f)
        
        with open(args.agent_output, 'r') as f:
            agent_output = json.load(f)
        
        result = reward_system.calculate_reward(
            task_data, agent_output, 
            task_data.get("task_id", "unknown"),
            agent_output.get("agent_id", "unknown")
        )
        
        print(f"Total Reward: {result.total_reward:.4f}")
        print("Component Rewards:")
        for name, score in result.component_rewards.items():
            print(f"  {name}: {score:.4f}")
        
        # Save result
        result_file = output_dir / f"reward_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        
        print(f"Result saved to {result_file}")
    
    elif args.train_reward_model:
        # Train reward model (placeholder)
        print("Reward model training not yet implemented")
    
    elif args.optimize_rewards:
        # Optimize reward parameters
        print("Reward optimization not yet implemented")

if __name__ == "__main__":
    main()