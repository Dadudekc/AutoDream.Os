from __future__ import annotations

import asyncio
import random

from .metrics import TestConfiguration


async def simulate_handoff_execution(config: TestConfiguration) -> bool:
    """Simulate a basic handoff execution."""
    await asyncio.sleep(0.1)
    return random.random() < 0.95


async def simulate_stressed_handoff_execution(config: TestConfiguration) -> bool:
    """Simulate a handoff execution under stress."""
    stress_duration = 0.1 * config.stress_factor
    await asyncio.sleep(stress_duration)
    base_success_rate = 0.95
    stress_penalty = min(0.2, (config.stress_factor - 1.0) * 0.1)
    success_rate = max(0.5, base_success_rate - stress_penalty)
    return random.random() < success_rate


async def simulate_failure_injection_handoff(config: TestConfiguration) -> bool:
    """Simulate a handoff execution with failure injection."""
    await asyncio.sleep(0.1)
    if random.random() < config.failure_rate:
        return False
    return random.random() < 0.95


async def simulate_concurrent_handoff(config: TestConfiguration) -> bool:
    """Simulate a concurrent handoff execution."""
    await asyncio.sleep(0.05)
    return random.random() < 0.90


async def simulate_endurance_handoff_execution(
    config: TestConfiguration, iteration: int
) -> bool:
    """Simulate a handoff execution for endurance testing."""
    base_duration = 0.1
    degradation_factor = 1.0 + (iteration / config.iterations) * 0.5
    await asyncio.sleep(base_duration * degradation_factor)
    base_success_rate = 0.95
    degradation_penalty = (iteration / config.iterations) * 0.1
    success_rate = max(0.8, base_success_rate - degradation_penalty)
    return random.random() < success_rate
