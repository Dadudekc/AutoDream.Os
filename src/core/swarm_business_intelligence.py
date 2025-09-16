#!/usr/bin/env python3
"""
Swarm Business Intelligence System - Agent-5 Specialized Module
==============================================================

Comprehensive business intelligence and analytics system for swarm coordination,
performance monitoring, and consolidation progress tracking.

V2 Compliance: < 400 lines, single responsibility for swarm BI operations.
Author: Agent-5 (Business Intelligence Specialist)
Mission: Phase 1 Consolidation - Business Intelligence Support
License: MIT
"""

import json
import logging
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from .unified_analytics_engine import UnifiedAnalyticsEngine, AnalyticsData, PerformanceMetric

logger = logging.getLogger(__name__)


class SwarmMetricType(Enum):
    """Swarm-specific metric types for business intelligence."""
    AGENT_RESPONSE_TIME = "agent_response_time"
    CONSOLIDATION_PROGRESS = "consolidation_progress"
    SWARM_COORDINATION_EFFICIENCY = "swarm_coordination_efficiency"
    TASK_COMPLETION_RATE = "task_completion_rate"
    COMMUNICATION_LATENCY = "communication_latency"
    SYSTEM_HEALTH = "system_health"


class ConsolidationPhase(Enum):
    """Consolidation phase tracking."""
    PHASE_1_CRITICAL = "phase_1_critical"
    PHASE_2_OPTIMIZATION = "phase_2_optimization"
    PHASE_3_SPECIALIZED = "phase_3_specialized"
    PHASE_4_DOCUMENTATION = "phase_4_documentation"


@dataclass
class SwarmMetric:
    """Swarm business intelligence metric."""
    metric_type: SwarmMetricType
    agent_id: str
    value: float
    timestamp: float
    metadata: Dict[str, Any]
    phase: Optional[ConsolidationPhase] = None

    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()


@dataclass
class ConsolidationProgress:
    """Consolidation progress tracking."""
    chunk_id: str
    agent_id: str
    phase: ConsolidationPhase
    files_processed: int
    files_target: int
    completion_percentage: float
    estimated_completion: Optional[datetime] = None
    blockers: List[str] = None

    def __post_init__(self):
        if self.blockers is None:
            self.blockers = []


@dataclass
class SwarmHealthReport:
    """Comprehensive swarm health report."""
    timestamp: float
    total_agents: int
    active_agents: int
    average_response_time: float
    coordination_efficiency: float
    consolidation_progress: float
    system_health_score: float
    recommendations: List[str] = None

    def __post_init__(self):
        if self.recommendations is None:
            self.recommendations = []


