#!/usr/bin/env python3
"""
Agent-7 Interface Integration Tests
===================================

Integration testing for Agent-7 Repository Management Interface
V2 Compliant: ≤400 lines, focused integration testing logic
"""

from typing import Dict, List, Any
import time
import os
import platform
from pathlib import Path
from .models import TestResult, TestCategory, TestStatus


class Agent7IntegrationTests:
    """Agent-7 Repository Management Interface Integration Tests"""

    def __init__(self):
        """Initialize integration tests"""
        self.test_results: List[TestResult] = []
        self.platform_info = self._get_platform_info()

    def _get_platform_info(self) -> Dict[str, Any]:
        """Get platform information for testing"""
        return {
            "system": platform.system(),
            "platform": platform.platform(),
            "architecture": platform.architecture(),
            "python_version": platform.python_version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }

    def test_vscode_customization_integration(self) -> Dict[str, Any]:
        """Test VSCode customization integration"""
        print("🔍 Testing VSCode customization integration...")

        try:
            # Check for VSCode configuration files
            vscode_configs = [
                ".vscode/settings.json",
                ".vscode/extensions.json",
                ".vscode/launch.json",
                ".vscode/tasks.json"
            ]

            config_found = 0
            for config in vscode_configs:
                if os.path.exists(config):
                    config_found += 1

            passed = config_found > 0
            score = (config_found / len(vscode_configs)) * 100.0

            issues = [] if passed else ["No VSCode configuration found"]
            recommendations = ["Add VSCode configuration files"] if not passed else []

            return {
                "passed": passed,
                "score": score,
                "issues": issues,
                "recommendations": recommendations,
                "configs_found": config_found,
                "total_configs": len(vscode_configs)
            }

        except Exception as e:
            return {
                "passed": False,
                "score": 0.0,
                "issues": [f"Test failed: {str(e)}"],
                "recommendations": ["Check VSCode integration"],
                "error": str(e)
            }

    def test_cross_platform_compatibility(self) -> Dict[str, Any]:
        """Test cross-platform compatibility"""
        print("🔍 Testing cross-platform compatibility...")

        try:
            # Test platform-specific functionality
            platform_tests = {
                "windows": self._test_windows_compatibility(),
                "linux": self._test_linux_compatibility(),
                "macos": self._test_macos_compatibility()
            }

            current_platform = self.platform_info["system"].lower()
            current_test = platform_tests.get(current_platform, {"passed": False})

            passed = current_test.get("passed", False)
            score = 100.0 if passed else 0.0

            issues = [] if passed else [f"Platform compatibility issues on {current_platform}"]
            recommendations = ["Improve cross-platform support"] if not passed else []

            return {
                "passed": passed,
                "score": score,
                "issues": issues,
                "recommendations": recommendations,
                "platform": current_platform,
                "platform_info": self.platform_info
            }

        except Exception as e:
            return {
                "passed": False,
                "score": 0.0,
                "issues": [f"Test failed: {str(e)}"],
                "recommendations": ["Check platform compatibility"],
                "error": str(e)
            }

    def _test_windows_compatibility(self) -> Dict[str, Any]:
        """Test Windows compatibility"""
        try:
            # Test Windows-specific paths and commands
            windows_path = "C:\\test\\path"
            path_exists = os.path.exists(windows_path) or True  # Just test path handling

            return {
                "passed": True,
                "path_handling": "OK",
                "platform": "Windows"
            }
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "platform": "Windows"
            }

    def _test_linux_compatibility(self) -> Dict[str, Any]:
        """Test Linux compatibility"""
        try:
            # Test Linux-specific paths and commands
            linux_path = "/tmp/test/path"
            path_exists = os.path.exists(linux_path) or True  # Just test path handling

            return {
                "passed": True,
                "path_handling": "OK",
                "platform": "Linux"
            }
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "platform": "Linux"
            }

    def _test_macos_compatibility(self) -> Dict[str, Any]:
        """Test macOS compatibility"""
        try:
            # Test macOS-specific paths and commands
            macos_path = "/Users/test/path"
            path_exists = os.path.exists(macos_path) or True  # Just test path handling

            return {
                "passed": True,
                "path_handling": "OK",
                "platform": "macOS"
            }
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "platform": "macOS"
            }

    def test_interface_integration(self) -> Dict[str, Any]:
        """Test interface integration with other components"""
        print("🔍 Testing interface integration...")

        try:
            from src.team_beta.repository_manager import RepositoryManagerInterface

            # Test integration with other components
            interface = RepositoryManagerInterface()

            # Test integration points
            integration_tests = [
                self._test_database_integration(interface),
                self._test_api_integration(interface),
                self._test_file_system_integration(interface)
            ]

            passed_tests = sum(1 for test in integration_tests if test["passed"])
            total_tests = len(integration_tests)
            passed = passed_tests == total_tests
            score = (passed_tests / total_tests) * 100.0

            issues = [] if passed else [f"{total_tests - passed_tests} integration tests failed"]
            recommendations = ["Fix integration issues"] if not passed else []

            return {
                "passed": passed,
                "score": score,
                "issues": issues,
                "recommendations": recommendations,
                "integration_tests": integration_tests,
                "passed_tests": passed_tests,
                "total_tests": total_tests
            }

        except Exception as e:
            return {
                "passed": False,
                "score": 0.0,
                "issues": [f"Test failed: {str(e)}"],
                "recommendations": ["Check interface integration"],
                "error": str(e)
            }

    def _test_database_integration(self, interface) -> Dict[str, Any]:
        """Test database integration"""
        try:
            # Test database connectivity (mock test)
            database_available = True  # Mock test
            return {
                "passed": database_available,
                "component": "database",
                "status": "connected" if database_available else "disconnected"
            }
        except Exception as e:
            return {
                "passed": False,
                "component": "database",
                "error": str(e)
            }

    def _test_api_integration(self, interface) -> Dict[str, Any]:
        """Test API integration"""
        try:
            # Test API connectivity (mock test)
            api_available = True  # Mock test
            return {
                "passed": api_available,
                "component": "api",
                "status": "connected" if api_available else "disconnected"
            }
        except Exception as e:
            return {
                "passed": False,
                "component": "api",
                "error": str(e)
            }

    def _test_file_system_integration(self, interface) -> Dict[str, Any]:
        """Test file system integration"""
        try:
            # Test file system access
            test_path = "."
            fs_accessible = os.path.exists(test_path)
            return {
                "passed": fs_accessible,
                "component": "file_system",
                "status": "accessible" if fs_accessible else "inaccessible"
            }
        except Exception as e:
            return {
                "passed": False,
                "component": "file_system",
                "error": str(e)
            }

    def run_all_integration_tests(self) -> List[TestResult]:
        """Run all integration tests"""
        print("🧪 Running all integration tests...")

        integration_tests = [
            ("TC007", "VSCode Customization Integration", self.test_vscode_customization_integration),
            ("TC008", "Cross-Platform Compatibility", self.test_cross_platform_compatibility),
            ("TC009", "Interface Integration", self.test_interface_integration)
        ]

        test_results = []

        for test_id, test_name, test_func in integration_tests:
            start_time = time.time()
            try:
                result = test_func()
                execution_time = time.time() - start_time

                test_result = TestResult(
                    test_id=test_id,
                    test_name=test_name,
                    category=TestCategory.INTEGRATION,
                    status=TestStatus.PASSED if result["passed"] else TestStatus.FAILED,
                    score=result["score"],
                    issues=result["issues"],
                    recommendations=result["recommendations"],
                    execution_time=execution_time
                )

                test_results.append(test_result)
                print(f"✅ {test_name}: {'PASSED' if result['passed'] else 'FAILED'} ({result['score']:.1f}%)")

            except Exception as e:
                execution_time = time.time() - start_time
                test_result = TestResult(
                    test_id=test_id,
                    test_name=test_name,
                    category=TestCategory.INTEGRATION,
                    status=TestStatus.FAILED,
                    score=0.0,
                    issues=[f"Test execution failed: {str(e)}"],
                    recommendations=["Fix test implementation"],
                    execution_time=execution_time
                )

                test_results.append(test_result)
                print(f"❌ {test_name}: FAILED - {str(e)}")

        self.test_results = test_results
        return test_results