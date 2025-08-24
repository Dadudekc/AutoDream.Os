#!/usr/bin/env python3
"""Orchestrator for the FSM-Cursor integration test suite."""

import os
import sys
import unittest

if __name__ == "__main__" and __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import tests.test_fsm_cursor_setup as test_fsm_cursor_setup
import tests.test_fsm_cursor_execution as test_fsm_cursor_execution
import tests.test_fsm_cursor_validation as test_fsm_cursor_validation
import tests.test_fsm_cursor_cleanup as test_fsm_cursor_cleanup


def run_fsm_cursor_integration_tests() -> bool:
    """Run all FSM-Cursor integration tests"""
    print("🧪 RUNNING FSM-CURSOR INTEGRATION SYSTEM TESTS")
    print("=" * 70)
    print("Focus: Perpetual motion machine, state machine logic, agent orchestration")
    print("Note: All systems are mocked for safe testing")
    print()

    test_suite = unittest.TestSuite()
    for module in (
        test_fsm_cursor_setup,
        test_fsm_cursor_execution,
        test_fsm_cursor_validation,
        test_fsm_cursor_cleanup,
    ):
        test_suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    print("\n" + "=" * 70)
    print("📊 FSM-CURSOR INTEGRATION TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if not result.failures and not result.errors:
        print("\n✅ ALL TESTS PASSED!")
        print("   FSM-Cursor integration validation successful!")
        print("   Perpetual motion machine working correctly!")
        print("   State machine logic functioning properly!")
        print("   Agent orchestration validated!")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_fsm_cursor_integration_tests()
    exit(0 if success else 1)
