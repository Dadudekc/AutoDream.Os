"""Core test logic for the auth integration tester."""
from typing import List
import time

from .auth_service import AuthService, AuthStatus
from .auth_integration_tester_reporting import TestResult
from .auth_integration_tester_config import AuthTesterConfig


def run_core_tests(config: AuthTesterConfig) -> List[TestResult]:
    """Execute a minimal set of integration tests."""
    service = AuthService()
    results: List[TestResult] = []

    start = time.time()
    ok = service.authenticate_user_v2(
        config.test_user,
        config.valid_password,
        config.source_ip,
        "integration_tester",
    )
    duration = time.time() - start
    results.append(
        TestResult(
            name="valid_login",
            passed=ok.status == AuthStatus.SUCCESS,
            duration=duration,
            details={"status": ok.status.value},
        )
    )

    start = time.time()
    bad = service.authenticate_user_v2(
        config.test_user,
        config.invalid_password,
        config.source_ip,
        "integration_tester",
    )
    duration = time.time() - start
    results.append(
        TestResult(
            name="invalid_login",
            passed=bad.status != AuthStatus.SUCCESS,
            duration=duration,
            details={"status": bad.status.value},
        )
    )

    if config.run_performance:
        metrics = service.get_performance_metrics()
        results.append(
            TestResult(
                name="performance_metrics",
                passed=bool(metrics),
                duration=0.0,
                details={"metrics": metrics},
            )
        )

    if config.run_security:
        status = service.get_security_status()
        results.append(
            TestResult(
                name="security_status",
                passed=bool(status),
                duration=0.0,
                details={"status": status},
            )
        )

    return results
