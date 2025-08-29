"""
Output Formatter

Handles all output formatting for the testing framework.
"""

from typing import Dict, Any
from datetime import datetime


class OutputFormatter:
    """Handles output formatting for test results."""
    
    def __init__(self, color_available: bool = True):
        self.color_available = color_available
        self._setup_colors()
    
    def _setup_colors(self):
        """Setup color formatting."""
        if self.color_available:
            try:
                import colorama
                from colorama import Fore, Style
                colorama.init(autoreset=True)
                self.Fore = Fore
                self.Style = Style
            except ImportError:
                self.color_available = False
        
        if not self.color_available:
            # Fallback for systems without colorama
            class Fore:
                GREEN = ""
                RED = ""
                YELLOW = ""
                BLUE = ""
                CYAN = ""
                RESET = ""

            class Style:
                RESET_ALL = ""

            self.Fore = Fore
            self.Style = Style
    
    def print_banner(self, repo_root: str):
        """Print the test runner banner."""
        print(f"{self.Fore.CYAN}{'='*70}")
        print(f"{self.Fore.CYAN}🧪 AGENT_CELLPHONE_V2 COMPREHENSIVE TEST RUNNER")
        print(f"{self.Fore.CYAN}{'='*70}")
        print(f"{self.Fore.CYAN}Foundation & Testing Specialist - TDD Integration Project")
        print(f"{self.Fore.CYAN}Repository: {repo_root}")
        print(f"{self.Fore.CYAN}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{self.Fore.CYAN}{'='*70}{self.Style.RESET_ALL}\n")
    
    def print_prerequisites_check(self, message: str):
        """Print prerequisites check message."""
        print(f"{self.Fore.YELLOW}🔍 {message}{self.Style.RESET_ALL}")
    
    def print_success(self, message: str):
        """Print success message."""
        print(f"✅ {message}")
    
    def print_error(self, message: str):
        """Print error message."""
        print(f"{self.Fore.RED}❌ {message}{self.Style.RESET_ALL}")
    
    def print_info(self, message: str):
        """Print info message."""
        print(f"{self.Fore.BLUE}ℹ️  {message}{self.Style.RESET_ALL}")
    
    def print_test_category_header(self, category: str, description: str, timeout: int, critical: bool):
        """Print test category execution header."""
        print(f"\n{self.Fore.BLUE}🚀 Running {category.upper()} tests...{self.Style.RESET_ALL}")
        print(f"   Description: {description}")
        print(f"   Timeout: {timeout}s")
        print(f"   Critical: {'Yes' if critical else 'No'}")
    
    def print_test_results(self, results: Dict[str, Any]):
        """Print test execution results."""
        if results.get('success'):
            print(f"{self.Fore.GREEN}✅ {results['category']} tests completed successfully{self.Style.RESET_ALL}")
            print(f"   Duration: {results.get('duration', 0):.2f}s")
            print(f"   Tests: {results.get('tests_run', 0)}")
            print(f"   Failures: {results.get('failures', 0)}")
            print(f"   Errors: {results.get('errors', 0)}")
        else:
            print(f"{self.Fore.RED}❌ {results['category']} tests failed{self.Style.RESET_ALL}")
            if 'error' in results:
                print(f"   Error: {results['error']}")
    
    def print_summary(self, summary: Dict[str, Any]):
        """Print test execution summary."""
        print(f"\n{self.Fore.CYAN}{'='*50}")
        print(f"🧪 TEST EXECUTION SUMMARY")
        print(f"{'='*50}{self.Style.RESET_ALL}")
        print(f"Total Categories: {summary.get('total_categories', 0)}")
        print(f"Successful: {summary.get('successful', 0)}")
        print(f"Failed: {summary.get('failed', 0)}")
        print(f"Total Duration: {summary.get('total_duration', 0):.2f}s")
        print(f"Overall Status: {'✅ PASSED' if summary.get('overall_success') else '❌ FAILED'}")

