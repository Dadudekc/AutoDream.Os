#!/usr/bin/env python3
"""
Swarm BI Coordinator - Agent-5 Specialized Module
================================================

Central coordination system for business intelligence across all swarm agents,
integrating analytics, performance monitoring, and data optimization.

V2 Compliance: < 400 lines, single responsibility for swarm BI coordination.
Author: Agent-5 (Business Intelligence Specialist)
Mission: Phase 1 Consolidation - BI Coordination Support
License: MIT
"""

import json
import logging
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from .swarm_business_intelligence import SwarmBusinessIntelligence, SwarmMetricType, ConsolidationPhase
from .swarm_performance_monitor import SwarmPerformanceMonitor, PerformanceAlertLevel
from .swarm_data_optimizer import SwarmDataOptimizer, DataType, OptimizationStrategy

logger = logging.getLogger(__name__)


class CoordinationStatus(Enum):
    """BI coordination status."""
    ACTIVE = "active"
    STANDBY = "standby"
    MAINTENANCE = "maintenance"
    ERROR = "error"


@dataclass
class SwarmBICoordinationReport:
    """Comprehensive swarm BI coordination report."""
    timestamp: float
    coordination_status: CoordinationStatus
    total_agents: int
    active_agents: int
    bi_systems_status: Dict[str, str]
    performance_summary: Dict[str, Any]
    optimization_summary: Dict[str, Any]
    consolidation_progress: Dict[str, Any]
    recommendations: List[str]
    alerts: List[Dict[str, Any]]


