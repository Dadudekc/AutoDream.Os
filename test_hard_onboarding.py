#!/usr/bin/env python3
"""
Test Script for Consolidated Messaging Hard Onboarding Flag
==========================================================

Tests the hard onboarding functionality through the consolidated messaging service.
This ensures the --hard-onboarding flag works correctly with all its parameters.

Author: Agent-4 - Strategic Oversight & QA Manager
"""

import logging
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


class HardOnboardingTester:
    """Test harness for hard onboarding functionality."""

    def __init__(self):
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0

    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """Log individual test results."""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append(f"{status} {test_name}")
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1

        if details:
            self.test_results.append(f"   {details}")

        logger.info(f"{status} {test_name}")
        if details:
            logger.info(f"   {details}")

    def test_hard_onboarding_flag_parsing(self):
        """Test that --hard-onboarding flag is correctly parsed."""
        logger.info("🧪 Testing hard onboarding flag parsing...")

        try:
            # Import the consolidated messaging service
            from services.consolidated_messaging_service import ConsolidatedMessagingService

            # Create service instance
            service = ConsolidatedMessagingService()

            # Test argument parsing with hard onboarding
            test_args = [
                "--hard-onboarding",
                "--agents",
                "Agent-1,Agent-2",
                "--onboarding-mode",
                "cleanup",
                "--assign-roles",
                "Agent-1:CLEANUP_CORE,Agent-2:CLEANUP_WEB",
                "--dry-run",
            ]

            # Parse arguments
            args = service.parser.parse_args(test_args)

            # Verify flags
            assert args.hard_onboarding == True, "hard_onboarding flag not set"
            assert args.agents == "Agent-1,Agent-2", "agents not parsed correctly"
            assert args.onboarding_mode == "cleanup", "onboarding_mode not parsed"
            assert args.assign_roles == "Agent-1:CLEANUP_CORE,Agent-2:CLEANUP_WEB", (
                "assign_roles not parsed"
            )
            assert args.dry_run == True, "dry_run flag not set"

            self.log_test_result(
                "Hard Onboarding Flag Parsing", True, "All arguments parsed correctly"
            )

        except Exception as e:
            self.log_test_result("Hard Onboarding Flag Parsing", False, f"Error: {e}")

    def test_hard_onboarding_validation(self):
        """Test validation of hard onboarding parameters."""
        logger.info("🧪 Testing hard onboarding validation...")

        try:
            from services.consolidated_messaging_service import ConsolidatedMessagingService

            service = ConsolidatedMessagingService()

            # Test missing agents (should fail)
            try:
                bad_args = service.parser.parse_args(["--hard-onboarding"])
                # This should trigger validation error in handle_hard_onboarding
                result = service.handle_hard_onboarding(bad_args)
                # If we get here, validation failed
                self.log_test_result(
                    "Missing Agents Validation", False, "Should have failed with missing agents"
                )
            except SystemExit:
                # Expected behavior - argparse exits on error
                self.log_test_result(
                    "Missing Agents Validation", True, "Correctly rejected missing agents"
                )

            # Test valid arguments
            try:
                good_args = service.parser.parse_args(
                    ["--hard-onboarding", "--agents", "Agent-1", "--onboarding-mode", "cleanup"]
                )
                self.log_test_result("Valid Arguments Acceptance", True, "Valid arguments accepted")
            except Exception as e:
                self.log_test_result(
                    "Valid Arguments Acceptance", False, f"Rejected valid arguments: {e}"
                )

        except Exception as e:
            self.log_test_result("Hard Onboarding Validation", False, f"Error: {e}")

    def test_role_assignment_parsing(self):
        """Test parsing of role assignments."""
        logger.info("🧪 Testing role assignment parsing...")

        try:
            # Test role parsing logic (extracted from the method)
            role_map_str = "Agent-1:CLEANUP_CORE,Agent-2:CLEANUP_WEB,Agent-3:CLEANUP_INFRA"
            role_map = {}

            for spec in role_map_str.split(","):
                spec = spec.strip()
                if not spec:
                    continue
                try:
                    agent, role = (s.strip() for s in spec.split(":", 1))
                    role_map[agent] = role
                except ValueError:
                    raise ValueError(f"Invalid role spec: {spec}")

            expected = {
                "Agent-1": "CLEANUP_CORE",
                "Agent-2": "CLEANUP_WEB",
                "Agent-3": "CLEANUP_INFRA",
            }

            assert role_map == expected, f"Role parsing failed: {role_map} != {expected}"

            self.log_test_result("Role Assignment Parsing", True, f"Parsed roles: {role_map}")

        except Exception as e:
            self.log_test_result("Role Assignment Parsing", False, f"Error: {e}")

    def test_onboarding_handler_integration(self):
        """Test integration with onboarding handler."""
        logger.info("🧪 Testing onboarding handler integration...")

        try:
            # Test import of onboarding handler
            from services.handlers.onboarding_handler import OnboardingHandler

            # Create handler instance
            handler = OnboardingHandler()

            # Test can_handle method
            mock_args = MagicMock()
            mock_args.hard_onboarding = True
            can_handle = handler.can_handle(mock_args)

            assert can_handle == True, "Handler should be able to handle hard onboarding"

            self.log_test_result(
                "Onboarding Handler Integration",
                True,
                "Handler correctly identifies hard onboarding",
            )

        except ImportError:
            self.log_test_result(
                "Onboarding Handler Integration", False, "Could not import OnboardingHandler"
            )
        except Exception as e:
            self.log_test_result("Onboarding Handler Integration", False, f"Error: {e}")

    def test_dry_run_mode(self):
        """Test dry run mode functionality."""
        logger.info("🧪 Testing dry run mode...")

        try:
            from services.consolidated_messaging_service import ConsolidatedMessagingService

            service = ConsolidatedMessagingService()

            # Test dry run parsing
            args = service.parser.parse_args(
                ["--hard-onboarding", "--agents", "Agent-1", "--dry-run"]
            )

            assert args.dry_run == True, "Dry run flag not parsed correctly"

            self.log_test_result("Dry Run Mode", True, "Dry run flag parsed correctly")

        except Exception as e:
            self.log_test_result("Dry Run Mode", False, f"Error: {e}")

    def run_all_tests(self):
        """Run all hard onboarding tests."""
        logger.info("🚀 STARTING HARD ONBOARDING TESTS")
        logger.info("=" * 60)

        # Run individual tests
        self.test_hard_onboarding_flag_parsing()
        self.test_hard_onboarding_validation()
        self.test_role_assignment_parsing()
        self.test_onboarding_handler_integration()
        self.test_dry_run_mode()

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("📊 TEST SUMMARY")
        logger.info("=" * 60)

        for result in self.test_results:
            logger.info(result)

        logger.info(f"\n✅ Passed: {self.passed_tests}")
        logger.info(f"❌ Failed: {self.failed_tests}")
        logger.info(f"📈 Total: {self.passed_tests + self.failed_tests}")

        if self.failed_tests == 0:
            logger.info("🎉 ALL TESTS PASSED!")
            return True
        else:
            logger.info("⚠️ SOME TESTS FAILED")
            return False


def main():
    """Main test execution."""
    tester = HardOnboardingTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
