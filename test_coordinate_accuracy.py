#!/usr/bin/env python3
"""
PyAutoGUI Coordinate Accuracy Test Script
=========================================

Tests coordinate targeting, cursor positioning, and click accuracy for dual-monitor setup.
Identifies potential failures and routing issues in messaging_pyautogui.py.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import sys
import time
import json
from pathlib import Path
from typing import Dict, Tuple, List, Optional
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_coordinate_loading():
    """Test coordinate loading from SSOT."""
    logger.info("🔍 Testing coordinate loading...")

    try:
        from src.core.coordinate_loader import get_coordinate_loader

        loader = get_coordinate_loader()
        all_agents = loader.get_all_agents()

        logger.info(f"📊 Found {len(all_agents)} agents in coordinate system")
        logger.info(f"📋 Agents: {all_agents}")

        # Test each agent's coordinates
        issues = []
        for agent_id in all_agents:
            try:
                coords = loader.get_chat_coordinates(agent_id)
                logger.info(f"✅ {agent_id}: {coords}")

                # Validate coordinate bounds
                x, y = coords
                if x < -2000 or x > 2000:
                    issues.append(f"{agent_id}: X coordinate {x} out of bounds (-2000, 2000)")
                if y < 0 or y > 1500:
                    issues.append(f"{agent_id}: Y coordinate {y} out of bounds (0, 1500)")

            except Exception as e:
                issues.append(f"{agent_id}: Failed to load coordinates - {e}")

        # Check agent activity status
        active_count = 0
        inactive_count = 0
        for agent_id in all_agents:
            try:
                if loader.is_agent_active(agent_id):
                    active_count += 1
                else:
                    inactive_count += 1
                    logger.warning(f"⚠️ {agent_id} is marked as inactive")
            except Exception as e:
                logger.error(f"❌ Failed to check activity status for {agent_id}: {e}")

        logger.info(f"📊 Active agents: {active_count}, Inactive agents: {inactive_count}")

        return issues

    except Exception as e:
        return [f"❌ Coordinate loading failed: {e}"]

def test_messaging_pyautogui_integration():
    """Test messaging_pyautogui integration."""
    logger.info("🔍 Testing messaging_pyautogui integration...")

    issues = []

    try:
        from src.core.messaging_pyautogui import (
            load_coordinates_from_json,
            get_agent_coordinates,
            PYAUTOGUI_AVAILABLE,
            PYPERCLIP_AVAILABLE
        )

        # Test dependency availability
        logger.info(f"🔧 PyAutoGUI available: {PYAUTOGUI_AVAILABLE}")
        logger.info(f"🔧 Pyperclip available: {PYPERCLIP_AVAILABLE}")

        if not PYAUTOGUI_AVAILABLE:
            issues.append("❌ PyAutoGUI not available - coordinate testing will fail")
        if not PYPERCLIP_AVAILABLE:
            issues.append("⚠️ Pyperclip not available - will fallback to typewrite")

        # Test coordinate loading
        coords_dict = load_coordinates_from_json()
        logger.info(f"📊 Loaded {len(coords_dict)} coordinate pairs")

        # Test individual coordinate retrieval
        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]:
            coords = get_agent_coordinates(agent_id)
            if coords:
                logger.info(f"✅ {agent_id} coordinates: {coords}")
            else:
                issues.append(f"❌ Failed to get coordinates for {agent_id}")

        return issues

    except Exception as e:
        return [f"❌ Messaging PyAutoGUI integration test failed: {e}"]

def test_coordinate_validation():
    """Test coordinate validation and bounds checking."""
    logger.info("🔍 Testing coordinate validation...")

    issues = []

    try:
        # Load coordinate data directly
        coord_file = Path("cursor_agent_coords.json")
        if not coord_file.exists():
            return ["❌ cursor_agent_coords.json not found"]

        with open(coord_file, 'r') as f:
            data = json.load(f)

        # Validate coordinate system configuration
        coord_system = data.get("coordinate_system", {})
        logger.info(f"📐 Coordinate system: {coord_system}")

        if not coord_system.get("multi_monitor_support", False):
            issues.append("⚠️ Multi-monitor support not enabled in coordinate system")

        # Validate each agent's coordinates
        agents = data.get("agents", {})
        validation_rules = data.get("validation_rules", {})

        bounds = validation_rules.get("coordinate_bounds", {})
        min_x = bounds.get("min_x", -2000)
        max_x = bounds.get("max_x", 2000)
        min_y = bounds.get("min_y", 0)
        max_y = bounds.get("max_y", 1500)

        logger.info(f"📏 Validation bounds: X({min_x}, {max_x}), Y({min_y}, {max_y})")

        for agent_id, agent_data in agents.items():
            chat_coords = agent_data.get("chat_input_coordinates", [])

            if len(chat_coords) != 2:
                issues.append(f"❌ {agent_id}: Invalid chat coordinates format")
                continue

            x, y = chat_coords

            # Check bounds
            if x < min_x or x > max_x:
                issues.append(f"❌ {agent_id}: X coordinate {x} out of bounds ({min_x}, {max_x})")
            if y < min_y or y > max_y:
                issues.append(f"❌ {agent_id}: Y coordinate {y} out of bounds ({min_y}, {max_y})")

            # Check for negative coordinates (dual monitor)
            if x < 0:
                logger.info(f"📺 {agent_id}: Left monitor coordinate ({x}, {y})")
            else:
                logger.info(f"🖥️ {agent_id}: Right monitor coordinate ({x}, {y})")

            # Check activity status
            if not agent_data.get("active", True):
                logger.warning(f"⚠️ {agent_id}: Marked as inactive - may cause routing failures")

        return issues

    except Exception as e:
        return [f"❌ Coordinate validation failed: {e}"]

def test_dual_monitor_detection():
    """Test dual-monitor coordinate system detection."""
    logger.info("🔍 Testing dual-monitor coordinate system...")

    issues = []

    try:
        # Analyze coordinate distribution
        coord_file = Path("cursor_agent_coords.json")
        with open(coord_file, 'r') as f:
            data = json.load(f)

        agents = data.get("agents", {})
        left_monitor_coords = []
        right_monitor_coords = []

        for agent_id, agent_data in agents.items():
            if not agent_data.get("active", True):
                continue

            chat_coords = agent_data.get("chat_input_coordinates", [])
            if len(chat_coords) == 2:
                x, y = chat_coords
                if x < 0:
                    left_monitor_coords.append((agent_id, x, y))
                else:
                    right_monitor_coords.append((agent_id, x, y))

        logger.info(f"📺 Left monitor agents: {len(left_monitor_coords)}")
        for agent_id, x, y in left_monitor_coords:
            logger.info(f"  • {agent_id}: ({x}, {y})")

        logger.info(f"🖥️ Right monitor agents: {len(right_monitor_coords)}")
        for agent_id, x, y in right_monitor_coords:
            logger.info(f"  • {agent_id}: ({x}, {y})")

        # Check for coordinate conflicts
        all_coords = left_monitor_coords + right_monitor_coords
        coord_dict = {}
        for agent_id, x, y in all_coords:
            coord_key = (x, y)
            if coord_key in coord_dict:
                issues.append(f"❌ Coordinate conflict: {agent_id} and {coord_dict[coord_key]} both at ({x}, {y})")
            else:
                coord_dict[coord_key] = agent_id

        # Check monitor balance
        total_agents = len(left_monitor_coords) + len(right_monitor_coords)
        if total_agents > 0:
            left_percentage = (len(left_monitor_coords) / total_agents) * 100
            right_percentage = (len(right_monitor_coords) / total_agents) * 100
            logger.info(f"⚖️ Monitor balance: Left {left_percentage:.1f}%, Right {right_percentage:.1f}%")

        return issues

    except Exception as e:
        return [f"❌ Dual-monitor detection failed: {e}"]

def analyze_routing_failures():
    """Analyze potential routing failure causes."""
    logger.info("🔍 Analyzing routing failure causes...")

    issues = []

    try:
        # Check for inactive agents that might cause routing issues
        coord_file = Path("cursor_agent_coords.json")
        with open(coord_file, 'r') as f:
            data = json.load(f)

        agents = data.get("agents", {})
        inactive_agents = []

        for agent_id, agent_data in agents.items():
            if not agent_data.get("active", True):
                inactive_agents.append(agent_id)
                issues.append(f"⚠️ {agent_id} is inactive - may cause routing failures if targeted")

        if inactive_agents:
            logger.warning(f"🚨 {len(inactive_agents)} inactive agents detected: {inactive_agents}")

        # Check coordinate loading robustness
        from src.core.coordinate_loader import get_coordinate_loader
        loader = get_coordinate_loader()

        # Test loading all agents
        all_agents = loader.get_all_agents()
        successful_loads = 0
        failed_loads = 0

        for agent_id in all_agents:
            try:
                coords = loader.get_chat_coordinates(agent_id)
                successful_loads += 1
            except Exception as e:
                failed_loads += 1
                issues.append(f"❌ Failed to load coordinates for {agent_id}: {e}")

        logger.info(f"📊 Coordinate loading: {successful_loads} successful, {failed_loads} failed")

        # Check messaging_pyautogui error handling
        try:
            from src.core.messaging_pyautogui import PYAUTOGUI_AVAILABLE, PYPERCLIP_AVAILABLE

            if not PYAUTOGUI_AVAILABLE:
                issues.append("❌ PyAutoGUI unavailable - will fallback to inbox delivery")
            if not PYPERCLIP_AVAILABLE:
                issues.append("⚠️ Pyperclip unavailable - will use typewrite instead of paste")

        except Exception as e:
            issues.append(f"❌ Failed to check messaging dependencies: {e}")

        return issues

    except Exception as e:
        return [f"❌ Routing failure analysis failed: {e}"]

def main():
    """Run all coordinate accuracy tests."""
    logger.info("🚀 Starting PyAutoGUI Coordinate Accuracy Audit")
    logger.info("=" * 60)

    all_issues = []

    # Test 1: Coordinate Loading
    logger.info("\n" + "="*40)
    logger.info("TEST 1: COORDINATE LOADING")
    logger.info("="*40)
    issues = test_coordinate_loading()
    all_issues.extend(issues)

    # Test 2: Messaging Integration
    logger.info("\n" + "="*40)
    logger.info("TEST 2: MESSAGING INTEGRATION")
    logger.info("="*40)
    issues = test_messaging_pyautogui_integration()
    all_issues.extend(issues)

    # Test 3: Coordinate Validation
    logger.info("\n" + "="*40)
    logger.info("TEST 3: COORDINATE VALIDATION")
    logger.info("="*40)
    issues = test_coordinate_validation()
    all_issues.extend(issues)

    # Test 4: Dual Monitor Detection
    logger.info("\n" + "="*40)
    logger.info("TEST 4: DUAL-MONITOR DETECTION")
    logger.info("="*40)
    issues = test_dual_monitor_detection()
    all_issues.extend(issues)

    # Test 5: Routing Failure Analysis
    logger.info("\n" + "="*40)
    logger.info("TEST 5: ROUTING FAILURE ANALYSIS")
    logger.info("="*40)
    issues = analyze_routing_failures()
    all_issues.extend(issues)

    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 AUDIT SUMMARY")
    logger.info("="*60)

    if all_issues:
        logger.warning(f"🚨 Found {len(all_issues)} issues:")
        for i, issue in enumerate(all_issues, 1):
            logger.warning(f"{i:2d}. {issue}")
    else:
        logger.info("✅ No issues found - coordinate system appears healthy")

    # Recommendations
    logger.info("\n📋 RECOMMENDATIONS:")
    if any("inactive" in issue for issue in all_issues):
        logger.info("• Review inactive agent status in cursor_agent_coords.json")
    if any("bounds" in issue for issue in all_issues):
        logger.info("• Update coordinate bounds in validation_rules")
    if any("PyAutoGUI" in issue for issue in all_issues):
        logger.info("• Ensure PyAutoGUI is properly installed and configured")
    if any("routing" in issue for issue in all_issues):
        logger.info("• Review coordinate accuracy and agent activity status")

    logger.info("\n🎯 Audit completed successfully!")

    return len(all_issues)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
