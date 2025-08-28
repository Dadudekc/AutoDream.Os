from __future__ import annotations

from typing import Dict
import logging

from .metrics import TestConfiguration, TestSession, TestType


def load_default_test_configurations() -> Dict[str, TestConfiguration]:
    """Return a dictionary of default test configurations."""
    default_configs = [
        TestConfiguration(
            test_id="RELIABILITY_STANDARD",
            test_type=TestType.RELIABILITY,
            procedure_id="PHASE_TRANSITION_STANDARD",
            iterations=100,
            timeout=30.0,
            concurrent_limit=5,
        ),
        TestConfiguration(
            test_id="PERFORMANCE_STANDARD",
            test_type=TestType.PERFORMANCE,
            procedure_id="PHASE_TRANSITION_STANDARD",
            iterations=50,
            timeout=60.0,
            concurrent_limit=10,
        ),
        TestConfiguration(
            test_id="STRESS_STANDARD",
            test_type=TestType.STRESS,
            procedure_id="PHASE_TRANSITION_STANDARD",
            iterations=25,
            timeout=120.0,
            concurrent_limit=20,
            stress_factor=2.0,
        ),
        TestConfiguration(
            test_id="FAILURE_INJECTION_STANDARD",
            test_type=TestType.FAILURE_INJECTION,
            procedure_id="PHASE_TRANSITION_STANDARD",
            iterations=75,
            timeout=45.0,
            concurrent_limit=5,
            failure_rate=0.1,
        ),
        TestConfiguration(
            test_id="CONCURRENCY_STANDARD",
            test_type=TestType.CONCURRENCY,
            procedure_id="PHASE_TRANSITION_STANDARD",
            iterations=30,
            timeout=90.0,
            concurrent_limit=50,
        ),
        TestConfiguration(
            test_id="ENDURANCE_STANDARD",
            test_type=TestType.ENDURANCE,
            procedure_id="PHASE_TRANSITION_STANDARD",
            iterations=200,
            timeout=180.0,
            concurrent_limit=3,
        ),
    ]
    return {cfg.test_id: cfg for cfg in default_configs}


def add_test_configuration(
    configs: Dict[str, TestConfiguration], config: TestConfiguration, logger: logging.Logger
) -> bool:
    """Add a new test configuration."""
    try:
        if config.test_id in configs:
            logger.warning(f"Test configuration {config.test_id} already exists, overwriting")
        configs[config.test_id] = config
        logger.info(f"✅ Added test configuration: {config.test_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to add test configuration: {e}")
        return False


def remove_test_configuration(
    configs: Dict[str, TestConfiguration],
    active_sessions: Dict[str, TestSession],
    config_id: str,
    logger: logging.Logger,
) -> bool:
    """Remove a test configuration if not in use."""
    try:
        if config_id not in configs:
            logger.warning(f"Test configuration {config_id} not found")
            return False
        for session in active_sessions.values():
            if session.test_config.test_id == config_id:
                logger.error(
                    f"Cannot remove configuration {config_id} - in use by session {session.session_id}"
                )
                return False
        del configs[config_id]
        logger.info(f"✅ Removed test configuration: {config_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to remove test configuration: {e}")
        return False
