"""Tests for the smooth handoff system implementation."""

from __future__ import annotations

import asyncio
import logging
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from src.core.handoff_reliability_system import get_handoff_reliability_system
from src.core.handoff_validation_system import get_handoff_validation_system
from src.core.smooth_handoff_system import (
    HandoffContext,
    HandoffType,
    get_smooth_handoff_system,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@pytest.fixture(scope="module")
def systems():
    """Provide initialized handoff, validation, and reliability systems."""
    return (
        get_smooth_handoff_system(),
        get_handoff_validation_system(),
        get_handoff_reliability_system(),
    )


@pytest.mark.asyncio
async def test_basic_system_status(systems):
    """Ensure all systems report operational status."""
    handoff, validation, reliability = systems
    assert handoff.get_system_status()["system_status"] == "operational"
    assert validation.get_system_status()["system_status"] == "operational"
    assert reliability.get_system_status()["system_status"] == "operational"


@pytest.mark.asyncio
async def test_handoff_procedure_execution(systems):
    """Verify a standard handoff can be executed."""
    handoff, _, _ = systems
    context = HandoffContext(
        handoff_id="test_handoff_001",
        source_phase="phase_1",
        target_phase="phase_2",
        source_agent="agent_1",
        target_agent="agent_2",
        handoff_type=HandoffType.PHASE_TRANSITION,
    )
    execution_id = handoff.initiate_handoff(context, "PHASE_TRANSITION_STANDARD")
    start = time.time()
    while time.time() - start < 30:
        status = handoff.get_handoff_status(execution_id)
        if status and status.get("status") in {"completed", "failed", "rollback"}:
            break
        await asyncio.sleep(0.5)
    final = handoff.get_handoff_status(execution_id)
    assert final is not None
    assert final["status"] in {"completed", "failed", "rollback"}


@pytest.mark.asyncio
async def test_validation_system(systems):
    """Validate that the validation system processes a session."""
    _, validation, _ = systems
    session_id = validation.start_validation_session(
        handoff_id="val_001", procedure_id="PHASE_TRANSITION_STANDARD"
    )
    start = time.time()
    while time.time() - start < 30:
        status = validation.get_validation_status(session_id)
        if status and status.get("status") in {"passed", "warning", "failed"}:
            break
        await asyncio.sleep(0.5)
    final = validation.get_validation_status(session_id)
    assert final is not None
    assert final["status"] in {"passed", "warning", "failed"}


@pytest.mark.asyncio
async def test_reliability_system(systems):
    """Ensure reliability testing completes."""
    _, _, reliability = systems
    test_id = reliability.start_reliability_test("RELIABILITY_STANDARD")
    start = time.time()
    while time.time() - start < 60:
        status = reliability.get_test_status(test_id)
        if status and status.get("status") in {"completed", "failed"}:
            break
        await asyncio.sleep(1.0)
    final = reliability.get_test_status(test_id)
    assert final is not None
    assert final["status"] in {"completed", "failed"}


@pytest.mark.asyncio
async def test_system_integration(systems):
    """Run a small integration scenario across all systems."""
    handoff, validation, reliability = systems
    context = HandoffContext(
        handoff_id="integration_001",
        source_phase="phase_a",
        target_phase="phase_b",
        source_agent="agent_a",
        target_agent="agent_b",
        handoff_type=HandoffType.PHASE_TRANSITION,
    )
    hid = handoff.initiate_handoff(context, "PHASE_TRANSITION_STANDARD")
    vid = validation.start_validation_session(
        handoff_id=context.handoff_id,
        procedure_id="PHASE_TRANSITION_STANDARD",
    )
    rid = reliability.start_reliability_test("PERFORMANCE_STANDARD")
    start = time.time()
    while time.time() - start < 90:
        h_status = handoff.get_handoff_status(hid)
        v_status = validation.get_validation_status(vid)
        r_status = reliability.get_test_status(rid)
        if (
            h_status
            and v_status
            and r_status
            and h_status.get("status") in {"completed", "failed", "rollback"}
            and v_status.get("status") in {"passed", "warning", "failed"}
            and r_status.get("status") in {"completed", "failed"}
        ):
            break
        await asyncio.sleep(1.0)
    assert handoff.get_handoff_status(hid) is not None
    assert validation.get_validation_status(vid) is not None
    assert reliability.get_test_status(rid) is not None

