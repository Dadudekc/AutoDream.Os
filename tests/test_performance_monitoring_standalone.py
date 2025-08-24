#!/usr/bin/env python3
"""Orchestrator for standalone performance monitoring tests."""

import asyncio

from test_performance_setup import (
    test_performance_monitor_standalone,
    test_metrics_collectors_standalone,
    test_dashboard_backend_standalone,
)
from test_performance_execution import (
    test_dashboard_frontend_standalone,
    test_integration_workflow_standalone,
)
from test_performance_analysis import (
    test_alerting_system_standalone,
    test_configuration_standalone,
)
from test_performance_cleanup import (
    test_launcher_script_standalone,
)


async def main():
    """Run all standalone performance monitoring tests."""
    tests = [
        ("Performance Monitor", test_performance_monitor_standalone),
        ("Metrics Collectors", test_metrics_collectors_standalone),
        ("Dashboard Backend", test_dashboard_backend_standalone),
        ("Dashboard Frontend", test_dashboard_frontend_standalone),
        ("Alerting System", test_alerting_system_standalone),
        ("Configuration", test_configuration_standalone),
        ("Integration Workflow", test_integration_workflow_standalone),
        ("Launcher Script", test_launcher_script_standalone),
    ]

    results = {}
    for name, func in tests:
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func()
            else:
                result = func()
            results[name] = result
        except Exception as exc:  # pragma: no cover - best effort logging
            print(f"❌ {name} test failed with exception: {exc}")
            results[name] = False

    print("\n📊 Test Summary")
    print("=" * 20)
    passed = sum(1 for r in results.values() if r)
    failed = len(results) - passed

    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")

    print(f"\nTotal Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    if len(results):
        print(f"Success Rate: {(passed / len(results) * 100):.1f}%")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    raise SystemExit(exit_code)
