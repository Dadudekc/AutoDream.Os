"""
Suite Command Handler

Handles test suite management commands for the testing framework CLI.
"""


class SuiteCommandHandler:
    """Handles test suite management commands"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
    
    def handle(self, args) -> int:
        """Handle the suite command"""
        if args.list:
            suites = self.orchestrator.suite_manager.list_test_suites()
            if suites:
                print("📁 Available Test Suites:")
                for suite in suites:
                    print(f"  • {suite.suite_id}: {suite.suite_name}")
                    print(f"    Description: {suite.description}")
                    print(f"    Tests: {suite.get_test_count()}")
                    print(f"    Priority: {suite.priority.value}")
                    print()
            else:
                print("No test suites available.")
        
        elif args.create:
            if not args.suite_id:
                print("Suite ID required for creation. Use --suite-id")
                return 1
            
            description = args.description or f"Test suite: {args.create}"
            suite = self.orchestrator.suite_manager.create_test_suite(
                args.suite_id, args.create, description
            )
            print(f"✅ Created test suite: {suite.suite_id}")
        
        elif args.add_test:
            if not args.suite_id:
                print("Suite ID required. Use --suite-id")
                return 1
            
            success = self.orchestrator.suite_manager.add_test_to_suite(args.suite_id, args.add_test)
            if success:
                print(f"✅ Added test {args.add_test} to suite {args.suite_id}")
            else:
                print(f"❌ Failed to add test {args.add_test} to suite {args.suite_id}")
        
        else:
            print("No suite action specified. Use --list, --create, or --add-test")
            return 1
        
        return 0

