#!/usr/bin/env python3
"""Test script to verify refactored performance validation system works correctly"""

import sys
import os

def test_performance_validation_refactoring():
    """Test that the refactored performance validation system works correctly"""
    print("🧪 Testing Performance Validation System Refactoring")
    print("=" * 60)
    
    try:
        # Test import from new modular structure
        from src.core.performance_validation import (
            BenchmarkType,
            PerformanceLevel,
            OptimizationTarget,
            PerformanceBenchmark,
            SystemPerformanceReport,
            PerformanceValidationSystem
        )
        print("✅ Successfully imported all performance validation components")
        
        # Test that we can create instances
        print("\n🔧 Testing Component Instantiation...")
        
        # Test enums
        benchmark_type = BenchmarkType.RESPONSE_TIME
        performance_level = PerformanceLevel.PRODUCTION_READY
        optimization_target = OptimizationTarget.RESPONSE_TIME_IMPROVEMENT
        
        print(f"✅ Enums: {benchmark_type.value}, {performance_level.value}, {optimization_target.value}")
        
        # Test data models
        benchmark = PerformanceBenchmark(
            benchmark_id="test-001",
            benchmark_type=BenchmarkType.RESPONSE_TIME,
            test_name="API Response Test",
            start_time="2025-08-23T19:00:00",
            end_time="2025-08-23T19:00:01",
            duration=1.0,
            metrics={"response_time": 150.0},
            target_metrics={"response_time": 100.0},
            performance_level=PerformanceLevel.DEVELOPMENT_READY,
            optimization_recommendations=["Reduce response time to meet 100ms target"]
        )
        print(f"✅ Benchmark created: {benchmark.test_name} with {len(benchmark.metrics)} metrics")
        
        # Test performance validation system
        validation_system = PerformanceValidationSystem()
        print(f"✅ Validation system created: {type(validation_system)}")
        
        # Test benchmark execution
        test_metrics = {"response_time": 120.0}
        result = validation_system.run_benchmark(
            BenchmarkType.RESPONSE_TIME, 
            "Test Response Time", 
            test_metrics
        )
        print(f"✅ Benchmark executed: {result.benchmark_id} with level {result.performance_level.value}")
        
        # Test report generation
        report = validation_system.generate_performance_report([result.benchmark_id])
        print(f"✅ Report generated: {report.report_id} with {len(report.benchmark_results)} benchmarks")
        
        print("\n🎉 All performance validation system components working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Performance validation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_old_monolith_removed():
    """Test that the old monolith file is no longer needed"""
    print("\n🗑️  Testing Old Monolith Removal")
    print("=" * 50)
    
    old_file = "src/core/performance_validation_system.py"
    if os.path.exists(old_file):
        print(f"⚠️  Old monolith still exists: {old_file}")
        print("   This file should be deleted after confirming new structure works")
        return False
    else:
        print("✅ Old monolith file has been removed")
        return True

def main():
    """Main test function"""
    print("🚀 Performance Validation System Refactoring Test")
    print("=" * 70)
    
    # Test 1: New modular imports
    imports_work = test_performance_validation_refactoring()
    
    # Test 2: Old monolith status
    monolith_removed = test_old_monolith_removed()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 PERFORMANCE VALIDATION REFACTORING TEST RESULTS")
    print("=" * 70)
    print(f"New Modular Imports: {'✅ PASS' if imports_work else '❌ FAIL'}")
    print(f"Old Monolith Status: {'✅ REMOVED' if monolith_removed else '⚠️  STILL EXISTS'}")
    
    if imports_work:
        print("\n🎉 Performance validation system refactoring is COMPLETE and working!")
        print("\n📋 Status:")
        print("✅ All components imported from new modular structure")
        print("✅ All classes instantiate correctly")
        print("✅ Benchmark execution working")
        print("✅ Report generation working")
        if not monolith_removed:
            print("⚠️  Old monolith file can now be safely deleted")
    else:
        print("\n❌ Some tests failed. Please review the issues above.")
    
    return imports_work

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
