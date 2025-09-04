#!/usr/bin/env python3
"""
Core Test Runner - Gaming Test Runner
===================================

Core testing functionality for the gaming test runner system.

Author: Agent-3 - Infrastructure & DevOps Specialist (Refactored for V2 Compliance)
License: MIT
"""


# Add paths for imports
sys.path.append(get_unified_utility().path.join(get_unified_utility().path.dirname(__file__), '..'))

# Django setup for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.django_settings')

try:
    django.setup()
except ImportError:
    # Django not available, use mocks
    pass

# Try to import test models, use mocks if not available
try:
except ImportError:
    # Create mock classes
    TestResult = Mock
    TestSuite = Mock
    TestStatus = Mock
    TestType = Mock

# Try to import test functions, use mocks if not available
try:
    from tests.utils.test_functions import GamingTestFunctions, GamingTestHandlers
except ImportError:
    # Create mock classes
    GamingTestFunctions = Mock
    GamingTestHandlers = Mock

logger = logging.getLogger(__name__)


class GamingTestRunnerCore:
    """
    Core test runner for gaming and entertainment systems.
    
    Provides automated testing capabilities including unit tests, integration
    tests, performance tests, and stress testing for gaming systems.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the gaming test runner."""
        self.config = config or {}
        self.test_results: Dict[str, TestResult] = {}
        self.test_suites: Dict[str, TestSuite] = {}
        self.running_tests: Dict[str, TestResult] = {}
        self.test_handlers: Dict[str, Callable] = {}
        self.performance_baselines: Dict[str, Dict[str, Any]] = {}
        self._initialize_test_runner()
    
    def _initialize_test_runner(self):
        """Initialize the test runner system."""
        get_logger(__name__).info("Initializing Gaming Test Runner")
        self._setup_default_test_handlers()
        self._load_performance_baselines()
        self._register_default_test_suites()
    
    def _setup_default_test_handlers(self):
        """Setup default test handlers."""
        self.test_handlers = {
            "unit_test": GamingTestHandlers.run_unit_test,
            "integration_test": GamingTestHandlers.run_integration_test,
            "performance_test": GamingTestHandlers.run_performance_test,
            "stress_test": GamingTestHandlers.run_stress_test,
            "compatibility_test": GamingTestHandlers.run_compatibility_test,
            "user_acceptance_test": GamingTestHandlers.run_user_acceptance_test
        }
    
    def _load_performance_baselines(self):
        """Load performance baselines."""
        self.performance_baselines = {
            "fps": {"min": 30, "target": 60, "excellent": 120},
            "memory_usage": {"max": 80, "target": 50, "excellent": 30},
            "cpu_usage": {"max": 90, "target": 60, "excellent": 40},
            "response_time": {"max": 100, "target": 50, "excellent": 20}
        }
    
    def _register_default_test_suites(self):
        """Register default test suites."""
        default_suites = {
            "unit_tests": TestSuite(
                suite_id="unit_tests",
                suite_name="Unit Tests",
                description="Basic unit tests for gaming components",
                tests=["session_creation", "performance_monitoring", "alert_handling"],
                dependencies=[],
                timeout=30,
                metadata={"category": "unit"}
            ),
            "performance_tests": TestSuite(
                suite_id="performance_tests",
                suite_name="Performance Tests",
                description="Performance and stress testing",
                tests=["fps_test", "memory_test", "cpu_test", "stress_test"],
                dependencies=["unit_tests"],
                timeout=120,
                metadata={"category": "performance"}
            ),
            "integration_tests": TestSuite(
                suite_id="integration_tests",
                suite_name="Integration Tests",
                description="Integration testing for external systems",
                tests=["api_integration", "database_integration", "network_integration"],
                dependencies=["unit_tests"],
                timeout=60,
                metadata={"category": "integration"}
            )
        }
        
        for suite_id, suite in default_suites.items():
            self.test_suites[suite_id] = suite
    
    async def run_test(self, test_id: str, test_data: Optional[Dict[str, Any]] = None) -> TestResult:
        """
        Run a single test.
        
        Args:
            test_id: Unique identifier for the test
            test_data: Optional test configuration data
            
        Returns:
            TestResult object with test execution results
        """
        test_data = test_data or {}
        test_name = test_data.get("name", test_id)
        test_type = TestType(test_data.get("type", "unit"))
        
        # Create test result
        test_result = TestResult(
            test_id=test_id,
            test_name=test_name,
            test_type=test_type,
            status=TestStatus.RUNNING,
            start_time=datetime.now(),
            end_time=None,
            duration=None,
            error_message=None,
            performance_metrics={},
            metadata=test_data.get("metadata", {})
        )
        
        self.running_tests[test_id] = test_result
        
        try:
            # Get test function
            test_func = self._get_default_test_function(test_id)
            
            # Execute test
            execution_result = await self._execute_test(test_func, test_result)
            
            # Update test result
            test_result.end_time = datetime.now()
            test_result.duration = (test_result.end_time - test_result.start_time).total_seconds()
            
            if execution_result["success"]:
                test_result.status = TestStatus.PASSED
                test_result.performance_metrics = execution_result.get("metrics", {})
            else:
                test_result.status = TestStatus.FAILED
                test_result.error_message = execution_result.get("error", "Unknown error")
                
        except Exception as e:
            test_result.status = TestStatus.ERROR
            test_result.error_message = str(e)
            test_result.end_time = datetime.now()
            test_result.duration = (test_result.end_time - test_result.start_time).total_seconds()
        
        # Store result and remove from running
        self.test_results[test_id] = test_result
        del self.running_tests[test_id]
        
        return test_result
    
    async def run_test_suite(self, suite_id: str) -> List[TestResult]:
        """
        Run a complete test suite.
        
        Args:
            suite_id: ID of the test suite to run
            
        Returns:
            List of TestResult objects
        """
        if suite_id not in self.test_suites:
            get_unified_validator().raise_validation_error(f"Test suite {suite_id} not found")
        
        suite = self.test_suites[suite_id]
        results = []
        
        get_logger(__name__).info(f"Running test suite: {suite.suite_name}")
        
        for test_id in suite.tests:
            test_result = await self.run_test(test_id)
            results.append(test_result)
        
        return results
    
    async def _execute_test(self, test_func: Callable, test_result: TestResult) -> Dict[str, Any]:
        """Execute a test function."""
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                # Run in thread pool for synchronous functions
                loop = asyncio.get_event_loop()
                with ThreadPoolExecutor() as executor:
                    result = await loop.run_in_executor(executor, test_func)
            
            return {"success": True, "result": result, "metrics": {}}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_default_test_function(self, test_name: str) -> Callable:
        """Get default test function for common test names."""
        default_tests = {
            "session_creation": GamingTestFunctions.test_session_creation,
            "performance_monitoring": GamingTestFunctions.test_performance_monitoring,
            "alert_handling": GamingTestFunctions.test_alert_handling,
            "fps_test": GamingTestFunctions.test_fps_performance,
            "memory_test": GamingTestFunctions.test_memory_usage,
            "cpu_test": GamingTestFunctions.test_cpu_usage,
            "stress_test": GamingTestFunctions.test_stress_conditions,
            "api_integration": GamingTestFunctions.test_api_integration,
            "database_integration": GamingTestFunctions.test_database_integration,
            "network_integration": GamingTestFunctions.test_network_integration
        }
        
        return default_tests.get(test_name, GamingTestFunctions.test_placeholder)
    
    def get_test_results(self, test_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get test results.
        
        Args:
            test_id: Optional specific test ID
            
        Returns:
            Test results summary
        """
        if test_id:
            if test_id not in self.test_results:
                return {"error": f"Test {test_id} not found"}
            return asdict(self.test_results[test_id])
        
        # Return summary of all tests
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results.values() if r.status == TestStatus.PASSED])
        failed_tests = len([r for r in self.test_results.values() if r.status == TestStatus.FAILED])
        error_tests = len([r for r in self.test_results.values() if r.status == TestStatus.ERROR])
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "error_tests": error_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "results": [asdict(result) for result in self.test_results.values()]
        }
    
    def export_test_results(self, filepath: str) -> bool:
        """
        Export test results to JSON file.
        
        Args:
            filepath: Path to export file
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            export_data = {
                "test_results": self.get_test_results(),
                "test_suites": {
                    suite_id: asdict(suite) for suite_id, suite in self.test_suites.items()
                },
                "performance_baselines": self.performance_baselines,
                "export_timestamp": datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                write_json(export_data, f, indent=2, default=str)
            
            get_logger(__name__).info(f"Exported test results to {filepath}")
            return True
        except Exception as e:
            get_logger(__name__).error(f"Failed to export test results: {e}")
            return False
