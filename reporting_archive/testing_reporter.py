"""
Testing Framework Reporter
==========================

Handles test result reporting, coverage analysis, and output generation
in various formats for the consolidated testing framework.
"""

import json
import csv
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import html

from src.core.testing.testing_types import (
    TestStatus,
    TestType,
    TestPriority,
    TestEnvironment,
    TestResult,
    TestSuite,
    TestReport
)


class TestReporter:
    """Base reporter class for test results"""
    
    def __init__(self, output_dir: str = "test_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_report(self, results: List[TestResult], filename: str = None) -> str:
        """Generate a basic report (to be overridden by subclasses)"""
        raise NotImplementedError("Subclasses must implement generate_report")
    
    def _ensure_output_dir(self) -> None:
        """Ensure output directory exists"""
        self.output_dir.mkdir(exist_ok=True, parents=True)


class CoverageReporter(TestReporter):
    """Generates test coverage reports"""
    
    def __init__(self, output_dir: str = "test_reports"):
        super().__init__(output_dir)
        self.coverage_data = {}
    
    def analyze_coverage(self, results: List[TestResult]) -> Dict[str, Any]:
        """Analyze test coverage from results"""
        if not results:
            return {"total_coverage": 0.0, "coverage_by_type": {}}
        
        # Group results by test type
        coverage_by_type = {}
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.status == TestStatus.PASSED)
        
        for result in results:
            test_type = result.test_type.value
            if test_type not in coverage_by_type:
                coverage_by_type[test_type] = {"total": 0, "passed": 0, "coverage": 0.0}
            
            coverage_by_type[test_type]["total"] += 1
            if result.status == TestStatus.PASSED:
                coverage_by_type[test_type]["passed"] += 1
        
        # Calculate coverage percentages
        for test_type, data in coverage_by_type.items():
            if data["total"] > 0:
                data["coverage"] = (data["passed"] / data["total"]) * 100
        
        total_coverage = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        return {
            "total_coverage": total_coverage,
            "coverage_by_type": coverage_by_type,
            "total_tests": total_tests,
            "passed_tests": passed_tests
        }
    
    def generate_report(self, results: List[TestResult], filename: str = None) -> str:
        """Generate a coverage report"""
        coverage_data = self.analyze_coverage(results)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"coverage_report_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(coverage_data, f, indent=2, default=str)
        
        return str(filepath)
    
    def print_coverage_summary(self, results: List[TestResult]) -> None:
        """Print a formatted coverage summary"""
        coverage_data = self.analyze_coverage(results)
        
        print(f"\n📊 TEST COVERAGE SUMMARY")
        print(f"=" * 50)
        print(f"Total Coverage: {coverage_data['total_coverage']:.1f}%")
        print(f"Total Tests: {coverage_data['total_tests']}")
        print(f"Passed Tests: {coverage_data['passed_tests']}")
        
        print(f"\n📈 COVERAGE BY TEST TYPE:")
        for test_type, data in coverage_data['coverage_by_type'].items():
            print(f"  {test_type.title()}: {data['coverage']:.1f}% ({data['passed']}/{data['total']})")


class PerformanceReporter(TestReporter):
    """Generates performance analysis reports"""
    
    def __init__(self, output_dir: str = "test_reports"):
        super().__init__(output_dir)
    
    def analyze_performance(self, results: List[TestResult]) -> Dict[str, Any]:
        """Analyze performance metrics from test results"""
        if not results:
            return {
                "total_tests": 0,
                "avg_execution_time": 0.0,
                "slowest_tests": [],
                "fastest_tests": [],
                "performance_distribution": {}
            }
        
        # Calculate basic metrics
        total_tests = len(results)
        execution_times = [r.execution_time for r in results]
        avg_execution_time = sum(execution_times) / total_tests if total_tests > 0 else 0
        
        # Find slowest and fastest tests
        sorted_results = sorted(results, key=lambda r: r.execution_time, reverse=True)
        slowest_tests = [
            {
                "test_name": r.test_name,
                "execution_time": r.execution_time,
                "test_type": r.test_type.value
            }
            for r in sorted_results[:5]  # Top 5 slowest
        ]
        
        fastest_tests = [
            {
                "test_name": r.test_name,
                "execution_time": r.execution_time,
                "test_type": r.test_type.value
            }
            for r in sorted_results[-5:]  # Top 5 fastest
        ]
        
        # Performance distribution by test type
        performance_distribution = {}
        for result in results:
            test_type = result.test_type.value
            if test_type not in performance_distribution:
                performance_distribution[test_type] = {
                    "count": 0,
                    "total_time": 0.0,
                    "avg_time": 0.0
                }
            
            performance_distribution[test_type]["count"] += 1
            performance_distribution[test_type]["total_time"] += result.execution_time
        
        # Calculate averages for each type
        for test_type, data in performance_distribution.items():
            if data["count"] > 0:
                data["avg_time"] = data["total_time"] / data["count"]
        
        return {
            "total_tests": total_tests,
            "avg_execution_time": avg_execution_time,
            "slowest_tests": slowest_tests,
            "fastest_tests": fastest_tests,
            "performance_distribution": performance_distribution
        }
    
    def generate_report(self, results: List[TestResult], filename: str = None) -> str:
        """Generate a performance report"""
        performance_data = self.analyze_performance(results)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(performance_data, f, indent=2, default=str)
        
        return str(filepath)
    
    def print_performance_summary(self, results: List[TestResult]) -> None:
        """Print a formatted performance summary"""
        performance_data = self.analyze_performance(results)
        
        print(f"\n⏱️  PERFORMANCE ANALYSIS")
        print(f"=" * 50)
        print(f"Total Tests: {performance_data['total_tests']}")
        print(f"Average Execution Time: {performance_data['avg_execution_time']:.3f}s")
        
        print(f"\n🐌 SLOWEST TESTS:")
        for i, test in enumerate(performance_data['slowest_tests'], 1):
            print(f"  {i}. {test['test_name']} ({test['test_type']}): {test['execution_time']:.3f}s")
        
        print(f"\n⚡ FASTEST TESTS:")
        for i, test in enumerate(performance_data['fastest_tests'], 1):
            print(f"  {i}. {test['test_name']} ({test['test_type']}): {test['execution_time']:.3f}s")
        
        print(f"\n📊 PERFORMANCE BY TEST TYPE:")
        for test_type, data in performance_data['performance_distribution'].items():
            print(f"  {test_type.title()}: {data['avg_time']:.3f}s avg ({data['count']} tests)")


