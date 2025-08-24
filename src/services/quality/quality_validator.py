#!/usr/bin/env python3
"""
Quality Validation System
=========================

Quality validation, gate enforcement, and compliance checking for V2 services.
Follows V2 coding standards: ≤300 lines per module.
"""

import time
import logging
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

from .core_framework import QualityLevel, QualityMetric, TestResult

logger = logging.getLogger(__name__)


class ValidationStatus(Enum):
    """Validation status enumeration"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    PENDING = "pending"


@dataclass
class ValidationRule:
    """Quality validation rule"""
    rule_id: str
    rule_name: str
    rule_type: str
    threshold: Any
    severity: str
    description: str
    enabled: bool = True


@dataclass
class ValidationResult:
    """Quality validation result"""
    validation_id: str
    rule_id: str
    service_id: str
    status: ValidationStatus
    timestamp: float
    actual_value: Any
    expected_value: Any
    message: str
    details: Dict[str, Any]


class QualityValidator:
    """Core quality validation engine"""
    
    def __init__(self):
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.validation_results: Dict[str, List[ValidationResult]] = {}
        self._lock = threading.Lock()
        
        # Setup default validation rules
        self._setup_default_rules()
        
        logger.info("Quality Validator initialized")
        
    def _setup_default_rules(self) -> None:
        """Setup default quality validation rules"""
        default_rules = [
            ValidationRule(
                rule_id="test_coverage_min",
                rule_name="Minimum Test Coverage",
                rule_type="coverage",
                threshold=80.0,
                severity="high",
                description="Ensure test coverage is at least 80%"
            ),
            ValidationRule(
                rule_id="code_quality_min",
                rule_name="Minimum Code Quality",
                rule_type="quality",
                threshold=7.0,
                severity="medium",
                description="Ensure code quality score is at least 7.0"
            ),
            ValidationRule(
                rule_id="performance_latency_max",
                rule_name="Maximum Performance Latency",
                rule_type="performance",
                threshold=100.0,
                severity="medium",
                description="Ensure performance latency is under 100ms"
            ),
            ValidationRule(
                rule_id="security_score_min",
                rule_name="Minimum Security Score",
                rule_type="security",
                threshold=8.0,
                severity="critical",
                description="Ensure security score is at least 8.0"
            )
        ]
        
        for rule in default_rules:
            self.add_validation_rule(rule)
            
    def add_validation_rule(self, rule: ValidationRule) -> bool:
        """Add a new validation rule"""
        try:
            with self._lock:
                self.validation_rules[rule.rule_id] = rule
            logger.info(f"Validation rule added: {rule.rule_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add validation rule: {e}")
            return False
            
    def remove_validation_rule(self, rule_id: str) -> bool:
        """Remove a validation rule"""
        try:
            with self._lock:
                self.validation_rules.pop(rule_id, None)
            logger.info(f"Validation rule removed: {rule_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove validation rule: {e}")
            return False
            
    def validate_service_quality(self, service_id: str, 
                               quality_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate service quality against all applicable rules"""
        try:
            validation_results = []
            current_time = time.time()
            
            with self._lock:
                for rule_id, rule in self.validation_rules.items():
                    if not rule.enabled:
                        continue
                        
                    # Check if rule applies to this service
                    if self._rule_applies_to_service(rule, service_id):
                        result = self._validate_rule(rule, service_id, quality_data, current_time)
                        if result:
                            validation_results.append(result)
                            
            # Store results
            if service_id not in self.validation_results:
                self.validation_results[service_id] = []
            self.validation_results[service_id].extend(validation_results)
            
            logger.info(f"Quality validation completed for {service_id}: {len(validation_results)} rules checked")
            return validation_results
            
        except Exception as e:
            logger.error(f"Failed to validate service quality for {service_id}: {e}")
            return []
            
    def _rule_applies_to_service(self, rule: ValidationRule, service_id: str) -> bool:
        """Check if a validation rule applies to a specific service"""
        # For now, all rules apply to all services
        # This could be extended with service-specific rule targeting
        return True
        
    def _validate_rule(self, rule: ValidationRule, service_id: str, 
                       quality_data: Dict[str, Any], timestamp: float) -> Optional[ValidationResult]:
        """Validate a specific rule against quality data"""
        try:
            # Extract the relevant metric value
            metric_value = self._extract_metric_value(rule.rule_type, quality_data)
            
            if metric_value is None:
                return None
                
            # Perform validation
            status, message = self._evaluate_rule(rule, metric_value)
            
            # Create validation result
            result = ValidationResult(
                validation_id=f"validation_{service_id}_{rule.rule_id}_{int(timestamp)}",
                rule_id=rule.rule_id,
                service_id=service_id,
                status=status,
                timestamp=timestamp,
                actual_value=metric_value,
                expected_value=rule.threshold,
                message=message,
                details={
                    "rule_name": rule.rule_name,
                    "rule_type": rule.rule_type,
                    "severity": rule.severity
                }
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to validate rule {rule.rule_id}: {e}")
            return None
            
    def _extract_metric_value(self, rule_type: str, quality_data: Dict[str, Any]) -> Any:
        """Extract metric value based on rule type"""
        metric_mapping = {
            "coverage": "test_coverage",
            "quality": "code_quality",
            "performance": "performance_latency",
            "security": "security_score"
        }
        
        metric_key = metric_mapping.get(rule_type)
        if metric_key and metric_key in quality_data:
            return quality_data[metric_key]
            
        return None
        
    def _evaluate_rule(self, rule: ValidationRule, actual_value: Any) -> tuple[ValidationStatus, str]:
        """Evaluate a rule against actual value"""
        try:
            if isinstance(actual_value, (int, float)) and isinstance(rule.threshold, (int, float)):
                # Numeric comparison
                if rule.rule_type in ["coverage", "quality", "security"]:
                    # Higher is better
                    if actual_value >= rule.threshold:
                        return ValidationStatus.PASSED, f"Value {actual_value} meets threshold {rule.threshold}"
                    else:
                        return ValidationStatus.FAILED, f"Value {actual_value} below threshold {rule.threshold}"
                elif rule.rule_type == "performance":
                    # Lower is better
                    if actual_value <= rule.threshold:
                        return ValidationStatus.PASSED, f"Value {actual_value} meets threshold {rule.threshold}"
                    else:
                        return ValidationStatus.FAILED, f"Value {actual_value} above threshold {rule.threshold}"
                        
            # Fallback for non-numeric or unmatched types
            if actual_value == rule.threshold:
                return ValidationStatus.PASSED, f"Value {actual_value} matches threshold {rule.threshold}"
            else:
                return ValidationStatus.FAILED, f"Value {actual_value} does not match threshold {rule.threshold}"
                
        except Exception as e:
            logger.error(f"Error evaluating rule {rule.rule_id}: {e}")
            return ValidationStatus.FAILED, f"Validation error: {str(e)}"
            
    def get_validation_results(self, service_id: str = None) -> Dict[str, List[ValidationResult]]:
        """Get validation results"""
        with self._lock:
            if service_id:
                return {service_id: self.validation_results.get(service_id, [])}
            return self.validation_results.copy()
            
    def get_validation_summary(self, service_id: str = None) -> Dict[str, Any]:
        """Get validation summary statistics"""
        try:
            results = self.get_validation_results(service_id)
            
            summary = {
                "total_validations": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0,
                "pending": 0,
                "pass_rate": 0.0
            }
            
            for service_results in results.values():
                for result in service_results:
                    summary["total_validations"] += 1
                    if result.status == ValidationStatus.PASSED:
                        summary["passed"] += 1
                    elif result.status == ValidationStatus.FAILED:
                        summary["failed"] += 1
                    elif result.status == ValidationStatus.WARNING:
                        summary["warnings"] += 1
                    elif result.status == ValidationStatus.PENDING:
                        summary["pending"] += 1
                        
            if summary["total_validations"] > 0:
                summary["pass_rate"] = (summary["passed"] / summary["total_validations"]) * 100
                
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get validation summary: {e}")
            return {"error": str(e)}


class QualityGateEnforcer:
    """Enforces quality gates and deployment controls"""
    
    def __init__(self, quality_validator: QualityValidator):
        self.validator = quality_validator
        self.quality_gates: Dict[str, Dict[str, Any]] = {}
        self.gate_results: Dict[str, Dict[str, Any]] = {}
        
        logger.info("Quality Gate Enforcer initialized")
        
    def add_quality_gate(self, gate_id: str, gate_name: str, 
                        required_rules: List[str], 
                        pass_threshold: float = 100.0) -> bool:
        """Add a new quality gate"""
        try:
            self.quality_gates[gate_id] = {
                "gate_name": gate_name,
                "required_rules": required_rules,
                "pass_threshold": pass_threshold,
                "enabled": True
            }
            logger.info(f"Quality gate added: {gate_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add quality gate: {e}")
            return False
            
    def evaluate_quality_gate(self, gate_id: str, service_id: str, 
                            quality_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a quality gate for a service"""
        try:
            if gate_id not in self.quality_gates:
                return {"error": f"Quality gate {gate_id} not found"}
                
            gate = self.quality_gates[gate_id]
            if not gate["enabled"]:
                return {"status": "disabled", "message": "Quality gate is disabled"}
                
            # Run validation for required rules
            validation_results = self.validator.validate_service_quality(service_id, quality_data)
            
            # Filter results for required rules
            required_results = [
                result for result in validation_results
                if result.rule_id in gate["required_rules"]
            ]
            
            # Calculate pass rate
            total_required = len(gate["required_rules"])
            passed = sum(1 for result in required_results if result.status == ValidationStatus.PASSED)
            pass_rate = (passed / total_required) * 100 if total_required > 0 else 0
            
            # Determine gate status
            gate_passed = pass_rate >= gate["pass_threshold"]
            gate_status = "passed" if gate_passed else "failed"
            
            # Store gate result
            gate_result = {
                "gate_id": gate_id,
                "service_id": service_id,
                "status": gate_status,
                "pass_rate": pass_rate,
                "required_threshold": gate["pass_threshold"],
                "total_required": total_required,
                "passed": passed,
                "failed": total_required - passed,
                "timestamp": time.time(),
                "validation_results": required_results
            }
            
            if service_id not in self.gate_results:
                self.gate_results[service_id] = {}
            self.gate_results[service_id][gate_id] = gate_result
            
            logger.info(f"Quality gate {gate_id} evaluation completed for {service_id}: {gate_status}")
            return gate_result
            
        except Exception as e:
            logger.error(f"Failed to evaluate quality gate {gate_id}: {e}")
            return {"error": str(e)}
            
    def is_deployment_allowed(self, service_id: str, quality_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if deployment is allowed based on quality gates"""
        try:
            deployment_result = {
                "deployment_allowed": True,
                "failed_gates": [],
                "overall_status": "approved",
                "quality_score": 0.0,
                "timestamp": time.time()
            }
            
            failed_gates = []
            total_score = 0.0
            gate_count = 0
            
            # Evaluate all enabled quality gates
            for gate_id, gate in self.quality_gates.items():
                if gate["enabled"]:
                    gate_result = self.evaluate_quality_gate(gate_id, service_id, quality_data)
                    
                    if "error" not in gate_result:
                        gate_count += 1
                        if gate_result["status"] == "passed":
                            total_score += gate_result["pass_rate"]
                        else:
                            failed_gates.append(gate_id)
                            deployment_result["deployment_allowed"] = False
                            
            # Calculate overall quality score
            if gate_count > 0:
                deployment_result["quality_score"] = total_score / gate_count
                
            # Update overall status
            if failed_gates:
                deployment_result["failed_gates"] = failed_gates
                deployment_result["overall_status"] = "rejected"
                
            # Store deployment result
            if service_id not in self.gate_results:
                self.gate_results[service_id] = {}
            self.gate_results[service_id]["deployment"] = deployment_result
            
            logger.info(f"Deployment check for {service_id}: {'ALLOWED' if deployment_result['deployment_allowed'] else 'REJECTED'}")
            return deployment_result
            
        except Exception as e:
            logger.error(f"Failed to check deployment allowance for {service_id}: {e}")
            return {"error": str(e), "deployment_allowed": False}


class QualityComplianceChecker:
    """Checks compliance with quality standards and policies"""
    
    def __init__(self, quality_validator: QualityValidator):
        self.validator = quality_validator
        self.compliance_policies: Dict[str, Dict[str, Any]] = {}
        
        # Setup default compliance policies
        self._setup_default_policies()
        
        logger.info("Quality Compliance Checker initialized")
        
    def _setup_default_policies(self) -> None:
        """Setup default compliance policies"""
        self.compliance_policies = {
            "v2_standards": {
                "name": "V2 Coding Standards Compliance",
                "description": "Ensure compliance with V2 coding standards",
                "rules": ["test_coverage_min", "code_quality_min"],
                "required_pass_rate": 90.0
            },
            "security_compliance": {
                "name": "Security Compliance",
                "description": "Ensure security standards are met",
                "rules": ["security_score_min"],
                "required_pass_rate": 100.0
            },
            "performance_compliance": {
                "name": "Performance Compliance",
                "description": "Ensure performance standards are met",
                "rules": ["performance_latency_max"],
                "required_pass_rate": 85.0
            }
        }
        
    def check_compliance(self, service_id: str, 
                        quality_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with all applicable policies"""
        try:
            compliance_result = {
                "service_id": service_id,
                "timestamp": time.time(),
                "overall_compliance": "compliant",
                "policies": {},
                "compliance_score": 0.0
            }
            
            total_score = 0.0
            policy_count = 0
            
            for policy_id, policy in self.compliance_policies.items():
                policy_result = self._check_policy_compliance(policy_id, policy, service_id, quality_data)
                compliance_result["policies"][policy_id] = policy_result
                
                if "compliance_score" in policy_result:
                    total_score += policy_result["compliance_score"]
                    policy_count += 1
                    
            # Calculate overall compliance score
            if policy_count > 0:
                compliance_result["compliance_score"] = total_score / policy_count
                
            # Determine overall compliance status
            if compliance_result["compliance_score"] >= 90.0:
                compliance_result["overall_compliance"] = "compliant"
            elif compliance_result["compliance_score"] >= 70.0:
                compliance_result["overall_compliance"] = "partially_compliant"
            else:
                compliance_result["overall_compliance"] = "non_compliant"
                
            logger.info(f"Compliance check for {service_id}: {compliance_result['overall_compliance']}")
            return compliance_result
            
        except Exception as e:
            logger.error(f"Failed to check compliance for {service_id}: {e}")
            return {"error": str(e)}
            
    def _check_policy_compliance(self, policy_id: str, policy: Dict[str, Any], 
                                service_id: str, quality_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with a specific policy"""
        try:
            # Run validation for policy rules
            validation_results = self.validator.validate_service_quality(service_id, quality_data)
            
            # Filter results for policy rules
            policy_results = [
                result for result in validation_results
                if result.rule_id in policy["rules"]
            ]
            
            # Calculate compliance score
            total_rules = len(policy["rules"])
            passed_rules = sum(1 for result in policy_results if result.status == ValidationStatus.PASSED)
            compliance_score = (passed_rules / total_rules) * 100 if total_rules > 0 else 0
            
            # Determine policy compliance
            required_rate = policy.get("required_pass_rate", 100.0)
            compliant = compliance_score >= required_rate
            
            policy_result = {
                "policy_name": policy["name"],
                "description": policy["description"],
                "compliance_score": compliance_score,
                "required_rate": required_rate,
                "compliant": compliant,
                "total_rules": total_rules,
                "passed_rules": passed_rules,
                "failed_rules": total_rules - passed_rules,
                "validation_results": policy_results
            }
            
            return policy_result
            
        except Exception as e:
            logger.error(f"Failed to check policy compliance for {policy_id}: {e}")
            return {"error": str(e)}
