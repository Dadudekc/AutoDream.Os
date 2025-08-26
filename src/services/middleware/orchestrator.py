"""Middleware orchestrator for managing data flow through components."""

from __future__ import annotations

import asyncio
import json
import logging
import time
from collections import deque
from typing import Any, Dict, List, Optional

from .base import BaseMiddlewareComponent
from .models import DataPacket, MiddlewareChain

logger = logging.getLogger(__name__)


class MiddlewareOrchestrator:
    """Main orchestrator for managing middleware chains and data flow."""

    def __init__(self) -> None:
        self.middleware_components: Dict[str, BaseMiddlewareComponent] = {}
        self.middleware_chains: List[MiddlewareChain] = []
        self.data_flow_history: deque = deque(maxlen=1000)
        self.running = False

        # Performance monitoring
        self.total_packets_processed = 0
        self.total_processing_time = 0.0
        self.start_time = time.time()

    def register_middleware(self, middleware: BaseMiddlewareComponent) -> None:
        """Register a middleware component."""
        if middleware.name in self.middleware_components:
            logger.warning(
                "Middleware %s already registered, overwriting", middleware.name
            )
        self.middleware_components[middleware.name] = middleware

    def create_chain(self, chain: MiddlewareChain) -> None:
        """Create a new middleware chain."""
        for middleware_name in chain.middleware_list:
            if middleware_name not in self.middleware_components:
                raise ValueError(
                    f"Middleware '{middleware_name}' not found in chain '{chain.name}'"
                )
        self.middleware_chains.append(chain)
        self.middleware_chains.sort(key=lambda x: x.priority)

    async def process_data_packet(
        self, data_packet: DataPacket, chain_name: Optional[str] = None
    ) -> DataPacket:
        """Process a data packet through the appropriate middleware chain."""
        start_time = time.time()

        try:
            chain = self._resolve_chain(data_packet, chain_name)
            if not chain or not chain.enabled:
                logger.warning(
                    "No appropriate chain found for packet %s", data_packet.id
                )
                return data_packet

            processed_packet = await self._execute_chain(data_packet, chain, {})

            processing_time = time.time() - start_time
            self.total_packets_processed += 1
            self.total_processing_time += processing_time

            self.data_flow_history.append(
                {
                    "packet_id": data_packet.id,
                    "chain_name": chain.name,
                    "processing_time": processing_time,
                    "timestamp": time.time(),
                    "success": "error" not in processed_packet.metadata,
                }
            )

            return processed_packet

        except Exception as exc:  # noqa: BLE001
            logger.error("Error processing data packet %s: %s", data_packet.id, exc)
            data_packet.metadata["error"] = str(exc)
            data_packet.metadata["processing_failed"] = True
            return data_packet

    def _resolve_chain(
        self, data_packet: DataPacket, chain_name: Optional[str]
    ) -> Optional[MiddlewareChain]:
        if chain_name:
            return self._find_chain(chain_name)
        return self._select_appropriate_chain(data_packet)

    def _find_chain(self, chain_name: str) -> Optional[MiddlewareChain]:
        for chain in self.middleware_chains:
            if chain.name == chain_name:
                return chain
        return None

    def _select_appropriate_chain(
        self, data_packet: DataPacket
    ) -> Optional[MiddlewareChain]:
        for chain in self.middleware_chains:
            if not chain.enabled:
                continue
            if self._chain_matches_packet(chain, data_packet):
                return chain
        return None

    @staticmethod
    def _chain_matches_packet(chain: MiddlewareChain, data_packet: DataPacket) -> bool:
        for key, value in chain.conditions.items():
            if key in data_packet.metadata:
                if data_packet.metadata[key] != value:
                    return False
            elif key in data_packet.tags:
                if value not in data_packet.tags:
                    return False
            else:
                return False
        return True

    async def _execute_chain(
        self, data_packet: DataPacket, chain: MiddlewareChain, context: Dict[str, Any]
    ) -> DataPacket:
        """Execute a middleware chain on a data packet.

        Middleware components run sequentially in the order defined by the
        chain's ``middleware_list``. Each component receives the packet returned
        by the previous component. Components that are disabled or whose
        ``should_process`` method returns ``False`` are skipped.
        """
        current_packet = data_packet

        for middleware_name in chain.middleware_list:
            middleware = self.middleware_components.get(middleware_name)
            if not middleware or not middleware.enabled:
                continue
            if middleware.should_process(current_packet, context):
                try:
                    current_packet = await middleware.process(current_packet, context)
                except Exception as exc:  # noqa: BLE001
                    logger.error("Error in middleware %s: %s", middleware_name, exc)
                    current_packet.metadata["error"] = str(exc)
                    current_packet.metadata["failed_middleware"] = middleware_name
                    break

        return current_packet

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get overall performance metrics."""
        uptime = time.time() - self.start_time
        avg_processing_time = (
            self.total_processing_time / self.total_packets_processed
            if self.total_packets_processed
            else 0
        )
        return {
            "uptime": uptime,
            "processed_packets": self.total_packets_processed,
            "total_processing_time": self.total_processing_time,
            "average_processing_time": avg_processing_time,
        }

    def get_middleware_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get metrics for all registered middleware components."""
        return {
            name: component.get_metrics()
            for name, component in self.middleware_components.items()
        }

    def get_chain_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all middleware chains."""
        return [
            {
                "name": chain.name,
                "enabled": chain.enabled,
                "priority": chain.priority,
                "component_count": len(chain.middleware_list),
                "description": chain.description,
            }
            for chain in self.middleware_chains
        ]

    async def start(self) -> None:
        """Start the middleware orchestrator."""
        self.running = True
        self.start_time = time.time()
        logger.info("Middleware Orchestrator started")

    async def stop(self) -> None:
        """Stop the middleware orchestrator."""
        self.running = False
        logger.info("Middleware Orchestrator stopped")


async def run_demo() -> None:
    """Run a small demo of the orchestrator with basic components."""
    from .components.routing import RoutingMiddleware
    from .components.transformations import DataTransformationMiddleware
    from .components.validation import ValidationMiddleware

    orchestrator = MiddlewareOrchestrator()

    orchestrator.register_middleware(
        DataTransformationMiddleware(
            {"transformations": {"json": "json_to_dict", "string": "string_uppercase"}}
        )
    )
    orchestrator.register_middleware(
        ValidationMiddleware(
            {
                "validation_rules": {
                    "source": {"required": True},
                    "priority": {"type": "number", "min_value": 1, "max_value": 10},
                },
                "strict_mode": False,
            }
        )
    )
    orchestrator.register_middleware(
        RoutingMiddleware(
            {
                "routing_rules": {
                    "tag:high_priority": "priority_queue",
                    "tag:low_priority": "standard_queue",
                    "metadata:type=urgent": "urgent_queue",
                },
                "default_route": "default_queue",
            }
        )
    )

    from .models import DataPacket

    orchestrator.create_chain(
        MiddlewareChain(
            name="standard_processing",
            middleware_list=[
                "DataTransformationMiddleware",
                "ValidationMiddleware",
                "RoutingMiddleware",
            ],
            priority=1,
            description="Standard packet processing",
        )
    )

    await orchestrator.start()
    packet = DataPacket(
        id="demo",
        data='{"message": "Hello"}',
        metadata={"priority": "medium", "source": "agent"},
        tags={"standard"},
    )
    result = await orchestrator.process_data_packet(packet)
    print(json.dumps(result.metadata, indent=2))
    await orchestrator.stop()


if __name__ == "__main__":
    asyncio.run(run_demo())
