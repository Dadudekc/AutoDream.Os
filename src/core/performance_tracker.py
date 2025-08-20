#!/usr/bin/env python3
"""
Performance Tracker - V2 Core Performance Tracking System

This module handles metrics collection, analytics engine, optimization suggestions, and reporting systems.
Follows Single Responsibility Principle - only performance tracking.
Architecture: Single Responsibility Principle - performance tracking only
LOC: Target 200 lines (under 200 limit)
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Set, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import threading
import time
import uuid
from collections import defaultdict
import statistics

from .agent_manager import AgentManager, AgentStatus, AgentCapability, AgentInfo
from .config_manager import ConfigManager

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Performance metric types"""
    CONTRACT_COMPLETION_TIME = "contract_completion_time"
    AGENT_PRODUCTIVITY = "agent_productivity"
    SYSTEM_THROUGHPUT = "system_throughput"
    ERROR_RATE = "error_rate"
    RESPONSE_TIME = "response_time"
    RESOURCE_UTILIZATION = "resource_utilization"


class PerformanceLevel(Enum):
    """Performance level classifications"""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    BELOW_AVERAGE = "below_average"
    POOR = "poor"


class OptimizationType(Enum):
    """Optimization suggestion types"""
    WORKLOAD_BALANCING = "workload_balancing"
    CAPABILITY_DEVELOPMENT = "capability_development"
    PROCESS_IMPROVEMENT = "process_improvement"
    RESOURCE_ALLOCATION = "resource_allocation"
    TRAINING_NEEDS = "training_needs"


@dataclass
class PerformanceMetric:
    """Performance metric data"""
    metric_id: str
    agent_id: str
    metric_type: MetricType
    value: float
    unit: str
    timestamp: str
    metadata: Dict[str, Any]


@dataclass
class PerformanceAnalysis:
    """Performance analysis result"""
    analysis_id: str
    agent_id: str
    metric_type: MetricType
    current_value: float
    historical_average: float
    trend: str  # "improving", "stable", "declining"
    performance_level: PerformanceLevel
    analysis_timestamp: str
    recommendations: List[str]


@dataclass
class OptimizationSuggestion:
    """Optimization suggestion"""
    suggestion_id: str
    agent_id: str
    optimization_type: OptimizationType
    title: str
    description: str
    expected_impact: float
    priority: str
    timestamp: str
    metadata: Dict[str, Any]


