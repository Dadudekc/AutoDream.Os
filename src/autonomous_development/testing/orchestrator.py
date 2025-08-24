"""
Testing Orchestrator - Extracted from autonomous_development.py

This module handles testing orchestration including:
- Test execution and coordination
- Test result analysis
- Test coverage reporting
- Automated testing workflows

Original file: src/core/autonomous_development.py
Extraction date: 2024-12-19
"""

import subprocess
import time
import logging
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

# Configure logging
logger = logging.getLogger(__name__)

# Import from main file - using type hints to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...core.autonomous_development import DevelopmentAction


@dataclass
class TestResult:
    """Test execution result"""
    test_name: str
    test_file: str
    status: str  # 'passed', 'failed', 'skipped', 'error'
    duration: float
    output: str
    error_message: Optional[str] = None
    line_number: Optional[int] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class TestSuite:
    """Test suite definition"""
    name: str
    test_files: List[str]
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    error_tests: int
    duration: float
    coverage_percentage: float


class TestingOrchestrator:
    """Testing orchestrator - SRP: Coordinate and execute tests"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.TestingOrchestrator")
        
        # Test configuration
        self.test_config: Dict[str, Any] = {}
        self.test_results: List[TestResult] = []
        self.test_suites: Dict[str, TestSuite] = {}
        
        # Execution state
        self.is_running = False
        self.current_tests: List[str] = []
        self.test_start_time: Optional[datetime] = None
        
        # Coverage tracking
        self.coverage_data: Dict[str, float] = {}
        
        # Initialize default configuration
        self._initialize_config()
    
    def _initialize_config(self):
        """Initialize default test configuration"""
        try:
            self.test_config = {
                'test_runner': 'pytest',
                'test_directory': 'tests',
                'coverage_tool': 'coverage',
                'parallel_execution': False,
                'max_workers': 4,
                'timeout_per_test': 30,
                'retry_failed_tests': True,
                'max_retries': 2,
                'generate_reports': True,
                'report_formats': ['html', 'xml', 'json'],
                'coverage_threshold': 80.0,
                'exclude_patterns': [
                    '*/__pycache__/*',
                    '*/venv/*',
                    '*/node_modules/*',
                    '*/build/*',
                    '*/dist/*'
                ]
            }
            
            self.logger.debug("Initialized test configuration")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize test configuration: {e}")
    
    def configure_testing(self, config: Dict[str, Any]) -> bool:
        """Configure testing parameters"""
        try:
            # Validate configuration
            if not self._validate_config(config):
                return False
            
            # Update configuration
            self.test_config.update(config)
            
            self.logger.info("Updated test configuration")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure testing: {e}")
            return False
    
    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate test configuration"""
        try:
            required_keys = ['test_runner', 'test_directory']
            
            for key in required_keys:
                if key not in config:
                    self.logger.error(f"Missing required configuration key: {key}")
                    return False
            
            # Validate test directory exists
            test_dir = config.get('test_directory', 'tests')
            if not Path(test_dir).exists():
                self.logger.warning(f"Test directory does not exist: {test_dir}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False
    
    def discover_tests(self, test_directory: Optional[str] = None) -> List[str]:
        """Discover test files in the specified directory"""
        try:
            if test_directory is None:
                test_directory = self.test_config.get('test_directory', 'tests')
            
            test_files = []
            test_path = Path(test_directory)
            
            if not test_path.exists():
                self.logger.warning(f"Test directory not found: {test_directory}")
                return []
            
            # Find Python test files
            for file_path in test_path.rglob('*.py'):
                if self._is_test_file(file_path):
                    test_files.append(str(file_path))
            
            # Find other test file types
            for file_path in test_path.rglob('*'):
                if self._is_test_file(file_path):
                    test_files.append(str(file_path))
            
            self.logger.info(f"Discovered {len(test_files)} test files in {test_directory}")
            return test_files
            
        except Exception as e:
            self.logger.error(f"Failed to discover tests: {e}")
            return []
    
    def _is_test_file(self, file_path: Path) -> bool:
        """Check if a file is a test file"""
        try:
            filename = file_path.name.lower()
            
            # Python test files
            if filename.endswith('.py'):
                return (filename.startswith('test_') or 
                       filename.endswith('_test.py') or
                       'test' in filename)
            
            # Other test file types
            test_extensions = ['.js', '.ts', '.java', '.cpp', '.cs']
            for ext in test_extensions:
                if filename.endswith(ext):
                    return (filename.startswith('test') or 
                           filename.endswith('test') or
                           'test' in filename)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to check if file is test file: {e}")
            return False
    
    def run_tests(self, test_files: Optional[List[str]] = None, 
                  test_suite_name: str = "default") -> bool:
        """Run tests and collect results"""
        try:
            if self.is_running:
                self.logger.warning("Tests already running")
                return False
            
            # Discover tests if not provided
            if test_files is None:
                test_files = self.discover_tests()
            
            if not test_files:
                self.logger.warning("No test files found")
                return False
            
            self.is_running = True
            self.test_start_time = datetime.now()
            self.current_tests = test_files.copy()
            
            self.logger.info(f"Starting test execution for {len(test_files)} test files")
            
            # Execute tests
            test_results = []
            total_tests = 0
            passed_tests = 0
            failed_tests = 0
            skipped_tests = 0
            error_tests = 0
            total_duration = 0.0
            
            for test_file in test_files:
                result = self._execute_test_file(test_file)
                if result:
                    test_results.append(result)
                    total_tests += 1
                    
                    if result.status == 'passed':
                        passed_tests += 1
                    elif result.status == 'failed':
                        failed_tests += 1
                    elif result.status == 'skipped':
                        skipped_tests += 1
                    elif result.status == 'error':
                        error_tests += 1
                    
                    total_duration += result.duration
            
            # Create test suite
            test_suite = TestSuite(
                name=test_suite_name,
                test_files=test_files,
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                skipped_tests=skipped_tests,
                error_tests=error_tests,
                duration=total_duration,
                coverage_percentage=self._calculate_coverage(test_files)
            )
            
            # Store results
            self.test_results.extend(test_results)
            self.test_suites[test_suite_name] = test_suite
            
            # Generate reports if enabled
            if self.test_config.get('generate_reports', True):
                self._generate_test_reports(test_suite_name)
            
            self.logger.info(f"Test execution completed: {passed_tests} passed, {failed_tests} failed")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to run tests: {e}")
            return False
        
        finally:
            self.is_running = False
            self.current_tests = []
            self.test_start_time = None
    
    def _execute_test_file(self, test_file: str) -> Optional[TestResult]:
        """Execute a single test file"""
        try:
            self.logger.debug(f"Executing test file: {test_file}")
            
            start_time = time.time()
            
            # Determine test runner
            test_runner = self.test_config.get('test_runner', 'pytest')
            
            if test_runner == 'pytest':
                result = self._run_pytest_test(test_file)
            elif test_runner == 'unittest':
                result = self._run_unittest_test(test_file)
            else:
                result = self._run_generic_test(test_file)
            
            if result:
                result.duration = time.time() - start_time
                result.test_file = test_file
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to execute test file {test_file}: {e}")
            return None
    
    def _run_pytest_test(self, test_file: str) -> Optional[TestResult]:
        """Run test using pytest"""
        try:
            cmd = [
                'python', '-m', 'pytest', test_file,
                '--tb=short',
                '--quiet',
                '--json-report',
                '--json-report-file=/tmp/pytest_report.json'
            ]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.test_config.get('timeout_per_test', 30)
            )
            
            # Parse pytest output
            if process.returncode == 0:
                status = 'passed'
                error_message = None
            elif process.returncode == 1:
                status = 'failed'
                error_message = process.stderr
            elif process.returncode == 2:
                status = 'error'
                error_message = process.stderr
            else:
                status = 'error'
                error_message = f"Unexpected return code: {process.returncode}"
            
            return TestResult(
                test_name=Path(test_file).stem,
                test_file=test_file,
                status=status,
                duration=0.0,  # Will be set by caller
                output=process.stdout,
                error_message=error_message
            )
            
        except subprocess.TimeoutExpired:
            return TestResult(
                test_name=Path(test_file).stem,
                test_file=test_file,
                status='error',
                duration=0.0,
                output='',
                error_message='Test execution timed out'
            )
        except Exception as e:
            self.logger.error(f"Pytest execution failed: {e}")
            return None
    
    def _run_unittest_test(self, test_file: str) -> Optional[TestResult]:
        """Run test using unittest"""
        try:
            cmd = [
                'python', '-m', 'unittest', 'discover',
                '--start-directory', str(Path(test_file).parent),
                '--pattern', Path(test_file).name
            ]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.test_config.get('timeout_per_test', 30)
            )
            
            # Parse unittest output
            if process.returncode == 0:
                status = 'passed'
                error_message = None
            else:
                status = 'failed'
                error_message = process.stderr
            
            return TestResult(
                test_name=Path(test_file).stem,
                test_file=test_file,
                status=status,
                duration=0.0,
                output=process.stdout,
                error_message=error_message
            )
            
        except subprocess.TimeoutExpired:
            return TestResult(
                test_name=Path(test_file).stem,
                test_file=test_file,
                status='error',
                duration=0.0,
                output='',
                error_message='Test execution timed out'
            )
        except Exception as e:
            self.logger.error(f"Unittest execution failed: {e}")
            return None
    
    def _run_generic_test(self, test_file: str) -> Optional[TestResult]:
        """Run test using generic method"""
        try:
            # Try to execute the file directly
            cmd = ['python', test_file]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.test_config.get('timeout_per_test', 30)
            )
            
            # Generic status determination
            if process.returncode == 0:
                status = 'passed'
                error_message = None
            else:
                status = 'failed'
                error_message = process.stderr
            
            return TestResult(
                test_name=Path(test_file).stem,
                test_file=test_file,
                status=status,
                duration=0.0,
                output=process.stdout,
                error_message=error_message
            )
            
        except subprocess.TimeoutExpired:
            return TestResult(
                test_name=Path(test_file).stem,
                test_file=test_file,
                status='error',
                duration=0.0,
                output='',
                error_message='Test execution timed out'
            )
        except Exception as e:
            self.logger.error(f"Generic test execution failed: {e}")
            return None
    
    def _calculate_coverage(self, test_files: List[str]) -> float:
        """Calculate test coverage percentage"""
        try:
            coverage_tool = self.test_config.get('coverage_tool', 'coverage')
            
            if coverage_tool == 'coverage':
                return self._run_coverage_analysis()
            else:
                # Placeholder coverage calculation
                return 75.0  # Default coverage
                
        except Exception as e:
            self.logger.error(f"Failed to calculate coverage: {e}")
            return 0.0
    
    def _run_coverage_analysis(self) -> float:
        """Run coverage analysis using coverage tool"""
        try:
            # Run coverage
            cmd = [
                'python', '-m', 'coverage', 'run', '--source=.',
                '-m', 'pytest', '--collect-only'
            ]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Generate coverage report
            cmd = ['python', '-m', 'coverage', 'report', '--format=json']
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if process.returncode == 0:
                try:
                    coverage_data = json.loads(process.stdout)
                    total_coverage = coverage_data.get('totals', {}).get('percent_covered', 0.0)
                    return float(total_coverage)
                except json.JSONDecodeError:
                    self.logger.warning("Failed to parse coverage JSON output")
                    return 0.0
            else:
                self.logger.warning("Coverage analysis failed")
                return 0.0
                
        except Exception as e:
            self.logger.error(f"Coverage analysis failed: {e}")
            return 0.0
    
    def _generate_test_reports(self, test_suite_name: str):
        """Generate test reports in specified formats"""
        try:
            if test_suite_name not in self.test_suites:
                return
            
            test_suite = self.test_suites[test_suite_name]
            report_formats = self.test_config.get('report_formats', ['json'])
            
            for format_type in report_formats:
                if format_type == 'json':
                    self._generate_json_report(test_suite)
                elif format_type == 'xml':
                    self._generate_xml_report(test_suite)
                elif format_type == 'html':
                    self._generate_html_report(test_suite)
            
            self.logger.info(f"Generated test reports for suite: {test_suite_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate test reports: {e}")
    
    def _generate_json_report(self, test_suite: TestSuite):
        """Generate JSON test report"""
        try:
            report_data = {
                'test_suite': test_suite.name,
                'summary': {
                    'total_tests': test_suite.total_tests,
                    'passed_tests': test_suite.passed_tests,
                    'failed_tests': test_suite.failed_tests,
                    'skipped_tests': test_suite.skipped_tests,
                    'error_tests': test_suite.error_tests,
                    'duration': test_suite.duration,
                    'coverage_percentage': test_suite.coverage_percentage
                },
                'test_files': test_suite.test_files,
                'timestamp': datetime.now().isoformat()
            }
            
            report_file = f"test_report_{test_suite.name}.json"
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            self.logger.debug(f"Generated JSON report: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate JSON report: {e}")
    
    def _generate_xml_report(self, test_suite: TestSuite):
        """Generate XML test report"""
        try:
            # Create XML structure
            root = ET.Element('testsuite')
            root.set('name', test_suite.name)
            root.set('tests', str(test_suite.total_tests))
            root.set('failures', str(test_suite.failed_tests))
            root.set('errors', str(test_suite.error_tests))
            root.set('skipped', str(test_suite.skipped_tests))
            root.set('time', str(test_suite.duration))
            
            # Add test cases
            for test_file in test_suite.test_files:
                testcase = ET.SubElement(root, 'testcase')
                testcase.set('name', Path(test_file).stem)
                testcase.set('file', test_file)
                
                # Find corresponding test result
                for result in self.test_results:
                    if result.test_file == test_file:
                        if result.status == 'failed':
                            failure = ET.SubElement(testcase, 'failure')
                            failure.set('message', result.error_message or 'Test failed')
                        elif result.status == 'error':
                            error = ET.SubElement(testcase, 'error')
                            error.set('message', result.error_message or 'Test error')
                        elif result.status == 'skipped':
                            skip = ET.SubElement(testcase, 'skipped')
                            skip.set('message', 'Test skipped')
                        break
            
            # Write XML file
            tree = ET.ElementTree(root)
            report_file = f"test_report_{test_suite.name}.xml"
            tree.write(report_file, encoding='utf-8', xml_declaration=True)
            
            self.logger.debug(f"Generated XML report: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate XML report: {e}")
    
    def _generate_html_report(self, test_suite: TestSuite):
        """Generate HTML test report"""
        try:
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Test Report - {test_suite.name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: white; border-radius: 3px; }}
        .passed {{ color: green; }}
        .failed {{ color: red; }}
        .skipped {{ color: orange; }}
        .error {{ color: red; }}
    </style>
