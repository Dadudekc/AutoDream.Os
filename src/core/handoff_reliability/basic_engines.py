from __future__ import annotations

import asyncio
import time
from typing import List, Awaitable, Callable

from .metrics import TestResult, TestSession, TestConfiguration
from .evaluation import calculate_test_results, create_error_result
from .simulations import (
    simulate_handoff_execution,
    simulate_stressed_handoff_execution,
    simulate_failure_injection_handoff,
)


async def _run_iterations(
    cfg: TestConfiguration,
    simulate: Callable[[TestConfiguration, int], Awaitable[bool]],
    logger,
    description: str,
    progress_interval: int = 10,
) -> tuple[int, int, int, List[float]]:
    succ = fail = timeout = 0
    durations: List[float] = []
    for i in range(cfg.iterations):
        start = time.time()
        try:
            if await simulate(cfg, i):
                succ += 1
            else:
                fail += 1
            durations.append(time.time() - start)
            if (i + 1) % progress_interval == 0:
                logger.info(f"📊 {description} progress: {i + 1}/{cfg.iterations}")
        except asyncio.TimeoutError:
            timeout += 1
            durations.append(cfg.timeout)
        except Exception:
            fail += 1
            durations.append(time.time() - start)
    return succ, fail, timeout, durations


async def run_reliability_test(session: TestSession, logger) -> TestResult:
    try:
        cfg = session.test_config
        logger.info(f"🧪 Running reliability test: {cfg.iterations} iterations")
        start = time.time()
        s, f, t, d = await _run_iterations(cfg, lambda c, i: simulate_handoff_execution(c), logger, "Reliability test")
        end = time.time()
        return calculate_test_results(cfg, start, end, end - start, s, f, t, d)
    except Exception as e:
        logger.error(f"Reliability test failed: {e}")
        return create_error_result(session.test_config, str(e))


async def run_performance_test(session: TestSession, logger) -> TestResult:
    try:
        cfg = session.test_config
        logger.info(f"🧪 Running performance test: {cfg.iterations} iterations")
        start = time.time()
        s, f, t, d = await _run_iterations(cfg, lambda c, i: simulate_handoff_execution(c), logger, "Performance test")
        end = time.time()
        return calculate_test_results(cfg, start, end, end - start, s, f, t, d)
    except Exception as e:
        logger.error(f"Performance test failed: {e}")
        return create_error_result(session.test_config, str(e))


async def run_stress_test(session: TestSession, logger) -> TestResult:
    try:
        cfg = session.test_config
        logger.info(
            f"🧪 Running stress test: {cfg.iterations} iterations (stress factor: {cfg.stress_factor})"
        )
        start = time.time()
        s, f, t, d = await _run_iterations(
            cfg,
            lambda c, i: simulate_stressed_handoff_execution(c),
            logger,
            "Stress test",
        )
        end = time.time()
        return calculate_test_results(cfg, start, end, end - start, s, f, t, d)
    except Exception as e:
        logger.error(f"Stress test failed: {e}")
        return create_error_result(session.test_config, str(e))


async def run_failure_injection_test(session: TestSession, logger) -> TestResult:
    try:
        cfg = session.test_config
        logger.info(
            f"🧪 Running failure injection test: {cfg.iterations} iterations (failure rate: {cfg.failure_rate:.1%})"
        )
        start = time.time()
        s, f, t, d = await _run_iterations(
            cfg,
            lambda c, i: simulate_failure_injection_handoff(c),
            logger,
            "Failure injection test",
        )
        end = time.time()
        return calculate_test_results(cfg, start, end, end - start, s, f, t, d)
    except Exception as e:
        logger.error(f"Failure injection test failed: {e}")
        return create_error_result(session.test_config, str(e))