class SwarmBICoordinator:
    """Central coordinator for swarm business intelligence systems."""

    def __init__(self, config_path: str = "config/coordinates.json"):
        """Initialize swarm BI coordinator."""
        self.config_path = config_path
        self.coordination_status = CoordinationStatus.ACTIVE
        
        # Initialize BI systems
        self.business_intelligence = SwarmBusinessIntelligence()
        self.performance_monitor = SwarmPerformanceMonitor(config_path)
        self.data_optimizer = SwarmDataOptimizer()
        
        # Coordination tracking
        self.agent_bi_status: Dict[str, Dict[str, Any]] = {}
        self.coordination_history: List[Dict[str, Any]] = []
        
        # Load agent coordinates
        self.agent_coordinates = self._load_agent_coordinates()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("SwarmBICoordinator initialized")

    def _load_agent_coordinates(self) -> Dict[str, List[int]]:
        """Load agent coordinates for coordination."""
        try:
            with open(self.config_path) as f:
                data = json.load(f)
                return {
                    agent: info["chat_input_coordinates"]
                    for agent, info in data.get("agents", {}).items()
                }
        except Exception as e:
            self.logger.warning(f"Could not load coordinates: {e}")
            return {}

    def coordinate_agent_bi(self, agent_id: str, bi_data: Dict[str, Any]) -> bool:
        """Coordinate business intelligence for a specific agent."""
        try:
            current_time = time.time()
            
            # Update agent BI status
            self.agent_bi_status[agent_id] = {
                "last_update": current_time,
                "bi_data": bi_data,
                "status": "active"
            }
            
            # Process through BI systems
            self._process_agent_metrics(agent_id, bi_data)
            self._process_agent_performance(agent_id, bi_data)
            self._optimize_agent_data(agent_id, bi_data)
            
            # Record coordination activity
            self._record_coordination_activity(agent_id, "bi_coordination", bi_data)
            
            self.logger.debug(f"Coordinated BI for agent {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error coordinating BI for agent {agent_id}: {e}")
            return False

    def _process_agent_metrics(self, agent_id: str, bi_data: Dict[str, Any]) -> None:
        """Process agent metrics through business intelligence system."""
        try:
            # Extract metrics from BI data
            if "response_time" in bi_data:
                self.business_intelligence.record_agent_metric(
                    agent_id=agent_id,
                    metric_type=SwarmMetricType.AGENT_RESPONSE_TIME,
                    value=bi_data["response_time"],
                    metadata={"source": "bi_coordination"}
                )
            
            if "task_completion_rate" in bi_data:
                self.business_intelligence.record_agent_metric(
                    agent_id=agent_id,
                    metric_type=SwarmMetricType.TASK_COMPLETION_RATE,
                    value=bi_data["task_completion_rate"],
                    metadata={"source": "bi_coordination"}
                )
            
            if "consolidation_progress" in bi_data:
                progress_data = bi_data["consolidation_progress"]
                if "chunk_id" in progress_data and "phase" in progress_data:
                    phase = ConsolidationPhase(progress_data["phase"])
                    self.business_intelligence.update_consolidation_progress(
                        chunk_id=progress_data["chunk_id"],
                        agent_id=agent_id,
                        phase=phase,
                        files_processed=progress_data.get("files_processed", 0),
                        files_target=progress_data.get("files_target", 0),
                        blockers=progress_data.get("blockers", [])
                    )
                    
        except Exception as e:
            self.logger.error(f"Error processing agent metrics: {e}")

    def _process_agent_performance(self, agent_id: str, bi_data: Dict[str, Any]) -> None:
        """Process agent performance through performance monitor."""
        try:
            # Extract performance data
            response_time = bi_data.get("response_time", 0)
            task_completed = bi_data.get("task_completed", False)
            error_occurred = bi_data.get("error_occurred", False)
            
            # Record performance data
            self.performance_monitor.record_agent_activity(
                agent_id=agent_id,
                response_time=response_time,
                task_completed=task_completed,
                error_occurred=error_occurred,
                metadata=bi_data
            )
            
        except Exception as e:
            self.logger.error(f"Error processing agent performance: {e}")

    def _optimize_agent_data(self, agent_id: str, bi_data: Dict[str, Any]) -> None:
        """Optimize agent data through data optimizer."""
        try:
            # Determine data type based on content
            data_type = self._determine_data_type(bi_data)
            
            # Optimize the data
            optimization_result = self.data_optimizer.optimize_data(
                data=bi_data,
                data_type=data_type,
                strategies=[OptimizationStrategy.CACHING, OptimizationStrategy.COMPRESSION]
            )
            
            if optimization_result.success:
                self.logger.debug(f"Optimized data for agent {agent_id}: {optimization_result.compression_ratio:.1%} reduction")
            
        except Exception as e:
            self.logger.error(f"Error optimizing agent data: {e}")

    def _determine_data_type(self, bi_data: Dict[str, Any]) -> DataType:
        """Determine data type based on content."""
        try:
            if "consolidation_progress" in bi_data:
                return DataType.PROGRESS
            elif "response_time" in bi_data or "performance" in bi_data:
                return DataType.METRICS
            elif "messages" in bi_data or "communication" in bi_data:
                return DataType.MESSAGES
            elif "coordinates" in bi_data or "position" in bi_data:
                return DataType.COORDINATES
            elif "report" in bi_data or "summary" in bi_data:
                return DataType.REPORTS
            else:
                return DataType.CONFIGURATION
                
        except Exception as e:
            self.logger.error(f"Error determining data type: {e}")
            return DataType.CONFIGURATION

    def _record_coordination_activity(self, agent_id: str, activity_type: str, data: Dict[str, Any]) -> None:
        """Record coordination activity."""
        try:
            activity = {
                "timestamp": time.time(),
                "agent_id": agent_id,
                "activity_type": activity_type,
                "data_summary": {
                    "keys": list(data.keys()),
                    "size": len(str(data))
                }
            }
            
            self.coordination_history.append(activity)
            
            # Keep only recent history (last 1000 entries)
            if len(self.coordination_history) > 1000:
                self.coordination_history = self.coordination_history[-1000:]
                
        except Exception as e:
            self.logger.error(f"Error recording coordination activity: {e}")

    def get_swarm_bi_status(self) -> Dict[str, Any]:
        """Get comprehensive swarm BI status."""
        try:
            # Get status from all BI systems
            bi_health = self.business_intelligence.generate_health_report()
            performance_report = self.performance_monitor.generate_performance_report()
            optimization_report = self.data_optimizer.get_optimization_report()
            
            # Calculate overall BI health
            bi_health_score = (
                bi_health.system_health_score * 0.4 +
                performance_report.performance_score * 0.4 +
                (100 - len(performance_report.alerts) * 5) * 0.2  # Alert penalty
            )
            
            return {
                "coordination_status": self.coordination_status.value,
                "bi_health_score": max(0, min(100, bi_health_score)),
                "total_agents": len(self.agent_coordinates),
                "active_agents": len([
                    agent for agent, status in self.agent_bi_status.items()
                    if time.time() - status["last_update"] < 300  # Active within 5 minutes
                ]),
                "bi_systems": {
                    "business_intelligence": "operational",
                    "performance_monitor": "operational",
                    "data_optimizer": "operational"
                },
                "performance_summary": {
                    "average_response_time": performance_report.average_response_time,
                    "total_tasks_completed": performance_report.total_tasks_completed,
                    "performance_score": performance_report.performance_score
                },
                "optimization_summary": {
                    "total_optimizations": optimization_report.get("optimization_stats", {}).get("total_optimizations", 0),
                    "cache_hit_rate": optimization_report.get("cache_stats", {}).get("cache_hit_rate", 0),
                    "average_compression": optimization_report.get("optimization_stats", {}).get("average_compression", 0)
                },
                "consolidation_progress": {
                    "total_chunks": len(bi_health.recommendations),
                    "overall_progress": bi_health.consolidation_progress
                },
                "active_alerts": len(performance_report.alerts),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting swarm BI status: {e}")
            return {"error": str(e)}

    def generate_coordination_report(self) -> SwarmBICoordinationReport:
        """Generate comprehensive BI coordination report."""
        try:
            current_time = time.time()
            
            # Get data from all systems
            bi_health = self.business_intelligence.generate_health_report()
            performance_report = self.performance_monitor.generate_performance_report()
            optimization_report = self.data_optimizer.get_optimization_report()
            
            # Calculate active agents
            active_agents = len([
                agent for agent, status in self.agent_bi_status.items()
                if current_time - status["last_update"] < 300
            ])
            
            # Generate recommendations
            recommendations = self._generate_coordination_recommendations(
                bi_health, performance_report, optimization_report
            )
            
            # Collect alerts
            alerts = [
                {
                    "agent_id": alert.agent_id,
                    "level": alert.alert_level.value,
                    "message": alert.message,
                    "timestamp": alert.timestamp
                }
                for alert in performance_report.alerts
            ]
            
            report = SwarmBICoordinationReport(
                timestamp=current_time,
                coordination_status=self.coordination_status,
                total_agents=len(self.agent_coordinates),
                active_agents=active_agents,
                bi_systems_status={
                    "business_intelligence": "operational",
                    "performance_monitor": "operational",
                    "data_optimizer": "operational"
                },
                performance_summary={
                    "average_response_time": performance_report.average_response_time,
                    "performance_score": performance_report.performance_score,
                    "total_tasks": performance_report.total_tasks_completed
                },
                optimization_summary={
                    "total_optimizations": optimization_report.get("optimization_stats", {}).get("total_optimizations", 0),
                    "cache_hit_rate": optimization_report.get("cache_stats", {}).get("cache_hit_rate", 0)
                },
                consolidation_progress={
                    "overall_progress": bi_health.consolidation_progress,
                    "active_chunks": len(self.business_intelligence.consolidation_progress)
                },
                recommendations=recommendations,
                alerts=alerts
            )
            
            self.logger.info(f"Generated BI coordination report - Active agents: {active_agents}/{len(self.agent_coordinates)}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating coordination report: {e}")
            return SwarmBICoordinationReport(
                timestamp=time.time(),
                coordination_status=CoordinationStatus.ERROR,
                total_agents=0,
                active_agents=0,
                bi_systems_status={},
                performance_summary={},
                optimization_summary={},
                consolidation_progress={},
                recommendations=["Error generating report"],
                alerts=[]
            )

    def _generate_coordination_recommendations(
        self,
        bi_health,
        performance_report,
        optimization_report
    ) -> List[str]:
        """Generate coordination recommendations."""
        recommendations = []
        
        try:
            # Performance recommendations
            if performance_report.performance_score < 70:
                recommendations.append("Improve swarm performance - review agent response times")
            
            if len(performance_report.alerts) > 5:
                recommendations.append("Address performance alerts - multiple agents showing issues")
            
            # BI recommendations
            if bi_health.system_health_score < 80:
                recommendations.append("Enhance business intelligence systems - low health score")
            
            # Optimization recommendations
            cache_hit_rate = optimization_report.get("cache_stats", {}).get("cache_hit_rate", 0)
            if cache_hit_rate < 70:
                recommendations.append("Optimize caching strategy - low cache hit rate")
            
            # Coordination recommendations
            active_ratio = performance_report.active_agents / performance_report.total_agents
            if active_ratio < 0.8:
                recommendations.append("Activate more agents - low agent participation")
            
            if not recommendations:
                recommendations.append("Swarm BI coordination operating optimally")
                
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            recommendations.append("Error generating recommendations")
        
        return recommendations

    def save_coordination_data(self, data_path: str = "data/bi_coordination") -> None:
        """Save coordination data to persistent storage."""
        try:
            data_dir = Path(data_path)
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # Save agent BI status
            status_file = data_dir / "agent_bi_status.json"
            with open(status_file, "w") as f:
                json.dump(self.agent_bi_status, f, indent=2)
            
            # Save coordination history
            history_file = data_dir / "coordination_history.json"
            with open(history_file, "w") as f:
                json.dump(self.coordination_history, f, indent=2)
            
            # Save coordination report
            report = self.generate_coordination_report()
            report_file = data_dir / "coordination_report.json"
            with open(report_file, "w") as f:
                json.dump(asdict(report), f, indent=2)
            
            self.logger.info("BI coordination data saved to persistent storage")
            
        except Exception as e:
            self.logger.error(f"Error saving coordination data: {e}")


# Export main classes
__all__ = [
    "SwarmBICoordinator",
    "SwarmBICoordinationReport",
    "CoordinationStatus",
]



