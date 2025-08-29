from __future__ import annotations

"""Middleware orchestrator coordinating registration, ordering, and errors."""

import asyncio
import json
import logging
import time
from collections import deque
from typing import Any, Dict, List, Optional

from .base import BaseMiddlewareComponent
from .models import DataPacket, MiddlewareChain
from .ordering import execute_chain, resolve_chain
from .registry import create_chain, register_middleware
from .errors import handle_packet_error

from .components.routing import RoutingMiddleware
from .components.transformations import DataTransformationMiddleware
from .components.validation import ValidationMiddleware

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
        register_middleware(self.middleware_components, middleware)

    def create_chain(self, chain: MiddlewareChain) -> None:
        create_chain(self.middleware_chains, chain)

    async def process_data_packet(
        self, data_packet: DataPacket, chain_name: Optional[str] = None
    ) -> DataPacket:
        """Process a data packet through the appropriate middleware chain."""
        start_time = time.time()
        try:
            chain = resolve_chain(self.middleware_chains, data_packet, chain_name)
            if not chain or not chain.enabled:
                logger.warning(
                    "No appropriate chain found for packet %s", data_packet.id
                )
                return data_packet

            processed_packet = await execute_chain(
                self.middleware_components, data_packet, chain
            )

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
            return handle_packet_error(data_packet, exc)

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
        metadata={"priority": 5, "source": "agent"},
        tags={"standard", "json"},
    )
    result = await orchestrator.process_data_packet(packet)
    print(json.dumps(result.metadata, indent=2))
    await orchestrator.stop()


if __name__ == "__main__":
    asyncio.run(run_demo())
