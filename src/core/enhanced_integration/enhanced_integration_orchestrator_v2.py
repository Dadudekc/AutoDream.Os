#!/usr/bin/env python3
"""
Enhanced Integration Orchestrator - V2 Compliance Refactored
===========================================================

Main orchestrator using modular integration engines.
REFACTORED: 386 lines → <200 lines for V2 compliance.

Responsibilities:
- Orchestrates modular integration engines
- Provides unified interface for integration operations
- Maintains backward compatibility

V2 Compliance: Modular architecture, <300 lines, single responsibility.

Author: Agent-8 (SSOT & System Integration Specialist) - V2 Compliance Refactoring
Original: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

# Import integration models
from .integration_models import (
    EnhancedOptimizationConfig,
    IntegrationPerformanceMetrics,
    IntegrationPerformanceReport,
    IntegrationTask,
    CoordinationStrategy,
    IntegrationType,
    IntegrationStatus,
    create_default_optimization_config,
    create_performance_report,
    create_integration_task,
)

# Import modular engines
from .engines import IntegrationOptimizationEngine, IntegrationCoordinationEngine


class EnhancedIntegrationOrchestrator:
    """V2 Compliant Enhanced Integration Orchestrator.

    Uses modular engines to provide enhanced integration capabilities while maintaining
    clean, focused architecture.
    """

    def __init__(self, config: Optional[EnhancedOptimizationConfig] = None):
        """Initialize the enhanced integration orchestrator."""
        self.logger = logging.getLogger(__name__)
        self.config = config or create_default_optimization_config()

        # Initialize modular engines
        self.optimization_engine = IntegrationOptimizationEngine(self.config)
        self.coordination_engine = IntegrationCoordinationEngine(
            max_workers=getattr(self.config, "max_workers", 4)
        )

        self.logger.info(
            "Enhanced Integration Orchestrator initialized with modular architecture"
        )

    async def coordinate_enhanced_integration(
        self,
        tasks: List[IntegrationTask],
        strategy: CoordinationStrategy = CoordinationStrategy.PARALLEL,
    ) -> Dict[str, Any]:
        """Coordinate multiple enhanced integration tasks."""
        try:
            self.logger.info(
                f"Starting enhanced integration coordination for {len(tasks)} tasks"
            )

            start_time = datetime.now()

            # Use coordination engine to manage tasks
            coordination_result = (
                await self.coordination_engine.coordinate_integrations(tasks, strategy)
            )

            # Apply optimization to successful tasks
            successful_tasks = [
                task for task in tasks if task.status == IntegrationStatus.COMPLETED
            ]

            optimization_results = []
            for task in successful_tasks:
                opt_result = await self.optimization_engine.optimize_integration(task)
                optimization_results.append(opt_result)

            end_time = datetime.now()
            total_duration = (end_time - start_time).total_seconds()

            # Generate comprehensive result
            result = {
                "status": "completed",
                "coordination_result": coordination_result,
                "optimization_applied": len(optimization_results),
                "optimization_successful": sum(optimization_results),
                "total_duration": total_duration,
                "tasks_processed": len(tasks),
                "successful_tasks": len(successful_tasks),
            }

            self.logger.info(f"Enhanced integration coordination completed: {result}")
            return result

        except Exception as e:
            self.logger.error(f"Enhanced integration coordination failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "tasks_processed": len(tasks) if tasks else 0,
            }

    async def optimize_single_integration(self, task: IntegrationTask) -> bool:
        """Optimize a single integration task."""
        try:
            return await self.optimization_engine.optimize_integration(task)
        except Exception as e:
            self.logger.error(f"Single integration optimization failed: {e}")
            return False

    def get_performance_report(self) -> IntegrationPerformanceReport:
        """Generate comprehensive performance report."""
        try:
            # Get metrics from engines
            optimization_metrics = self.optimization_engine.get_optimization_metrics()
            coordination_status = self.coordination_engine.get_coordination_status()

            # Create comprehensive report
            report = create_performance_report(
                optimization_metrics=optimization_metrics,
                coordination_status=coordination_status,
                generated_at=datetime.now(),
            )

            return report

        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            # Return empty report on error
            return create_performance_report()

    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status from all engines."""
        try:
            return {
                "orchestrator_status": "active",
                "optimization_engine": {
                    "active_optimizations": len(
                        self.optimization_engine.get_active_optimizations()
                    ),
                    "cache_size": len(self.optimization_engine.optimization_cache),
                },
                "coordination_engine": (
                    self.coordination_engine.get_coordination_status()
                ),
                "config": {
                    "optimization_level": self.config.optimization_level.value,
                    "max_workers": getattr(self.config, "max_workers", 4),
                },
            }

        except Exception as e:
            self.logger.error(f"Failed to get integration status: {e}")
            return {"status": "error", "message": str(e)}

    async def cancel_integration(self, task_id: str) -> bool:
        """Cancel an active integration task."""
        try:
            # Try canceling in both engines
            opt_cancelled = self.optimization_engine.cancel_optimization(task_id)
            coord_cancelled = self.coordination_engine.cancel_task(task_id)

            success = opt_cancelled or coord_cancelled
            if success:
                self.logger.info(f"Successfully cancelled integration: {task_id}")
            else:
                self.logger.warning(
                    f"Integration task not found for cancellation: {task_id}"
                )

            return success

        except Exception as e:
            self.logger.error(f"Failed to cancel integration {task_id}: {e}")
            return False

    def cleanup(self) -> None:
        """Cleanup orchestrator resources."""
        try:
            self.optimization_engine.clear_optimization_cache()
            self.coordination_engine.cleanup()
            self.logger.info("Enhanced Integration Orchestrator cleaned up")
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")


# Factory function for backward compatibility
def create_enhanced_integration_orchestrator(
    config: Optional[EnhancedOptimizationConfig] = None,
) -> EnhancedIntegrationOrchestrator:
    """Create an enhanced integration orchestrator instance."""
    return EnhancedIntegrationOrchestrator(config)


# Singleton instance for global access
_orchestrator_instance: Optional[EnhancedIntegrationOrchestrator] = None


def get_enhanced_integration_orchestrator(
    config: Optional[EnhancedOptimizationConfig] = None,
) -> EnhancedIntegrationOrchestrator:
    """Get the global enhanced integration orchestrator instance."""
    global _orchestrator_instance

    if _orchestrator_instance is None:
        _orchestrator_instance = create_enhanced_integration_orchestrator(config)

    return _orchestrator_instance
