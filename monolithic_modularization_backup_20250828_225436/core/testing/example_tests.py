"""
Example Tests for Consolidated Testing Framework
===============================================

Demonstrates how to use the new unified testing framework
with various test types and scenarios.
"""

from src.core.testing.testing_utils import (
    BaseTest,
    BaseIntegrationTest,
    TestType,
    TestPriority,
    TestEnvironment,
)


class ExampleUnitTest(BaseTest):
    """Example unit test demonstrating basic functionality"""

    def __init__(self):
        super().__init__(test_name="Example Unit Test")
        self.test_type = TestType.UNIT
        self.priority = TestPriority.NORMAL

    def test_logic(self) -> bool:
        """Simple test logic that always passes"""
        # Simulate some test logic
        result = 2 + 2 == 4
        return result


class ExampleIntegrationTest(BaseIntegrationTest):
    """Example integration test demonstrating component interaction"""

    def __init__(self):
        super().__init__(test_name="Example Integration Test")
        self.test_type = TestType.INTEGRATION
        self.priority = TestPriority.HIGH

        # Add dependencies
        self.add_dependency("database_connection")
        self.add_dependency("api_service")

    def test_logic(self) -> bool:
        """Test logic that simulates integration testing"""
        # Simulate integration test logic
        try:
            # Mock integration test
            component_a_working = True
            component_b_working = True
            interaction_working = component_a_working and component_b_working

            return interaction_working
        except Exception:
            return False

    def setup(self) -> None:
        """Setup integration test environment"""
        super().setup()
        print("🔧 Setting up integration test environment...")

    def teardown(self) -> None:
        """Cleanup integration test environment"""
        print("🧹 Cleaning up integration test environment...")
        super().teardown()


class ExamplePerformanceTest(BaseTest):
    """Example performance test demonstrating timing and metrics"""

    def __init__(self):
        super().__init__(test_name="Example Performance Test")
        self.test_type = TestType.PERFORMANCE
        self.priority = TestPriority.HIGH

    def test_logic(self) -> bool:
        """Test logic that simulates performance testing"""
        import time

        # Simulate performance test
        start_time = time.time()

        # Simulate some work
        time.sleep(0.1)  # Simulate 100ms of work

        end_time = time.time()
        execution_time = end_time - start_time

        # Performance assertion: should complete within 200ms
        return execution_time < 0.2


class ExampleSmokeTest(BaseTest):
    """Example smoke test for basic functionality verification"""

    def __init__(self):
        super().__init__(test_name="Example Smoke Test")
        self.test_type = TestType.SMOKE
        self.priority = TestPriority.CRITICAL

    def test_logic(self) -> bool:
        """Basic smoke test logic"""
        # Simulate smoke test - basic functionality check
        basic_functionality_working = True
        core_components_accessible = True

        return basic_functionality_working and core_components_accessible


class ExampleSecurityTest(BaseTest):
    """Example security test demonstrating security validation"""

    def __init__(self):
        super().__init__(test_name="Example Security Test")
        self.test_type = TestType.SECURITY
        self.priority = TestPriority.HIGH

    def test_logic(self) -> bool:
        """Security test logic"""
        # Simulate security checks
        authentication_working = True
        authorization_working = True
        input_validation_working = True

        return (
            authentication_working
            and authorization_working
            and input_validation_working
        )


def create_example_test_suite():
    """Create a suite of example tests for demonstration"""
    tests = [
        ExampleUnitTest(),
        ExampleIntegrationTest(),
        ExamplePerformanceTest(),
        ExampleSmokeTest(),
        ExampleSecurityTest(),
    ]

    return tests


def run_example_tests():
    """Run all example tests and display results"""
    from src.core.testing.testing_orchestrator import TestOrchestrator

    print("🧪 RUNNING EXAMPLE TEST SUITE")
    print("=" * 50)

    # Create orchestrator
    orchestrator = TestOrchestrator()

    # Register example tests
    test_ids = orchestrator.register_tests(create_example_test_suite())
    print(f"📝 Registered {len(test_ids)} example tests")

    # Run all tests
    results = orchestrator.run_all_tests()

    # Display results
    if results:
        print(f"\n✅ Test execution completed!")
        print(f"📊 Results: {len(results)} tests run")

        for result in results:
            status_emoji = "✅" if result.status.value == "passed" else "❌"
            print(
                f"  {status_emoji} {result.test_name}: {result.status.value} ({result.execution_time:.3f}s)"
            )

        # Show summary
        orchestrator.print_status()
    else:
        print("❌ No tests were executed")

    return results


if __name__ == "__main__":
    run_example_tests()
