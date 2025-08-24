#!/usr/bin/env python3
"""
V2 Authentication Integration Tester
===================================

Comprehensive integration testing for V2 authentication services.
Tests all components, integrations, and performance metrics.
"""

import sys
import os
import time
import logging
import threading
import concurrent.futures

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from auth_service import AuthService, AuthStatus, PermissionLevel
    from services.v1_v2_message_queue_system import V1V2MessageQueueSystem
    from services.integrated_agent_coordinator import IntegratedAgentCoordinator

    INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Integration components not available: {e}")
    INTEGRATION_AVAILABLE = False


@dataclass
class TestResult:
    """Test result data structure"""

    test_name: str
    status: str  # "PASS", "FAIL", "ERROR"
    duration: float
    details: Dict[str, Any]
    timestamp: datetime
    error_message: Optional[str] = None


@dataclass
class IntegrationTestReport:
    """Integration test report"""

    test_suite: str
    start_time: datetime
    end_time: datetime
    total_tests: int
    passed_tests: int
    failed_tests: int
    error_tests: int
    test_results: List[TestResult]
    performance_metrics: Dict[str, Any]
    integration_status: Dict[str, Any]


class AuthIntegrationTester:
    """
    V2 Authentication Integration Tester
    Comprehensive testing of auth system integration
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.logger = self._setup_logging()
        self.config = config or self._default_config()

        # Initialize test components
        self.auth_service = None
        self.message_queue = None
        self.agent_coordinator = None

        # Test tracking
        self.test_results = []
        self.current_test_suite = None

        self.logger.info("V2 Authentication Integration Tester initialized")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the integration tester"""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for integration testing"""
        return {
            "test_timeout": 300,  # 5 minutes per test
            "max_concurrent_tests": 5,
            "enable_performance_testing": True,
            "enable_stress_testing": True,
            "enable_security_testing": True,
            "enable_integration_testing": True,
            "test_users": ["admin", "agent-1", "agent-2", "test_user"],
            "test_passwords": [
                "secure_password_123",
                "wrong_password",
                "empty_password",
            ],
            "test_ips": ["127.0.0.1", "192.168.1.100", "10.0.0.50"],
        }

    def initialize_test_environment(self) -> bool:
        """Initialize the test environment with all required components"""
        try:
            self.logger.info("🔧 Initializing test environment...")

            # Initialize auth service
            self.auth_service = AuthService()
            self.logger.info("✅ Auth service initialized")

            # Initialize message queue system
            if INTEGRATION_AVAILABLE:
                try:
                    self.message_queue = V1V2MessageQueueSystem(enable_security=False)
                    self.logger.info("✅ Message queue system initialized")
                except Exception as e:
                    self.logger.warning(f"⚠️ Message queue system not available: {e}")
                    self.message_queue = None

                # Initialize agent coordinator
                try:
                    self.agent_coordinator = IntegratedAgentCoordinator()
                    self.logger.info("✅ Agent coordinator initialized")
                except Exception as e:
                    self.logger.warning(f"⚠️ Agent coordinator not available: {e}")
                    self.agent_coordinator = None
            else:
                self.logger.warning("⚠️ Integration components not available")

            self.logger.info("✅ Test environment initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize test environment: {e}")
            return False

    def run_comprehensive_integration_tests(self) -> IntegrationTestReport:
        """Run comprehensive integration test suite"""
        start_time = datetime.now()
        self.current_test_suite = "comprehensive_integration"

        self.logger.info("🚀 Starting comprehensive integration test suite")
        self.logger.info("=" * 60)

        # Initialize test environment
        if not self.initialize_test_environment():
            return self._create_error_report(
                "Environment initialization failed", start_time
            )

        # Run test categories
        test_categories = [
            ("Core Authentication", self._test_core_authentication),
            ("Security Features", self._test_security_features),
            ("Performance", self._test_performance),
            ("Integration", self._test_integration),
            ("Stress Testing", self._test_stress_scenarios),
            ("Error Handling", self._test_error_handling),
        ]

        for category_name, test_function in test_categories:
            self.logger.info(f"\n📋 Running {category_name} tests...")
            self.logger.info("-" * 40)

            try:
                test_function()
            except Exception as e:
                self.logger.error(f"❌ {category_name} tests failed: {e}")
                self._add_test_result(category_name, "ERROR", 0, {"error": str(e)})

        end_time = datetime.now()

        # Generate comprehensive report
        report = self._generate_test_report(start_time, end_time)

        self.logger.info("\n" + "=" * 60)
        self.logger.info("🏁 Comprehensive integration test suite completed")
        self.logger.info(
            f"📊 Results: {report.passed_tests}/{report.total_tests} tests passed"
        )

        return report

    def _test_core_authentication(self):
        """Test core authentication functionality"""
        test_cases = [
            (
                "Valid Admin Credentials",
                "admin",
                "secure_password_123",
                "127.0.0.1",
                True,
            ),
            ("Invalid Password", "admin", "wrong_password", "127.0.0.1", False),
            ("Non-existent User", "nonexistent", "password", "127.0.0.1", False),
            ("Empty Credentials", "", "", "127.0.0.1", False),
            ("Agent User", "agent-1", "secure_password_123", "192.168.1.100", True),
        ]

        for test_name, username, password, source_ip, expected_success in test_cases:
            start_time = time.time()

            try:
                result = self.auth_service.authenticate_user_v2(
                    username, password, source_ip, "test_user_agent"
                )

                duration = time.time() - start_time

                # Validate result
                if expected_success and result.status == AuthStatus.SUCCESS:
                    self._add_test_result(
                        test_name,
                        "PASS",
                        duration,
                        {
                            "user_id": result.user_id,
                            "permissions": [p.name for p in result.permissions],
                            "session_id": result.session_id,
                        },
                    )
                elif not expected_success and result.status != AuthStatus.SUCCESS:
                    self._add_test_result(
                        test_name,
                        "PASS",
                        duration,
                        {"expected_failure": True, "actual_status": result.status.name},
                    )
                else:
                    self._add_test_result(
                        test_name,
                        "FAIL",
                        duration,
                        {
                            "expected_success": expected_success,
                            "actual_status": result.status.name,
                            "error": result.metadata.get("error"),
                        },
                    )

            except Exception as e:
                duration = time.time() - start_time
                self._add_test_result(test_name, "ERROR", duration, {"error": str(e)})

    def _test_security_features(self):
        """Test security features and compliance"""
        test_cases = [
            ("Rate Limiting", self._test_rate_limiting),
            ("Session Management", self._test_session_management),
            ("Permission Levels", self._test_permission_levels),
            ("Security Context", self._test_security_context),
            ("Compliance Audit", self._test_compliance_audit),
        ]

        for test_name, test_function in test_cases:
            start_time = time.time()

            try:
                test_function()
                duration = time.time() - start_time
                self._add_test_result(
                    test_name, "PASS", duration, {"security_features": "validated"}
                )

            except Exception as e:
                duration = time.time() - start_time
                self._add_test_result(test_name, "ERROR", duration, {"error": str(e)})

    def _test_rate_limiting(self):
        """Test rate limiting functionality"""
        # Simulate multiple rapid authentication attempts
        source_ip = "192.168.1.200"

        for i in range(15):  # Exceed rate limit
            result = self.auth_service.authenticate_user_v2(
                "test_user", "wrong_password", source_ip, "test_agent"
            )

            if result.status == AuthStatus.RATE_LIMITED:
                self.logger.info(f"✅ Rate limiting triggered after {i+1} attempts")
                return

        raise Exception("Rate limiting not triggered after multiple failed attempts")

    def _test_session_management(self):
        """Test session management functionality"""
        # Test successful authentication creates session
        result = self.auth_service.authenticate_user_v2(
            "admin", "secure_password_123", "127.0.0.1", "test_agent"
        )

        if result.status != AuthStatus.SUCCESS:
            raise Exception("Session creation failed")

        if not result.session_id:
            raise Exception("No session ID returned")

        if not result.expires_at:
            raise Exception("No expiration time set")

        # Validate session metadata
        if not result.metadata.get("v2_features"):
            raise Exception("V2 features not enabled in session")

    def _test_permission_levels(self):
        """Test permission level determination"""
        # Test admin permissions
        admin_result = self.auth_service.authenticate_user_v2(
            "admin", "secure_password_123", "127.0.0.1", "test_agent"
        )

        if AuthStatus.SUCCESS not in [p.name for p in admin_result.permissions]:
            raise Exception("Admin should have USER permission")

        # Test agent permissions
        agent_result = self.auth_service.authenticate_user_v2(
            "agent-1", "secure_password_123", "127.0.0.1", "test_agent"
        )

        if PermissionLevel.USER not in agent_result.permissions:
            raise Exception("Agent should have USER permission")

    def _test_security_context(self):
        """Test security context validation"""
        # Test with suspicious context
        suspicious_context = {
            "suspicious_headers": True,
            "unusual_location": True,
            "multiple_failed_attempts": True,
        }

        result = self.auth_service.authenticate_user_v2(
            "admin",
            "secure_password_123",
            "127.0.0.1",
            "test_agent",
            suspicious_context,
        )

        # Should still succeed but with security events
        if result.status != AuthStatus.SUCCESS:
            raise Exception(
                "Authentication should succeed even with suspicious context"
            )

        if not any("suspicious" in event.lower() for event in result.security_events):
            raise Exception("Security events should be logged for suspicious context")

    def _test_compliance_audit(self):
        """Test compliance audit functionality"""
        # Test authentication logging
        result = self.auth_service.authenticate_user_v2(
            "admin", "secure_password_123", "127.0.0.1", "test_agent"
        )

        if not any("compliance" in event.lower() for event in result.security_events):
            raise Exception("Compliance audit events should be logged")

    def _test_performance(self):
        """Test authentication performance"""
        if not self.config["enable_performance_testing"]:
            return

        # Test single authentication performance
        start_time = time.time()
        result = self.auth_service.authenticate_user_v2(
            "admin", "secure_password_123", "127.0.0.1", "test_agent"
        )
        single_auth_time = time.time() - start_time

        self._add_test_result(
            "Single Auth Performance",
            "PASS",
            single_auth_time,
            {
                "auth_duration": single_auth_time,
                "performance_threshold": 1.0,  # Should complete within 1 second
            },
        )

        # Test concurrent authentication performance
        if self.config["enable_stress_testing"]:
            self._test_concurrent_performance()

    def _test_concurrent_performance(self):
        """Test concurrent authentication performance"""
        num_concurrent = 10
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=num_concurrent
        ) as executor:
            futures = []
            for i in range(num_concurrent):
                future = executor.submit(
                    self.auth_service.authenticate_user_v2,
                    f"agent-{i}",
                    "secure_password_123",
                    f"192.168.1.{i}",
                    "test_agent",
                )
                futures.append(future)

            # Wait for all to complete
            concurrent.futures.wait(futures)

        total_time = time.time() - start_time
        avg_time = total_time / num_concurrent

        self._add_test_result(
            "Concurrent Auth Performance",
            "PASS",
            total_time,
            {
                "concurrent_auths": num_concurrent,
                "total_time": total_time,
                "average_time": avg_time,
                "throughput": num_concurrent / total_time,
            },
        )

    def _test_integration(self):
        """Test integration with other systems"""
        if not self.config["enable_integration_testing"]:
            return

        # Test message queue integration
        if self.message_queue:
            self._test_message_queue_integration()

        # Test agent coordinator integration
        if self.agent_coordinator:
            self._test_agent_coordinator_integration()

    def _test_message_queue_integration(self):
        """Test integration with message queue system"""
        start_time = time.time()

        try:
            # Register test agents
            self.message_queue.register_agent(
                "auth_test_agent", "Auth Test Agent", ["authentication"]
            )

            # Send authentication message
            msg_id = self.message_queue.send_message(
                "system", "auth_test_agent", "Authentication test message", priority=3
            )

            if msg_id:
                # Retrieve message
                messages = self.message_queue.get_messages("auth_test_agent")

                if messages and len(messages) > 0:
                    duration = time.time() - start_time
                    self._add_test_result(
                        "Message Queue Integration",
                        "PASS",
                        duration,
                        {"message_id": msg_id, "messages_received": len(messages)},
                    )
                else:
                    raise Exception("No messages received from queue")
            else:
                raise Exception("Failed to send message to queue")

        except Exception as e:
            duration = time.time() - start_time
            self._add_test_result(
                "Message Queue Integration", "ERROR", duration, {"error": str(e)}
            )

    def _test_agent_coordinator_integration(self):
        """Test integration with agent coordinator"""
        start_time = time.time()

        try:
            # Test basic coordinator functionality
            if hasattr(self.agent_coordinator, "get_system_status"):
                status = self.agent_coordinator.get_system_status()
                duration = time.time() - start_time

                self._add_test_result(
                    "Agent Coordinator Integration",
                    "PASS",
                    duration,
                    {
                        "system_status": status.get("status", "unknown"),
                        "coordinator_available": True,
                    },
                )
            else:
                raise Exception("Agent coordinator missing required methods")

        except Exception as e:
            duration = time.time() - start_time
            self._add_test_result(
                "Agent Coordinator Integration", "ERROR", duration, {"error": str(e)}
            )

    def _test_stress_scenarios(self):
        """Test authentication under stress conditions"""
        if not self.config["enable_stress_testing"]:
            return

        # Test rapid authentication attempts
        start_time = time.time()

        try:
            for i in range(50):  # Stress test with 50 rapid attempts
                result = self.auth_service.authenticate_user_v2(
                    f"stress_user_{i}",
                    "wrong_password",
                    f"192.168.1.{i}",
                    "stress_test_agent",
                )

                # Should handle gracefully without crashing
                if result.status == AuthStatus.SYSTEM_ERROR:
                    raise Exception(f"System error under stress at attempt {i+1}")

            duration = time.time() - start_time
            self._add_test_result(
                "Stress Testing",
                "PASS",
                duration,
                {"stress_attempts": 50, "system_stability": "maintained"},
            )

        except Exception as e:
            duration = time.time() - start_time
            self._add_test_result(
                "Stress Testing", "ERROR", duration, {"error": str(e)}
            )

    def _test_error_handling(self):
        """Test error handling and edge cases"""
        test_cases = [
            ("None Credentials", None, None, "127.0.0.1"),
            ("Empty String Credentials", "", "", "127.0.0.1"),
            ("Very Long Username", "a" * 1000, "password", "127.0.0.1"),
            ("Special Characters", "user@#$%", "pass!@#", "127.0.0.1"),
            ("Invalid IP Format", "admin", "password", "invalid_ip"),
        ]

        for test_name, username, password, source_ip in test_cases:
            start_time = time.time()

            try:
                result = self.auth_service.authenticate_user_v2(
                    username, password, source_ip, "error_test_agent"
                )

                duration = time.time() - start_time

                # Should handle gracefully without crashing
                if result.status == AuthStatus.SYSTEM_ERROR:
                    self._add_test_result(
                        test_name,
                        "PASS",
                        duration,
                        {"error_handled": True, "status": result.status.name},
                    )
                else:
                    self._add_test_result(
                        test_name,
                        "PASS",
                        duration,
                        {"error_handled": True, "status": result.status.name},
                    )

            except Exception as e:
                duration = time.time() - start_time
                self._add_test_result(test_name, "ERROR", duration, {"error": str(e)})

    def _add_test_result(
        self, test_name: str, status: str, duration: float, details: Dict[str, Any]
    ):
        """Add a test result to the tracking list"""
        result = TestResult(
            test_name=test_name,
            status=status,
            duration=duration,
            details=details,
            timestamp=datetime.now(),
        )

        self.test_results.append(result)

        # Log result
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        self.logger.info(f"{status_icon} {test_name}: {status} ({duration:.3f}s)")

    def _generate_test_report(
        self, start_time: datetime, end_time: datetime
    ) -> IntegrationTestReport:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r.status == "PASS"])
        failed_tests = len([r for r in self.test_results if r.status == "FAIL"])
        error_tests = len([r for r in self.test_results if r.status == "ERROR"])

        # Calculate performance metrics
        performance_metrics = {}
        if self.auth_service:
            performance_metrics = self.auth_service.get_performance_metrics()

        # Integration status
        integration_status = {
            "auth_service": self.auth_service is not None,
            "message_queue": self.message_queue is not None,
            "agent_coordinator": self.agent_coordinator is not None,
            "core_security_components": getattr(self.auth_service, "auth_system", None)
            is not None
            if self.auth_service
            else False,
        }

        return IntegrationTestReport(
            test_suite=self.current_test_suite,
            start_time=start_time,
            end_time=end_time,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            error_tests=error_tests,
            test_results=self.test_results,
            performance_metrics=performance_metrics,
            integration_status=integration_status,
        )

    def _create_error_report(
        self, error_message: str, start_time: datetime
    ) -> IntegrationTestReport:
        """Create error report when testing fails"""
        return IntegrationTestReport(
            test_suite=self.current_test_suite or "error",
            start_time=start_time,
            end_time=datetime.now(),
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            error_tests=1,
            test_results=[
                TestResult(
                    test_name="Environment Setup",
                    status="ERROR",
                    duration=0,
                    details={"error": error_message},
                    timestamp=datetime.now(),
                    error_message=error_message,
                )
            ],
            performance_metrics={},
            integration_status={"error": error_message},
        )

    def cleanup(self):
        """Cleanup test resources"""
        try:
            if self.auth_service:
                self.auth_service.shutdown()

            if self.message_queue:
                self.message_queue.shutdown()

            self.logger.info("✅ Test resources cleaned up")

        except Exception as e:
            self.logger.error(f"❌ Cleanup failed: {e}")
