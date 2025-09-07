"""
Reporting and export functionality for automated integration test suites.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from .models import TestSuiteResult


class TestSuiteReporter:
    """Handles reporting and export of test suite results."""
    
    def __init__(self, results: List[TestSuiteResult]):
        self.results = results
        self.export_dir = Path("test_results")
        self.export_dir.mkdir(exist_ok=True)
    
    def export_suite_results(self, format_type: str = "json") -> str:
        """Export test suite results in specified format."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type.lower() == "json":
            return self._export_json(timestamp)
        elif format_type.lower() == "html":
            return self._export_html(timestamp)
        elif format_type.lower() == "markdown":
            return self._export_markdown(timestamp)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _export_json(self, timestamp: str) -> str:
        """Export results to JSON format."""
        filepath = self.export_dir / f"test_suite_results_{timestamp}.json"
        
        # Convert results to serializable format
        serializable_results = []
        for result in self.results:
            serializable_result = {
                'suite_id': result.suite_id,
                'suite_name': result.suite_name,
                'execution_start': result.execution_start.isoformat(),
                'execution_end': result.execution_end.isoformat(),
                'total_tests': result.total_tests,
                'passed_tests': result.passed_tests,
                'failed_tests': result.failed_tests,
                'error_tests': result.error_tests,
                'skipped_tests': result.skipped_tests,
                'execution_time': result.execution_time,
                'status': result.status,
                'test_results': result.test_results,
                'summary': result.summary,
                'error_details': result.error_details
            }
            serializable_results.append(serializable_result)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, default=str)
        
        return str(filepath)
    
    def _export_html(self, timestamp: str) -> str:
        """Export results to HTML format."""
        filepath = self.export_dir / f"test_suite_results_{timestamp}.html"
        
        html_content = self._generate_html_content()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _export_markdown(self, timestamp: str) -> str:
        """Export results to Markdown format."""
        filepath = self.export_dir / f"test_suite_results_{timestamp}.md"
        
        markdown_content = self._generate_markdown_content()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return str(filepath)
    
    def _generate_html_content(self) -> str:
        """Generate HTML content for test suite results."""
        summary = self._calculate_summary()
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Suite Results</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .suite-result {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
        .passed {{ border-left: 5px solid #4CAF50; }}
        .failed {{ border-left: 5px solid #f44336; }}
        .error {{ border-left: 5px solid #ff9800; }}
        .partial {{ border-left: 5px solid #ffeb3b; }}
        .skipped {{ border-left: 5px solid #9e9e9e; }}
        .status-badge {{ padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold; }}
        .status-passed {{ background-color: #4CAF50; }}
        .status-failed {{ background-color: #f44336; }}
        .status-error {{ background-color: #ff9800; }}
        .status-partial {{ background-color: #ffeb3b; color: black; }}
        .status-skipped {{ background-color: #9e9e9e; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 Test Suite Results</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>📊 Summary</h2>
        <ul>
            <li><strong>Total Suites:</strong> {summary['total_suites']}</li>
            <li><strong>Passed Suites:</strong> {summary['passed_suites']}</li>
            <li><strong>Failed Suites:</strong> {summary['failed_suites']}</li>
            <li><strong>Error Suites:</strong> {summary['error_suites']}</li>
            <li><strong>Partial Suites:</strong> {summary['partial_suites']}</li>
            <li><strong>Skipped Suites:</strong> {summary['skipped_suites']}</li>
            <li><strong>Suite Pass Rate:</strong> {summary['suite_pass_rate']:.1f}%</li>
            <li><strong>Total Tests:</strong> {summary['total_tests']}</li>
            <li><strong>Test Pass Rate:</strong> {summary['test_pass_rate']:.1f}%</li>
        </ul>
    </div>
    
    <h2>📋 Suite Results</h2>
"""
        
        for result in self.results:
            status_class = f"status-{result.status}"
            status_badge_class = f"status-badge {status_class}"
            
            html_content += f"""
    <div class="suite-result {result.status}">
        <h3>{result.suite_name}</h3>
        <p><strong>Suite ID:</strong> {result.suite_id}</p>
        <p><strong>Status:</strong> <span class="{status_badge_class}">{result.status.upper()}</span></p>
        <p><strong>Total Tests:</strong> {result.total_tests}</p>
        <p><strong>Passed:</strong> {result.passed_tests}</p>
        <p><strong>Failed:</strong> {result.failed_tests}</p>
        <p><strong>Errors:</strong> {result.error_tests}</p>
        <p><strong>Execution Time:</strong> {result.execution_time:.3f}s</p>
"""
            
            if result.error_details:
                html_content += f'        <p><strong>Error Details:</strong> {result.error_details}</p>\n'
            
            html_content += "    </div>\n"
        
        html_content += """
</body>
</html>"""
        
        return html_content
    
    def _generate_markdown_content(self) -> str:
        """Generate Markdown content for test suite results."""
        summary = self._calculate_summary()
        
        markdown_content = f"""# 🧪 Test Suite Results

**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Summary

- **Total Suites:** {summary['total_suites']}
- **Passed Suites:** {summary['passed_suites']}
- **Failed Suites:** {summary['failed_suites']}
- **Error Suites:** {summary['error_suites']}
- **Partial Suites:** {summary['partial_suites']}
- **Skipped Suites:** {summary['skipped_suites']}
- **Suite Pass Rate:** {summary['suite_pass_rate']:.1f}%
- **Total Tests:** {summary['total_tests']}
- **Test Pass Rate:** {summary['test_pass_rate']:.1f}%

## 📋 Suite Results

"""
        
        for result in self.results:
            status_emoji = {
                "passed": "✅",
                "failed": "❌",
                "error": "⚠️",
                "partial": "🟡",
                "skipped": "⏭️"
            }.get(result.status, "❓")
            
            markdown_content += f"""### {status_emoji} {result.suite_name}

- **Suite ID:** {result.suite_id}
- **Status:** {result.status.upper()}
- **Total Tests:** {result.total_tests}
- **Passed:** {result.passed_tests}
- **Failed:** {result.failed_tests}
- **Errors:** {result.error_tests}
- **Execution Time:** {result.execution_time:.3f}s
"""
            
            if result.error_details:
                markdown_content += f"\n**Error Details:** {result.error_details}\n"
            
            markdown_content += "\n---\n\n"
        
        return markdown_content
    
    def _calculate_summary(self) -> Dict[str, Any]:
        """Calculate summary statistics from results."""
        if not self.results:
            return {
                "total_suites": 0,
                "passed_suites": 0,
                "failed_suites": 0,
                "error_suites": 0,
                "partial_suites": 0,
                "skipped_suites": 0,
                "suite_pass_rate": 0.0,
                "total_tests": 0,
                "test_pass_rate": 0.0
            }
        
        total_suites = len(self.results)
        passed_suites = len([r for r in self.results if r.status == "passed"])
        failed_suites = len([r for r in self.results if r.status == "failed"])
        error_suites = len([r for r in self.results if r.status == "error"])
        partial_suites = len([r for r in self.results if r.status == "partial"])
        skipped_suites = len([r for r in self.results if r.status == "skipped"])
        
        suite_pass_rate = (passed_suites / total_suites * 100) if total_suites > 0 else 0
        
        total_tests = sum(r.total_tests for r in self.results)
        total_passed_tests = sum(r.passed_tests for r in self.results)
        test_pass_rate = (total_passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "total_suites": total_suites,
            "passed_suites": passed_suites,
            "failed_suites": failed_suites,
            "error_suites": error_suites,
            "partial_suites": partial_suites,
            "skipped_suites": skipped_suites,
            "suite_pass_rate": suite_pass_rate,
            "total_tests": total_tests,
            "test_pass_rate": test_pass_rate
        }
