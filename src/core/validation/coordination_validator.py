#!/usr/bin/env python3
"""
Coordination & Communication Validation Engine - Agent Cellphone V2
================================================================

Comprehensive validation system for coordination and communication systems.

Author: Agent-6 (Gaming & Entertainment Specialist)
License: MIT
"""

import os
import yaml
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class ValidationSeverity(Enum):
    """Validation severity levels."""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class ValidationResult(Enum):
    """Validation result types."""
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"


@dataclass
class ValidationIssue:
    """Individual validation issue."""
    rule_id: str
    rule_name: str
    severity: ValidationSeverity
    message: str
    details: Dict[str, Any]
    timestamp: datetime
    component: str


class CoordinationValidator:
    """Comprehensive validation engine for coordination systems."""
    
    def __init__(self, rules_dir: str = "src/core/validation/rules"):
        """Initialize the validation engine."""
        self.rules_dir = rules_dir
        self.rules = self._load_validation_rules()
        self.validation_history: List[ValidationIssue] = []
        
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules from YAML files."""
        rules = {}
        
        try:
            # Load message validation rules
            message_rules_path = os.path.join(self.rules_dir, "message.yaml")
            if os.path.exists(message_rules_path):
                with open(message_rules_path, 'r') as f:
                    rules['message'] = yaml.safe_load(f)
            
            # Load quality validation rules
            quality_rules_path = os.path.join(self.rules_dir, "quality.yaml")
            if os.path.exists(quality_rules_path):
                with open(quality_rules_path, 'r') as f:
                    rules['quality'] = yaml.safe_load(f)
            
            # Load security validation rules
            security_rules_path = os.path.join(self.rules_dir, "security.yaml")
            if os.path.exists(security_rules_path):
                with open(security_rules_path, 'r') as f:
                    rules['security'] = yaml.safe_load(f)
                    
        except Exception as e:
            print(f"⚠️ Warning: Could not load validation rules: {e}")
            rules = {}
            
        return rules
    
    def validate_message_structure(self, message_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate message structure against rules."""
        issues = []
        
        # Check required fields
        required_fields = ['content', 'sender', 'recipient']
        for field in required_fields:
            if field not in message_data:
                issues.append(ValidationIssue(
                    rule_id="required_fields",
                    rule_name="Required Fields",
                    severity=ValidationSeverity.ERROR,
                    message=f"Missing required field: {field}",
                    details={"field": field, "message_data": message_data},
                    timestamp=datetime.now(),
                    component="message_structure"
                ))
        
        # Check message format
        if 'content' in message_data and not isinstance(message_data['content'], str):
            issues.append(ValidationIssue(
                rule_id="message_format",
                rule_name="Message Format",
                severity=ValidationSeverity.ERROR,
                message="Message content must be a string",
                details={"field": "content", "type": type(message_data['content'])},
                timestamp=datetime.now(),
                component="message_structure"
            ))
        
        # Check enum values
        if 'message_type' in message_data:
            valid_types = ['text', 'broadcast', 'onboarding']
            if message_data['message_type'] not in valid_types:
                issues.append(ValidationIssue(
                    rule_id="enum_validation",
                    rule_name="Enum Validation",
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid message type: {message_data['message_type']}",
                    details={"valid_types": valid_types, "provided": message_data['message_type']},
                    timestamp=datetime.now(),
                    component="message_structure"
                ))
        
        return issues
    
    def validate_coordination_system(self, system_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate coordination system configuration."""
        issues = []
        
        # Check agent configuration
        if 'agents' in system_data:
            agent_data = system_data['agents']
            for agent_id, agent_info in agent_data.items():
                if not isinstance(agent_info, dict):
                    issues.append(ValidationIssue(
                        rule_id="coordination_structure",
                        rule_name="Coordination Structure",
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid agent configuration for {agent_id}",
                        details={"agent_id": agent_id, "agent_info": agent_info},
                        timestamp=datetime.now(),
                        component="coordination_system"
                    ))
                    continue
                
                # Check required agent fields
                required_agent_fields = ['description', 'coords']
                for field in required_agent_fields:
                    if field not in agent_info:
                        issues.append(ValidationIssue(
                            rule_id="agent_required_fields",
                            rule_name="Agent Required Fields",
                            severity=ValidationSeverity.ERROR,
                            message=f"Missing required field '{field}' for agent {agent_id}",
                            details={"agent_id": agent_id, "field": field},
                            timestamp=datetime.now(),
                            component="coordination_system"
                        ))
        
        return issues
    
    def validate_performance_metrics(self, metrics_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate performance metrics and thresholds."""
        issues = []
        
        # Check response time thresholds
        if 'response_time' in metrics_data:
            response_time = metrics_data['response_time']
            if isinstance(response_time, (int, float)) and response_time > 5.0:
                issues.append(ValidationIssue(
                    rule_id="performance_threshold",
                    rule_name="Performance Threshold",
                    severity=ValidationSeverity.WARNING,
                    message=f"Response time exceeds threshold: {response_time}s",
                    details={"threshold": 5.0, "actual": response_time},
                    timestamp=datetime.now(),
                    component="performance_metrics"
                ))
        
        # Check throughput metrics
        if 'throughput' in metrics_data:
            throughput = metrics_data['throughput']
            if isinstance(throughput, (int, float)) and throughput < 100:
                issues.append(ValidationIssue(
                    rule_id="performance_threshold",
                    rule_name="Performance Threshold",
                    severity=ValidationSeverity.WARNING,
                    message=f"Throughput below threshold: {throughput}",
                    details={"threshold": 100, "actual": throughput},
                    timestamp=datetime.now(),
                    component="performance_metrics"
                ))
        
        return issues
    
    def validate_security_compliance(self, security_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate security compliance requirements."""
        issues = []
        
        # Check authentication mechanisms
        if 'authentication' in security_data:
            auth_data = security_data['authentication']
            if not isinstance(auth_data, dict):
                issues.append(ValidationIssue(
                    rule_id="security_structure",
                    rule_name="Security Structure",
                    severity=ValidationSeverity.ERROR,
                    message="Authentication configuration must be a dictionary",
                    details={"authentication": auth_data},
                    timestamp=datetime.now(),
                    component="security_compliance"
                ))
            else:
                # Check for required auth fields
                if 'enabled' not in auth_data:
                    issues.append(ValidationIssue(
                        rule_id="authentication_validation",
                        rule_name="Authentication Validation",
                        severity=ValidationSeverity.WARNING,
                        message="Authentication enabled status not specified",
                        details={"authentication": auth_data},
                        timestamp=datetime.now(),
                        component="security_compliance"
                    ))
        
        return issues
    
    def run_comprehensive_validation(self, target_system: str, 
                                   validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive validation on a target system."""
        all_issues = []
        
        # Run all validation types
        all_issues.extend(self.validate_message_structure(validation_data.get('messages', {})))
        all_issues.extend(self.validate_coordination_system(validation_data.get('coordination', {})))
        all_issues.extend(self.validate_performance_metrics(validation_data.get('performance', {})))
        all_issues.extend(self.validate_security_compliance(validation_data.get('security', {})))
        
        # Store validation history
        self.validation_history.extend(all_issues)
        
        # Categorize issues by severity
        errors = [issue for issue in all_issues if issue.severity == ValidationSeverity.ERROR]
        warnings = [issue for issue in all_issues if issue.severity == ValidationSeverity.WARNING]
        info = [issue for issue in all_issues if issue.severity == ValidationSeverity.INFO]
        
        # Determine overall validation result
        if errors:
            overall_result = ValidationResult.FAIL
        elif warnings:
            overall_result = ValidationResult.WARNING
        else:
            overall_result = ValidationResult.PASS
        
        return {
            "target_system": target_system,
            "timestamp": datetime.now(),
            "overall_result": overall_result.value,
            "total_issues": len(all_issues),
            "errors": len(errors),
            "warnings": len(warnings),
            "info": len(info),
            "issues": all_issues,
            "validation_summary": {
                "passed": overall_result == ValidationResult.PASS,
                "has_errors": len(errors) > 0,
                "has_warnings": len(warnings) > 0,
                "compliance_score": self._calculate_compliance_score(all_issues)
            }
        }
    
    def _calculate_compliance_score(self, issues: List[ValidationIssue]) -> float:
        """Calculate compliance score based on issues."""
        if not issues:
            return 100.0
        
        total_issues = len(issues)
        error_weight = 3.0
        warning_weight = 1.0
        
        weighted_score = sum([
            error_weight if issue.severity == ValidationSeverity.ERROR else warning_weight
            for issue in issues
        ])
        
        max_possible_score = total_issues * error_weight
        compliance_score = max(0.0, 100.0 - (weighted_score / max_possible_score * 100.0))
        
        return round(compliance_score, 2)
    
    def get_validation_report(self, target_system: str = None) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        if target_system:
            system_issues = [issue for issue in self.validation_history 
                           if issue.component == target_system]
        else:
            system_issues = self.validation_history
        
        return {
            "validation_summary": {
                "total_validations": len(self.validation_history),
                "target_system_validations": len(system_issues),
                "last_validation": self.validation_history[-1].timestamp if self.validation_history else None
            },
            "compliance_metrics": {
                "overall_compliance": self._calculate_compliance_score(self.validation_history),
                "system_compliance": self._calculate_compliance_score(system_issues) if system_issues else 100.0
            },
            "recent_issues": system_issues[-10:] if system_issues else []
        }
