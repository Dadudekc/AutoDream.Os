"""
🎯 VALIDATION PROTOCOLS - PROTOCOLS COMPONENT
Agent-7 - Quality Completion Optimization Manager

Validation processes and quality gates for quality assurance.
Follows V2 coding standards: ≤300 lines per module.
"""

import os
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class ValidationStatus(Enum):
    """Validation status enumeration."""
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    ERROR = "ERROR"
    PENDING = "PENDING"


@dataclass
class QualityGate:
    """Quality gate definition for validation."""
    name: str
    description: str
    threshold: float
    weight: float
    critical: bool = False
    status: ValidationStatus = ValidationStatus.PENDING
    
    def evaluate(self, value: float) -> ValidationStatus:
        """Evaluate if the gate passes based on the value."""
        if value >= self.threshold:
            self.status = ValidationStatus.PASSED
            return ValidationStatus.PASSED
        elif self.critical:
            self.status = ValidationStatus.FAILED
            return ValidationStatus.FAILED
        else:
            self.status = ValidationStatus.WARNING
            return ValidationStatus.WARNING


class ValidationProcesses:
    """Validation processes for modularized components."""
    
    def __init__(self):
        """Initialize validation processes."""
        self.quality_gates = self._initialize_quality_gates()
    
    def _initialize_quality_gates(self) -> Dict[str, QualityGate]:
        """Initialize quality gates for validation."""
        return {
            "file_size_reduction": QualityGate(
                "File Size Reduction",
                "Minimum 30% reduction in main file size",
                30.0,
                0.2,
                critical=True
            ),
            "module_count": QualityGate(
                "Module Count",
                "Minimum 5 modules created",
                5.0,
                0.15,
                critical=True
            ),
            "v2_compliance": QualityGate(
                "V2 Compliance",
                "All modules under 400 lines",
                100.0,
                0.2,
                critical=True
            ),
            "interface_quality": QualityGate(
                "Interface Quality",
                "Minimum 0.7 interface quality score",
                0.7,
                0.15,
                critical=False
            ),
            "test_coverage": QualityGate(
                "Test Coverage",
                "Minimum 80% test coverage",
                80.0,
                0.1,
                critical=False
            ),
            "documentation": QualityGate(
                "Documentation",
                "Minimum 0.7 documentation score",
                0.7,
                0.1,
                critical=False
            ),
            "code_organization": QualityGate(
                "Code Organization",
                "Minimum 0.75 organization score",
                0.75,
                0.1,
                critical=False
            )
        }
    
    def validate_modularization(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate modularization against quality gates.
        
        Args:
            metrics: Quality metrics to validate
            
        Returns:
            dict: Validation results and status
        """
        validation_results = {
            "gates": {},
            "overall_status": ValidationStatus.PENDING,
            "passed_gates": 0,
            "failed_gates": 0,
            "warning_gates": 0,
            "critical_failures": 0,
            "recommendations": []
        }
        
        try:
            # Evaluate each quality gate
            for gate_name, gate in self.quality_gates.items():
                if gate_name in metrics:
                    metric_value = metrics[gate_name]
                    if isinstance(metric_value, dict) and "value" in metric_value:
                        value = metric_value["value"]
                    else:
                        value = metric_value
                    
                    gate_status = gate.evaluate(value)
                    validation_results["gates"][gate_name] = {
                        "status": gate_status.value,
                        "threshold": gate.threshold,
                        "actual_value": value,
                        "passed": gate_status == ValidationStatus.PASSED,
                        "critical": gate.critical
                    }
                    
                    # Count gate results
                    if gate_status == ValidationStatus.PASSED:
                        validation_results["passed_gates"] += 1
                    elif gate_status == ValidationStatus.FAILED:
                        validation_results["failed_gates"] += 1
                        if gate.critical:
                            validation_results["critical_failures"] += 1
                    elif gate_status == ValidationStatus.WARNING:
                        validation_results["warning_gates"] += 1
            
            # Determine overall status
            validation_results["overall_status"] = self._determine_validation_status(validation_results)
            
            # Generate recommendations
            validation_results["recommendations"] = self._generate_validation_recommendations(
                validation_results["gates"]
            )
            
        except Exception as e:
            validation_results["error"] = str(e)
            validation_results["overall_status"] = ValidationStatus.ERROR
        
        return validation_results
    
    def _determine_validation_status(self, validation_results: Dict[str, Any]) -> ValidationStatus:
        """Determine overall validation status."""
        if "error" in validation_results:
            return ValidationStatus.ERROR
        
        critical_failures = validation_results.get("critical_failures", 0)
        failed_gates = validation_results.get("failed_gates", 0)
        total_gates = len(self.quality_gates)
        
        if critical_failures > 0:
            return ValidationStatus.FAILED
        elif failed_gates == 0:
            return ValidationStatus.PASSED
        elif failed_gates < total_gates:
            return ValidationStatus.WARNING
        else:
            return ValidationStatus.FAILED
    
    def _generate_validation_recommendations(self, gates: Dict[str, Any]) -> List[str]:
        """Generate validation improvement recommendations."""
        recommendations = []
        
        for gate_name, gate_result in gates.items():
            if not gate_result["passed"]:
                gate = self.quality_gates.get(gate_name)
                if gate:
                    if gate.critical:
                        recommendations.append(f"CRITICAL: Fix {gate.description} (current: {gate_result['actual_value']}, required: {gate.threshold})")
                    else:
                        recommendations.append(f"Improve {gate.description} (current: {gate_result['actual_value']}, required: {gate.threshold})")
        
        return recommendations


class ValidationProtocols:
    """Main validation protocols for quality assurance."""
    
    def __init__(self):
        """Initialize validation protocols."""
        self.validation_processes = ValidationProcesses()
    
    def run_validation(self, target_file: str, modularized_dir: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run comprehensive validation protocols.
        
        Args:
            target_file: Path to the original monolithic file
            modularized_dir: Path to the modularized components directory
            metrics: Quality metrics to validate
            
        Returns:
            dict: Validation results and recommendations
        """
        validation_results = {
            "file_validation": {},
            "structure_validation": {},
            "quality_validation": {},
            "overall_validation": {},
            "recommendations": []
        }
        
        try:
            # Validate file structure
            validation_results["file_validation"] = self._validate_file_structure(target_file, modularized_dir)
            
            # Validate modularized structure
            validation_results["structure_validation"] = self._validate_modularized_structure(modularized_dir)
            
            # Validate quality metrics
            validation_results["quality_validation"] = self.validation_processes.validate_modularization(metrics)
            
            # Overall validation summary
            validation_results["overall_validation"] = self._create_overall_validation_summary(validation_results)
            
            # Consolidate recommendations
            validation_results["recommendations"] = self._consolidate_recommendations(validation_results)
            
        except Exception as e:
            validation_results["error"] = str(e)
        
        return validation_results
    
    def _validate_file_structure(self, target_file: str, modularized_dir: str) -> Dict[str, Any]:
        """Validate file structure requirements."""
        validation = {
            "original_file_exists": os.path.exists(target_file),
            "modularized_dir_exists": os.path.exists(modularized_dir),
            "original_file_size": 0,
            "modularized_dir_size": 0,
            "status": ValidationStatus.PENDING
        }
        
        if validation["original_file_exists"]:
            validation["original_file_size"] = os.path.getsize(target_file)
        
        if validation["modularized_dir_exists"]:
            validation["modularized_dir_size"] = self._get_directory_size(modularized_dir)
        
        # Determine status
        if not validation["original_file_exists"] or not validation["modularized_dir_exists"]:
            validation["status"] = ValidationStatus.FAILED
        else:
            validation["status"] = ValidationStatus.PASSED
        
        return validation
    
    def _validate_modularized_structure(self, modularized_dir: str) -> Dict[str, Any]:
        """Validate modularized structure requirements."""
        validation = {
            "module_count": 0,
            "max_module_lines": 0,
            "total_lines": 0,
            "v2_compliant": False,
            "status": ValidationStatus.PENDING
        }
        
        try:
            for root, dirs, files in os.walk(modularized_dir):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        validation["module_count"] += 1
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                lines = len(f.readlines())
                                validation["total_lines"] += lines
                                validation["max_module_lines"] = max(
                                    validation["max_module_lines"], lines
                                )
                        except (OSError, UnicodeDecodeError):
                            pass
            
            # Check V2 compliance
            validation["v2_compliant"] = validation["max_module_lines"] <= 400
            
            # Determine status
            if validation["module_count"] >= 5 and validation["v2_compliant"]:
                validation["status"] = ValidationStatus.PASSED
            elif validation["module_count"] >= 5:
                validation["status"] = ValidationStatus.WARNING
            else:
                validation["status"] = ValidationStatus.FAILED
                
        except (OSError, FileNotFoundError):
            validation["status"] = ValidationStatus.ERROR
        
        return validation
    
    def _get_directory_size(self, dir_path: str) -> int:
        """Get total size of directory in bytes."""
        total_size = 0
        try:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
        except (OSError, FileNotFoundError):
            pass
        return total_size
    
    def _create_overall_validation_summary(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create overall validation summary."""
        summary = {
            "overall_status": ValidationStatus.PENDING,
            "total_validations": 0,
            "passed_validations": 0,
            "failed_validations": 0,
            "warning_validations": 0,
            "critical_failures": 0
        }
        
        # Count validation results
        for validation_type, results in validation_results.items():
            if validation_type != "overall_validation" and validation_type != "recommendations":
                if "status" in results:
                    summary["total_validations"] += 1
                    if results["status"] == ValidationStatus.PASSED:
                        summary["passed_validations"] += 1
                    elif results["status"] == ValidationStatus.FAILED:
                        summary["failed_validations"] += 1
                    elif results["status"] == ValidationStatus.WARNING:
                        summary["warning_validations"] += 1
        
        # Determine overall status
        if summary["failed_validations"] > 0:
            summary["overall_status"] = ValidationStatus.FAILED
        elif summary["warning_validations"] > 0:
            summary["overall_status"] = ValidationStatus.WARNING
        elif summary["passed_validations"] > 0:
            summary["overall_status"] = ValidationStatus.PASSED
        
        return summary
    
    def _consolidate_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """Consolidate recommendations from all validation types."""
        recommendations = []
        
        for validation_type, results in validation_results.items():
            if validation_type != "overall_validation" and validation_type != "recommendations":
                if "recommendations" in results:
                    recommendations.extend(results["recommendations"])
        
        return list(set(recommendations))  # Remove duplicates
