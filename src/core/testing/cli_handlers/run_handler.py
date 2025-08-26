"""
Run Command Handler

Handles test execution commands for the testing framework CLI.
"""

from typing import List
from src.core.testing.testing_types import TestType, TestPriority


class RunCommandHandler:
    """Handles test execution commands"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
    
    def handle(self, args) -> int:
        """Handle the run command"""
        results = []
        
        if args.all:
            print("🧪 Running all registered tests...")
            results = self.orchestrator.run_all_tests()
        elif args.suite:
            print(f"🧪 Running tests in suite: {args.suite}")
            results = self.orchestrator.run_test_suite(args.suite)
        elif args.type:
            test_type = TestType(args.type)
            print(f"🧪 Running {test_type.value} tests...")
            results = self.orchestrator.run_tests_by_type(test_type)
        elif args.priority:
            priority = TestPriority(args.priority)
            print(f"🧪 Running tests with priority {priority.value}...")
            results = self.orchestrator.run_tests_by_priority(priority)
        elif args.test_id:
            print(f"🧪 Running test: {args.test_id}")
            result = self.orchestrator.run_test(args.test_id)
            if result:
                results = [result]
        else:
            print("No run target specified. Use --help for usage information.")
            return 1
        
        if results:
            print(f"\n✅ Test execution completed. {len(results)} tests run.")
            
            # Save results if requested
            if args.save_results:
                filepath = self.orchestrator.save_results(args.save_results)
                print(f"📁 Results saved to: {filepath}")
            
            # Print summary
            self.orchestrator.print_status()
        else:
            print("No tests were executed.")
        
        return 0

