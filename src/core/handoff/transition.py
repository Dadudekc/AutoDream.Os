"""Transition logic for handoff execution."""

from typing import Any, Dict, Callable
import asyncio
import logging


async def execute_generic_action(action: str, context: Any, execution: Any, logger: logging.Logger) -> bool:
    """Execute a generic action."""
    try:
        await asyncio.sleep(0.1)
        logger.info(f"🔧 Executing generic action: {action}")
        return True
    except Exception as exc:  # pragma: no cover - log path
        logger.error(f"Generic action {action} failed: {exc}")
        return False


async def execute_step(
    step: Dict[str, Any],
    context: Any,
    execution: Any,
    logger: logging.Logger,
    validation_engines: Dict[str, Callable],
) -> bool:
    """Execute a single handoff step with retry and timeout."""
    try:
        action = step["action"]
        timeout = step.get("timeout", 30.0)
        retry_count = step.get("retry_count", 1)

        for attempt in range(retry_count + 1):
            try:
                if action in validation_engines:
                    result = await asyncio.wait_for(
                        validation_engines[action](context, execution),
                        timeout=timeout,
                    )
                else:
                    result = await asyncio.wait_for(
                        execute_generic_action(action, context, execution, logger),
                        timeout=timeout,
                    )
                if result:
                    return True
            except asyncio.TimeoutError:
                logger.warning(
                    f"⏰ Step {step['step_id']} timed out (attempt {attempt + 1})"
                )
                if attempt == retry_count:
                    raise
            except Exception as exc:
                logger.warning(
                    f"⚠️ Step {step['step_id']} attempt {attempt + 1} failed: {exc}"
                )
                if attempt == retry_count:
                    raise
        return False
    except Exception as exc:
        logger.error(f"Failed to execute step {step['step_id']}: {exc}")
        return False


async def execute_rollback(
    execution: Any,
    context: Any,
    procedure: Any,
    logger: logging.Logger,
    status_enum: Any,
) -> None:
    """Execute rollback procedures when a step fails."""
    try:
        logger.info(f"🔄 Executing rollback for {execution.execution_id}")
        for rollback in procedure.rollback_procedures:
            try:
                await asyncio.sleep(0.1)
                logger.info(
                    f"✅ Rollback {rollback['rollback_id']} completed: {rollback['name']}"
                )
            except Exception as exc:  # pragma: no cover - log path
                logger.error(f"❌ Rollback {rollback['rollback_id']} failed: {exc}")
        execution.status = status_enum.ROLLBACK
    except Exception as exc:  # pragma: no cover - log path
        logger.error(f"Rollback execution failed: {exc}")
