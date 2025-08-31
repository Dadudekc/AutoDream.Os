"""
🧪 Simple QA Framework Test
Agent-7 - Quality Completion Optimization Manager

Basic functionality test for the QA framework.
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_core_components():
    """Test core framework components."""
    print("🧪 QA Framework Core Components Test")
    print("=" * 40)
    
    test_results = {
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "overall_status": "PENDING"
    }
    
    try:
        # Test 1: Import core tools
        print("\n📋 Test 1: Import Core Tools")
        test_results["tests_run"] += 1
        
        try:
            from tools.coverage_analyzer import TestCoverageAnalyzer
            from tools.complexity_analyzer import CodeComplexityAnalyzer
            from tools.dependency_analyzer import DependencyAnalyzer
            print("✅ All core tools imported successfully")
            test_results["tests_passed"] += 1
        except ImportError as e:
            print(f"❌ Import failed: {e}")
            test_results["tests_failed"] += 1
        
        # Test 2: Initialize analyzers
        print("\n📋 Test 2: Initialize Analyzers")
        test_results["tests_run"] += 1
        
        try:
            coverage_analyzer = TestCoverageAnalyzer()
            complexity_analyzer = CodeComplexityAnalyzer()
            dependency_analyzer = DependencyAnalyzer()
            print("✅ All analyzers initialized successfully")
            test_results["tests_passed"] += 1
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            test_results["tests_failed"] += 1
        
        # Test 3: Test directory analysis
        print("\n📋 Test 3: Directory Analysis")
        test_results["tests_run"] += 1
        
        test_dir = str(Path(__file__).parent.parent.parent.parent / "testing")
        
        if os.path.exists(test_dir):
            print(f"✅ Test directory found: {test_dir}")
            
            try:
                # Test coverage analysis
                coverage_results = coverage_analyzer.analyze_coverage(test_dir)
                print(f"✅ Coverage analysis: {len(coverage_results)} metrics")
                
                # Test complexity analysis
                complexity_results = complexity_analyzer.analyze_complexity(test_dir)
                print(f"✅ Complexity analysis: {len(complexity_results)} metrics")
                
                # Test dependency analysis
                dependency_results = dependency_analyzer.analyze_dependencies(test_dir)
                print(f"✅ Dependency analysis: {len(dependency_results)} metrics")
                
                test_results["tests_passed"] += 1
            except Exception as e:
                print(f"❌ Analysis failed: {e}")
                test_results["tests_failed"] += 1
        else:
            print(f"⚠️ Test directory not found: {test_dir}")
            test_results["tests_failed"] += 1
        
        # Test 4: V2 Compliance Check
        print("\n📋 Test 4: V2 Compliance Validation")
        test_results["tests_run"] += 1
        
        compliance_score = 0
        total_files = 0
        
        # Check line count compliance for all framework files
        framework_dir = Path(__file__).parent
        for py_file in framework_dir.rglob("*.py"):
            if py_file.name not in ["__init__.py", "simple_test.py"]:
                total_files += 1
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        line_count = len(f.readlines())
                        if line_count <= 300:
                            compliance_score += 1
                        else:
                            print(f"⚠️ File exceeds V2 standard: {py_file.name} ({line_count} lines)")
                except Exception as e:
                    print(f"⚠️ Error reading {py_file.name}: {e}")
        
        if total_files > 0:
            compliance_percentage = (compliance_score / total_files) * 100
            print(f"✅ V2 Compliance: {compliance_percentage:.1f}% ({compliance_score}/{total_files} files)")
            
            if compliance_percentage >= 95:
                test_results["tests_passed"] += 1
            else:
                test_results["tests_failed"] += 1
        
        # Calculate overall status
        if test_results["tests_run"] > 0:
            success_rate = (test_results["tests_passed"] / test_results["tests_run"]) * 100
            
            if test_results["tests_failed"] == 0:
                test_results["overall_status"] = "PASSED"
            elif success_rate >= 75:
                test_results["overall_status"] = "PARTIAL"
            else:
                test_results["overall_status"] = "FAILED"
        
        # Print final results
        print("\n" + "=" * 40)
        print("📊 TEST RESULTS")
        print("=" * 40)
        print(f"Tests Run: {test_results['tests_run']}")
        print(f"Tests Passed: {test_results['tests_passed']}")
        print(f"Tests Failed: {test_results['tests_failed']}")
        print(f"Overall Status: {test_results['overall_status']}")
        
        return test_results
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        test_results["overall_status"] = "ERROR"
        test_results["error"] = str(e)
        return test_results


if __name__ == "__main__":
    test_core_components()
