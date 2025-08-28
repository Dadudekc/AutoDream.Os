#!/usr/bin/env python3
"""
Coordination Metrics Implementation

Contract: COORD-003 - Coordination Metrics Implementation
Agent: Agent-7 (QUALITY ASSURANCE MANAGER)
Mission: SPRINT_ACCELERATION_QUALITY_COMPLETION_OPTIMIZATION
Sprint Deadline: INNOVATION_PLANNING_MODE
"""

import time
import logging
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from datetime import datetime, timedelta
import threading
import queue
import statistics
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of coordination metrics"""
    PERFORMANCE = "performance"
    EFFICIENCY = "efficiency"
    QUALITY = "quality"
    COMMUNICATION = "communication"
    SYNCHRONIZATION = "synchronization"
    COORDINATION = "coordination"

class MetricStatus(Enum):
    """Status of metric collection"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    COLLECTING = "collecting"

@dataclass
class CoordinationMetric:
    """Individual coordination metric"""
    name: str
    metric_type: MetricType
    value: float
    unit: str
    timestamp: datetime
    agent_id: str
    context: Dict[str, Any] = field(default_factory=dict)
    quality_score: float = 0.0
    status: MetricStatus = MetricStatus.ACTIVE

@dataclass
class CoordinationMetrics:
    """Collection of coordination metrics"""
    agent_id: str
    timestamp: datetime
    metrics: Dict[str, CoordinationMetric] = field(default_factory=dict)
    overall_score: float = 0.0
    quality_compliance: float = 0.0
    performance_index: float = 0.0

@dataclass
class QualityGate:
    """Quality gate for coordination metrics"""
    metric_name: str
    threshold: float
    operator: str  # ">=", "<=", "==", "!="
    severity: str  # "critical", "warning", "info"
    description: str

