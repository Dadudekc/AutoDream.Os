#!/usr/bin/env python3
"""
Test Concurrent Messaging Race Condition Fix
============================================

Tests that multiple agents can send messages simultaneously
without race conditions or misrouting.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13 (Race Condition Fix Test)
"""

import logging
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_message_subprocess(agent_id: str, message: str, index: int) -> dict:
    """
    Send message via subprocess (simulates real multi-agent usage).

    Args:
        agent_id: Target agent ID
        message: Message content
        index: Message index for tracking

    Returns:
        Result dictionary with status and timing
    """
    start_time = time.time()

    try:
        cmd = [
            "python",
            "-m",
            "src.services.messaging_cli",
            "--agent",
            agent_id,
            "--message",
            f"{message} (Test #{index})",
            "--priority",
            "regular",
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(Path(__file__).parent.parent),
        )

        elapsed = time.time() - start_time

        return {
            "success": result.returncode == 0,
            "agent": agent_id,
            "index": index,
            "elapsed": elapsed,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "success": False,
            "agent": agent_id,
            "index": index,
            "elapsed": elapsed,
            "error": str(e),
        }


def test_concurrent_messaging_basic():
    """
    Test basic concurrent messaging (3 agents, 2 messages each).

    Expected: All messages delivered successfully without misrouting.
    """
    logger.info("🧪 TEST 1: Basic Concurrent Messaging (3 agents, 2 messages each)")

    test_agents = ["Agent-1", "Agent-2", "Agent-3"]
    messages_per_agent = 2

    tasks = []
    for agent in test_agents:
        for i in range(messages_per_agent):
            tasks.append((agent, f"Concurrent test message from {agent}", i))

    results = []

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [
            executor.submit(send_message_subprocess, agent, msg, idx) for agent, msg, idx in tasks
        ]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            status = "✅" if result["success"] else "❌"
            logger.info(
                f"{status} {result['agent']} msg #{result['index']}: " f"{result['elapsed']:.2f}s"
            )

    # Verify results
    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)

    logger.info(f"\n📊 Results: {success_count}/{total_count} messages sent successfully")

    if success_count == total_count:
        logger.info("✅ TEST 1 PASSED: All messages sent successfully!")
        return True
    else:
        logger.error(f"❌ TEST 1 FAILED: {total_count - success_count} messages failed")
        return False


def test_concurrent_messaging_stress():
    """
    Test stress scenario (8 agents, 5 messages each).

    Expected: All messages delivered successfully under load.
    """
    logger.info("\n🧪 TEST 2: Stress Test (8 agents, 5 messages each)")

    test_agents = [f"Agent-{i}" for i in range(1, 9)]
    messages_per_agent = 5

    tasks = []
    for agent in test_agents:
        for i in range(messages_per_agent):
            tasks.append((agent, f"Stress test message from {agent}", i))

    results = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [
            executor.submit(send_message_subprocess, agent, msg, idx) for agent, msg, idx in tasks
        ]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            status = "✅" if result["success"] else "❌"
            logger.info(
                f"{status} {result['agent']} msg #{result['index']}: " f"{result['elapsed']:.2f}s"
            )

    total_time = time.time() - start_time

    # Verify results
    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    avg_time = sum(r["elapsed"] for r in results) / len(results)

    logger.info("\n📊 Results:")
    logger.info(f"  • Success: {success_count}/{total_count} messages")
    logger.info(f"  • Total time: {total_time:.2f}s")
    logger.info(f"  • Avg time per message: {avg_time:.2f}s")

    if success_count == total_count:
        logger.info("✅ TEST 2 PASSED: All messages sent successfully under stress!")
        return True
    else:
        logger.error(f"❌ TEST 2 FAILED: {total_count - success_count} messages failed")
        return False


def test_message_routing_accuracy():
    """
    Test message routing accuracy (verify messages go to correct agents).

    Expected: Each agent receives only their intended messages.
    """
    logger.info("\n🧪 TEST 3: Message Routing Accuracy")

    # Clear inboxes first
    logger.info("📭 Clearing agent inboxes...")
    for i in range(1, 4):
        inbox_file = Path(f"agent_workspaces/Agent-{i}/inbox/Agent-{i}_inbox.txt")
        if inbox_file.exists():
            inbox_file.write_text("", encoding="utf-8")

    # Send unique messages to each agent
    test_data = [
        ("Agent-1", "UNIQUE_MESSAGE_FOR_AGENT_1", 1),
        ("Agent-2", "UNIQUE_MESSAGE_FOR_AGENT_2", 2),
        ("Agent-3", "UNIQUE_MESSAGE_FOR_AGENT_3", 3),
    ]

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(send_message_subprocess, agent, msg, idx)
            for agent, msg, idx in test_data
        ]

        for future in as_completed(futures):
            result = future.result()
            status = "✅" if result["success"] else "❌"
            logger.info(f"{status} Sent to {result['agent']}")

    time.sleep(1)  # Allow messages to be written

    # Verify routing
    routing_correct = True

    for agent_id, expected_msg, _ in test_data:
        inbox_file = Path(f"agent_workspaces/{agent_id}/inbox/{agent_id}_inbox.txt")

        if inbox_file.exists():
            content = inbox_file.read_text(encoding="utf-8")

            if expected_msg in content:
                logger.info(f"✅ {agent_id} received correct message")
            else:
                logger.error(f"❌ {agent_id} did NOT receive correct message!")
                routing_correct = False

            # Check for wrong messages
            for other_agent, other_msg, _ in test_data:
                if other_agent != agent_id and other_msg in content:
                    logger.error(
                        f"❌ {agent_id} received message for {other_agent}! "
                        "(RACE CONDITION DETECTED)"
                    )
                    routing_correct = False
        else:
            logger.warning(f"⚠️ No inbox file for {agent_id}")

    if routing_correct:
        logger.info("✅ TEST 3 PASSED: All messages routed correctly!")
        return True
    else:
        logger.error("❌ TEST 3 FAILED: Message misrouting detected!")
        return False


def main():
    """Run all concurrent messaging tests."""
    logger.info("=" * 60)
    logger.info("🧪 CONCURRENT MESSAGING RACE CONDITION FIX TESTS")
    logger.info("=" * 60)

    results = []

    # Test 1: Basic concurrent messaging
    results.append(("Basic Concurrent", test_concurrent_messaging_basic()))

    # Test 2: Stress test
    results.append(("Stress Test", test_concurrent_messaging_stress()))

    # Test 3: Routing accuracy
    results.append(("Routing Accuracy", test_message_routing_accuracy()))

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 60)

    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"{test_name}: {status}")

    all_passed = all(passed for _, passed in results)

    if all_passed:
        logger.info("\n🎉 ALL TESTS PASSED! Race condition fix is working!")
        return 0
    else:
        logger.error("\n❌ SOME TESTS FAILED! Review the output above.")
        return 1


if __name__ == "__main__":
    exit(main())
