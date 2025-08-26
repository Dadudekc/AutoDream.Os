"""
Report Command Handler

Handles test report generation commands for the testing framework CLI.
"""

from src.core.testing.testing_reporter import CoverageReporter, PerformanceReporter, HTMLReporter


class ReportCommandHandler:
    """Handles test report generation commands"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
    
    def handle(self, args) -> int:
        """Handle the report command"""
        results = self.orchestrator.get_test_results()
        
        if not results:
            print("No test results available for reporting.")
            return 1
        
        print(f"📊 Generating reports for {len(results)} test results...")
        
        if args.coverage:
            coverage_reporter = CoverageReporter(args.output_dir)
            filepath = coverage_reporter.generate_report(results)
            print(f"📈 Coverage report generated: {filepath}")
            coverage_reporter.print_coverage_summary(results)
        
        if args.performance:
            performance_reporter = PerformanceReporter(args.output_dir)
            filepath = performance_reporter.generate_report(results)
            print(f"⏱️  Performance report generated: {filepath}")
            performance_reporter.print_performance_summary(results)
        
        if args.html:
            html_reporter = HTMLReporter(args.output_dir)
            filepath = html_reporter.generate_report(results)
            print(f"🌐 HTML report generated: {filepath}")
        
        if not any([args.coverage, args.performance, args.html]):
            print("No report types specified. Use --coverage, --performance, or --html")
            return 1
        
        return 0