class HTMLReporter(TestReporter):
    """Generates HTML test reports"""
    
    def __init__(self, output_dir: str = "test_reports"):
        super().__init__(output_dir)
        self.template_dir = Path(__file__).parent / "templates"
    
    def generate_report(self, results: List[TestResult], filename: str = None) -> str:
        """Generate an HTML report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_report_{timestamp}.html"
        
        filepath = self.output_dir / filename
        
        html_content = self._generate_html_content(results)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _generate_html_content(self, results: List[TestResult]) -> str:
        """Generate HTML content for the report"""
        if not results:
            return self._generate_empty_html()
        
        # Calculate summary statistics
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.status == TestStatus.PASSED)
        failed_tests = sum(1 for r in results if r.status == TestStatus.FAILED)
        error_tests = sum(1 for r in results if r.status == TestStatus.ERROR)
        skipped_tests = sum(1 for r in results if r.status == TestStatus.SKIPPED)
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        total_execution_time = sum(r.execution_time for r in results)
        
        # Group results by status
        results_by_status = {}
        for result in results:
            status = result.status.value
            if status not in results_by_status:
                results_by_status[status] = []
            results_by_status[status].append(result)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Execution Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .summary-card {{ background-color: #f8f9fa; padding: 20px; border-radius: 6px; text-align: center; }}
        .summary-card h3 {{ margin: 0 0 10px 0; color: #495057; }}
        .summary-card .number {{ font-size: 2em; font-weight: bold; }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .error {{ color: #fd7e14; }}
        .skipped {{ color: #6c757d; }}
        .results-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .results-table th, .results-table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; }}
        .results-table th {{ background-color: #f8f9fa; font-weight: bold; }}
        .status-badge {{ padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }}
        .status-passed {{ background-color: #d4edda; color: #155724; }}
        .status-failed {{ background-color: #f8d7da; color: #721c24; }}
        .status-error {{ background-color: #fff3cd; color: #856404; }}
        .status-skipped {{ background-color: #e2e3e5; color: #383d41; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Test Execution Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total Tests</h3>
                <div class="number">{total_tests}</div>
            </div>
            <div class="summary-card">
                <h3>Success Rate</h3>
                <div class="number passed">{success_rate:.1f}%</div>
            </div>
            <div class="summary-card">
                <h3>Total Time</h3>
                <div class="number">{total_execution_time:.2f}s</div>
            </div>
            <div class="summary-card">
                <h3>Passed</h3>
                <div class="number passed">{passed_tests}</div>
            </div>
            <div class="summary-card">
                <h3>Failed</h3>
                <div class="number failed">{failed_tests}</div>
            </div>
            <div class="summary-card">
                <h3>Errors</h3>
                <div class="number error">{error_tests}</div>
            </div>
        </div>
        
        <h2>Test Results</h2>
        <table class="results-table">
            <thead>
                <tr>
                    <th>Test Name</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Execution Time</th>
                    <th>Priority</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add test result rows
        for result in results:
            status_class = f"status-{result.status.value}"
            html_content += f"""
                <tr>
                    <td>{html.escape(result.test_name)}</td>
                    <td>{result.test_type.value}</td>
                    <td><span class="status-badge {status_class}">{result.status.value.upper()}</span></td>
                    <td>{result.execution_time:.3f}s</td>
                    <td>{result.priority.value}</td>
                </tr>
"""
        
        html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        
        return html_content
    
    def _generate_empty_html(self) -> str:
        """Generate HTML for empty results"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Execution Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background-color: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test Execution Report</h1>
        <p>No test results available.</p>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>
"""
