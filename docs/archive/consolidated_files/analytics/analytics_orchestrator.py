#!/usr/bin/env python3
"""
Analytics Orchestrator - V2 Compliant Module
===========================================

Main orchestrator for unified analytics system coordinating all analytics components.
V2 COMPLIANT: Focused orchestration under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .interfaces.analytics_interfaces import AnalyticsEngine
from .models.analytics_models import AnalyticsData, AnalyticsInfo, AnalyticsResult

logger = logging.getLogger(__name__)


class AnalyticsOrchestrator:
    """Main orchestrator for unified analytics system."""

    def __init__(self):
        self.engines: Dict[str, AnalyticsEngine] = {}
        self.analytics_registry: Dict[str, AnalyticsInfo] = {}
        self.logger = logging.getLogger(__name__)

    def register_engine(self, engine: AnalyticsEngine) -> bool:
        """Register an analytics engine."""
        try:
            engine_id = engine.analytics_id

            if engine_id in self.engines:
                self.logger.warning(f"Engine {engine_id} already registered")
                return False

            self.engines[engine_id] = engine

            # Create analytics info
            analytics_info = AnalyticsInfo(
                analytics_id=engine_id,
                name=engine.name,
                analytics_type=engine.analytics_type,
                status=engine.status,
                intelligence_type=getattr(engine, 'intelligence_type', None),
                processing_mode=getattr(engine, 'processing_mode', None),
                metadata={"registered_at": datetime.now().isoformat()}
            )

            self.analytics_registry[engine_id] = analytics_info
            self.logger.info(f"Registered analytics engine: {engine_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to register engine: {e}")
            return False

    def unregister_engine(self, engine_id: str) -> bool:
        """Unregister an analytics engine."""
        try:
            if engine_id not in self.engines:
                self.logger.warning(f"Engine {engine_id} not found")
                return False

            # Stop engine if running
            engine = self.engines[engine_id]
            if hasattr(engine, 'status') and engine.status.name == 'RUNNING':
                engine.stop()

            # Remove from registry
            del self.engines[engine_id]
            if engine_id in self.analytics_registry:
                del self.analytics_registry[engine_id]

            self.logger.info(f"Unregistered analytics engine: {engine_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to unregister engine {engine_id}: {e}")
            return False

    def start_engine(self, engine_id: str) -> bool:
        """Start a specific analytics engine."""
        try:
            if engine_id not in self.engines:
                self.logger.error(f"Engine {engine_id} not found")
                return False

            engine = self.engines[engine_id]
            success = engine.start()

            if success:
                engine.status = engine.status.__class__.RUNNING
                if engine_id in self.analytics_registry:
                    self.analytics_registry[engine_id].status = engine.status
                    self.analytics_registry[engine_id].last_updated = datetime.now()

                self.logger.info(f"Started analytics engine: {engine_id}")
            else:
                self.logger.error(f"Failed to start engine: {engine_id}")

            return success

        except Exception as e:
            self.logger.error(f"Error starting engine {engine_id}: {e}")
            return False

    def stop_engine(self, engine_id: str) -> bool:
        """Stop a specific analytics engine."""
        try:
            if engine_id not in self.engines:
                self.logger.error(f"Engine {engine_id} not found")
                return False

            engine = self.engines[engine_id]
            success = engine.stop()

            if success:
                engine.status = engine.status.__class__.STOPPED
                if engine_id in self.analytics_registry:
                    self.analytics_registry[engine_id].status = engine.status
                    self.analytics_registry[engine_id].last_updated = datetime.now()

                self.logger.info(f"Stopped analytics engine: {engine_id}")
            else:
                self.logger.error(f"Failed to stop engine: {engine_id}")

            return success

        except Exception as e:
            self.logger.error(f"Error stopping engine {engine_id}: {e}")
            return False

    def process_data(self, engine_id: str, data: AnalyticsData) -> Optional[AnalyticsResult]:
        """Process data using a specific analytics engine."""
        try:
            if engine_id not in self.engines:
                self.logger.error(f"Engine {engine_id} not found")
                return None

            engine = self.engines[engine_id]
            start_time = datetime.now()

            # Process data
            result = engine.process_data(data)

            # Update metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            success = result is not None
            engine.update_metrics(processing_time, success)

            if result:
                self.logger.info(f"Data processed by {engine_id}: {result.result_id}")
            else:
                self.logger.warning(f"Data processing failed for {engine_id}")

            return result

        except Exception as e:
            self.logger.error(f"Error processing data with {engine_id}: {e}")
            return None

    def get_engine_status(self, engine_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific analytics engine."""
        try:
            if engine_id not in self.engines:
                return None

            engine = self.engines[engine_id]
            analytics_info = self.analytics_registry.get(engine_id)

            return {
                "engine_id": engine_id,
                "name": engine.name,
                "status": engine.status.name if hasattr(engine.status, 'name') else str(engine.status),
                "type": engine.analytics_type.value,
                "capabilities": engine.get_capabilities(),
                "metrics": {
                    "total_processed": engine.metrics.total_processed,
                    "successful_processed": engine.metrics.successful_processed,
                    "failed_processed": engine.metrics.failed_processed,
                    "average_processing_time": engine.metrics.average_processing_time,
                    "last_updated": engine.metrics.last_updated.isoformat(),
                },
                "registered_at": analytics_info.created_at.isoformat() if analytics_info else None,
                "last_updated": analytics_info.last_updated.isoformat() if analytics_info else None,
            }

        except Exception as e:
            self.logger.error(f"Error getting engine status for {engine_id}: {e}")
            return None

    def get_all_engine_statuses(self) -> Dict[str, Any]:
        """Get status of all registered analytics engines."""
        try:
            statuses = {}
            for engine_id in self.engines.keys():
                status = self.get_engine_status(engine_id)
                if status:
                    statuses[engine_id] = status

            return {
                "total_engines": len(self.engines),
                "active_engines": sum(1 for s in statuses.values() if s["status"] == "RUNNING"),
                "engines": statuses,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error getting all engine statuses: {e}")
            return {"error": str(e)}

    def get_engine_capabilities(self, engine_id: str) -> Optional[List[str]]:
        """Get capabilities of a specific analytics engine."""
        try:
            if engine_id not in self.engines:
                return None

            return self.engines[engine_id].get_capabilities()

        except Exception as e:
            self.logger.error(f"Error getting capabilities for {engine_id}: {e}")
            return None


# Factory function for dependency injection
def create_analytics_orchestrator() -> AnalyticsOrchestrator:
    """Factory function to create analytics orchestrator."""
    return AnalyticsOrchestrator()


# Export for DI
__all__ = ["AnalyticsOrchestrator", "create_analytics_orchestrator"]