class CoordinationMetricsFramework:
    """Comprehensive coordination performance metrics framework"""
    
    def __init__(self):
        self.quality_gates = self._setup_quality_gates()
        self.metrics_history: List[CoordinationMetrics] = []
        self.active_metrics: Dict[str, CoordinationMetric] = {}
        self.performance_monitors: Dict[str, Callable] = {}
        self.quality_validators: Dict[str, Callable] = {}
        
    def _setup_quality_gates(self) -> List[QualityGate]:
        """Setup quality gates based on V2 standards"""
        return [
            QualityGate("response_time", 100.0, "<=", "critical", "Response time must be <= 100ms"),
            QualityGate("throughput", 1000.0, ">=", "critical", "Throughput must be >= 1000 msg/s"),
            QualityGate("error_rate", 5.0, "<=", "critical", "Error rate must be <= 5%"),
            QualityGate("synchronization_latency", 50.0, "<=", "warning", "Synchronization latency must be <= 50ms"),
            QualityGate("coordination_efficiency", 85.0, ">=", "critical", "Coordination efficiency must be >= 85%"),
            QualityGate("quality_score", 80.0, ">=", "critical", "Overall quality score must be >= 80")
        ]
    
    def register_performance_monitor(self, metric_name: str, monitor_func: Callable):
        """Register a performance monitoring function"""
        self.performance_monitors[metric_name] = monitor_func
        logger.info(f"Registered performance monitor for {metric_name}")
    
    def register_quality_validator(self, metric_name: str, validator_func: Callable):
        """Register a quality validation function"""
        self.quality_validators[metric_name] = validator_func
        logger.info(f"Registered quality validator for {metric_name}")
    
    def collect_metric(self, agent_id: str, metric_name: str, value: float, 
                      unit: str, metric_type: MetricType, context: Dict[str, Any] = None) -> CoordinationMetric:
        """Collect a coordination metric with quality validation"""
        timestamp = datetime.now()
        
        # Create metric
        metric = CoordinationMetric(
            name=metric_name,
            metric_type=metric_type,
            value=value,
            unit=unit,
            timestamp=timestamp,
            agent_id=agent_id,
            context=context or {}
        )
        
        # Apply quality validation if available
        if metric_name in self.quality_validators:
            try:
                quality_score = self.quality_validators[metric_name](metric)
                metric.quality_score = quality_score
            except Exception as e:
                logger.error(f"Quality validation failed for {metric_name}: {e}")
                metric.quality_score = 0.0
        
        # Store metric
        self.active_metrics[metric_name] = metric
        
        logger.info(f"Collected metric {metric_name}: {value} {unit} for agent {agent_id}")
        return metric
    
    def calculate_coordination_efficiency(self, agent_id: str) -> float:
        """Calculate coordination efficiency score"""
        agent_metrics = [m for m in self.active_metrics.values() if m.agent_id == agent_id]
        
        if not agent_metrics:
            return 0.0
        
        # Calculate efficiency based on multiple factors
        efficiency_factors = []
        
        # Response time efficiency (lower is better)
        response_metrics = [m for m in agent_metrics if "response" in m.name.lower()]
        if response_metrics:
            avg_response = statistics.mean([m.value for m in response_metrics])
            response_efficiency = max(0, 100 - (avg_response / 10))  # Normalize to 0-100
            efficiency_factors.append(response_efficiency)
        
        # Throughput efficiency (higher is better)
        throughput_metrics = [m for m in agent_metrics if "throughput" in m.name.lower()]
        if throughput_metrics:
            avg_throughput = statistics.mean([m.value for m in throughput_metrics])
            throughput_efficiency = min(100, avg_throughput / 10)  # Normalize to 0-100
            efficiency_factors.append(throughput_efficiency)
        
        # Error rate efficiency (lower is better)
        error_metrics = [m for m in agent_metrics if "error" in m.name.lower()]
        if error_metrics:
            avg_error_rate = statistics.mean([m.value for m in error_metrics])
            error_efficiency = max(0, 100 - (avg_error_rate * 20))  # Normalize to 0-100
            efficiency_factors.append(error_efficiency)
        
        # Quality score efficiency
        quality_scores = [m.quality_score for m in agent_metrics if m.quality_score > 0]
        if quality_scores:
            avg_quality = statistics.mean(quality_scores)
            efficiency_factors.append(avg_quality)
        
        # Calculate overall efficiency
        if efficiency_factors:
            overall_efficiency = statistics.mean(efficiency_factors)
            return round(overall_efficiency, 2)
        
        return 0.0
    
    def calculate_performance_index(self, agent_id: str) -> float:
        """Calculate performance index score"""
        agent_metrics = [m for m in self.active_metrics.values() if m.agent_id == agent_id]
        
        if not agent_metrics:
            return 0.0
        
        # Performance factors
        performance_factors = []
        
        # Response time performance
        response_metrics = [m for m in agent_metrics if "response" in m.name.lower()]
        if response_metrics:
            avg_response = statistics.mean([m.value for m in response_metrics])
            response_performance = max(0, 100 - (avg_response / 5))  # Normalize to 0-100
            performance_factors.append(response_performance)
        
        # Throughput performance
        throughput_metrics = [m for m in agent_metrics if "throughput" in m.name.lower()]
        if throughput_metrics:
            avg_throughput = statistics.mean([m.value for m in throughput_metrics])
            throughput_performance = min(100, avg_throughput / 20)  # Normalize to 0-100
            performance_factors.append(throughput_performance)
        
        # Synchronization performance
        sync_metrics = [m for m in agent_metrics if "sync" in m.name.lower()]
        if sync_metrics:
            avg_sync = statistics.mean([m.value for m in sync_metrics])
            sync_performance = max(0, 100 - (avg_sync / 2))  # Normalize to 0-100
            performance_factors.append(sync_performance)
        
        # Calculate overall performance
        if performance_factors:
            overall_performance = statistics.mean(performance_factors)
            return round(overall_performance, 2)
        
        return 0.0
    
    def calculate_quality_compliance(self, agent_id: str) -> float:
        """Calculate quality compliance score"""
        agent_metrics = [m for m in self.active_metrics.values() if m.agent_id == agent_id]
        
        if not agent_metrics:
            return 0.0
        
        # Quality compliance factors
        compliance_factors = []
        
        # Individual metric quality scores
        quality_scores = [m.quality_score for m in agent_metrics if m.quality_score > 0]
        if quality_scores:
            avg_quality = statistics.mean(quality_scores)
            compliance_factors.append(avg_quality)
        
        # Quality gate compliance
        gate_compliance = self._check_quality_gates_compliance(agent_metrics)
        compliance_factors.append(gate_compliance)
        
        # Calculate overall compliance
        if compliance_factors:
            overall_compliance = statistics.mean(compliance_factors)
            return round(overall_compliance, 2)
        
        return 0.0
    
    def _check_quality_gates_compliance(self, metrics: List[CoordinationMetric]) -> float:
        """Check compliance with quality gates"""
        if not metrics:
            return 0.0
        
        compliance_scores = []
        
        for gate in self.quality_gates:
            # Find relevant metrics
            relevant_metrics = [m for m in metrics if gate.metric_name in m.name.lower()]
            
            if relevant_metrics:
                for metric in relevant_metrics:
                    # Check gate compliance
                    if gate.operator == ">=":
                        passed = metric.value >= gate.threshold
                    elif gate.operator == "<=":
                        passed = metric.value <= gate.threshold
                    elif gate.operator == "==":
                        passed = metric.value == gate.threshold
                    elif gate.operator == "!=":
                        passed = metric.value != gate.threshold
                    else:
                        passed = False
                    
                    # Score based on compliance
                    if passed:
                        compliance_scores.append(100.0)
                    else:
                        # Partial score based on how close to threshold
                        if gate.operator in [">=", "<="]:
                            if gate.operator == ">=":
                                ratio = min(1.0, metric.value / gate.threshold)
                            else:
                                ratio = min(1.0, gate.threshold / metric.value)
                            partial_score = ratio * 100
                            compliance_scores.append(partial_score)
                        else:
                            compliance_scores.append(0.0)
        
        if compliance_scores:
            return statistics.mean(compliance_scores)
        
        return 0.0
    
    def generate_coordination_report(self, agent_id: str) -> CoordinationMetrics:
        """Generate comprehensive coordination report for an agent"""
        timestamp = datetime.now()
        
        # Calculate scores
        efficiency = self.calculate_coordination_efficiency(agent_id)
        performance = self.calculate_performance_index(agent_id)
        quality_compliance = self.calculate_quality_compliance(agent_id)
        
        # Calculate overall score
        overall_score = (efficiency + performance + quality_compliance) / 3
        
        # Create report
        report = CoordinationMetrics(
            agent_id=agent_id,
            timestamp=timestamp,
            metrics=self.active_metrics.copy(),
            overall_score=round(overall_score, 2),
            quality_compliance=quality_compliance,
            performance_index=performance
        )
        
        # Store in history
        self.metrics_history.append(report)
        
        return report
    
    def validate_quality_gates(self, metrics: CoordinationMetrics) -> Dict[str, Any]:
        """Validate metrics against quality gates"""
        results = {
            'passed': True,
            'gates': [],
            'overall_status': 'PASSED'
        }
        
        for gate in self.quality_gates:
            # Find relevant metrics
            relevant_metrics = [m for m in metrics.metrics.values() if gate.metric_name in m.name.lower()]
            
            if relevant_metrics:
                for metric in relevant_metrics:
                    # Check gate compliance
                    if gate.operator == ">=":
                        passed = metric.value >= gate.threshold
                    elif gate.operator == "<=":
                        passed = metric.value <= gate.threshold
                    elif gate.operator == "==":
                        passed = metric.value == gate.threshold
                    elif gate.operator == "!=":
                        passed = metric.value != gate.threshold
                    else:
                        passed = False
                    
                    gate_result = {
                        'metric_name': metric.name,
                        'gate_name': gate.metric_name,
                        'threshold': gate.threshold,
                        'operator': gate.operator,
                        'actual': metric.value,
                        'passed': passed,
                        'severity': gate.severity,
                        'description': gate.description
                    }
                    
                    results['gates'].append(gate_result)
                    
                    if not passed and gate.severity == 'critical':
                        results['passed'] = False
                        results['overall_status'] = 'FAILED'
        
        return results
    
    def export_metrics(self, filepath: str, format_type: str = "json"):
        """Export metrics to file"""
        try:
            if format_type.lower() == "json":
                export_data = {
                    'timestamp': datetime.now().isoformat(),
                    'active_metrics': {
                        name: {
                            'name': metric.name,
                            'type': metric.metric_type.value,
                            'value': metric.value,
                            'unit': metric.unit,
                            'timestamp': metric.timestamp.isoformat(),
                            'agent_id': metric.agent_id,
                            'quality_score': metric.quality_score,
                            'status': metric.status.value
                        }
                        for name, metric in self.active_metrics.items()
                    },
                    'metrics_history': [
                        {
                            'agent_id': report.agent_id,
                            'timestamp': report.timestamp.isoformat(),
                            'overall_score': report.overall_score,
                            'quality_compliance': report.quality_compliance,
                            'performance_index': report.performance_index
                        }
                        for report in self.metrics_history
                    ]
                }
                
                with open(filepath, 'w') as f:
                    json.dump(export_data, f, indent=2)
                
                logger.info(f"Metrics exported to {filepath}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")
            return False
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        if not self.active_metrics:
            return {}
        
        summary = {
            'total_metrics': len(self.active_metrics),
            'agents_monitored': list(set(m.agent_id for m in self.active_metrics.values())),
            'metric_types': list(set(m.metric_type.value for m in self.active_metrics.values())),
            'overall_quality': statistics.mean([m.quality_score for m in self.active_metrics.values() if m.quality_score > 0]),
            'recent_metrics': len([m for m in self.active_metrics.values() 
                                 if m.timestamp > datetime.now() - timedelta(hours=1)]),
            'quality_gates': len(self.quality_gates),
            'active_monitors': len(self.performance_monitors),
            'active_validators': len(self.quality_validators)
        }
        
        return summary

