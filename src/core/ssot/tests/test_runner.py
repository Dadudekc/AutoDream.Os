from ..core.unified_entry_point_system import main
#!/usr/bin/env python3
"""
SSOT System Test Runner

Comprehensive test runner for all SSOT system tests.
Provides unified test execution, reporting, and performance monitoring.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Version: 1.0.0
License: MIT
"""




class SSOTTestRunner:
    """Comprehensive test runner for SSOT system tests."""
    
    def __init__(self):
        self.test_results = {}
        self.performance_metrics = {}
        self.start_time = None
        self.end_time = None
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all SSOT system tests."""
        get_logger(__name__).info("🚀 Starting SSOT System Test Suite")
        get_logger(__name__).info("=" * 50)
        
        self.start_time = time.time()
        
        # Test modules to run
        test_modules = [
            "test_execution_coordinator",
            "test_validation_system", 
            "test_integration",
        ]
        
        results = {}
        
        for module in test_modules:
            get_logger(__name__).info(f"\n📋 Running {module} tests...")
            module_start = time.time()
            
            try:
                # Run tests for this module
                result = await self._run_test_module(module)
                results[module] = result
                
                module_time = time.time() - module_start
                get_logger(__name__).info(f"✅ {module} completed in {module_time:.2f}s")
                
            except Exception as e:
                get_logger(__name__).info(f"❌ {module} failed: {e}")
                results[module] = {
                    "status": "failed",
                    "error": str(e),
                    "execution_time": time.time() - module_start,
                }
        
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        
        # Generate summary
        summary = self._generate_test_summary(results, total_time)
        
        get_logger(__name__).info("\n" + "=" * 50)
        get_logger(__name__).info("📊 Test Summary")
        get_logger(__name__).info("=" * 50)
        get_logger(__name__).info(f"Total execution time: {total_time:.2f}s")
        get_logger(__name__).info(f"Modules tested: {len(test_modules)}")
        get_logger(__name__).info(f"Overall status: {summary['overall_status']}")
        
        return {
            "summary": summary,
            "results": results,
            "performance_metrics": self.performance_metrics,
        }
    
    async def _run_test_module(self, module_name: str) -> Dict[str, Any]:
        """Run tests for a specific module."""
        # Import the test module
        test_module = __import__(f"tests.{module_name}", fromlist=[module_name])
        
        # Get test classes
        test_classes = [
            get_unified_validator().safe_getattr(test_module, attr)
            for attr in dir(test_module)
            if attr.startswith("Test") and get_unified_validator().validate_hasattr(get_unified_validator().safe_getattr(test_module, attr), "__bases__")
        ]
        
        results = {
            "module": module_name,
            "test_classes": len(test_classes),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "execution_time": 0,
            "status": "passed",
        }
        
        start_time = time.time()
        
        for test_class in test_classes:
            get_logger(__name__).info(f"  🔍 Running {test_class.__name__}...")
            
            try:
                # Run tests for this class
                class_results = await self._run_test_class(test_class)
                results["tests_run"] += class_results["tests_run"]
                results["tests_passed"] += class_results["tests_passed"]
                results["tests_failed"] += class_results["tests_failed"]
                
                if class_results["tests_failed"] > 0:
                    results["status"] = "failed"
                
            except Exception as e:
                get_logger(__name__).info(f"    ❌ {test_class.__name__} failed: {e}")
                results["status"] = "failed"
                results["error"] = str(e)
        
        results["execution_time"] = time.time() - start_time
        
        return results
    
    async def _run_test_class(self, test_class) -> Dict[str, Any]:
        """Run tests for a specific test class."""
        results = {
            "class_name": test_class.__name__,
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
        }
        
        # Get test methods
        test_methods = [
            method for method in dir(test_class)
            if method.startswith("test_") and callable(get_unified_validator().safe_getattr(test_class, method))
        ]
        
        for method_name in test_methods:
            results["tests_run"] += 1
            
            try:
                # Create test instance
                test_instance = test_class()
                
                # Run the test method
                method = get_unified_validator().safe_getattr(test_instance, method_name)
                
                if asyncio.iscoroutinefunction(method):
                    await method()
                else:
                    method()
                
                results["tests_passed"] += 1
                get_logger(__name__).info(f"    ✅ {method_name}")
                
            except Exception as e:
                results["tests_failed"] += 1
                get_logger(__name__).info(f"    ❌ {method_name}: {e}")
        
        return results
    
    def _generate_test_summary(self, results: Dict[str, Any], total_time: float) -> Dict[str, Any]:
        """Generate test summary."""
        total_tests = sum(r.get("tests_run", 0) for r in results.values())
        total_passed = sum(r.get("tests_passed", 0) for r in results.values())
        total_failed = sum(r.get("tests_failed", 0) for r in results.values())
        
        overall_status = "passed" if total_failed == 0 else "failed"
        
        return {
            "overall_status": overall_status,
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0,
            "total_execution_time": total_time,
            "modules_tested": len(results),
        }
    
    async def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance-specific tests."""
        get_logger(__name__).info("\n🏃 Running Performance Tests")
        get_logger(__name__).info("=" * 30)
        
        performance_results = {}
        
        # Test execution coordinator performance
        get_logger(__name__).info("Testing execution coordinator performance...")
        start_time = time.time()
        
        try:
            perf_test = TestSSOTExecutionCoordinatorPerformance()
            
            # Run performance tests
            await perf_test.test_large_task_set_performance()
            
            performance_results["execution_coordinator"] = {
                "status": "passed",
                "execution_time": time.time() - start_time,
            }
            get_logger(__name__).info("✅ Execution coordinator performance tests passed")
            
        except Exception as e:
            performance_results["execution_coordinator"] = {
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time,
            }
            get_logger(__name__).info(f"❌ Execution coordinator performance tests failed: {e}")
        
        # Test validation system performance
        get_logger(__name__).info("Testing validation system performance...")
        start_time = time.time()
        
        try:
            perf_test = TestSSOTValidationSystemPerformance()
            
            # Run performance tests
            await perf_test.test_large_validation_suite_performance()
            await perf_test.test_memory_usage_validation()
            
            performance_results["validation_system"] = {
                "status": "passed",
                "execution_time": time.time() - start_time,
            }
            get_logger(__name__).info("✅ Validation system performance tests passed")
            
        except Exception as e:
            performance_results["validation_system"] = {
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time,
            }
            get_logger(__name__).info(f"❌ Validation system performance tests failed: {e}")
        
        return performance_results
    
    def generate_report(self, test_results: Dict[str, Any]) -> str:
        """Generate a comprehensive test report."""
        report = []
        report.append("# SSOT System Test Report")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")
        
        # Summary
        summary = test_results["summary"]
        report.append("## Summary")
        report.append(f"- **Overall Status**: {summary['overall_status']}")
        report.append(f"- **Total Tests**: {summary['total_tests']}")
        report.append(f"- **Passed**: {summary['total_passed']}")
        report.append(f"- **Failed**: {summary['total_failed']}")
        report.append(f"- **Success Rate**: {summary['success_rate']:.1f}%")
        report.append(f"- **Total Execution Time**: {summary['total_execution_time']:.2f}s")
        report.append("")
        
        # Module Results
        report.append("## Module Results")
        for module, result in test_results["results"].items():
            status_emoji = "✅" if result["status"] == "passed" else "❌"
            report.append(f"### {module}")
            report.append(f"- **Status**: {status_emoji} {result['status']}")
            report.append(f"- **Tests Run**: {result.get('tests_run', 0)}")
            report.append(f"- **Passed**: {result.get('tests_passed', 0)}")
            report.append(f"- **Failed**: {result.get('tests_failed', 0)}")
            report.append(f"- **Execution Time**: {result.get('execution_time', 0):.2f}s")
            
            if "error" in result:
                report.append(f"- **Error**: {result['error']}")
            report.append("")
        
        return "\n".join(report)


async 
if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
