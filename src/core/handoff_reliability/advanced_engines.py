from __future__ import annotations

import asyncio
import time
from typing import List

from .metrics import TestResult, TestSession
from .evaluation import calculate_test_results, create_error_result
from .simulations import (
    simulate_concurrent_handoff,
    simulate_endurance_handoff_execution,
)


async def run_concurrency_test(session: TestSession, logger) -> TestResult:
    try:
        cfg = session.test_config
        logger.info(f"🧪 Running concurrency test: {cfg.iterations} iterations")
        start = time.time()
        succ = fail = timeout = 0
        durations: List[float] = []
        for i in range(0, cfg.iterations, cfg.concurrent_limit):
            batch = min(cfg.concurrent_limit, cfg.iterations - i)
            iteration_start = time.time()
            tasks = [simulate_concurrent_handoff(cfg) for _ in range(batch)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, Exception) or not res:
                    fail += 1
                else:
                    succ += 1
                durations.append(time.time() - iteration_start)
            if (i + batch) % 10 == 0:
                logger.info(f"📊 Concurrency test progress: {i + batch}/{cfg.iterations}")
        end = time.time()
        return calculate_test_results(cfg, start, end, end - start, succ, fail, timeout, durations)
    except Exception as e:
        logger.error(f"Concurrency test failed: {e}")
        return create_error_result(session.test_config, str(e))


async def run_endurance_test(session: TestSession, logger) -> TestResult:
    try:
        cfg = session.test_config
        logger.info(f"🧪 Running endurance test: {cfg.iterations} iterations")
        start = time.time()
        succ = fail = timeout = 0
        durations: List[float] = []
        for i in range(cfg.iterations):
            iteration_start = time.time()
            try:
                if await simulate_endurance_handoff_execution(cfg, i):
                    succ += 1
                else:
                    fail += 1
                durations.append(time.time() - iteration_start)
                if (i + 1) % 25 == 0:
                    logger.info(f"📊 Endurance test progress: {i + 1}/{cfg.iterations}")
                await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                timeout += 1
                durations.append(cfg.timeout)
            except Exception:
                fail += 1
                durations.append(time.time() - iteration_start)
        end = time.time()
        return calculate_test_results(cfg, start, end, end - start, succ, fail, timeout, durations)
    except Exception as e:
        logger.error(f"Endurance test failed: {e}")
        return create_error_result(session.test_config, str(e))
