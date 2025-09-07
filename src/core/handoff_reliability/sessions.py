from __future__ import annotations

import asyncio
import time
from typing import Dict

from .metrics import TestSession, TestStatus, update_reliability_metrics


def start_reliability_test(system, test_config_id: str) -> str:
    """Start a reliability test session."""
    if test_config_id not in system.test_configurations:
        raise ValueError(f"Unknown test configuration ID: {test_config_id}")
    config = system.test_configurations[test_config_id]
    session_id = f"reliability_{int(time.time())}_{test_config_id}"
    session = TestSession(session_id=session_id, test_config=config, start_time=time.time())
    system.active_sessions[session_id] = session
    system.logger.info(
        f"🚀 Starting reliability test session {session_id} for {test_config_id}"
    )
    asyncio.create_task(execute_test_session(system, session))
    return session_id


async def execute_test_session(system, session: TestSession):
    """Execute a reliability test session."""
    try:
        session.status = TestStatus.RUNNING
        system.logger.info(
            f"🔄 Executing reliability test session {session.session_id}"
        )
        engine = system.test_engines.get(session.test_config.test_type)
        if not engine:
            raise ValueError(f"No test engine for type: {session.test_config.test_type}")
        result = await engine(session, system.logger)
        session.results.append(result)
        if result.error_details:
            session.status = TestStatus.FAILED
            session.error_details = result.error_details
        else:
            session.status = TestStatus.COMPLETED
        session.end_time = time.time()
        emoji = "✅" if session.status == TestStatus.COMPLETED else "❌"
        system.logger.info(
            f"{emoji} Reliability test session {session.session_id} completed: {session.status.value}"
        )
        update_reliability_metrics(system.reliability_metrics, result)
    except Exception as e:
        session.status = TestStatus.FAILED
        session.error_details = str(e)
        session.end_time = time.time()
        system.logger.error(
            f"❌ Reliability test session {session.session_id} failed: {e}"
        )
    finally:
        system.test_history.append(session)
        system.active_sessions.pop(session.session_id, None)
