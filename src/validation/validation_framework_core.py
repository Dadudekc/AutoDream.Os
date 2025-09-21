#!/usr/bin/env python3
"""
V3 Validation Framework Core
============================

Core validation framework that orchestrates all V3 validation tests.
V2 Compliance: ≤200 lines, modular design, single responsibility.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from .v3_directives_validator import V3DirectivesValidator
from .quality_gates_validator import QualityGatesValidator
from .contract_system_validator import ContractSystemValidator
from .integration_validator import IntegrationValidator
from .performance_validator import PerformanceValidator
from .security_validator import SecurityValidator
from .documentation_validator import DocumentationValidator


class V3ValidationFrameworkCore:
    """Core V3 validation framework orchestrator."""
    
    def __init__(self):
        self.agent_workspaces = Path("agent_workspaces")
        self.validation_results = {}
        
        # Initialize validators
        self.validators = {
            "v3_directives": V3DirectivesValidator(self.agent_workspaces),
            "quality_gates": QualityGatesValidator(),
            "contract_system": ContractSystemValidator(self.agent_workspaces),
            "integration": IntegrationValidator(),
            "performance": PerformanceValidator(),
            "security": SecurityValidator(),
            "documentation": DocumentationValidator()
        }
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run full V3 validation suite."""
        print("🚀 Starting V3 Validation Testing Framework")
        print("=" * 60)
        
        validation_results = {}
        
        # Run all validation tests
        for validator_name, validator in self.validators.items():
            try:
                result = validator.validate()
                validation_results[result["category"]] = result
                print(f"{'✅' if result['status'] == 'PASSED' else '❌'} {result['category']}: {result['summary']}")
            except Exception as e:
                print(f"❌ {validator_name}: Failed with error - {e}")
                validation_results[validator_name] = {
                    "status": "FAILED",
                    "error": str(e)
                }
        
        # Calculate overall status
        passed_tests = sum(1 for result in validation_results.values() 
                          if result.get("status") == "PASSED")
        total_tests = len(validation_results)
        overall_passed = passed_tests == total_tests
        
        print("\n" + "=" * 60)
        print(f"📊 VALIDATION SUMMARY: {passed_tests}/{total_tests} tests passed")
        print(f"🎯 OVERALL STATUS: {'PASSED' if overall_passed else 'FAILED'}")
        
        if overall_passed:
            print("🎉 V3 VALIDATION: READY FOR BETA RELEASE!")
        else:
            print("⚠️ V3 VALIDATION: ISSUES DETECTED - REVIEW REQUIRED")
        
        # Save validation results
        self._save_validation_results(validation_results, overall_passed)
        
        return {
            "overall_status": "PASSED" if overall_passed else "FAILED",
            "passed_tests": passed_tests,
            "total_tests": total_tests,
            "results": validation_results
        }
    
    def _save_validation_results(self, results: Dict[str, Any], overall_passed: bool):
        """Save validation results to file."""
        validation_report = {
            "validation_date": datetime.now().isoformat(),
            "overall_status": "PASSED" if overall_passed else "FAILED",
            "results": results
        }
        
        report_file = Path("V3_VALIDATION_REPORT.json")
        with open(report_file, 'w') as f:
            json.dump(validation_report, f, indent=2)
        
        print(f"📄 Validation report saved to: {report_file}")
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary without running full tests."""
        return {
            "available_validators": list(self.validators.keys()),
            "agent_workspaces": str(self.agent_workspaces),
            "validation_categories": [
                "v3_directives_deployment",
                "quality_gates_functionality", 
                "contract_system_validation",
                "component_integration",
                "performance_benchmarks",
                "security_validation",
                "documentation_completeness"
            ]
        }
