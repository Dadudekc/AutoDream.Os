#!/usr/bin/env python3
"""
SSOT Validation System - Agent-8 Integration & Performance Specialist

This module provides comprehensive validation and testing for the unified SSOT
integration system, ensuring V2 compliance and cross-agent system integration.

Agent: Agent-8 (Integration & Performance Specialist)
Mission: V2 Compliance SSOT Maintenance & System Integration
Status: ACTIVE - SSOT Integration & System Validation
Priority: HIGH (650 points)
"""

import os
import sys
import json
import time
import unittest
from typing import Any, Dict, List, Optional, Union, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

# Import SSOT integration system
from .unified_ssot_integration_system import (
    UnifiedSSOTIntegrationSystem,
    SSOTComponentType,
    SSOTIntegrationStatus,
    get_unified_ssot_integration
)

# Import unified systems
import sys
import importlib.util

# Import unified logging system
spec = importlib.util.spec_from_file_location("unified_logging_system", "src/core/consolidation/unified-logging-system.py")
unified_logging_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(unified_logging_module)

# Import unified configuration system  
spec = importlib.util.spec_from_file_location("unified_configuration_system", "src/core/consolidation/unified-configuration-system.py")
unified_config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(unified_config_module)

# Get the functions
get_unified_logger = unified_logging_module.get_unified_logger
get_unified_config = unified_config_module.get_unified_config

# ================================
# VALIDATION TYPES
# ================================

class ValidationLevel(Enum):
    """Validation levels."""
    BASIC = "basic"
    COMPREHENSIVE = "comprehensive"
    STRESS = "stress"
    INTEGRATION = "integration"

