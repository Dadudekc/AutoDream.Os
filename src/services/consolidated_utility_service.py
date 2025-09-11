#!/usr/bin/env python3
"""
Consolidated Utility Service - V2 Compliant Module
==================================================

Unified utility service consolidating:
- agent_utils_registry.py (agent registry and utilities)
- performance_analyzer.py (performance analysis)
- compliance_validator.py (V2 compliance validation)

V2 Compliance: < 400 lines, single responsibility for all utility operations.

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: Phase 2 Consolidation - Chunk 002 (Services)
License: MIT
"""

import logging
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

from .architectural_models import ArchitecturalPrinciple, ComplianceValidationResult

logger = logging.getLogger(__name__)

class ConsolidatedUtilityService:
    """Unified utility service combining registry, performance analysis, and compliance validation."""
    
    def __init__(self, agent_id: str = "default"):
        """Initialize the consolidated utility service."""
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)
        
        # Initialize agent registry
        self.agents = self._initialize_agent_registry()
        
        # Initialize performance tracking
        self.performance_metrics = defaultdict(list)
        self.compliance_history = []
        
        # Initialize configuration
        self.config = self._load_config()

    def _initialize_agent_registry(self) -> Dict[str, Dict[str, Any]]:
        """Initialize agent registry."""
        return {
            "Agent-1": {
                "description": "Integration & Core Systems",
                "coords": {"x": -100, "y": 1000},
                "inbox": "agent_workspaces/Agent-1/inbox",
            },
            "Agent-2": {
                "description": "Architecture & Design",
                "coords": {"x": -200, "y": 1000},
                "inbox": "agent_workspaces/Agent-2/inbox",
            },
            "Agent-3": {
                "description": "Infrastructure & DevOps",
                "coords": {"x": -300, "y": 1000},
                "inbox": "agent_workspaces/Agent-3/inbox",
            },
            "Agent-4": {
                "description": "Strategic Oversight & Emergency Intervention",
                "coords": {"x": -400, "y": 1000},
                "inbox": "agent_workspaces/Agent-4/inbox",
            },
            "Agent-5": {
                "description": "Business Intelligence",
                "coords": {"x": -500, "y": 1000},
                "inbox": "agent_workspaces/Agent-5/inbox",
            },
            "Agent-6": {
                "description": "Coordination & Communication",
                "coords": {"x": -600, "y": 1000},
                "inbox": "agent_workspaces/Agent-6/inbox",
            },
            "Agent-7": {
                "description": "Web Development",
                "coords": {"x": -700, "y": 1000},
                "inbox": "agent_workspaces/Agent-7/inbox",
            },
            "Agent-8": {
                "description": "SSOT & System Integration",
                "coords": {"x": -800, "y": 1000},
                "inbox": "agent_workspaces/Agent-8/inbox",
            },
        }

    def _load_config(self) -> Dict[str, Any]:
        """Load utility service configuration."""
        return {
            "analysis_period_days": 30,
            "performance_thresholds": {
                "task_completion_rate": 0.8,
                "coordination_effectiveness": 0.7,
                "knowledge_utilization": 0.75
            },
            "metrics_weights": {
                "task_completion": 0.4,
                "coordination": 0.3,
                "knowledge": 0.3
            },
            "compliance_thresholds": {
                "max_file_lines": 400,
                "max_function_lines": 50,
                "max_class_methods": 20
            }
        }

    # Agent Registry Methods
    def list_agents(self) -> List[str]:
        """Return sorted list of agent identifiers."""
        return sorted(self.agents.keys())

    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent information by ID."""
        return self.agents.get(agent_id)

    def get_agent_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get agent coordinates."""
        agent_info = self.get_agent_info(agent_id)
        if agent_info and "coords" in agent_info:
            coords = agent_info["coords"]
            return (coords["x"], coords["y"])
        return None

    def get_agent_inbox(self, agent_id: str) -> Optional[str]:
        """Get agent inbox path."""
        agent_info = self.get_agent_info(agent_id)
        return agent_info.get("inbox") if agent_info else None

    def register_agent(self, agent_id: str, description: str, 
                      coords: Tuple[int, int], inbox: str) -> bool:
        """Register a new agent."""
        try:
            self.agents[agent_id] = {
                "description": description,
                "coords": {"x": coords[0], "y": coords[1]},
                "inbox": inbox
            }
            self.logger.info(f"Registered agent {agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register agent {agent_id}: {e}")
            return False

    # Performance Analysis Methods
    def record_performance_metric(self, metric_name: str, value: float, 
                                timestamp: Optional[datetime] = None) -> None:
        """Record a performance metric."""
        if timestamp is None:
            timestamp = datetime.now()
        
        self.performance_metrics[metric_name].append({
            "value": value,
            "timestamp": timestamp
        })

    def get_performance_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get performance summary for the last N days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        summary = {}
        for metric_name, values in self.performance_metrics.items():
            recent_values = [
                v["value"] for v in values 
                if v["timestamp"] >= cutoff_date
            ]
            
            if recent_values:
                summary[metric_name] = {
                    "count": len(recent_values),
                    "average": sum(recent_values) / len(recent_values),
                    "min": min(recent_values),
                    "max": max(recent_values),
                    "latest": recent_values[-1]
                }
        
        return summary

    def analyze_performance_trends(self, metric_name: str, days: int = 30) -> Dict[str, Any]:
        """Analyze performance trends for a specific metric."""
        cutoff_date = datetime.now() - timedelta(days=days)
        values = [
            v["value"] for v in self.performance_metrics.get(metric_name, [])
            if v["timestamp"] >= cutoff_date
        ]
        
        if len(values) < 2:
            return {"trend": "insufficient_data", "values": values}
        
        # Simple trend analysis
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg * 1.1:
            trend = "improving"
        elif second_avg < first_avg * 0.9:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "values": values,
            "first_half_avg": first_avg,
            "second_half_avg": second_avg,
            "change_percent": ((second_avg - first_avg) / first_avg) * 100
        }

    def get_performance_recommendations(self) -> List[str]:
        """Get performance improvement recommendations."""
        recommendations = []
        summary = self.get_performance_summary()
        
        for metric_name, data in summary.items():
            threshold = self.config["performance_thresholds"].get(metric_name, 0.5)
            if data["average"] < threshold:
                recommendations.append(
                    f"Improve {metric_name}: current {data['average']:.2f}, "
                    f"target {threshold:.2f}"
                )
        
        return recommendations

    # Compliance Validation Methods
    def validate_agent_compliance(self, agent_id: str, principle: ArchitecturalPrinciple, 
                                code_changes: List[str]) -> ComplianceValidationResult:
        """Validate that an agent's changes comply with their assigned principle."""
        issues = []
        recommendations = []

        for change in code_changes:
            if principle == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY:
                validation_issues = self._validate_single_responsibility(change)
                issues.extend(validation_issues)
            elif principle == ArchitecturalPrinciple.DONT_REPEAT_YOURSELF:
                validation_issues = self._validate_dry_principle(change)
                issues.extend(validation_issues)
            elif principle == ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID:
                validation_issues = self._validate_kiss_principle(change)
                issues.extend(validation_issues)
            elif principle == ArchitecturalPrinciple.OPEN_CLOSED:
                validation_issues = self._validate_open_closed(change)
                issues.extend(validation_issues)

        recommendations = self._generate_recommendations(principle, issues)
        
        # Record compliance check
        self.compliance_history.append({
            "agent_id": agent_id,
            "principle": principle,
            "compliant": len(issues) == 0,
            "timestamp": datetime.now()
        })

        return ComplianceValidationResult(
            agent_id=agent_id,
            principle=principle,
            compliant=len(issues) == 0,
            issues=issues,
            recommendations=recommendations
        )

    def _validate_single_responsibility(self, code: str) -> List[str]:
        """Validate Single Responsibility Principle."""
        issues = []
        
        # Check for multiple responsibilities in a single class/function
        if "class " in code and code.count("def ") > 10:
            issues.append("Class has too many methods - consider splitting responsibilities")
        
        if "def " in code and code.count("if ") > 5:
            issues.append("Function has too many conditional branches - consider splitting")
        
        return issues

    def _validate_dry_principle(self, code: str) -> List[str]:
        """Validate Don't Repeat Yourself principle."""
        issues = []
        
        # Simple duplicate code detection
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if line.strip() and lines.count(line) > 2:
                issues.append(f"Duplicate code detected at line {i+1}: {line[:50]}...")
        
        return issues

    def _validate_kiss_principle(self, code: str) -> List[str]:
        """Validate Keep It Simple, Stupid principle."""
        issues = []
        
        # Check for overly complex code
        if len(code.split('\n')) > self.config["compliance_thresholds"]["max_file_lines"]:
            line_count = len(code.split('\n'))
            max_lines = self.config['compliance_thresholds']['max_file_lines']
            issues.append(f"File too long: {line_count} lines (max: {max_lines})")
        
        # Check for complex nested structures
        if code.count('    ') > 20:  # Deep nesting
            issues.append("Code has excessive nesting - consider simplifying")
        
        return issues

    def _validate_open_closed(self, code: str) -> List[str]:
        """Validate Open-Closed Principle."""
        issues = []
        
        # Check for hardcoded values that should be configurable
        if code.count('"') > 20:  # Many string literals
            issues.append("Consider extracting hardcoded strings to configuration")
        
        return issues

    def _generate_recommendations(self, principle: ArchitecturalPrinciple, 
                                issues: List[str]) -> List[str]:
        """Generate recommendations based on issues."""
        recommendations = []
        
        if principle == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY:
            recommendations.append("Split large classes into smaller, focused classes")
            recommendations.append("Extract complex methods into separate functions")
        
        elif principle == ArchitecturalPrinciple.DONT_REPEAT_YOURSELF:
            recommendations.append("Extract common code into reusable functions")
            recommendations.append("Use configuration files for repeated values")
        
        elif principle == ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID:
            recommendations.append("Break down complex functions into simpler ones")
            recommendations.append("Use descriptive variable and function names")
        
        elif principle == ArchitecturalPrinciple.OPEN_CLOSED:
            recommendations.append("Use dependency injection for external dependencies")
            recommendations.append("Design interfaces for extensibility")
        
        return recommendations

    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get compliance validation summary."""
        if not self.compliance_history:
            return {"total_checks": 0, "compliant_checks": 0, "compliance_rate": 0.0}
        
        total_checks = len(self.compliance_history)
        compliant_checks = sum(1 for check in self.compliance_history if check["compliant"])
        compliance_rate = (compliant_checks / total_checks) * 100
        
        return {
            "total_checks": total_checks,
            "compliant_checks": compliant_checks,
            "compliance_rate": compliance_rate,
            "recent_checks": self.compliance_history[-10:]  # Last 10 checks
        }

    def get_service_status(self) -> Dict[str, Any]:
        """Get overall service status."""
        return {
            "agent_id": self.agent_id,
            "registered_agents": len(self.agents),
            "performance_metrics": len(self.performance_metrics),
            "compliance_checks": len(self.compliance_history),
            "status": "active"
        }
