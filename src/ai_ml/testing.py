"""
Testing Module
Agent-2: AI & ML Framework Integration
TDD Integration Project - Agent_Cellphone_V2_Repository

Provides AI-powered testing, model validation, and quality assurance
"""

import os
import json
import logging
import time
import subprocess

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any, Union, Callable
from pathlib import Path
from datetime import datetime
import asyncio
import sys

# Try to import testing dependencies
try:
    import pytest

    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    logging.warning("pytest package not available")

try:
    import coverage

    COVERAGE_AVAILABLE = True
except ImportError:
    COVERAGE_AVAILABLE = False
    logging.warning("coverage package not available")

logger = logging.getLogger(__name__)


class AITestRunner:
    """AI-powered test runner with intelligent test generation and execution"""

    def __init__(self, project_path: str = ".", test_dir: str = "tests"):
        self.project_path = Path(project_path)
        self.test_dir = Path(test_dir)
        self.test_results: Dict[str, Any] = {}
        self.generated_tests: List[str] = []

        if not PYTEST_AVAILABLE:
            logger.warning("pytest not available. Install with: pip install pytest")

    def discover_tests(self) -> List[str]:
        """Discover existing test files in the project"""
        try:
            test_files = []

            # Search for test files recursively
            for test_file in self.test_dir.rglob("test_*.py"):
                if test_file.is_file():
                    test_files.append(str(test_file.relative_to(self.project_path)))

            # Also check for files ending with _test.py
            for test_file in self.test_dir.rglob("*_test.py"):
                if test_file.is_file():
                    test_files.append(str(test_file.relative_to(self.project_path)))

            logger.info(f"Discovered {len(test_files)} test files")
            return test_files

        except Exception as e:
            logger.error(f"Error discovering tests: {e}")
            return []

    def run_tests(
        self,
        test_path: Optional[str] = None,
        coverage: bool = True,
        verbose: bool = True,
    ) -> Dict[str, Any]:
        """Run tests using pytest"""
        if not PYTEST_AVAILABLE:
            logger.error("pytest not available")
            return {"error": "pytest not available"}

        try:
            cmd = [sys.executable, "-m", "pytest"]

            if test_path:
                cmd.append(test_path)
            else:
                cmd.append(str(self.test_dir))

            if verbose:
                cmd.append("-v")

            if coverage and COVERAGE_AVAILABLE:
                cmd.extend(
                    ["--cov=src", "--cov-report=html", "--cov-report=term-missing"]
                )

            # Add additional pytest options
            cmd.extend(["--tb=short", "--strict-markers", "--disable-warnings"])

            logger.info(f"Running tests with command: {' '.join(cmd)}")

            # Execute pytest
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.project_path
            )

            # Parse results
            test_results = {
                "command": cmd,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "timestamp": datetime.now().isoformat(),
                "success": result.returncode == 0,
            }

            # Try to extract test statistics from output
            if result.stdout:
                test_results.update(self._parse_pytest_output(result.stdout))

            self.test_results[datetime.now().isoformat()] = test_results

            if test_results["success"]:
                logger.info("Tests completed successfully")
            else:
                logger.warning("Tests completed with failures")

            return test_results

        except Exception as e:
            logger.error(f"Error running tests: {e}")
            return {"error": str(e)}

    def _parse_pytest_output(self, output: str) -> Dict[str, Any]:
        """Parse pytest output to extract test statistics"""
        stats = {}

        try:
            lines = output.split("\n")

            for line in lines:
                if "collected" in line and "items" in line:
                    # Extract total test count
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "collected":
                            if i + 1 < len(parts):
                                stats["total_tests"] = int(parts[i + 1])
                            break

                elif "passed" in line and "failed" in line:
                    # Extract pass/fail counts
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "passed":
                            if i + 1 < len(parts):
                                stats["passed"] = int(parts[i + 1])
                        elif part == "failed":
                            if i + 1 < len(parts):
                                stats["failed"] = int(parts[i + 1])

                elif "ERROR" in line:
                    stats["errors"] = stats.get("errors", 0) + 1

                elif "WARNING" in line:
                    stats["warnings"] = stats.get("warnings", 0) + 1

        except Exception as e:
            logger.debug(f"Error parsing pytest output: {e}")

        return stats

    def generate_tests_for_file(
        self, source_file: str, test_framework: str = "pytest"
    ) -> str:
        """Generate tests for a specific source file"""
        try:
            source_path = Path(source_file)
            if not source_path.exists():
                logger.error(f"Source file not found: {source_file}")
                return ""

            # Read source file content
            with open(source_path, "r") as f:
                source_code = f.read()

            # Generate test file name
            test_file_name = f"test_{source_path.stem}.py"
            test_file_path = self.test_dir / test_file_name

            # Create test content (this would typically use AI to generate)
            test_content = self._generate_test_content(source_code, test_framework)

            # Write test file
            test_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(test_file_path, "w") as f:
                f.write(test_content)

            self.generated_tests.append(str(test_file_path))
            logger.info(f"Generated test file: {test_file_path}")

            return str(test_file_path)

        except Exception as e:
            logger.error(f"Error generating tests for {source_file}: {e}")
            return ""

    def _generate_test_content(self, source_code: str, test_framework: str) -> str:
        """Generate test content using AI (placeholder implementation)"""
        # This is a placeholder - in practice, you would use OpenAI or Claude
        # to generate actual test content based on the source code

        test_content = f'''"""
Auto-generated tests for source code
Generated by AITestRunner
Framework: {test_framework}
"""

import pytest
import sys
from pathlib import Path

# Add source directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import the module to test
# TODO: Import statements will be generated based on source code analysis

class TestGenerated:
    """Auto-generated test cases"""

    def test_placeholder(self):
        """Placeholder test - replace with actual test cases"""
        assert True

    # TODO: Additional test methods will be generated based on source code analysis
    # This includes:
    # - Unit tests for all functions/methods
    # - Edge case testing
    # - Error handling tests
    # - Mock/stub examples where appropriate
    # - Test data generation

if __name__ == "__main__":
    pytest.main([__file__])
'''

        return test_content

    def run_coverage_analysis(self, source_dir: str = "src") -> Dict[str, Any]:
        """Run code coverage analysis"""
        if not COVERAGE_AVAILABLE:
            logger.error("coverage package not available")
            return {"error": "coverage package not available"}

        try:
            # Run coverage
            cmd = [
                sys.executable,
                "-m",
                "coverage",
                "run",
                "--source",
                source_dir,
                "-m",
                "pytest",
                str(self.test_dir),
            ]

            logger.info(f"Running coverage analysis: {' '.join(cmd)}")

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.project_path
            )

            if result.returncode != 0:
                logger.warning("Coverage analysis completed with warnings")

            # Generate coverage report
            report_cmd = [sys.executable, "-m", "coverage", "report"]
            report_result = subprocess.run(
                report_cmd, capture_output=True, text=True, cwd=self.project_path
            )

            # Generate HTML report
            html_cmd = [sys.executable, "-m", "coverage", "html"]
            html_result = subprocess.run(
                html_cmd, capture_output=True, text=True, cwd=self.project_path
            )

            coverage_results = {
                "coverage_run": {
                    "return_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                },
                "coverage_report": {
                    "return_code": report_result.returncode,
                    "stdout": report_result.stdout,
                    "stderr": report_result.stderr,
                },
                "html_report": {
                    "return_code": html_result.returncode,
                    "stdout": html_result.stdout,
                    "stderr": html_result.stderr,
                },
                "timestamp": datetime.now().isoformat(),
            }

            logger.info("Coverage analysis completed")
            return coverage_results

        except Exception as e:
            logger.error(f"Error running coverage analysis: {e}")
            return {"error": str(e)}

    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of test execution results"""
        if not self.test_results:
            return {"message": "No tests have been run yet"}

        summary = {
            "total_runs": len(self.test_results),
            "successful_runs": sum(
                1 for r in self.test_results.values() if r.get("success", False)
            ),
            "failed_runs": sum(
                1 for r in self.test_results.values() if not r.get("success", True)
            ),
            "generated_tests": len(self.generated_tests),
            "latest_run": max(self.test_results.keys()) if self.test_results else None,
            "test_files": self.discover_tests(),
        }

        return summary


class ModelValidator:
    """Validate AI/ML models and their outputs"""

    def __init__(self):
        self.validation_results: Dict[str, Any] = {}
        self.validation_rules: Dict[str, Callable] = {}

        # Register default validation rules
        self._register_default_rules()

    def _register_default_rules(self) -> None:
        """Register default validation rules"""
        self.register_rule("not_empty", lambda x: bool(x and str(x).strip()))
        self.register_rule("is_string", lambda x: isinstance(x, str))
        self.register_rule("is_number", lambda x: isinstance(x, (int, float)))
        self.register_rule(
            "is_positive", lambda x: isinstance(x, (int, float)) and x > 0
        )
        self.register_rule(
            "length_range",
            lambda x, min_len=0, max_len=1000: min_len <= len(str(x)) <= max_len,
        )

    def register_rule(self, rule_name: str, rule_func: Callable) -> None:
        """Register a custom validation rule"""
        self.validation_rules[rule_name] = rule_func
        logger.info(f"Registered validation rule: {rule_name}")

    def validate_model_output(
        self, model_name: str, output: Any, expected_rules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate model output against expected rules"""
        try:
            validation_result = {
                "model_name": model_name,
                "timestamp": datetime.now().isoformat(),
                "output": str(output)[:1000],  # Truncate long outputs
                "rules": expected_rules,
                "results": {},
                "overall_valid": True,
            }

            for rule_name, rule_params in expected_rules.items():
                if rule_name in self.validation_rules:
                    try:
                        rule_func = self.validation_rules[rule_name]

                        if isinstance(rule_params, dict):
                            # Rule with parameters
                            is_valid = rule_func(output, **rule_params)
                        else:
                            # Simple rule
                            is_valid = rule_func(output)

                        validation_result["results"][rule_name] = {
                            "valid": is_valid,
                            "params": rule_params,
                        }

                        if not is_valid:
                            validation_result["overall_valid"] = False

                    except Exception as e:
                        validation_result["results"][rule_name] = {
                            "valid": False,
                            "error": str(e),
                            "params": rule_params,
                        }
                        validation_result["overall_valid"] = False
                else:
                    validation_result["results"][rule_name] = {
                        "valid": False,
                        "error": f"Unknown validation rule: {rule_name}",
                        "params": rule_params,
                    }
                    validation_result["overall_valid"] = False

            # Store validation result
            self.validation_results[model_name] = validation_result

            if validation_result["overall_valid"]:
                logger.info(f"Model {model_name} validation passed")
            else:
                logger.warning(f"Model {model_name} validation failed")

            return validation_result

        except Exception as e:
            logger.error(f"Error validating model {model_name}: {e}")
            return {"error": str(e)}

    def validate_code_generation(
        self, generated_code: str, requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate generated code against requirements"""
        try:
            validation_rules = {
                "not_empty": True,
                "is_string": True,
                "length_range": {"min_len": 10, "max_len": 10000},
                "contains_imports": lambda x: "import" in x or "from" in x,
                "contains_functions": lambda x: "def " in x,
                "syntax_check": lambda x: self._check_python_syntax(x),
            }

            # Add custom requirements
            if "required_keywords" in requirements:
                for keyword in requirements["required_keywords"]:
                    validation_rules[f"contains_{keyword}"] = (
                        lambda x, kw=keyword: kw in x
                    )

            return self.validate_model_output(
                "code_generator", generated_code, validation_rules
            )

        except Exception as e:
            logger.error(f"Error validating code generation: {e}")
            return {"error": str(e)}

    def _check_python_syntax(self, code: str) -> bool:
        """Check if Python code has valid syntax"""
        try:
            compile(code, "<string>", "exec")
            return True
        except SyntaxError:
            return False

    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of validation results"""
        if not self.validation_results:
            return {"message": "No validations have been performed yet"}

        summary = {
            "total_validations": len(self.validation_results),
            "successful_validations": sum(
                1
                for r in self.validation_results.values()
                if r.get("overall_valid", False)
            ),
            "failed_validations": sum(
                1
                for r in self.validation_results.values()
                if not r.get("overall_valid", True)
            ),
            "models_validated": list(self.validation_results.keys()),
            "available_rules": list(self.validation_rules.keys()),
        }

        return summary


class QualityAssurance:
    """Comprehensive quality assurance for AI/ML systems"""

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.qa_results: Dict[str, Any] = {}
        self.quality_metrics: Dict[str, float] = {}

    def run_full_qa_check(self) -> Dict[str, Any]:
        """Run comprehensive quality assurance check"""
        try:
            logger.info("Starting comprehensive QA check...")

            qa_results = {
                "timestamp": datetime.now().isoformat(),
                "project_path": str(self.project_path),
                "checks": {},
            }

            # Code quality checks
            qa_results["checks"]["code_quality"] = self._check_code_quality()

            # Test coverage checks
            qa_results["checks"]["test_coverage"] = self._check_test_coverage()

            # Documentation checks
            qa_results["checks"]["documentation"] = self._check_documentation()

            # Security checks
            qa_results["checks"]["security"] = self._check_security()

            # Performance checks
            qa_results["checks"]["performance"] = self._check_performance()

            # Calculate overall quality score
            qa_results["overall_score"] = self._calculate_quality_score(
                qa_results["checks"]
            )

            # Store results
            self.qa_results[datetime.now().isoformat()] = qa_results

            logger.info(
                f"QA check completed. Overall score: {qa_results['overall_score']:.2f}/10"
            )

            return qa_results

        except Exception as e:
            logger.error(f"Error running QA check: {e}")
            return {"error": str(e)}

    def _check_code_quality(self) -> Dict[str, Any]:
        """Check code quality metrics"""
        try:
            # This would typically use tools like flake8, pylint, or black
            # For now, we'll do basic checks

            python_files = list(self.project_path.rglob("*.py"))
            total_lines = 0
            docstring_count = 0
            function_count = 0

            for py_file in python_files:
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        lines = content.split("\n")
                        total_lines += len(lines)

                        # Count docstrings
                        docstring_count += content.count('"""') // 2
                        docstring_count += content.count("'''") // 2

                        # Count functions
                        function_count += content.count("def ")

                except Exception as e:
                    logger.debug(f"Error reading {py_file}: {e}")

            quality_score = 0.0

            if total_lines > 0:
                # Calculate various quality metrics
                docstring_ratio = docstring_count / max(function_count, 1)
                quality_score += min(
                    docstring_ratio * 3, 3
                )  # Max 3 points for documentation

                # Add points for having tests
                test_files = list(self.project_path.rglob("test_*.py"))
                if test_files:
                    quality_score += 2  # 2 points for having tests

                # Add points for configuration files
                config_files = list(self.project_path.rglob("*.json")) + list(
                    self.project_path.rglob("*.yaml")
                )
                if config_files:
                    quality_score += 1  # 1 point for configuration

                # Add points for README
                readme_files = list(self.project_path.rglob("README*"))
                if readme_files:
                    quality_score += 1  # 1 point for README

                # Add points for requirements file
                req_files = list(self.project_path.rglob("requirements*.txt"))
                if req_files:
                    quality_score += 1  # 1 point for requirements

                # Add points for license
                license_files = list(self.project_path.rglob("LICENSE*"))
                if license_files:
                    quality_score += 1  # 1 point for license

            return {
                "score": min(quality_score, 10.0),
                "total_lines": total_lines,
                "docstring_count": docstring_count,
                "function_count": function_count,
                "python_files": len(python_files),
            }

        except Exception as e:
            logger.error(f"Error checking code quality: {e}")
            return {"error": str(e)}

    def _check_test_coverage(self) -> Dict[str, Any]:
        """Check test coverage metrics"""
        try:
            test_files = list(self.project_path.rglob("test_*.py"))
            test_file_count = len(test_files)

            # Basic test coverage score
            coverage_score = min(
                test_file_count * 2, 10.0
            )  # 2 points per test file, max 10

            return {
                "score": coverage_score,
                "test_files": test_file_count,
                "test_file_paths": [
                    str(f.relative_to(self.project_path)) for f in test_files
                ],
            }

        except Exception as e:
            logger.error(f"Error checking test coverage: {e}")
            return {"error": str(e)}

    def _check_documentation(self) -> Dict[str, Any]:
        """Check documentation quality"""
        try:
            doc_files = list(self.project_path.rglob("*.md"))
            doc_file_count = len(doc_files)

            # Basic documentation score
            doc_score = min(doc_file_count, 10.0)  # 1 point per doc file, max 10

            return {
                "score": doc_score,
                "doc_files": doc_file_count,
                "doc_file_paths": [
                    str(f.relative_to(self.project_path)) for f in doc_files
                ],
            }

        except Exception as e:
            logger.error(f"Error checking documentation: {e}")
            return {"error": str(e)}

    def _check_security(self) -> Dict[str, Any]:
        """Check security aspects"""
        try:
            # Basic security checks
            security_score = 5.0  # Base score

            # Check for common security issues
            python_files = list(self.project_path.rglob("*.py"))

            for py_file in python_files:
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()

                        # Check for hardcoded secrets
                        if any(
                            secret in content.lower()
                            for secret in [
                                "password",
                                "secret",
                                "key",
                                "token",
                                "api_key",
                            ]
                        ):
                            security_score -= 0.5

                        # Check for eval usage
                        if "eval(" in content:
                            security_score -= 2.0

                        # Check for exec usage
                        if "exec(" in content:
                            security_score -= 2.0

                except Exception as e:
                    logger.debug(f"Error reading {py_file}: {e}")

            return {"score": max(security_score, 0.0), "security_issues": []}

        except Exception as e:
            logger.error(f"Error checking security: {e}")
            return {"error": str(e)}

    def _check_performance(self) -> Dict[str, Any]:
        """Check performance aspects"""
        try:
            # Basic performance score
            performance_score = 5.0  # Base score

            # Check for performance-related patterns
            python_files = list(self.project_path.rglob("*.py"))

            for py_file in python_files:
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()

                        # Check for async usage
                        if "async def" in content or "await" in content:
                            performance_score += 1.0

                        # Check for multiprocessing
                        if "multiprocessing" in content:
                            performance_score += 1.0

                        # Check for threading
                        if "threading" in content:
                            performance_score += 0.5

                except Exception as e:
                    logger.debug(f"Error reading {py_file}: {e}")

            return {"score": min(performance_score, 10.0), "performance_features": []}

        except Exception as e:
            logger.error(f"Error checking performance: {e}")
            return {"error": str(e)}

    def _calculate_quality_score(self, checks: Dict[str, Any]) -> float:
        """Calculate overall quality score from individual checks"""
        try:
            total_score = 0.0
            valid_checks = 0

            for check_name, check_result in checks.items():
                if isinstance(check_result, dict) and "score" in check_result:
                    score = check_result["score"]
                    if isinstance(score, (int, float)):
                        total_score += score
                        valid_checks += 1

            if valid_checks > 0:
                return total_score / valid_checks
            else:
                return 0.0

        except Exception as e:
            logger.error(f"Error calculating quality score: {e}")
            return 0.0

    def generate_qa_report(self, output_file: str = "qa_report.json") -> bool:
        """Generate QA report and save to file"""
        try:
            if not self.qa_results:
                logger.warning("No QA results available. Run QA check first.")
                return False

            # Get latest QA result
            latest_timestamp = max(self.qa_results.keys())
            latest_result = self.qa_results[latest_timestamp]

            # Add summary information
            report = {
                "qa_report": latest_result,
                "summary": {
                    "overall_score": latest_result.get("overall_score", 0.0),
                    "timestamp": latest_timestamp,
                    "recommendations": self._generate_recommendations(latest_result),
                },
            }

            # Save report
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w") as f:
                json.dump(report, f, indent=2)

            logger.info(f"QA report generated: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error generating QA report: {e}")
            return False

    def _generate_recommendations(self, qa_result: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations based on QA results"""
        recommendations = []

        overall_score = qa_result.get("overall_score", 0.0)

        if overall_score < 5.0:
            recommendations.append(
                "Overall quality score is low. Focus on improving code quality and testing."
            )

        checks = qa_result.get("checks", {})

        # Code quality recommendations
        code_quality = checks.get("code_quality", {})
        if code_quality.get("score", 0) < 5.0:
            recommendations.append(
                "Improve code quality by adding docstrings, comments, and following PEP 8."
            )

        # Test coverage recommendations
        test_coverage = checks.get("test_coverage", {})
        if test_coverage.get("score", 0) < 5.0:
            recommendations.append(
                "Increase test coverage by adding more test files and test cases."
            )

        # Documentation recommendations
        documentation = checks.get("documentation", {})
        if documentation.get("score", 0) < 5.0:
            recommendations.append(
                "Improve documentation by adding more markdown files and README content."
            )

        # Security recommendations
        security = checks.get("security", {})
        if security.get("score", 0) < 5.0:
            recommendations.append(
                "Address security concerns by reviewing code for vulnerabilities."
            )

        # Performance recommendations
        performance = checks.get("performance", {})
        if performance.get("score", 0) < 5.0:
            recommendations.append(
                "Consider performance optimizations like async/await and multiprocessing."
            )

        if not recommendations:
            recommendations.append(
                "Good job! Code quality is high. Keep up the good work!"
            )

        return recommendations
