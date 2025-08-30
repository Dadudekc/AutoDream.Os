"""
🧪 QA FRAMEWORK INTEGRATION TEST
Agent-7 - Quality Completion Optimization Manager

Comprehensive integration testing for the QA framework.
Tests all components working together as a unified system.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from tools.coverage_analyzer import TestCoverageAnalyzer
from tools.complexity_analyzer import CodeComplexityAnalyzer
from tools.dependency_analyzer import DependencyAnalyzer
from reports.quality_reports import QualityReportGenerator
from reports.compliance_reports import ComplianceReportGenerator


def test_framework_integration():
    """Test complete QA framework integration."""
    print("🧪 QA Framework Integration Test Started")
    print("=" * 50)
    
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "integration_score": 0.0,
        "component_tests": {},
        "overall_status": "PENDING"
    }
    
    try:
        # Test 1: Component Import and Initialization
        print("\n📋 Test 1: Component Import and Initialization")
        test_results["tests_run"] += 1
        
        coverage_analyzer = TestCoverageAnalyzer()
        complexity_analyzer = CodeComplexityAnalyzer()
        dependency_analyzer = DependencyAnalyzer()
        
        print("✅ All core tools imported successfully")
        test_results["tests_passed"] += 1
        test_results["component_tests"]["core_tools"] = "PASSED"
        
        # Test 2: Reporting System Integration
        print("\n📋 Test 2: Reporting System Integration")
        test_results["tests_run"] += 1
        
        quality_reporter = QualityReportGenerator()
        compliance_reporter = ComplianceReportGenerator()
        
        print("✅ All reporting components initialized successfully")
        test_results["tests_passed"] += 1
        test_results["component_tests"]["reporting_system"] = "PASSED"
        
        # Test 3: Framework Interoperability
        print("\n📋 Test 3: Framework Interoperability")
        test_results["tests_run"] += 1
        
        # Test that all components can work together
        test_dir = str(Path(__file__).parent.parent.parent.parent / "testing")
        
        if os.path.exists(test_dir):
            print(f"✅ Test directory found: {test_dir}")
            
            # Test coverage analysis
            coverage_results = coverage_analyzer.analyze_coverage(test_dir)
            print(f"✅ Coverage analysis completed: {len(coverage_results)} metrics")
            
            # Test complexity analysis
            complexity_results = complexity_analyzer.analyze_complexity(test_dir)
            print(f"✅ Complexity analysis completed: {len(complexity_results)} metrics")
            
            # Test dependency analysis
            dependency_results = dependency_analyzer.analyze_dependencies(test_dir)
            print(f"✅ Dependency analysis completed: {len(dependency_results)} metrics")
            
            test_results["tests_passed"] += 1
            test_results["component_tests"]["interoperability"] = "PASSED"
        else:
            print(f"⚠️ Test directory not found: {test_dir}")
            test_results["tests_failed"] += 1
            test_results["component_tests"]["interoperability"] = "FAILED"
        
        # Test 4: Report Generation
        print("\n📋 Test 4: Report Generation")
        test_results["tests_run"] += 1
        
        try:
            # Generate quality report
            quality_report = quality_reporter.generate_quality_report(test_dir)
            print(f"✅ Quality report generated: {quality_report.report_id}")
            
            # Generate compliance report
            compliance_report = compliance_reporter.generate_compliance_report(test_dir)
            print(f"✅ Compliance report generated: {compliance_report.report_id}")
            
            test_results["tests_passed"] += 1
            test_results["component_tests"]["report_generation"] = "PASSED"
        except Exception as e:
            print(f"❌ Report generation failed: {e}")
            test_results["tests_failed"] += 1
            test_results["component_tests"]["report_generation"] = "FAILED"
        
        # Test 5: V2 Compliance Validation
        print("\n📋 Test 5: V2 Compliance Validation")
        test_results["tests_run"] += 1
        
        compliance_score = 0
        total_files = 0
        
        # Check line count compliance for all framework files
        framework_dir = Path(__file__).parent
        for py_file in framework_dir.rglob("*.py"):
            if py_file.name != "__init__.py":
                total_files += 1
                with open(py_file, 'r', encoding='utf-8') as f:
                    line_count = len(f.readlines())
                    if line_count <= 300:
                        compliance_score += 1
                    else:
                        print(f"⚠️ File exceeds V2 standard: {py_file.name} ({line_count} lines)")
        
        if total_files > 0:
            compliance_percentage = (compliance_score / total_files) * 100
            print(f"✅ V2 Compliance: {compliance_percentage:.1f}% ({compliance_score}/{total_files} files)")
            
            if compliance_percentage >= 95:
                test_results["tests_passed"] += 1
                test_results["component_tests"]["v2_compliance"] = "PASSED"
            else:
                test_results["tests_failed"] += 1
                test_results["component_tests"]["v2_compliance"] = "FAILED"
        
        # Calculate overall integration score
        if test_results["tests_run"] > 0:
            test_results["integration_score"] = (test_results["tests_passed"] / test_results["tests_run"]) * 100
        
        # Determine overall status
        if test_results["tests_failed"] == 0:
            test_results["overall_status"] = "PASSED"
        elif test_results["tests_passed"] > test_results["tests_failed"]:
            test_results["overall_status"] = "PARTIAL"
        else:
            test_results["overall_status"] = "FAILED"
        
        # Print final results
        print("\n" + "=" * 50)
        print("📊 INTEGRATION TEST RESULTS")
        print("=" * 50)
        print(f"Tests Run: {test_results['tests_run']}")
        print(f"Tests Passed: {test_results['tests_passed']}")
        print(f"Tests Failed: {test_results['tests_failed']}")
        print(f"Integration Score: {test_results['integration_score']:.1f}%")
        print(f"Overall Status: {test_results['overall_status']}")
        
        # Save test results
        results_file = Path(__file__).parent / "integration_test_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, default=str)
        
        print(f"\n💾 Test results saved to: {results_file}")
        
        return test_results
        
    except Exception as e:
        print(f"❌ Integration test failed with error: {e}")
        test_results["overall_status"] = "ERROR"
        test_results["error"] = str(e)
        return test_results


if __name__ == "__main__":
    test_framework_integration()
