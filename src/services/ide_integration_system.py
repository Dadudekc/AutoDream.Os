#!/usr/bin/env python3
"""
IDE Integration System
====================

Comprehensive IDE integration system for PyAutoGUI automation, coordinate testing,
and real-time development environment management.

Author: Agent-7 (Web Development Expert / Implementation Specialist)
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy import to prevent hard dependency
try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    pyautogui = None
    pyperclip = None
    PYAUTOGUI_AVAILABLE = False


class IDEIntegrationSystem:
    """Comprehensive IDE integration system for development automation."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.coordinates_file = self.project_root / "config/coordinates.json"
        self.pyautogui_available = PYAUTOGUI_AVAILABLE

        if self.pyautogui_available:
            # Configure PyAutoGUI settings
            pyautogui.PAUSE = 0.1
            pyautogui.FAILSAFE = True

        logger.info("IDEIntegrationSystem initialized")

    def load_agent_coordinates(self) -> dict[str, Any]:
        """Load agent coordinates from configuration file."""
        try:
            with open(self.coordinates_file) as f:
                coordinates = json.load(f)
            logger.info(f"Loaded coordinates for {len(coordinates.get('agents', {}))} agents")
            return coordinates
        except Exception as e:
            logger.error(f"Error loading coordinates: {e}")
            return {}

    def test_agent_coordinates(self, agent_id: str) -> dict[str, Any]:
        """Test agent coordinates for accessibility and accuracy."""
        if not self.pyautogui_available:
            return {"status": "error", "message": "PyAutoGUI not available", "agent_id": agent_id}

        try:
            coordinates_data = self.load_agent_coordinates()
            agents = coordinates_data.get("agents", {})

            if agent_id not in agents:
                return {
                    "status": "error",
                    "message": f"Agent {agent_id} not found in coordinates",
                    "agent_id": agent_id,
                }

            agent_data = agents[agent_id]
            chat_coords = agent_data.get("chat_input_coordinates", [])

            if not chat_coords or len(chat_coords) != 2:
                return {
                    "status": "error",
                    "message": f"Invalid coordinates for {agent_id}",
                    "agent_id": agent_id,
                    "coordinates": chat_coords,
                }

            x, y = chat_coords

            # Test coordinate accessibility
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.2)

            # Get current mouse position to verify
            current_pos = pyautogui.position()

            # Check if position is accessible (within reasonable range)
            distance = ((current_pos.x - x) ** 2 + (current_pos.y - y) ** 2) ** 0.5
            accessible = distance < 5  # Allow 5 pixel tolerance

            return {
                "status": "success" if accessible else "warning",
                "agent_id": agent_id,
                "coordinates": chat_coords,
                "target_position": [x, y],
                "actual_position": [current_pos.x, current_pos.y],
                "distance": round(distance, 2),
                "accessible": accessible,
                "message": "Coordinates accessible"
                if accessible
                else "Coordinates may need adjustment",
            }

        except Exception as e:
            logger.error(f"Error testing coordinates for {agent_id}: {e}")
            return {
                "status": "error",
                "message": f"Error testing coordinates: {e}",
                "agent_id": agent_id,
            }

    def send_test_message(self, agent_id: str, message: str = None) -> dict[str, Any]:
        """Send test message to agent coordinates."""
        if not self.pyautogui_available:
            return {"status": "error", "message": "PyAutoGUI not available"}

        try:
            coordinates_data = self.load_agent_coordinates()
            agents = coordinates_data.get("agents", {})

            if agent_id not in agents:
                return {"status": "error", "message": f"Agent {agent_id} not found"}

            agent_data = agents[agent_id]
            chat_coords = agent_data.get("chat_input_coordinates", [])

            if not chat_coords:
                return {"status": "error", "message": f"No coordinates found for {agent_id}"}

            x, y = chat_coords

            # Default test message if none provided
            if not message:
                message = f"IDE Integration Test Message - {agent_id} - {datetime.now().strftime('%H:%M:%S')}"

            # Focus on agent window
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            time.sleep(0.5)

            # Clear input area
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.1)
            pyautogui.press("delete")
            time.sleep(0.1)

            # Send message
            if pyperclip:
                pyperclip.copy(message)
                time.sleep(0.2)
                pyautogui.hotkey("ctrl", "v")
            else:
                pyautogui.typewrite(message, interval=0.01)

            time.sleep(0.2)
            pyautogui.press("enter")

            logger.info(f"Test message sent to {agent_id} at coordinates {chat_coords}")

            return {
                "status": "success",
                "agent_id": agent_id,
                "coordinates": chat_coords,
                "message": message,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error sending test message to {agent_id}: {e}")
            return {
                "status": "error",
                "message": f"Error sending message: {e}",
                "agent_id": agent_id,
            }

    def run_comprehensive_ide_test(self) -> dict[str, Any]:
        """Run comprehensive IDE integration test for all agents."""
        logger.info("Starting comprehensive IDE integration test")

        coordinates_data = self.load_agent_coordinates()
        agents = coordinates_data.get("agents", {})

        results = {
            "timestamp": datetime.now().isoformat(),
            "total_agents": len(agents),
            "tested_agents": 0,
            "successful_tests": 0,
            "failed_tests": 0,
            "agent_results": {},
            "overall_status": "unknown",
        }

        for agent_id, agent_data in agents.items():
            if not agent_data.get("active", False):
                continue

            logger.info(f"Testing {agent_id}")

            # Test coordinates
            coord_result = self.test_agent_coordinates(agent_id)
            results["agent_results"][agent_id] = {"coordinate_test": coord_result}

            # Only send test message if coordinates are accessible
            if coord_result.get("status") == "success":
                message_result = self.send_test_message(agent_id)
                results["agent_results"][agent_id]["message_test"] = message_result

                if message_result.get("status") == "success":
                    results["successful_tests"] += 1
                else:
                    results["failed_tests"] += 1
            else:
                results["failed_tests"] += 1
                results["agent_results"][agent_id]["message_test"] = {
                    "status": "skipped",
                    "reason": "Coordinates not accessible",
                }

            results["tested_agents"] += 1
            time.sleep(1)  # Brief pause between tests

        # Determine overall status
        if results["successful_tests"] == results["tested_agents"]:
            results["overall_status"] = "excellent"
        elif results["successful_tests"] > results["failed_tests"]:
            results["overall_status"] = "good"
        elif results["successful_tests"] > 0:
            results["overall_status"] = "fair"
        else:
            results["overall_status"] = "poor"

        logger.info(f"IDE integration test complete: {results['overall_status']}")
        return results

    def generate_ide_test_report(self, test_results: dict[str, Any]) -> str:
        """Generate comprehensive IDE test report."""
        report = f"""# IDE Integration Test Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Overall Status**: {test_results['overall_status'].upper()}
**Total Agents**: {test_results['total_agents']}
**Tested Agents**: {test_results['tested_agents']}
**Successful Tests**: {test_results['successful_tests']}
**Failed Tests**: {test_results['failed_tests']}

## Agent Test Results

"""

        for agent_id, agent_result in test_results["agent_results"].items():
            coord_test = agent_result.get("coordinate_test", {})
            message_test = agent_result.get("message_test", {})

            report += f"### {agent_id}\n"
            report += f"- **Coordinates**: {coord_test.get('coordinates', 'N/A')}\n"
            report += f"- **Coordinate Test**: {coord_test.get('status', 'unknown')}\n"
            report += f"- **Message Test**: {message_test.get('status', 'unknown')}\n"

            if coord_test.get("message"):
                report += f"- **Note**: {coord_test['message']}\n"

            report += "\n"

        report += f"""## Summary

- **PyAutoGUI Available**: {'Yes' if self.pyautogui_available else 'No'}
- **Integration Score**: {self._calculate_integration_score(test_results):.1f}%
- **Recommendations**: {self._generate_recommendations(test_results)}

---
*Report generated by IDE Integration System*
"""

        return report

    def _calculate_integration_score(self, test_results: dict[str, Any]) -> float:
        """Calculate overall integration score."""
        if test_results["tested_agents"] == 0:
            return 0.0

        success_rate = test_results["successful_tests"] / test_results["tested_agents"]
        return success_rate * 100

    def _generate_recommendations(self, test_results: dict[str, Any]) -> str:
        """Generate recommendations based on test results."""
        if test_results["overall_status"] == "excellent":
            return "All systems operational. No recommendations needed."
        elif test_results["overall_status"] == "good":
            return "Minor issues detected. Review failed tests for optimization."
        elif test_results["overall_status"] == "fair":
            return "Several issues detected. Coordinate adjustments may be needed."
        else:
            return "Major issues detected. Comprehensive review and fixes required."


def main():
    """Main function for IDE integration system."""
    print("🖥️ IDE Integration System")
    print("=" * 40)

    ide_system = IDEIntegrationSystem()

    if not ide_system.pyautogui_available:
        print("❌ PyAutoGUI not available")
        print("Install with: pip install pyautogui pyperclip")
        return

    print("✅ PyAutoGUI available")

    # Run comprehensive test
    print("\n🧪 Running comprehensive IDE integration test...")
    test_results = ide_system.run_comprehensive_ide_test()

    # Generate and display report
    report = ide_system.generate_ide_test_report(test_results)
    print(f"\n📊 Test Results: {test_results['overall_status'].upper()}")
    print(f"Integration Score: {ide_system._calculate_integration_score(test_results):.1f}%")

    # Save report
    report_file = ide_system.project_root / "ide_integration_test_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"📄 Report saved: {report_file}")
    print("\n✅ IDE integration test complete!")


if __name__ == "__main__":
    main()