def main():
    """Main function for testing the coordination metrics framework"""
    framework = CoordinationMetricsFramework()
    
    print("🚀 Coordination Metrics Framework for Sprint Acceleration")
    print("=" * 60)
    
    # Example usage
    agent_id = "Agent-7"
    
    # Collect sample metrics
    framework.collect_metric(agent_id, "response_time", 85.0, "ms", MetricType.PERFORMANCE)
    framework.collect_metric(agent_id, "throughput", 1200.0, "msg/s", MetricType.EFFICIENCY)
    framework.collect_metric(agent_id, "error_rate", 3.2, "%", MetricType.QUALITY)
    framework.collect_metric(agent_id, "synchronization_latency", 45.0, "ms", MetricType.SYNCHRONIZATION)
    
    # Generate report
    report = framework.generate_coordination_report(agent_id)
    
    print(f"✅ Coordination report generated for {agent_id}")
    print(f"📊 Overall Score: {report.overall_score}")
    print(f"🎯 Quality Compliance: {report.quality_compliance}")
    print(f"⚡ Performance Index: {report.performance_index}")
    
    # Validate quality gates
    validation = framework.validate_quality_gates(report)
    print(f"🔍 Quality Gates: {validation['overall_status']}")
    
    # Get summary
    summary = framework.get_metrics_summary()
    print(f"📈 Total Metrics: {summary.get('total_metrics', 0)}")
    print(f"🤖 Agents Monitored: {len(summary.get('agents_monitored', []))}")

if __name__ == "__main__":
    main()
