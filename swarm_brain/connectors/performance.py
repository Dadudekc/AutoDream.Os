#!/usr/bin/env python3
"""
Performance Connector
======================

Integration with performance monitoring system.
V2 Compliance: ≤400 lines, focused performance integration.
"""

import logging
from typing import Dict, Any, List, Optional
from ..ingest import Ingestor

logger = logging.getLogger(__name__)


def ingest_performance(metrics: Dict[str, Any], anomalies: Dict[str, Any] = None,
                      optimizations: Dict[str, Any] = None, trends: Dict[str, Any] = None,
                      project: str = "Agent_Cellphone_V2", agent_id: str = "Agent-8"):
    """
    Ingest performance monitoring data into the swarm brain.
    
    Args:
        metrics: Performance metrics dictionary
        anomalies: Anomaly detection results
        optimizations: Optimization strategies
        trends: Trend analysis data
        project: Project identifier
        agent_id: Agent monitoring performance
    """
    try:
        ingestor = Ingestor()
        
        # Default values
        anomalies = anomalies or {}
        optimizations = optimizations or {}
        trends = trends or {}
        
        # Extract key metrics
        cpu_usage = metrics.get("cpu_usage", 0.0)
        memory_usage = metrics.get("memory_usage", 0.0)
        response_time = metrics.get("response_time", 0.0)
        
        # Determine tags based on performance
        tags = ["performance", "monitoring"]
        if cpu_usage > 80.0:
            tags.append("high_cpu")
        if memory_usage > 80.0:
            tags.append("high_memory")
        if response_time > 5.0:
            tags.append("slow_response")
        if anomalies:
            tags.append("anomalies")
        if optimizations:
            tags.append("optimizations")
        
        # Create summary
        summary = f"CPU: {cpu_usage:.1f}%, Memory: {memory_usage:.1f}%, Response: {response_time:.2f}s"
        if anomalies:
            summary += f", {len(anomalies)} anomalies"
        
        # Record performance data
        doc_id = ingestor.performance(
            title="Performance Snapshot",
            metrics=metrics,
            anomalies=anomalies,
            optimizations=optimizations,
            trends=trends,
            project=project,
            agent_id=agent_id,
            tags=tags,
            summary=summary
        )
        
        # Record as action if there are significant issues
        if anomalies or cpu_usage > 90.0 or memory_usage > 90.0:
            outcome = "failure" if len(anomalies) > 3 else "partial"
            
            ingestor.action(
                title="Performance Monitoring Alert",
                tool="performance_monitor",
                outcome=outcome,
                context={
                    "metrics": metrics,
                    "anomalies_count": len(anomalies),
                    "critical_issues": cpu_usage > 90.0 or memory_usage > 90.0
                },
                project=project,
                agent_id=agent_id,
                tags=tags + ["action", "alert"],
                summary=f"Performance alert: {summary}"
            )
        
        logger.info(f"Successfully ingested performance data for {project}")
        return doc_id
        
    except Exception as e:
        logger.error(f"Failed to ingest performance data: {e}")
        raise


def ingest_optimization(optimization_type: str, before_metrics: Dict[str, Any],
                        after_metrics: Dict[str, Any], improvement_percentage: float,
                        project: str, agent_id: str = "Agent-8"):
    """
    Ingest optimization results.
    
    Args:
        optimization_type: Type of optimization applied
        before_metrics: Metrics before optimization
        after_metrics: Metrics after optimization
        improvement_percentage: Percentage improvement
        project: Project identifier
        agent_id: Agent performing optimization
    """
    try:
        ingestor = Ingestor()
        
        context = {
            "optimization_type": optimization_type,
            "before_metrics": before_metrics,
            "after_metrics": after_metrics,
            "improvement_percentage": improvement_percentage
        }
        
        outcome = "success" if improvement_percentage > 0 else "failure"
        
        ingestor.action(
            title=f"Performance Optimization: {optimization_type}",
            tool="performance_optimizer",
            outcome=outcome,
            context=context,
            project=project,
            agent_id=agent_id,
            tags=["performance", "optimization", optimization_type],
            summary=f"Applied {optimization_type} optimization, {improvement_percentage:.1f}% improvement"
        )
        
        # Record optimization strategy
        ingestor.performance(
            title=f"Optimization Strategy: {optimization_type}",
            metrics=after_metrics,
            anomalies={},
            optimizations={optimization_type: {"improvement": improvement_percentage}},
            trends={"optimization_applied": optimization_type},
            project=project,
            agent_id=agent_id,
            tags=["performance", "optimization", "strategy"],
            summary=f"Optimization strategy: {optimization_type}"
        )
        
        logger.info(f"Recorded optimization: {optimization_type}")
        
    except Exception as e:
        logger.error(f"Failed to ingest optimization: {e}")
        raise


def ingest_system_health(health_status: str, components: Dict[str, str],
                        project: str, agent_id: str = "Agent-8"):
    """
    Ingest system health status.
    
    Args:
        health_status: Overall health status (healthy/degraded/unhealthy)
        components: Component health statuses
        project: Project identifier
        agent_id: Agent monitoring health
    """
    try:
        ingestor = Ingestor()
        
        # Count component statuses
        healthy_components = sum(1 for status in components.values() if status == "healthy")
        total_components = len(components)
        health_percentage = (healthy_components / total_components * 100) if total_components > 0 else 0
        
        metrics = {
            "health_status": health_status,
            "healthy_components": healthy_components,
            "total_components": total_components,
            "health_percentage": health_percentage,
            "components": components
        }
        
        tags = ["performance", "health", "monitoring"]
        if health_status == "healthy":
            tags.append("success")
        elif health_status == "degraded":
            tags.append("warning")
        else:
            tags.append("error")
        
        ingestor.performance(
            title="System Health Check",
            metrics=metrics,
            anomalies={} if health_status == "healthy" else {"health_issues": components},
            optimizations={},
            trends={"health_trend": health_status},
            project=project,
            agent_id=agent_id,
            tags=tags,
            summary=f"System health: {health_status} ({health_percentage:.1f}% components healthy)"
        )
        
        logger.info(f"Recorded system health: {health_status}")
        
    except Exception as e:
        logger.error(f"Failed to ingest system health: {e}")
        raise