</head>
<body>
    <h1>Test Report: {test_suite.name}</h1>
    
    <div class="summary">
        <h2>Summary</h2>
        <div class="metric">Total Tests: {test_suite.total_tests}</div>
        <div class="metric passed">Passed: {test_suite.passed_tests}</div>
        <div class="metric failed">Failed: {test_suite.failed_tests}</div>
        <div class="metric skipped">Skipped: {test_suite.skipped_tests}</div>
        <div class="metric error">Errors: {test_suite.error_tests}</div>
        <div class="metric">Duration: {test_suite.duration:.2f}s</div>
        <div class="metric">Coverage: {test_suite.coverage_percentage:.1f}%</div>
    </div>
    
    <h2>Test Files</h2>
    <ul>
"""
            
            for test_file in test_suite.test_files:
                # Find test result
                result = next((r for r in self.test_results if r.test_file == test_file), None)
                status_class = result.status if result else 'unknown'
                
                html_content += f"""
        <li class="{status_class}">
            {test_file} - {result.status if result else 'unknown'}
            {f'({result.duration:.2f}s)' if result else ''}
        </li>"""
            
            html_content += """
    </ul>
    
    <p><em>Report generated on """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</em></p>
</body>
</html>"""
            
            report_file = f"test_report_{test_suite.name}.html"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.debug(f"Generated HTML report: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {e}")
    
    def get_test_results(self, test_suite_name: Optional[str] = None) -> List[TestResult]:
        """Get test results for a specific suite or all results"""
        try:
            if test_suite_name:
                if test_suite_name in self.test_suites:
                    suite = self.test_suites[test_suite_name]
                    return [r for r in self.test_results if r.test_file in suite.test_files]
                else:
                    return []
            else:
                return self.test_results.copy()
                
        except Exception as e:
            self.logger.error(f"Failed to get test results: {e}")
            return []
    
    def get_test_summary(self, test_suite_name: Optional[str] = None) -> Dict[str, Any]:
        """Get test execution summary"""
        try:
            if test_suite_name:
                if test_suite_name in self.test_suites:
                    suite = self.test_suites[test_suite_name]
                    return {
                        'name': suite.name,
                        'total_tests': suite.total_tests,
                        'passed_tests': suite.passed_tests,
                        'failed_tests': suite.failed_tests,
                        'skipped_tests': suite.skipped_tests,
                        'error_tests': suite.error_tests,
                        'duration': suite.duration,
                        'coverage_percentage': suite.coverage_percentage,
                        'success_rate': (suite.passed_tests / max(suite.total_tests, 1)) * 100
                    }
                else:
                    return {}
            else:
                # Overall summary
                total_results = len(self.test_results)
                if total_results == 0:
                    return {}
                
                passed = len([r for r in self.test_results if r.status == 'passed'])
                failed = len([r for r in self.test_results if r.status == 'failed'])
                skipped = len([r for r in self.test_results if r.status == 'skipped'])
                errors = len([r for r in self.test_results if r.status == 'error'])
                
                return {
                    'total_tests': total_results,
                    'passed_tests': passed,
                    'failed_tests': failed,
                    'skipped_tests': skipped,
                    'error_tests': errors,
                    'success_rate': (passed / total_results) * 100,
                    'test_suites': list(self.test_suites.keys())
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get test summary: {e}")
            return {}
    
    def clear_results(self):
        """Clear all test results and suites"""
        try:
            self.test_results.clear()
            self.test_suites.clear()
            self.coverage_data.clear()
            self.logger.info("Cleared all test results")
        except Exception as e:
            self.logger.error(f"Failed to clear results: {e}")
    
    def is_test_running(self) -> bool:
        """Check if tests are currently running"""
        return self.is_running
    
    def get_current_tests(self) -> List[str]:
        """Get list of currently running tests"""
        return self.current_tests.copy()
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the testing orchestrator"""
        try:
            if not self.test_start_time:
                return {
                    'total_tests_executed': 0,
                    'average_execution_time': 0.0,
                    'success_rate': 0.0,
                    'coverage_trend': 0.0,
                    'uptime': 0.0
                }
            
            # Calculate metrics
            total_tests_executed = len(self.test_results)
            if total_tests_executed > 0:
                average_execution_time = sum(r.duration for r in self.test_results) / total_tests_executed
                passed_tests = len([r for r in self.test_results if r.status == 'passed'])
                success_rate = (passed_tests / total_tests_executed) * 100
            else:
                average_execution_time = 0.0
                success_rate = 0.0
            
            # Calculate coverage trend (simple average for now)
            coverage_trend = sum(r.coverage_percentage for r in self.test_results) / max(len(self.test_results), 1)
            
            # Calculate uptime
            uptime = (datetime.now() - self.test_start_time).total_seconds() if self.test_start_time else 0.0
            
            return {
                'total_tests_executed': total_tests_executed,
                'average_execution_time': average_execution_time,
                'success_rate': success_rate,
                'coverage_trend': coverage_trend,
                'uptime': uptime
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get performance metrics: {e}")
            return {}
        
    def run_tests(self, test_files: List[str] = None, test_suite_name: str = "default") -> bool:
        """Run tests using the orchestrator"""
        try:
            if test_files:
                # Create a temporary test suite
                suite = TestSuite(
                    suite_id=f"temp_{test_suite_name}",
                    suite_name=f"Temporary {test_suite_name}",
                    test_files=test_files
                )
                return self.execute_test_suite(suite.suite_id)
            else:
                # Run default test suite if available
                if "default" in self.test_suites:
                    return self.execute_test_suite("default")
                return False
        except Exception as e:
            self.logger.error(f"Failed to run tests: {e}")
            return False
