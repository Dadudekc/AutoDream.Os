"""
Status Command Handler

Handles system status display commands for the testing framework CLI.
"""


class StatusCommandHandler:
    """Handles system status display commands"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
    
    def handle(self, args) -> int:
        """Handle the status command"""
        if args.detailed:
            self.orchestrator.print_status()
        else:
            status = self.orchestrator.get_system_status()
            print(f"🧪 Testing Framework Status: {status['system_status']}")
            print(f"📊 Registered Tests: {status['registered_tests']}")
            print(f"📁 Available Suites: {status['available_suites']}")
            print(f"📂 Results Directory: {status['results_directory']}")
        
        return 0