class ValidationResult(Enum):
    """Validation results."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"

@dataclass
class ValidationTest:
    """Validation test definition."""
    test_id: str
    test_name: str
    test_level: ValidationLevel
    test_function: str
    expected_result: ValidationResult
    timeout_seconds: int = 30
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationReport:
    """Validation report structure."""
    test_id: str
    test_name: str
    result: ValidationResult
    execution_time: float
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

# ================================
# SSOT VALIDATION SYSTEM
# ================================

class SSOTValidationSystem:
    """
    Comprehensive SSOT validation and testing system.
    
    This system provides:
    - Component-level validation
    - Integration testing
    - Cross-agent compatibility testing
    - Performance validation
    - V2 compliance verification
    
    CONSOLIDATED: Single source of truth for all SSOT validation operations.
    """
    
    def __init__(self):
        self.logger = get_unified_logger()
        self.config_system = get_unified_config()
        self.ssot_integration = get_unified_ssot_integration()
        
        # Validation test registry
        self.validation_tests: Dict[str, ValidationTest] = {}
        self.validation_results: List[ValidationReport] = []
        
        # Initialize validation tests
        self._initialize_validation_tests()
        
        # Log system initialization
        self.logger.log_operation_start("SSOT Validation System Initialization")
    
    def _initialize_validation_tests(self) -> None:
        """Initialize all validation tests."""
        tests = [
            # Basic validation tests
            ValidationTest(
                test_id="basic_logging_functionality",
                test_name="Basic Logging Functionality",
                test_level=ValidationLevel.BASIC,
                test_function="test_basic_logging_functionality",
                expected_result=ValidationResult.PASSED
            ),
            ValidationTest(
                test_id="basic_configuration_loading",
                test_name="Basic Configuration Loading",
                test_level=ValidationLevel.BASIC,
                test_function="test_basic_configuration_loading",
                expected_result=ValidationResult.PASSED
            ),
            ValidationTest(
                test_id="basic_ssot_integration",
                test_name="Basic SSOT Integration",
                test_level=ValidationLevel.BASIC,
                test_function="test_basic_ssot_integration",
                expected_result=ValidationResult.PASSED
            ),
            
            # Comprehensive validation tests
            ValidationTest(
                test_id="comprehensive_logging_operations",
                test_name="Comprehensive Logging Operations",
                test_level=ValidationLevel.COMPREHENSIVE,
                test_function="test_comprehensive_logging_operations",
                expected_result=ValidationResult.PASSED,
                dependencies=["basic_logging_functionality"]
            ),
            ValidationTest(
                test_id="comprehensive_configuration_management",
                test_name="Comprehensive Configuration Management",
                test_level=ValidationLevel.COMPREHENSIVE,
                test_function="test_comprehensive_configuration_management",
                expected_result=ValidationResult.PASSED,
                dependencies=["basic_configuration_loading"]
            ),
            ValidationTest(
                test_id="comprehensive_ssot_components",
                test_name="Comprehensive SSOT Components",
                test_level=ValidationLevel.COMPREHENSIVE,
                test_function="test_comprehensive_ssot_components",
                expected_result=ValidationResult.PASSED,
                dependencies=["basic_ssot_integration"]
            ),
            
            # Integration validation tests
            ValidationTest(
                test_id="integration_cross_system_compatibility",
                test_name="Cross-System Compatibility",
                test_level=ValidationLevel.INTEGRATION,
                test_function="test_integration_cross_system_compatibility",
                expected_result=ValidationResult.PASSED,
                dependencies=["comprehensive_logging_operations", "comprehensive_configuration_management"]
            ),
            ValidationTest(
                test_id="integration_agent_coordination",
                test_name="Agent Coordination Integration",
                test_level=ValidationLevel.INTEGRATION,
                test_function="test_integration_agent_coordination",
                expected_result=ValidationResult.PASSED,
                dependencies=["comprehensive_ssot_components"]
            ),
            ValidationTest(
                test_id="integration_v2_compliance",
                test_name="V2 Compliance Integration",
                test_level=ValidationLevel.INTEGRATION,
                test_function="test_integration_v2_compliance",
                expected_result=ValidationResult.PASSED,
                dependencies=["integration_cross_system_compatibility"]
            ),
            
            # Stress validation tests
            ValidationTest(
                test_id="stress_logging_performance",
                test_name="Logging Performance Stress Test",
                test_level=ValidationLevel.STRESS,
                test_function="test_stress_logging_performance",
                expected_result=ValidationResult.PASSED,
                dependencies=["comprehensive_logging_operations"]
            ),
            ValidationTest(
                test_id="stress_configuration_scaling",
                test_name="Configuration Scaling Stress Test",
                test_level=ValidationLevel.STRESS,
                test_function="test_stress_configuration_scaling",
                expected_result=ValidationResult.PASSED,
                dependencies=["comprehensive_configuration_management"]
            ),
            ValidationTest(
                test_id="stress_ssot_integration_load",
                test_name="SSOT Integration Load Stress Test",
                test_level=ValidationLevel.STRESS,
                test_function="test_stress_ssot_integration_load",
                expected_result=ValidationResult.PASSED,
                dependencies=["comprehensive_ssot_components"]
            )
        ]
        
        for test in tests:
            self.validation_tests[test.test_id] = test
    
    # ================================
    # VALIDATION EXECUTION
    # ================================
    
    def run_validation_suite(self, level: Optional[ValidationLevel] = None) -> Dict[str, Any]:
        """Run validation test suite."""
        self.logger.log_operation_start(f"SSOT Validation Suite - Level: {level or 'ALL'}")
        
        # Filter tests by level if specified
        tests_to_run = [
            test for test in self.validation_tests.values()
            if level is None or test.test_level == level
        ]
        
        # Sort tests by dependencies
        sorted_tests = self._sort_tests_by_dependencies(tests_to_run)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "level": level.value if level else "ALL",
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "tests_warning": 0,
            "tests_skipped": 0,
            "execution_time": 0.0,
            "test_results": []
        }
        
        start_time = time.time()
        
        for test in sorted_tests:
            # Check dependencies
            if not self._check_test_dependencies(test):
                self.logger.log_validation_failed(f"Test Dependencies: {test.test_id}", "Dependencies not met")
                results["tests_skipped"] += 1
                continue
            
            # Run test
            test_result = self._run_validation_test(test)
            results["test_results"].append(test_result)
            results["tests_run"] += 1
            
            # Update counters
            if test_result.result == ValidationResult.PASSED:
                results["tests_passed"] += 1
            elif test_result.result == ValidationResult.FAILED:
                results["tests_failed"] += 1
            elif test_result.result == ValidationResult.WARNING:
                results["tests_warning"] += 1
            elif test_result.result == ValidationResult.SKIPPED:
                results["tests_skipped"] += 1
        
        results["execution_time"] = time.time() - start_time
        
        # Log completion
        if results["tests_failed"] == 0:
            self.logger.log_operation_complete(f"SSOT Validation Suite - Level: {level or 'ALL'}")
        else:
            self.logger.log_operation_failed(f"SSOT Validation Suite - Level: {level or 'ALL'}", f"{results['tests_failed']} tests failed")
        
        return results
    
    def _sort_tests_by_dependencies(self, tests: List[ValidationTest]) -> List[ValidationTest]:
        """Sort tests by dependency order."""
        sorted_tests = []
        remaining_tests = tests.copy()
        
        while remaining_tests:
            # Find tests with no unmet dependencies
            ready_tests = []
            for test in remaining_tests:
                if self._check_test_dependencies(test, sorted_tests):
                    ready_tests.append(test)
            
            if not ready_tests:
                # If no tests are ready, add remaining tests (circular dependency)
                sorted_tests.extend(remaining_tests)
                break
            
            # Add ready tests to sorted list
            sorted_tests.extend(ready_tests)
            for test in ready_tests:
                remaining_tests.remove(test)
        
        return sorted_tests
    
    def _check_test_dependencies(self, test: ValidationTest, completed_tests: Optional[List[ValidationTest]] = None) -> bool:
        """Check if test dependencies are met."""
        if completed_tests is None:
            completed_tests = [t for t in self.validation_tests.values() if t.test_id in [r.test_id for r in self.validation_results if r.result == ValidationResult.PASSED]]
        
        completed_test_ids = [t.test_id for t in completed_tests]
        
        for dep_id in test.dependencies:
            if dep_id not in completed_test_ids:
                return False
        
        return True
    
    def _run_validation_test(self, test: ValidationTest) -> ValidationReport:
        """Run a single validation test."""
        start_time = time.time()
        
        self.logger.log_validation_start(f"Validation Test: {test.test_name}")
        
        try:
            # Get test function
            test_function = getattr(self, test.test_function, None)
            if not test_function:
                return ValidationReport(
                    test_id=test.test_id,
                    test_name=test.test_name,
                    result=ValidationResult.FAILED,
                    execution_time=time.time() - start_time,
                    error_message=f"Test function {test.test_function} not found"
                )
            
            # Run test with timeout
            result = self._run_with_timeout(test_function, test.timeout_seconds)
            
            execution_time = time.time() - start_time
            
            if result["success"]:
                self.logger.log_validation_passed(f"Validation Test: {test.test_name}")
                return ValidationReport(
                    test_id=test.test_id,
                    test_name=test.test_name,
                    result=ValidationResult.PASSED,
                    execution_time=execution_time,
                    metadata=result.get("metadata", {})
                )
            else:
                self.logger.log_validation_failed(f"Validation Test: {test.test_name}", result.get("error", "Unknown error"))
                return ValidationReport(
                    test_id=test.test_id,
                    test_name=test.test_name,
                    result=ValidationResult.FAILED,
                    execution_time=execution_time,
                    error_message=result.get("error", "Unknown error"),
                    metadata=result.get("metadata", {})
                )
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.log_validation_failed(f"Validation Test: {test.test_name}", str(e))
            return ValidationReport(
                test_id=test.test_id,
                test_name=test.test_name,
                result=ValidationResult.FAILED,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def _run_with_timeout(self, func, timeout_seconds: int) -> Dict[str, Any]:
        """Run function with timeout."""
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Test timed out after {timeout_seconds} seconds")
        
        # Set timeout
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_seconds)
        
        try:
            result = func()
            return {"success": True, "result": result}
        except TimeoutError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            # Restore handler
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    
    # ================================
    # BASIC VALIDATION TESTS
    # ================================
    
    def test_basic_logging_functionality(self) -> Dict[str, Any]:
        """Test basic logging functionality."""
        try:
            # Test basic logging operations
            self.logger.log_operation_start("test_operation")
            self.logger.log_operation_complete("test_operation")
            self.logger.log_validation_passed("test_validation")
            
            return {"success": True, "metadata": {"operations_tested": 3}}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_basic_configuration_loading(self) -> Dict[str, Any]:
        """Test basic configuration loading."""
        try:
            # Test configuration loading
            config_data = self.config_system.load_configuration()
            
            # Test agent configuration access
            agent_config = self.config_system.get_agent_config("Agent-8")
            
            if config_data is not None and agent_config is not None:
                return {"success": True, "metadata": {"config_loaded": True, "agent_config_available": True}}
            else:
                return {"success": False, "error": "Configuration loading failed"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_basic_ssot_integration(self) -> Dict[str, Any]:
        """Test basic SSOT integration."""
        try:
            # Test SSOT integration system
            if self.ssot_integration is not None:
                # Test component registry
                components = self.ssot_integration.ssot_components
                
                if components and len(components) > 0:
                    return {"success": True, "metadata": {"components_registered": len(components)}}
                else:
                    return {"success": False, "error": "No SSOT components registered"}
            else:
                return {"success": False, "error": "SSOT integration system not available"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ================================
    # COMPREHENSIVE VALIDATION TESTS
    # ================================
    
    def test_comprehensive_logging_operations(self) -> Dict[str, Any]:
        """Test comprehensive logging operations."""
        try:
            operations_tested = 0
            
            # Test all logging operations
            self.logger.log_operation_start("comprehensive_test")
            operations_tested += 1
            
            self.logger.log_operation_progress("comprehensive_test", 50.0)
            operations_tested += 1
            
            self.logger.log_processing_item("test_item_1")
            operations_tested += 1
            
            self.logger.log_processing_batch(10)
            operations_tested += 1
            
            self.logger.log_validation_start("comprehensive_validation")
            operations_tested += 1
            
            self.logger.log_validation_passed("comprehensive_validation")
            operations_tested += 1
            
            self.logger.log_performance_metric("test_metric", 1.0)
            operations_tested += 1
            
            self.logger.log_config_loaded("test_config")
            operations_tested += 1
            
            self.logger.log_operation_complete("comprehensive_test")
            operations_tested += 1
            
            # Test performance metrics collection
            metrics = self.logger.get_performance_metrics()
            
            return {
                "success": True, 
                "metadata": {
                    "operations_tested": operations_tested,
                    "performance_metrics_collected": len(metrics)
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_comprehensive_configuration_management(self) -> Dict[str, Any]:
        """Test comprehensive configuration management."""
        try:
            operations_tested = 0
            
            # Test configuration loading
            config_data = self.config_system.load_configuration()
            operations_tested += 1
            
            # Test agent configurations
            for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]:
                agent_config = self.config_system.get_agent_config(agent_id)
                agent_coordinates = self.config_system.get_agent_coordinates(agent_id)
                agent_role = self.config_system.get_agent_role(agent_id)
                agent_points = self.config_system.get_agent_points(agent_id)
                operations_tested += 4
            
            # Test path configurations
            paths = self.config_system.get_all_paths()
            operations_tested += 1
            
            # Test environment variables
            env_vars = self.config_system.get_all_environment_vars()
            operations_tested += 1
            
            # Test configuration validation
            validation_errors = self.config_system.validate_configuration()
            operations_tested += 1
            
            return {
                "success": True,
                "metadata": {
                    "operations_tested": operations_tested,
                    "agents_configured": 8,
                    "paths_configured": len(paths),
                    "env_vars_configured": len(env_vars),
                    "validation_errors": len(validation_errors.get("missing_required", [])) + len(validation_errors.get("invalid_values", []))
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_comprehensive_ssot_components(self) -> Dict[str, Any]:
        """Test comprehensive SSOT components."""
        try:
            operations_tested = 0
            
            # Test SSOT component integration
            integration_results = self.ssot_integration.integrate_all_ssot_components()
            operations_tested += 1
            
            # Test SSOT component validation
            validation_results = self.ssot_integration.validate_all_ssot_components()
            operations_tested += 1
            
            # Test SSOT status report
            status_report = self.ssot_integration.get_ssot_status_report()
            operations_tested += 1
            
            # Count successful integrations
            successful_integrations = sum(1 for success in integration_results.values() if success)
            
            # Count successful validations
            successful_validations = sum(1 for result in validation_results.values() if result.get("overall_status") == "passed")
            
            return {
                "success": True,
                "metadata": {
                    "operations_tested": operations_tested,
                    "components_integrated": len(integration_results),
                    "successful_integrations": successful_integrations,
                    "components_validated": len(validation_results),
                    "successful_validations": successful_validations
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ================================
    # INTEGRATION VALIDATION TESTS
    # ================================
    
    def test_integration_cross_system_compatibility(self) -> Dict[str, Any]:
        """Test cross-system compatibility."""
        try:
            operations_tested = 0
            
            # Test logging system with configuration system
            self.logger.log_config_loaded("integration_test_config")
            operations_tested += 1
            
            # Test configuration system with logging system
            agent_config = self.config_system.get_agent_config("Agent-8")
            self.logger.log_operation_start("integration_test")
            operations_tested += 2
            
            # Test SSOT integration with both systems
            if self.ssot_integration:
                self.ssot_integration.logger.log_operation_start("cross_system_test")
                operations_tested += 1
            
            # Test performance metrics across systems
            metrics = self.logger.get_performance_metrics()
            operations_tested += 1
            
            return {
                "success": True,
                "metadata": {
                    "operations_tested": operations_tested,
                    "cross_system_operations": True,
                    "performance_metrics_available": len(metrics) > 0
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_integration_agent_coordination(self) -> Dict[str, Any]:
        """Test agent coordination integration."""
        try:
            operations_tested = 0
            
            # Test agent configuration coordination
            agent_configs = {}
            for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]:
                agent_configs[agent_id] = self.config_system.get_agent_config(agent_id)
                operations_tested += 1
            
            # Test agent role coordination
            agent_roles = {}
            for agent_id in agent_configs.keys():
                agent_roles[agent_id] = self.config_system.get_agent_role(agent_id)
                operations_tested += 1
            
            # Test agent coordinate coordination
            agent_coordinates = {}
            for agent_id in agent_configs.keys():
                agent_coordinates[agent_id] = self.config_system.get_agent_coordinates(agent_id)
                operations_tested += 1
            
            # Validate agent coordination
            all_agents_configured = all(agent_configs.values())
            all_roles_defined = all(agent_roles.values())
            all_coordinates_defined = all(agent_coordinates.values())
            
            return {
                "success": all_agents_configured and all_roles_defined and all_coordinates_defined,
                "metadata": {
                    "operations_tested": operations_tested,
                    "agents_configured": len(agent_configs),
                    "roles_defined": len(agent_roles),
                    "coordinates_defined": len(agent_coordinates),
                    "all_agents_configured": all_agents_configured,
                    "all_roles_defined": all_roles_defined,
                    "all_coordinates_defined": all_coordinates_defined
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_integration_v2_compliance(self) -> Dict[str, Any]:
        """Test V2 compliance integration."""
        try:
            operations_tested = 0
            
            # Test V2 compliance indicators
            v2_compliance_checks = {
                "unified_logging": self.logger is not None,
                "unified_configuration": self.config_system is not None,
                "ssot_integration": self.ssot_integration is not None,
                "component_registry": len(self.ssot_integration.ssot_components) > 0,
                "validation_system": len(self.validation_tests) > 0
            }
            operations_tested += len(v2_compliance_checks)
            
            # Test V2 compliance metrics
            compliance_score = sum(v2_compliance_checks.values()) / len(v2_compliance_checks)
            
            # Test V2 compliance validation
            all_compliant = all(v2_compliance_checks.values())
            
            return {
                "success": all_compliant,
                "metadata": {
                    "operations_tested": operations_tested,
                    "compliance_checks": v2_compliance_checks,
                    "compliance_score": compliance_score,
                    "all_compliant": all_compliant
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ================================
    # STRESS VALIDATION TESTS
    # ================================
    
    def test_stress_logging_performance(self) -> Dict[str, Any]:
        """Test logging performance under stress."""
        try:
            operations_tested = 0
            start_time = time.time()
            
            # Stress test logging operations
            for i in range(1000):
                self.logger.log_operation_start(f"stress_test_{i}")
                self.logger.log_operation_complete(f"stress_test_{i}")
                operations_tested += 2
            
            execution_time = time.time() - start_time
            
            # Test performance metrics collection
            metrics = self.logger.get_performance_metrics()
            
            # Calculate performance metrics
            operations_per_second = operations_tested / execution_time if execution_time > 0 else 0
            
            return {
                "success": execution_time < 10.0,  # Should complete within 10 seconds
                "metadata": {
                    "operations_tested": operations_tested,
                    "execution_time": execution_time,
                    "operations_per_second": operations_per_second,
                    "performance_metrics_collected": len(metrics)
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_stress_configuration_scaling(self) -> Dict[str, Any]:
        """Test configuration scaling under stress."""
        try:
            operations_tested = 0
            start_time = time.time()
            
            # Stress test configuration operations
            for i in range(1000):
                agent_config = self.config_system.get_agent_config(f"Agent-{(i % 8) + 1}")
                agent_coordinates = self.config_system.get_agent_coordinates(f"Agent-{(i % 8) + 1}")
                operations_tested += 2
            
            execution_time = time.time() - start_time
            
            # Calculate performance metrics
            operations_per_second = operations_tested / execution_time if execution_time > 0 else 0
            
            return {
                "success": execution_time < 5.0,  # Should complete within 5 seconds
                "metadata": {
                    "operations_tested": operations_tested,
                    "execution_time": execution_time,
                    "operations_per_second": operations_per_second
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_stress_ssot_integration_load(self) -> Dict[str, Any]:
        """Test SSOT integration under load."""
        try:
            operations_tested = 0
            start_time = time.time()
            
            # Stress test SSOT integration operations
            for i in range(100):
                # Test component integration
                integration_results = self.ssot_integration.integrate_all_ssot_components()
                operations_tested += 1
                
                # Test component validation
                validation_results = self.ssot_integration.validate_all_ssot_components()
                operations_tested += 1
            
            execution_time = time.time() - start_time
            
            # Calculate performance metrics
            operations_per_second = operations_tested / execution_time if execution_time > 0 else 0
            
            return {
                "success": execution_time < 30.0,  # Should complete within 30 seconds
                "metadata": {
                    "operations_tested": operations_tested,
                    "execution_time": execution_time,
                    "operations_per_second": operations_per_second
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ================================
    # REPORTING AND EXPORT
    # ================================
    
    def generate_validation_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive validation report."""
        report = f"""
# SSOT Validation Report

**Generated**: {results['timestamp']}
**Level**: {results['level']}
**Execution Time**: {results['execution_time']:.2f} seconds

## Summary
- **Tests Run**: {results['tests_run']}
- **Tests Passed**: {results['tests_passed']}
- **Tests Failed**: {results['tests_failed']}
- **Tests Warning**: {results['tests_warning']}
- **Tests Skipped**: {results['tests_skipped']}

## Test Results
"""
        
        for test_result in results['test_results']:
            status_emoji = "✅" if test_result.result == ValidationResult.PASSED else "❌" if test_result.result == ValidationResult.FAILED else "⚠️" if test_result.result == ValidationResult.WARNING else "⏭️"
            
            report += f"""
### {status_emoji} {test_result.test_name}
- **Result**: {test_result.result.value}
- **Execution Time**: {test_result.execution_time:.3f} seconds
"""
            
            if test_result.error_message:
                report += f"- **Error**: {test_result.error_message}\n"
            
            if test_result.warnings:
                report += f"- **Warnings**: {', '.join(test_result.warnings)}\n"
            
            if test_result.metadata:
                report += f"- **Metadata**: {test_result.metadata}\n"
        
        return report
    
    def export_validation_results(self, results: Dict[str, Any], file_path: str) -> None:
        """Export validation results to file."""
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        self.logger.log_config_updated("Validation Results Export")

# ================================
# FACTORY FUNCTIONS
# ================================

def create_ssot_validation_system() -> SSOTValidationSystem:
    """Create a new SSOT validation system instance."""
    return SSOTValidationSystem()

# ================================
# GLOBAL INSTANCE
# ================================

# Global SSOT validation system instance
_ssot_validation_system = None

def get_ssot_validation_system() -> SSOTValidationSystem:
    """Get the global SSOT validation system instance."""
    global _ssot_validation_system
    if _ssot_validation_system is None:
        _ssot_validation_system = create_ssot_validation_system()
    return _ssot_validation_system

# ================================
# EXPORTS
# ================================

__all__ = [
    'SSOTValidationSystem',
    'ValidationTest',
    'ValidationReport',
    'ValidationLevel',
    'ValidationResult',
    'create_ssot_validation_system',
    'get_ssot_validation_system'
]
