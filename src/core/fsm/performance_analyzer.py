#!/usr/bin/env python3
"""
Performance Analyzer - V2 Modular Architecture
=============================================

Performance analysis functionality for the FSM system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4I - FSM System Modularization
License: MIT
"""

import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from .models import TaskState, TaskPriority
from .types import FSMConfig


logger = logging.getLogger(__name__)


class PerformanceAnalyzer:
    """
    Performance Analyzer - FSM Performance Analysis
    
    Single responsibility: Analyze FSM performance patterns, identify
    optimization opportunities, and provide performance insights following V2 architecture standards.
    """
    
    def __init__(self, config: Optional[FSMConfig] = None):
        """Initialize performance analyzer."""
        self.logger = logging.getLogger(f"{__name__}.PerformanceAnalyzer")
        
        # Configuration
        self.config = config or FSMConfig()
        
        # Performance tracking
        self._performance_history: List[Dict[str, Any]] = []
        self._optimization_history: List[Dict[str, Any]] = []
        
        self.logger.info("✅ Performance Analyzer initialized successfully")
    
    # ============================================================================
    # PERFORMANCE ANALYSIS
    # ============================================================================
    
    def analyze_fsm_performance_patterns(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Analyze FSM performance patterns for optimization insights."""
        try:
            # Get recent performance data
            recent_time = time.time() - (time_range_hours * 3600)
            
            performance_analysis = {
                "total_tasks": 0,
                "active_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "state_transition_patterns": {},
                "task_completion_times": {},
                "agent_performance": {},
                "optimization_opportunities": []
            }
            
            # This would be populated with actual task data from TaskManager
            # For now, return empty analysis structure
            self.logger.info(f"FSM performance analysis completed for {time_range_hours}h time range")
            return performance_analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze FSM performance patterns: {e}")
            return {"error": str(e)}
    
    def analyze_task_performance(self, tasks_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze task performance metrics."""
        try:
            if not tasks_data:
                return {
                    "total_tasks": 0,
                    "performance_metrics": {},
                    "recommendations": []
                }
            
            total_tasks = len(tasks_data)
            completed_tasks = len([t for t in tasks_data if t.get("state") == TaskState.COMPLETED.value])
            failed_tasks = len([t for t in tasks_data if t.get("state") == TaskState.FAILED.value])
            active_tasks = len([t for t in tasks_data if t.get("state") in [TaskState.IN_PROGRESS.value, TaskState.ONBOARDING.value]])
            
            # Calculate success rate
            success_rate = completed_tasks / total_tasks if total_tasks > 0 else 0
            
            # Analyze priority distribution
            priority_distribution = {}
            for task in tasks_data:
                priority = task.get("priority", TaskPriority.NORMAL.value)
                priority_distribution[priority] = priority_distribution.get(priority, 0) + 1
            
            # Analyze agent performance
            agent_performance = {}
            for task in tasks_data:
                agent = task.get("assigned_agent", "unknown")
                if agent not in agent_performance:
                    agent_performance[agent] = {"total": 0, "completed": 0, "failed": 0}
                
                agent_performance[agent]["total"] += 1
                if task.get("state") == TaskState.COMPLETED.value:
                    agent_performance[agent]["completed"] += 1
                elif task.get("state") == TaskState.FAILED.value:
                    agent_performance[agent]["failed"] += 1
            
            # Calculate agent success rates
            for agent, stats in agent_performance.items():
                if stats["total"] > 0:
                    stats["success_rate"] = stats["completed"] / stats["total"]
                else:
                    stats["success_rate"] = 0
            
            # Generate recommendations
            recommendations = []
            if success_rate < 0.8:
                recommendations.append("Low success rate - investigate task complexity or agent capabilities")
            if failed_tasks > completed_tasks * 0.3:
                recommendations.append("High failure rate - review task assignment and agent skills")
            if active_tasks > total_tasks * 0.7:
                recommendations.append("High active task ratio - consider task prioritization or agent allocation")
            
            return {
                "total_tasks": total_tasks,
                "active_tasks": active_tasks,
                "completed_tasks": completed_tasks,
                "failed_tasks": failed_tasks,
                "success_rate": success_rate,
                "priority_distribution": priority_distribution,
                "agent_performance": agent_performance,
                "recommendations": recommendations
            }
            
        except Exception as e:
            self.logger.error(f"Failed to analyze task performance: {e}")
            return {"error": str(e)}
    
    def analyze_communication_performance(self, communication_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze communication performance metrics."""
        try:
            if not communication_data:
                return {
                    "total_events": 0,
                    "communication_metrics": {},
                    "recommendations": []
                }
            
            total_events = len(communication_data)
            
            # Analyze event types
            event_type_distribution = {}
            for event in communication_data:
                event_type = event.get("event_type", "unknown")
                event_type_distribution[event_type] = event_type_distribution.get(event_type, 0) + 1
            
            # Analyze agent communication patterns
            agent_communication = {}
            for event in communication_data:
                source = event.get("source_agent", "unknown")
                target = event.get("target_agent", "unknown")
                
                if source not in agent_communication:
                    agent_communication[source] = {"sent": 0, "received": 0}
                if target not in agent_communication:
                    agent_communication[target] = {"sent": 0, "received": 0}
                
                agent_communication[source]["sent"] += 1
                agent_communication[target]["received"] += 1
            
            # Generate recommendations
            recommendations = []
            if total_events > 100:
                recommendations.append("High communication volume - consider optimization")
            
            # Check for communication bottlenecks
            high_volume_agents = [agent for agent, stats in agent_communication.items() if stats["sent"] > 20]
            if high_volume_agents:
                recommendations.append(f"High communication volume agents: {', '.join(high_volume_agents)}")
            
            return {
                "total_events": total_events,
                "event_type_distribution": event_type_distribution,
                "agent_communication": agent_communication,
                "recommendations": recommendations
            }
            
        except Exception as e:
            self.logger.error(f"Failed to analyze communication performance: {e}")
            return {"error": str(e)}
    
    # ============================================================================
    # OPTIMIZATION ANALYSIS
    # ============================================================================
    
    def identify_optimization_opportunities(self, performance_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify specific optimization opportunities."""
        try:
            opportunities = []
            
            # Check task performance opportunities
            if "success_rate" in performance_data:
                success_rate = performance_data["success_rate"]
                if success_rate < 0.8:
                    opportunities.append({
                        "type": "task_performance",
                        "priority": "high" if success_rate < 0.6 else "medium",
                        "description": f"Low success rate ({success_rate:.1%}) - investigate root causes",
                        "recommended_actions": [
                            "Review task complexity and requirements",
                            "Assess agent skill levels and training needs",
                            "Implement better error handling and retry logic"
                        ]
                    })
            
            # Check communication optimization opportunities
            if "total_events" in performance_data:
                total_events = performance_data["total_events"]
                if total_events > 100:
                    opportunities.append({
                        "type": "communication_optimization",
                        "priority": "medium",
                        "description": f"High communication volume ({total_events} events) - optimize patterns",
                        "recommended_actions": [
                            "Implement message batching and aggregation",
                            "Review communication frequency and necessity",
                            "Consider asynchronous communication patterns"
                        ]
                    })
            
            # Check resource utilization opportunities
            if "active_tasks" in performance_data and "total_tasks" in performance_data:
                active_ratio = performance_data["active_tasks"] / performance_data["total_tasks"]
                if active_ratio > 0.8:
                    opportunities.append({
                        "type": "resource_utilization",
                        "priority": "medium",
                        "description": f"High active task ratio ({active_ratio:.1%}) - optimize resource allocation",
                        "recommended_actions": [
                            "Implement task prioritization and queuing",
                            "Review agent workload distribution",
                            "Consider parallel task execution strategies"
                        ]
                    })
            
            return opportunities
            
        except Exception as e:
            self.logger.error(f"Failed to identify optimization opportunities: {e}")
            return []
    
    def generate_optimization_plan(self, opportunities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a comprehensive optimization plan."""
        try:
            if not opportunities:
                return {
                    "plan_id": f"optimization_plan_{int(time.time())}",
                    "generated_at": datetime.now().isoformat(),
                    "total_opportunities": 0,
                    "priority_breakdown": {},
                    "action_items": [],
                    "estimated_impact": "low",
                    "implementation_timeline": "not_applicable"
                }
            
            # Categorize opportunities by priority
            priority_breakdown = {"high": 0, "medium": 0, "low": 0}
            for opp in opportunities:
                priority = opp.get("priority", "medium")
                priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1
            
            # Generate action items
            action_items = []
            for opp in opportunities:
                for action in opp.get("recommended_actions", []):
                    action_items.append({
                        "opportunity_type": opp.get("type", "unknown"),
                        "priority": opp.get("priority", "medium"),
                        "action": action,
                        "estimated_effort": "medium" if opp.get("priority") == "high" else "low"
                    })
            
            # Determine estimated impact
            high_priority_count = priority_breakdown.get("high", 0)
            if high_priority_count > 0:
                estimated_impact = "high"
                implementation_timeline = "immediate"
            elif priority_breakdown.get("medium", 0) > 0:
                estimated_impact = "medium"
                implementation_timeline = "short_term"
            else:
                estimated_impact = "low"
                implementation_timeline = "long_term"
            
            return {
                "plan_id": f"optimization_plan_{int(time.time())}",
                "generated_at": datetime.now().isoformat(),
                "total_opportunities": len(opportunities),
                "priority_breakdown": priority_breakdown,
                "action_items": action_items,
                "estimated_impact": estimated_impact,
                "implementation_timeline": implementation_timeline
            }
            
        except Exception as e:
            self.logger.error(f"Failed to generate optimization plan: {e}")
            return {"error": str(e)}
    
    # ============================================================================
    # PERFORMANCE MONITORING
    # ============================================================================
    
    def record_performance_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Record performance metrics for historical analysis."""
        try:
            record = {
                "timestamp": time.time(),
                "metrics": metrics
            }
            self._performance_history.append(record)
            
            # Keep only recent history (last 1000 records)
            if len(self._performance_history) > 1000:
                self._performance_history = self._performance_history[-1000:]
            
            self.logger.debug(f"Performance metrics recorded: {len(metrics)} metrics")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to record performance metrics: {e}")
            return False
    
    def get_performance_history(self, time_range_hours: int = 24) -> List[Dict[str, Any]]:
        """Get performance history within specified time range."""
        try:
            cutoff_time = time.time() - (time_range_hours * 3600)
            recent_metrics = [m for m in self._performance_history if m.get("timestamp", 0) > cutoff_time]
            return recent_metrics
            
        except Exception as e:
            self.logger.error(f"Failed to get performance history: {e}")
            return []
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance analysis summary."""
        try:
            if not self._performance_history:
                return {
                    "total_records": 0,
                    "analysis_period": "no_data",
                    "trends": [],
                    "summary": "No performance data available"
                }
            
            total_records = len(self._performance_history)
            latest_record = self._performance_history[-1] if self._performance_history else None
            
            # Calculate analysis period
            if latest_record:
                oldest_timestamp = self._performance_history[0].get("timestamp", 0)
                newest_timestamp = latest_record.get("timestamp", 0)
                period_hours = (newest_timestamp - oldest_timestamp) / 3600
                analysis_period = f"{period_hours:.1f} hours"
            else:
                analysis_period = "unknown"
            
            return {
                "total_records": total_records,
                "analysis_period": analysis_period,
                "latest_metrics": latest_record.get("metrics", {}) if latest_record else {},
                "trends": self._identify_performance_trends(),
                "summary": f"Performance analysis based on {total_records} records over {analysis_period}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get performance summary: {e}")
            return {"error": str(e)}
    
    def _identify_performance_trends(self) -> List[str]:
        """Identify performance trends from historical data."""
        try:
            trends = []
            
            if len(self._performance_history) < 2:
                return ["Insufficient data for trend analysis"]
            
            # Simple trend analysis - compare recent vs older metrics
            recent_metrics = self._performance_history[-10:]  # Last 10 records
            older_metrics = self._performance_history[-20:-10]  # Previous 10 records
            
            if recent_metrics and older_metrics:
                # This would implement actual trend analysis logic
                trends.append("Performance trend analysis available")
            
            return trends
            
        except Exception as e:
            self.logger.error(f"Failed to identify performance trends: {e}")
            return ["Trend analysis failed"]
    
    # ============================================================================
    # CLEANUP AND MAINTENANCE
    # ============================================================================
    
    def cleanup_old_metrics(self, retention_hours: int = 168) -> int:  # Default: 1 week
        """Clean up old performance metrics."""
        try:
            cutoff_time = time.time() - (retention_hours * 3600)
            old_metrics = [m for m in self._performance_history if m.get("timestamp", 0) < cutoff_time]
            
            cleaned_count = 0
            for metric in old_metrics:
                try:
                    self._performance_history.remove(metric)
                    cleaned_count += 1
                except Exception as e:
                    self.logger.warning(f"Failed to cleanup metric: {e}")
            
            if cleaned_count > 0:
                self.logger.info(f"Cleaned up {cleaned_count} old performance metrics")
            
            return cleaned_count
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup old metrics: {e}")
            return 0
    
    def cleanup(self):
        """Cleanup performance analyzer resources."""
        try:
            # Clean up old metrics
            self.cleanup_old_metrics()
            
            self.logger.info("PerformanceAnalyzer cleanup completed")
        except Exception as e:
            self.logger.error(f"PerformanceAnalyzer cleanup failed: {e}")

