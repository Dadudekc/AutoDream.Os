#!/usr/bin/env python3
"""
🏥 Health Metrics Collector - Agent_Cellphone_V2

This component is responsible for collecting and storing health metrics.
Following V2 coding standards: ≤200 LOC, OOP design, SRP.

Author: Foundation & Testing Specialist
License: MIT
"""

import logging
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Optional
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)


class HealthMetricType(Enum):
    """Types of health metrics"""
    RESPONSE_TIME = "response_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    ERROR_RATE = "error_rate"
    TASK_COMPLETION_RATE = "task_completion_rate"
    HEARTBEAT_FREQUENCY = "heartbeat_frequency"
    CONTRACT_SUCCESS_RATE = "contract_success_rate"
    COMMUNICATION_LATENCY = "communication_latency"


class HealthStatus(Enum):
    """Agent health status levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"


@dataclass
class HealthMetric:
    """Individual health metric data"""
    agent_id: str
    metric_type: str
    value: float
    unit: str
    timestamp: datetime
    threshold: Optional[float] = None
    status: HealthStatus = HealthStatus.GOOD


@dataclass
class HealthSnapshot:
    """Complete health snapshot for an agent"""
    agent_id: str
    timestamp: datetime
    overall_status: HealthStatus
    health_score: float  # 0-100
    metrics: Dict[str, HealthMetric] = field(default_factory=dict)
    alerts: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)


class HealthMetricsCollector:
    """
    Health Metrics Collector - Single responsibility: Collect and store health metrics.
    
    Follows V2 standards: ≤200 LOC, OOP design, SRP.
    """
    
    def __init__(self):
        """Initialize the metrics collector"""
        self.health_data: Dict[str, HealthSnapshot] = {}
        logger.info("HealthMetricsCollector initialized")
    
    def record_health_metric(self, agent_id: str, metric_type: str, 
                           value: float, unit: str, threshold: Optional[float] = None):
        """Record a health metric for an agent"""
        try:
            # Create or update health snapshot
            if agent_id not in self.health_data:
                self.health_data[agent_id] = HealthSnapshot(
                    agent_id=agent_id,
                    timestamp=datetime.now(),
                    overall_status=HealthStatus.GOOD,
                    health_score=100.0
                )
            
            snapshot = self.health_data[agent_id]
            
            # Create metric
            metric = HealthMetric(
                agent_id=agent_id,
                metric_type=metric_type,
                value=value,
                unit=unit,
                timestamp=datetime.now(),
                threshold=threshold
            )
            
            # Update snapshot
            snapshot.metrics[metric_type] = metric
            snapshot.timestamp = datetime.now()
            
            logger.debug(f"Health metric recorded: {agent_id} - {metric_type}: {value}{unit}")
            
        except Exception as e:
            logger.error(f"Error recording health metric: {e}")
    
    def get_agent_health(self, agent_id: str) -> Optional[HealthSnapshot]:
        """Get health snapshot for a specific agent"""
        return self.health_data.get(agent_id)
    
    def get_all_agent_health(self) -> Dict[str, HealthSnapshot]:
        """Get health snapshots for all agents"""
        return self.health_data.copy()
    
    def clear_agent_data(self, agent_id: str):
        """Clear health data for a specific agent"""
        if agent_id in self.health_data:
            del self.health_data[agent_id]
            logger.info(f"Health data cleared for agent: {agent_id}")
    
    def clear_all_data(self):
        """Clear all health data"""
        self.health_data.clear()
        logger.info("All health data cleared")
    
    def get_metric_count(self, agent_id: str) -> int:
        """Get the number of metrics for a specific agent"""
        if agent_id in self.health_data:
            return len(self.health_data[agent_id].metrics)
        return 0
    
    def get_total_agents(self) -> int:
        """Get the total number of agents being monitored"""
        return len(self.health_data)
    
    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            logger.info("Running HealthMetricsCollector smoke test...")
            
            # Test basic initialization
            assert self.health_data == {}
            assert self.get_total_agents() == 0
            logger.info("Basic initialization passed")
            
            # Test metric recording
            self.record_health_metric("test_agent", "response_time", 500.0, "ms")
            assert "test_agent" in self.health_data
            assert self.get_total_agents() == 1
            assert self.get_metric_count("test_agent") == 1
            logger.info("Metric recording passed")
            
            # Test health snapshot retrieval
            health = self.get_agent_health("test_agent")
            assert health is not None
            assert health.agent_id == "test_agent"
            assert len(health.metrics) == 1
            logger.info("Health snapshot retrieval passed")
            
            # Test multiple metrics
            self.record_health_metric("test_agent", "memory_usage", 80.0, "%")
            assert self.get_metric_count("test_agent") == 2
            logger.info("Multiple metrics passed")
            
            # Test multiple agents
            self.record_health_metric("test_agent_2", "cpu_usage", 70.0, "%")
            assert self.get_total_agents() == 2
            logger.info("Multiple agents passed")
            
            # Test data retrieval
            all_health = self.get_all_agent_health()
            assert len(all_health) == 2
            assert "test_agent" in all_health
            assert "test_agent_2" in all_health
            logger.info("Data retrieval passed")
            
            # Cleanup
            self.clear_all_data()
            assert self.get_total_agents() == 0
            logger.info("Cleanup passed")
            
            logger.info("✅ HealthMetricsCollector smoke test PASSED")
            return True
            
        except Exception as e:
            logger.error(f"❌ HealthMetricsCollector smoke test FAILED: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False


def main():
    """CLI testing function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Health Metrics Collector CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    
    args = parser.parse_args()
    
    if args.test:
        collector = HealthMetricsCollector()
        success = collector.run_smoke_test()
        exit(0 if success else 1)
    
    elif args.demo:
        print("🚀 Starting Health Metrics Collector Demo...")
        collector = HealthMetricsCollector()
        
        # Record some sample metrics
        print("📈 Recording sample health metrics...")
        collector.record_health_metric("agent_001", "response_time", 500.0, "ms")
        collector.record_health_metric("agent_001", "memory_usage", 75.0, "%")
        collector.record_health_metric("agent_002", "cpu_usage", 60.0, "%")
        
        # Show results
        print(f"\n📊 Total Agents: {collector.get_total_agents()}")
        print(f"📈 Total Metrics: {sum(collector.get_metric_count(agent_id) for agent_id in collector.health_data)}")
        
        print("\n📋 Agent Details:")
        for agent_id in collector.health_data:
            health = collector.get_agent_health(agent_id)
            print(f"  {agent_id}: {len(health.metrics)} metrics")
            for metric_type, metric in health.metrics.items():
                print(f"    {metric_type}: {metric.value}{metric.unit}")
        
        print("\n✅ Demo completed")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
