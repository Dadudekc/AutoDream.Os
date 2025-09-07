"""
Results Command Handler

Handles test results management commands for the testing framework CLI.
"""


class ResultsCommandHandler:
    """Handles test results management commands"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
    
    def handle(self, args) -> int:
        """Handle the results command"""
        if args.list:
            results = self.orchestrator.get_test_results()
            if results:
                print(f"📊 Test Results ({len(results)} total):")
                for result in results:
                    status_emoji = "✅" if result.status.value == "passed" else "❌"
                    print(f"  {status_emoji} {result.test_name} ({result.test_type.value}) - {result.status.value}")
            else:
                print("No test results available.")
        
        elif args.export:
            if args.export == 'json':
                export_data = self.orchestrator.export_results('json')
                print("📤 JSON export completed")
                print(export_data[:500] + "..." if len(export_data) > 500 else export_data)
            elif args.export == 'csv':
                print("📤 CSV export not yet implemented")
        
        elif args.clear:
            self.orchestrator.clear_results()
            print("🗑️  All test results cleared.")
        
        else:
            print("No results action specified. Use --list, --export, or --clear")
            return 1
        
        return 0

