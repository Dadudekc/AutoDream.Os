#!/usr/bin/env python3
"""
Discord Commander Test Suite
============================

Simple test runner for Discord commander functionality.
Tests all slash commands and user experience without requiring a live Discord app.

Usage:
    python test_discord_commander.py                    # Run all tests
    python test_discord_commander.py --quick           # Run quick tests only
    python test_discord_commander.py --user-experience # Run user experience tests only
    python test_discord_commander.py --e2e             # Run E2E tests only

Author: Agent-7 (Web Development Specialist)
Date: 2025-01-16
Version: 1.0.0
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add tests to path for imports
sys.path.insert(0, str(Path(__file__).parent / "tests"))

from discord_user_experience_simulator import UserExperienceTester
from discord_e2e_testing_framework import DiscordE2ETestingFramework

logger = logging.getLogger(__name__)


class DiscordCommanderTestRunner:
    """Main test runner for Discord commander functionality."""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.DiscordCommanderTestRunner")
        self.test_results = {}
    
    async def run_quick_tests(self) -> Dict[str, Any]:
        """Run quick tests to verify basic functionality."""
        self.logger.info("⚡ Running Quick Tests...")
        
        from discord_user_experience_simulator import DiscordCommandSimulator
        
        simulator = DiscordCommandSimulator()
        
        # Test basic commands
        quick_commands = [
            ("ping", {}),
            ("commands", {}),
            ("agents", {}),
            ("status", {}),
            ("send", {"agent": "Agent-1", "message": "Quick test"}),
        ]
        
        results = []
        for command, params in quick_commands:
            response = await simulator.simulate_command(command, params)
            results.append({
                "command": command,
                "success": response.success,
                "response_length": len(response.response_text),
                "execution_time": response.execution_time
            })
        
        success_rate = sum(1 for r in results if r["success"]) / len(results)
        
        return {
            "test_type": "quick",
            "commands_tested": len(results),
            "success_rate": success_rate,
            "results": results,
            "status": "PASSED" if success_rate == 1.0 else "FAILED"
        }
    
    async def run_user_experience_tests(self) -> Dict[str, Any]:
        """Run comprehensive user experience tests."""
        self.logger.info("👤 Running User Experience Tests...")
        
        tester = UserExperienceTester()
        
        # Run all UX tests
        onboarding_results = await tester.test_new_user_onboarding()
        advanced_results = await tester.test_advanced_user_workflow()
        error_results = await tester.test_error_recovery_scenarios()
        performance_results = await tester.test_performance_under_load()
        
        return {
            "test_type": "user_experience",
            "onboarding": onboarding_results,
            "advanced_workflow": advanced_results,
            "error_recovery": error_results,
            "performance": performance_results,
            "overall_success": all([
                onboarding_results["success_rate"] >= 0.8,
                advanced_results["success_rate"] >= 0.8,
                performance_results["performance_rating"] in ["Excellent", "Good"]
            ])
        }
    
    async def run_e2e_tests(self) -> Dict[str, Any]:
        """Run comprehensive E2E tests."""
        self.logger.info("🧪 Running E2E Tests...")
        
        framework = DiscordE2ETestingFramework()
        e2e_results = await framework.run_all_e2e_tests()
        
        return {
            "test_type": "e2e",
            "results": e2e_results,
            "overall_success": e2e_results.get("summary", {}).get("success_rate", 0) >= 80
        }
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all available tests."""
        self.logger.info("🚀 Running All Discord Commander Tests...")
        
        start_time = datetime.now()
        
        # Run all test suites
        quick_results = await self.run_quick_tests()
        ux_results = await self.run_user_experience_tests()
        e2e_results = await self.run_e2e_tests()
        
        total_time = (datetime.now() - start_time).total_seconds()
        
        # Compile comprehensive report
        report = {
            "test_suite": "discord_commander",
            "timestamp": datetime.now().isoformat(),
            "total_execution_time": total_time,
            "test_results": {
                "quick_tests": quick_results,
                "user_experience": ux_results,
                "e2e_tests": e2e_results
            },
            "summary": {
                "quick_tests_status": quick_results["status"],
                "ux_tests_success": ux_results["overall_success"],
                "e2e_tests_success": e2e_results["overall_success"],
                "overall_status": "PASSED" if all([
                    quick_results["status"] == "PASSED",
                    ux_results["overall_success"],
                    e2e_results["overall_success"]
                ]) else "FAILED"
            }
        }
        
        return report
    
    def print_summary(self, results: Dict[str, Any]):
        """Print test summary."""
        print("\n" + "="*60)
        print("🎯 DISCORD COMMANDER TEST SUMMARY")
        print("="*60)
        
        summary = results.get("summary", {})
        test_results = results.get("test_results", {})
        
        print(f"📊 Overall Status: {summary.get('overall_status', 'UNKNOWN')}")
        print(f"⏱️  Total Time: {results.get('total_execution_time', 0):.2f}s")
        print()
        
        # Quick tests
        quick = test_results.get("quick_tests", {})
        print(f"⚡ Quick Tests: {quick.get('status', 'UNKNOWN')}")
        print(f"   Commands: {quick.get('commands_tested', 0)} tested")
        print(f"   Success Rate: {quick.get('success_rate', 0)*100:.1f}%")
        print()
        
        # User Experience tests
        ux = test_results.get("user_experience", {})
        print(f"👤 User Experience: {'✅ PASSED' if ux.get('overall_success') else '❌ FAILED'}")
        onboarding = ux.get("onboarding", {})
        performance = ux.get("performance", {})
        print(f"   New User Success: {onboarding.get('success_rate', 0)*100:.1f}%")
        print(f"   Performance Rating: {performance.get('performance_rating', 'Unknown')}")
        print()
        
        # E2E tests
        e2e = test_results.get("e2e_tests", {})
        print(f"🧪 E2E Tests: {'✅ PASSED' if e2e.get('overall_success') else '❌ FAILED'}")
        e2e_summary = e2e.get("results", {}).get("summary", {})
        print(f"   Scenarios: {e2e_summary.get('successful_scenarios', 0)}/{e2e_summary.get('total_scenarios', 0)} passed")
        print(f"   Commands: {e2e_summary.get('successful_commands', 0)}/{e2e_summary.get('total_commands_tested', 0)} passed")
        print(f"   Success Rate: {e2e_summary.get('success_rate', 0):.1f}%")
        print()
        
        print("="*60)
        
        if summary.get('overall_status') == 'PASSED':
            print("🎉 ALL TESTS PASSED! Discord Commander is ready for production!")
        else:
            print("⚠️  Some tests failed. Review the detailed report for issues.")
        
        print("="*60)


async def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Discord Commander Test Suite")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only")
    parser.add_argument("--user-experience", action="store_true", help="Run user experience tests only")
    parser.add_argument("--e2e", action="store_true", help="Run E2E tests only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create test runner
    runner = DiscordCommanderTestRunner()
    
    print("🎮 Discord Commander Test Suite")
    print("=" * 40)
    
    # Run selected tests
    if args.quick:
        results = await runner.run_quick_tests()
        print(f"\n⚡ Quick Tests: {results['status']}")
        
    elif args.user_experience:
        results = await runner.run_user_experience_tests()
        print(f"\n👤 User Experience Tests: {'✅ PASSED' if results['overall_success'] else '❌ FAILED'}")
        
    elif args.e2e:
        results = await runner.run_e2e_tests()
        print(f"\n🧪 E2E Tests: {'✅ PASSED' if results['overall_success'] else '❌ FAILED'}")
        
    else:
        # Run all tests
        results = await runner.run_all_tests()
        runner.print_summary(results)
    
    # Save results
    report_file = Path("discord_commander_test_report.json")
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📊 Detailed report saved to: {report_file}")
    
    # Exit with appropriate code
    if isinstance(results, dict) and results.get("summary", {}).get("overall_status") == "PASSED":
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