class SwarmBusinessIntelligence:
    """Swarm business intelligence and analytics system."""

    def __init__(self, data_path: str = "data/swarm_bi"):
        """Initialize swarm business intelligence system."""
        self.data_path = Path(data_path)
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize analytics engine
        self.analytics_engine = UnifiedAnalyticsEngine()
        
        # Metrics storage
        self.metrics: List[SwarmMetric] = []
        self.consolidation_progress: Dict[str, ConsolidationProgress] = {}
        
        # Agent coordinates for monitoring
        self.agent_coordinates = self._load_agent_coordinates()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("SwarmBusinessIntelligence initialized")

    def _load_agent_coordinates(self) -> Dict[str, List[int]]:
        """Load agent coordinates for monitoring."""
        try:
            coords_file = Path("config/coordinates.json")
            if coords_file.exists():
                with open(coords_file) as f:
                    data = json.load(f)
                    return {
                        agent: info["chat_input_coordinates"]
                        for agent, info in data.get("agents", {}).items()
                    }
        except Exception as e:
            self.logger.warning(f"Could not load coordinates: {e}")
        
        return {}

    def record_agent_metric(
        self,
        agent_id: str,
        metric_type: SwarmMetricType,
        value: float,
        metadata: Optional[Dict[str, Any]] = None,
        phase: Optional[ConsolidationPhase] = None
    ) -> None:
        """Record a swarm metric."""
        try:
            metric = SwarmMetric(
                metric_type=metric_type,
                agent_id=agent_id,
                value=value,
                timestamp=time.time(),
                metadata=metadata or {},
                phase=phase
            )
            
            self.metrics.append(metric)
            
            # Process through analytics engine
            analytics_data = AnalyticsData(
                id=f"{agent_id}_{metric_type.value}_{int(time.time())}",
                content=f"Agent {agent_id} {metric_type.value}: {value}",
                data_type="swarm_metric",
                metadata=asdict(metric),
                timestamp=time.time()
            )
            
            self.analytics_engine.process_data(analytics_data)
            
            self.logger.debug(f"Recorded metric: {agent_id} - {metric_type.value}: {value}")
            
        except Exception as e:
            self.logger.error(f"Error recording metric: {e}")

    def update_consolidation_progress(
        self,
        chunk_id: str,
        agent_id: str,
        phase: ConsolidationPhase,
        files_processed: int,
        files_target: int,
        blockers: Optional[List[str]] = None
    ) -> None:
        """Update consolidation progress tracking."""
        try:
            completion_percentage = (files_processed / files_target * 100) if files_target > 0 else 0
            
            # Estimate completion time
            estimated_completion = None
            if files_processed > 0 and files_target > files_processed:
                remaining_files = files_target - files_processed
                # Simple estimation based on current rate
                estimated_completion = datetime.now() + timedelta(
                    hours=remaining_files * 0.5  # Assume 0.5 hours per file
                )
            
            progress = ConsolidationProgress(
                chunk_id=chunk_id,
                agent_id=agent_id,
                phase=phase,
                files_processed=files_processed,
                files_target=files_target,
                completion_percentage=completion_percentage,
                estimated_completion=estimated_completion,
                blockers=blockers or []
            )
            
            self.consolidation_progress[chunk_id] = progress
            
            # Record as metric
            self.record_agent_metric(
                agent_id=agent_id,
                metric_type=SwarmMetricType.CONSOLIDATION_PROGRESS,
                value=completion_percentage,
                metadata={
                    "chunk_id": chunk_id,
                    "phase": phase.value,
                    "files_processed": files_processed,
                    "files_target": files_target,
                    "blockers": blockers or []
                },
                phase=phase
            )
            
            self.logger.info(f"Updated consolidation progress: {chunk_id} - {completion_percentage:.1f}%")
            
        except Exception as e:
            self.logger.error(f"Error updating consolidation progress: {e}")

    def calculate_swarm_efficiency(self) -> float:
        """Calculate overall swarm coordination efficiency."""
        try:
            if not self.metrics:
                return 0.0
            
            # Get recent metrics (last 24 hours)
            cutoff_time = time.time() - (24 * 60 * 60)
            recent_metrics = [
                m for m in self.metrics 
                if m.timestamp > cutoff_time
            ]
            
            if not recent_metrics:
                return 0.0
            
            # Calculate efficiency based on response times and completion rates
            response_times = [
                m.value for m in recent_metrics 
                if m.metric_type == SwarmMetricType.AGENT_RESPONSE_TIME
            ]
            
            completion_rates = [
                m.value for m in recent_metrics 
                if m.metric_type == SwarmMetricType.TASK_COMPLETION_RATE
            ]
            
            # Simple efficiency calculation
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            avg_completion_rate = sum(completion_rates) / len(completion_rates) if completion_rates else 0
            
            # Efficiency = completion rate / (response time + 1) to avoid division by zero
            efficiency = avg_completion_rate / (avg_response_time + 1)
            
            return min(efficiency, 100.0)  # Cap at 100%
            
        except Exception as e:
            self.logger.error(f"Error calculating swarm efficiency: {e}")
            return 0.0

    def generate_health_report(self) -> SwarmHealthReport:
        """Generate comprehensive swarm health report."""
        try:
            # Get recent metrics
            cutoff_time = time.time() - (24 * 60 * 60)
            recent_metrics = [
                m for m in self.metrics 
                if m.timestamp > cutoff_time
            ]
            
            # Calculate metrics
            total_agents = len(self.agent_coordinates)
            active_agents = len(set(m.agent_id for m in recent_metrics))
            
            response_times = [
                m.value for m in recent_metrics 
                if m.metric_type == SwarmMetricType.AGENT_RESPONSE_TIME
            ]
            average_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            coordination_efficiency = self.calculate_swarm_efficiency()
            
            # Calculate consolidation progress
            total_progress = 0
            if self.consolidation_progress:
                total_progress = sum(
                    p.completion_percentage for p in self.consolidation_progress.values()
                ) / len(self.consolidation_progress)
            
            # Calculate system health score
            system_health_score = (
                (active_agents / total_agents * 30) +  # Agent activity (30%)
                (coordination_efficiency * 0.3) +      # Coordination efficiency (30%)
                (total_progress * 0.4)                 # Consolidation progress (40%)
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                active_agents, total_agents, average_response_time, 
                coordination_efficiency, total_progress
            )
            
            report = SwarmHealthReport(
                timestamp=time.time(),
                total_agents=total_agents,
                active_agents=active_agents,
                average_response_time=average_response_time,
                coordination_efficiency=coordination_efficiency,
                consolidation_progress=total_progress,
                system_health_score=system_health_score,
                recommendations=recommendations
            )
            
            self.logger.info(f"Generated health report - System Health: {system_health_score:.1f}%")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating health report: {e}")
            return SwarmHealthReport(
                timestamp=time.time(),
                total_agents=0,
                active_agents=0,
                average_response_time=0,
                coordination_efficiency=0,
                consolidation_progress=0,
                system_health_score=0,
                recommendations=["Error generating report"]
            )

    def _generate_recommendations(
        self,
        active_agents: int,
        total_agents: int,
        avg_response_time: float,
        coordination_efficiency: float,
        consolidation_progress: float
    ) -> List[str]:
        """Generate actionable recommendations based on metrics."""
        recommendations = []
        
        # Agent activity recommendations
        if active_agents < total_agents:
            recommendations.append(f"Activate {total_agents - active_agents} inactive agents")
        
        # Response time recommendations
        if avg_response_time > 5.0:  # 5 seconds threshold
            recommendations.append("Optimize agent response times - consider load balancing")
        
        # Coordination efficiency recommendations
        if coordination_efficiency < 70:
            recommendations.append("Improve swarm coordination - review communication protocols")
        
        # Consolidation progress recommendations
        if consolidation_progress < 50:
            recommendations.append("Accelerate consolidation progress - identify blockers")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Swarm operating at optimal efficiency")
        
        return recommendations

    def get_analytics_dashboard_data(self) -> Dict[str, Any]:
        """Get data for analytics dashboard."""
        try:
            # Get analytics engine statistics
            analytics_stats = self.analytics_engine.get_analytics_statistics()
            
            # Get recent metrics summary
            cutoff_time = time.time() - (7 * 24 * 60 * 60)  # Last 7 days
            recent_metrics = [
                m for m in self.metrics 
                if m.timestamp > cutoff_time
            ]
            
            # Group metrics by type
            metrics_by_type = {}
            for metric in recent_metrics:
                metric_type = metric.metric_type.value
                if metric_type not in metrics_by_type:
                    metrics_by_type[metric_type] = []
                metrics_by_type[metric_type].append(metric.value)
            
            # Calculate averages
            avg_metrics = {
                metric_type: sum(values) / len(values) if values else 0
                for metric_type, values in metrics_by_type.items()
            }
            
            return {
                "analytics_engine_stats": analytics_stats,
                "swarm_metrics": avg_metrics,
                "consolidation_progress": {
                    chunk_id: asdict(progress) 
                    for chunk_id, progress in self.consolidation_progress.items()
                },
                "health_report": asdict(self.generate_health_report()),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard data: {e}")
            return {"error": str(e)}

    def save_metrics(self) -> None:
        """Save metrics to persistent storage."""
        try:
            metrics_file = self.data_path / "swarm_metrics.json"
            with open(metrics_file, "w") as f:
                json.dump([asdict(m) for m in self.metrics], f, indent=2)
            
            progress_file = self.data_path / "consolidation_progress.json"
            with open(progress_file, "w") as f:
                json.dump({
                    chunk_id: asdict(progress) 
                    for chunk_id, progress in self.consolidation_progress.items()
                }, f, indent=2)
            
            self.logger.info("Metrics saved to persistent storage")
            
        except Exception as e:
            self.logger.error(f"Error saving metrics: {e}")

    def load_metrics(self) -> None:
        """Load metrics from persistent storage."""
        try:
            metrics_file = self.data_path / "swarm_metrics.json"
            if metrics_file.exists():
                with open(metrics_file) as f:
                    metrics_data = json.load(f)
                    self.metrics = [
                        SwarmMetric(**metric_data) 
                        for metric_data in metrics_data
                    ]
            
            progress_file = self.data_path / "consolidation_progress.json"
            if progress_file.exists():
                with open(progress_file) as f:
                    progress_data = json.load(f)
                    self.consolidation_progress = {
                        chunk_id: ConsolidationProgress(**progress)
                        for chunk_id, progress in progress_data.items()
                    }
            
            self.logger.info("Metrics loaded from persistent storage")
            
        except Exception as e:
            self.logger.error(f"Error loading metrics: {e}")


# Export main classes
__all__ = [
    "SwarmBusinessIntelligence",
    "SwarmMetric",
    "SwarmMetricType",
    "ConsolidationProgress",
    "ConsolidationPhase",
    "SwarmHealthReport",
]