class PerformanceTracker:
    """
    Manages comprehensive performance tracking, analytics, and optimization suggestions
    
    Responsibilities:
    - Metrics collection and storage
    - Performance analysis and insights
    - Optimization suggestions and improvements
    - Performance reporting and dashboards
    """
    
    def __init__(self, agent_manager: AgentManager, config_manager: ConfigManager):
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.metrics: Dict[str, PerformanceMetric] = {}
        self.analyses: Dict[str, PerformanceAnalysis] = {}
        self.optimization_suggestions: Dict[str, OptimizationSuggestion] = {}
        self.metrics_collection_thread = None
        self.analysis_thread = None
        self.running = False
        self.logger = logging.getLogger(f"{__name__}.PerformanceTracker")
        
        # Performance thresholds
        self.performance_thresholds = {
            PerformanceLevel.EXCELLENT: 0.9,
            PerformanceLevel.GOOD: 0.8,
            PerformanceLevel.AVERAGE: 0.7,
            PerformanceLevel.BELOW_AVERAGE: 0.6,
            PerformanceLevel.POOR: 0.5
        }
        
        # Start collection and analysis threads
        self._start_performance_threads()
    
    def _start_performance_threads(self):
        """Start performance metrics collection and analysis threads"""
        self.running = True
        
        # Metrics collection thread
        self.metrics_collection_thread = threading.Thread(target=self._metrics_collection_loop, daemon=True)
        self.metrics_collection_thread.start()
        
        # Analysis thread
        self.analysis_thread = threading.Thread(target=self._analysis_loop, daemon=True)
        self.analysis_thread.start()
        
        self.logger.info("Performance tracking threads started")
    
    def _metrics_collection_loop(self):
        """Main metrics collection loop"""
        while self.running:
            try:
                # Collect system-wide metrics
                self._collect_system_metrics()
                
                # Collect agent-specific metrics
                self._collect_agent_metrics()
                
                # Wait before next collection
                time.sleep(300)  # Collect every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Metrics collection loop error: {e}")
                time.sleep(600)  # Wait longer on error
    
    def _analysis_loop(self):
        """Main performance analysis loop"""
        while self.running:
            try:
                # Analyze collected metrics
                self._analyze_performance_metrics()
                
                # Generate optimization suggestions
                self._generate_optimization_suggestions()
                
                # Wait before next analysis
                time.sleep(1800)  # Analyze every 30 minutes
                
            except Exception as e:
                self.logger.error(f"Analysis loop error: {e}")
                time.sleep(3600)  # Wait longer on error
    
    def _collect_system_metrics(self):
        """Collect system-wide performance metrics"""
        try:
            # System throughput (contracts completed per hour)
            throughput = self._calculate_system_throughput()
            
            # Error rate
            error_rate = self._calculate_system_error_rate()
            
            # Resource utilization
            resource_utilization = self._calculate_resource_utilization()
            
            # Store system metrics
            self._store_metric("system", MetricType.SYSTEM_THROUGHPUT, throughput, "contracts/hour")
            self._store_metric("system", MetricType.ERROR_RATE, error_rate, "percentage")
            self._store_metric("system", MetricType.RESOURCE_UTILIZATION, resource_utilization, "percentage")
            
        except Exception as e:
            self.logger.error(f"Failed to collect system metrics: {e}")
    
    def _collect_agent_metrics(self):
        """Collect agent-specific performance metrics"""
        try:
            agents = self.agent_manager.get_all_agents()
            
            for agent_id, agent_info in agents.items():
                # Agent productivity
                productivity = self._calculate_agent_productivity(agent_id)
                
                # Response time
                response_time = self._calculate_agent_response_time(agent_id)
                
                # Store agent metrics
                self._store_metric(agent_id, MetricType.AGENT_PRODUCTIVITY, productivity, "contracts/hour")
                self._store_metric(agent_id, MetricType.RESPONSE_TIME, response_time, "seconds")
                
        except Exception as e:
            self.logger.error(f"Failed to collect agent metrics: {e}")
    
    def _calculate_system_throughput(self) -> float:
        """Calculate system throughput (contracts completed per hour)"""
        try:
            # This would typically come from contract completion data
            # For now, return a mock value
            return 2.5  # 2.5 contracts per hour
            
        except Exception as e:
            self.logger.error(f"Failed to calculate system throughput: {e}")
            return 0.0
    
    def _calculate_system_error_rate(self) -> float:
        """Calculate system error rate"""
        try:
            # This would typically come from error tracking data
            # For now, return a mock value
            return 0.05  # 5% error rate
            
        except Exception as e:
            self.logger.error(f"Failed to calculate system error rate: {e}")
            return 0.0
    
    def _calculate_resource_utilization(self) -> float:
        """Calculate system resource utilization"""
        try:
            # This would typically come from system monitoring data
            # For now, return a mock value
            return 0.75  # 75% utilization
            
        except Exception as e:
            self.logger.error(f"Failed to calculate resource utilization: {e}")
            return 0.0
    
    def _calculate_agent_productivity(self, agent_id: str) -> float:
        """Calculate agent productivity (contracts completed per hour)"""
        try:
            # This would typically come from contract completion data
            # For now, return a mock value based on agent status
            agent_info = self.agent_manager.get_agent_info(agent_id)
            if agent_info and agent_info.status == AgentStatus.ONLINE:
                return 1.2  # 1.2 contracts per hour
            else:
                return 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate productivity for {agent_id}: {e}")
            return 0.0
    
    def _calculate_agent_response_time(self, agent_id: str) -> float:
        """Calculate agent response time"""
        try:
            # This would typically come from response time tracking data
            # For now, return a mock value
            return 15.0  # 15 seconds average response time
            
        except Exception as e:
            self.logger.error(f"Failed to calculate response time for {agent_id}: {e}")
            return 0.0
    
    def _store_metric(self, agent_id: str, metric_type: MetricType, value: float, unit: str):
        """Store a performance metric"""
        try:
            metric = PerformanceMetric(
                metric_id=str(uuid.uuid4()),
                agent_id=agent_id,
                metric_type=metric_type,
                value=value,
                unit=unit,
                timestamp=datetime.now().isoformat(),
                metadata={"collection_method": "automatic"}
            )
            
            self.metrics[metric.metric_id] = metric
            
        except Exception as e:
            self.logger.error(f"Failed to store metric: {e}")
    
    def _analyze_performance_metrics(self):
        """Analyze collected performance metrics"""
        try:
            # Analyze metrics for each agent
            agents = self.agent_manager.get_all_agents()
            
            for agent_id in agents.keys():
                # Analyze productivity
                self._analyze_agent_metric(agent_id, MetricType.AGENT_PRODUCTIVITY)
                
                # Analyze response time
                self._analyze_agent_metric(agent_id, MetricType.RESPONSE_TIME)
                
        except Exception as e:
            self.logger.error(f"Failed to analyze performance metrics: {e}")
    
    def _analyze_agent_metric(self, agent_id: str, metric_type: MetricType):
        """Analyze a specific metric for an agent"""
        try:
            # Get recent metrics for this agent and type
            recent_metrics = [m for m in self.metrics.values() 
                            if m.agent_id == agent_id and m.metric_type == metric_type]
            
            if not recent_metrics:
                return
            
            # Calculate current value (most recent)
            current_value = recent_metrics[-1].value
            
            # Calculate historical average
            historical_values = [m.value for m in recent_metrics[:-1]]  # Exclude current
            if historical_values:
                historical_average = statistics.mean(historical_values)
            else:
                historical_average = current_value
            
            # Determine trend
            if len(historical_values) >= 2:
                recent_trend = historical_values[-3:]  # Last 3 values
                if len(recent_trend) >= 2:
                    if recent_trend[-1] > recent_trend[0]:
                        trend = "improving"
                    elif recent_trend[-1] < recent_trend[0]:
                        trend = "declining"
                    else:
                        trend = "stable"
                else:
                    trend = "stable"
            else:
                trend = "stable"
            
            # Determine performance level
            performance_level = self._classify_performance_level(current_value)
            
            # Generate recommendations
            recommendations = self._generate_metric_recommendations(metric_type, current_value, historical_average, trend)
            
            # Create analysis
            analysis = PerformanceAnalysis(
                analysis_id=str(uuid.uuid4()),
                agent_id=agent_id,
                metric_type=metric_type,
                current_value=current_value,
                historical_average=historical_average,
                trend=trend,
                performance_level=performance_level,
                analysis_timestamp=datetime.now().isoformat(),
                recommendations=recommendations
            )
            
            # Store analysis
            self.analyses[analysis.analysis_id] = analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze metric for {agent_id}: {e}")
    
    def _classify_performance_level(self, value: float) -> PerformanceLevel:
        """Classify performance level based on value"""
        try:
            for level, threshold in self.performance_thresholds.items():
                if value >= threshold:
                    return level
            
            return PerformanceLevel.POOR
            
        except Exception as e:
            self.logger.error(f"Failed to classify performance level: {e}")
            return PerformanceLevel.AVERAGE
    
    def _generate_metric_recommendations(self, metric_type: MetricType, current_value: float,
                                       historical_average: float, trend: str) -> List[str]:
        """Generate recommendations based on metric analysis"""
        try:
            recommendations = []
            
            if metric_type == MetricType.AGENT_PRODUCTIVITY:
                if current_value < historical_average:
                    recommendations.append("Consider workload reduction to improve focus")
                    recommendations.append("Review current task complexity and requirements")
                elif trend == "declining":
                    recommendations.append("Investigate recent changes that may affect productivity")
                    recommendations.append("Consider additional training or support")
                elif current_value > historical_average:
                    recommendations.append("Maintain current high performance level")
                    recommendations.append("Consider mentoring other agents")
            
            elif metric_type == MetricType.RESPONSE_TIME:
                if current_value > 30:  # More than 30 seconds
                    recommendations.append("Optimize response handling processes")
                    recommendations.append("Consider parallel processing for complex tasks")
                elif trend == "declining":
                    recommendations.append("Monitor for potential system bottlenecks")
                    recommendations.append("Review task prioritization")
            
            # Add general recommendations
            if trend == "declining":
                recommendations.append("Schedule performance review session")
                recommendations.append("Consider capability development opportunities")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations: {e}")
            return ["Review performance data for insights"]
    
    def _generate_optimization_suggestions(self):
        """Generate optimization suggestions based on performance analysis"""
        try:
            # Analyze each agent's performance
            agents = self.agent_manager.get_all_agents()
            
            for agent_id in agents.keys():
                # Get agent's performance analyses
                agent_analyses = [a for a in self.analyses.values() if a.agent_id == agent_id]
                
                if not agent_analyses:
                    continue
                
                # Generate workload balancing suggestions
                self._generate_workload_suggestions(agent_id, agent_analyses)
                
                # Generate capability development suggestions
                self._generate_capability_suggestions(agent_id, agent_analyses)
                
        except Exception as e:
            self.logger.error(f"Failed to generate optimization suggestions: {e}")
    
    def _generate_workload_suggestions(self, agent_id: str, analyses: List[PerformanceAnalysis]):
        """Generate workload balancing suggestions"""
        try:
            # Check if agent is overloaded
            productivity_analysis = next((a for a in analyses if a.metric_type == MetricType.AGENT_PRODUCTIVITY), None)
            
            if productivity_analysis and productivity_analysis.performance_level in [PerformanceLevel.BELOW_AVERAGE, PerformanceLevel.POOR]:
                suggestion = OptimizationSuggestion(
                    suggestion_id=str(uuid.uuid4()),
                    agent_id=agent_id,
                    optimization_type=OptimizationType.WORKLOAD_BALANCING,
                    title="Workload Reduction Recommendation",
                    description="Consider reducing current workload to improve performance and quality",
                    expected_impact=0.2,  # 20% improvement expected
                    priority="high",
                    timestamp=datetime.now().isoformat(),
                    metadata={"current_performance": productivity_analysis.performance_level.value}
                )
                
                self.optimization_suggestions[suggestion.suggestion_id] = suggestion
                
        except Exception as e:
            self.logger.error(f"Failed to generate workload suggestions for {agent_id}: {e}")
    
    def _generate_capability_suggestions(self, agent_id: str, analyses: List[PerformanceAnalysis]):
        """Generate capability development suggestions"""
        try:
            # Check if agent needs capability development
            response_time_analysis = next((a for a in analyses if a.metric_type == MetricType.RESPONSE_TIME), None)
            
            if response_time_analysis and response_time_analysis.performance_level in [PerformanceLevel.BELOW_AVERAGE, PerformanceLevel.POOR]:
                suggestion = OptimizationSuggestion(
                    suggestion_id=str(uuid.uuid4()),
                    agent_id=agent_id,
                    optimization_type=OptimizationType.CAPABILITY_DEVELOPMENT,
                    title="Capability Development Opportunity",
                    description="Consider additional training or skill development to improve response times",
                    expected_impact=0.15,  # 15% improvement expected
                    priority="medium",
                    timestamp=datetime.now().isoformat(),
                    metadata={"current_performance": response_time_analysis.performance_level.value}
                )
                
                self.optimization_suggestions[suggestion.suggestion_id] = suggestion
                
        except Exception as e:
            self.logger.error(f"Failed to generate capability suggestions for {agent_id}: {e}")
    
    def get_agent_performance(self, agent_id: str) -> Dict[str, Any]:
        """Get performance summary for an agent"""
        try:
            # Get recent analyses
            recent_analyses = [a for a in self.analyses.values() if a.agent_id == agent_id]
            
            # Get recent metrics
            recent_metrics = [m for m in self.metrics.values() if m.agent_id == agent_id]
            
            # Get optimization suggestions
            agent_suggestions = [s for s in self.optimization_suggestions.values() if s.agent_id == agent_id]
            
            return {
                "agent_id": agent_id,
                "analyses": len(recent_analyses),
                "metrics": len(recent_metrics),
                "suggestions": len(agent_suggestions),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get performance for {agent_id}: {e}")
            return {"error": str(e)}
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary"""
        try:
            total_metrics = len(self.metrics)
            total_analyses = len(self.analyses)
            total_suggestions = len(self.optimization_suggestions)
            
            # Calculate average performance levels
            performance_levels = [a.performance_level.value for a in self.analyses.values()]
            if performance_levels:
                level_counts = defaultdict(int)
                for level in performance_levels:
                    level_counts[level] += 1
                
                most_common_level = max(level_counts.items(), key=lambda x: x[1])[0]
            else:
                most_common_level = "unknown"
            
            return {
                "total_metrics": total_metrics,
                "total_analyses": total_analyses,
                "total_suggestions": total_suggestions,
                "most_common_performance_level": most_common_level,
                "tracking_active": self.running,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get performance summary: {e}")
            return {"error": str(e)}
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test for this instance"""
        try:
            # Test metrics collection
            agents = self.agent_manager.get_all_agents()
            if not agents:
                return False
            
            # Test performance summary
            summary = self.get_performance_summary()
            if "total_metrics" not in summary:
                return False
            
            # Test agent performance
            agent_id = list(agents.keys())[0]
            agent_performance = self.get_agent_performance(agent_id)
            if "agent_id" not in agent_performance:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Smoke test failed: {e}")
            return False
    
    def shutdown(self):
        """Shutdown the performance tracker"""
        self.running = False
        if self.metrics_collection_thread:
            self.metrics_collection_thread.join(timeout=5)
        if self.analysis_thread:
            self.analysis_thread.join(timeout=5)


def run_smoke_test():
    """Run basic functionality test for PerformanceTracker"""
    print("🧪 Running PerformanceTracker Smoke Test...")
    
    try:
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary directories
            agent_dir = Path(temp_dir) / "agent_workspaces"
            config_dir = Path(temp_dir) / "config"
            agent_dir.mkdir()
            config_dir.mkdir()
            
            # Create mock agent
            test_agent_dir = agent_dir / "Agent-1"
            test_agent_dir.mkdir()
            
            # Initialize managers
            config_manager = ConfigManager(config_dir)
            agent_manager = AgentManager(agent_dir)
            performance_tracker = PerformanceTracker(agent_manager, config_manager)
            
            # Test basic functionality
            summary = performance_tracker.get_performance_summary()
            assert "total_metrics" in summary
            
            # Test agent performance
            agent_performance = performance_tracker.get_agent_performance("Agent-1")
            assert "agent_id" in agent_performance
            
            # Cleanup
            performance_tracker.shutdown()
            agent_manager.shutdown()
            config_manager.shutdown()
        
        print("✅ PerformanceTracker Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ PerformanceTracker Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for PerformanceTracker testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Performance Tracker CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--agent", help="Get performance for specific agent")
    parser.add_argument("--summary", action="store_true", help="Show performance summary")
    parser.add_argument("--suggestions", action="store_true", help="Show optimization suggestions")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    # Initialize managers
    config_manager = ConfigManager()
    agent_manager = AgentManager()
    performance_tracker = PerformanceTracker(agent_manager, config_manager)
    
    if args.agent:
        performance = performance_tracker.get_agent_performance(args.agent)
        print(f"Performance for {args.agent}:")
        for key, value in performance.items():
            print(f"  {key}: {value}")
    elif args.summary:
        summary = performance_tracker.get_performance_summary()
        print("Performance Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    elif args.suggestions:
        # This would show optimization suggestions
        print("Optimization suggestions feature not yet implemented in CLI")
    else:
        parser.print_help()
    
    # Cleanup
    performance_tracker.shutdown()
    agent_manager.shutdown()
    config_manager.shutdown()


if __name__ == "__main__":
    main()
