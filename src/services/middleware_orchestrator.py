"""
Middleware Orchestration System for Agent_Cellphone_V2_Repository
Manages data flow through middleware components and provides advanced routing capabilities.
"""

import asyncio
import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Union, Set
from pathlib import Path
import time
import uuid
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MiddlewareType(Enum):
    """Types of middleware for categorization."""

    PREPROCESSING = "preprocessing"
    PROCESSING = "processing"
    POSTPROCESSING = "postprocessing"
    ROUTING = "routing"
    VALIDATION = "validation"
    TRANSFORMATION = "transformation"
    MONITORING = "monitoring"


class DataFlowDirection(Enum):
    """Direction of data flow through middleware."""

    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BIDIRECTIONAL = "bidirectional"


@dataclass
class MiddlewareChain:
    """Represents a chain of middleware components."""

    name: str
    middleware_list: List[str] = field(default_factory=list)
    enabled: bool = True
    priority: int = 0
    conditions: Dict[str, Any] = field(default_factory=dict)
    description: str = ""


@dataclass
class DataPacket:
    """Represents a data packet flowing through the middleware system."""

    id: str
    data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    source: str = ""
    destination: str = ""
    flow_direction: DataFlowDirection = DataFlowDirection.INBOUND
    tags: Set[str] = field(default_factory=set)
    processing_history: List[str] = field(default_factory=list)


class BaseMiddlewareComponent(ABC):
    """Abstract base class for all middleware components."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = self.__class__.__name__
        self.middleware_type = self.config.get("type", MiddlewareType.PROCESSING)
        self.enabled = self.config.get("enabled", True)
        self.priority = self.config.get("priority", 0)
        self.conditions = self.config.get("conditions", {})

        # Performance metrics
        self.processed_count = 0
        self.error_count = 0
        self.total_processing_time = 0.0
        self.last_processed = None

    @abstractmethod
    async def process(
        self, data_packet: DataPacket, context: Dict[str, Any]
    ) -> DataPacket:
        """Process the data packet and return modified packet."""
        pass

    def should_process(self, data_packet: DataPacket, context: Dict[str, Any]) -> bool:
        """Determine if this middleware should process the given packet."""
        if not self.enabled:
            return False

        # Check conditions
        for key, value in self.conditions.items():
            if key in data_packet.metadata:
                if data_packet.metadata[key] != value:
                    return False
            elif key in data_packet.tags:
                if value not in data_packet.tags:
                    return False
            else:
                return False

        return True

    def update_metrics(self, processing_time: float, success: bool = True):
        """Update performance metrics."""
        self.processed_count += 1
        if not success:
            self.error_count += 1
        self.total_processing_time += processing_time
        self.last_processed = time.time()

    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        avg_time = (
            self.total_processing_time / self.processed_count
            if self.processed_count > 0
            else 0
        )

        return {
            "name": self.name,
            "type": self.middleware_type.value,
            "enabled": self.enabled,
            "processed_count": self.processed_count,
            "error_count": self.error_count,
            "total_processing_time": self.total_processing_time,
            "average_processing_time": avg_time,
            "last_processed": self.last_processed,
            "success_rate": (
                (self.processed_count - self.error_count) / self.processed_count
                if self.processed_count > 0
                else 0
            ),
        }


class DataTransformationMiddleware(BaseMiddlewareComponent):
    """Middleware for transforming data formats."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.middleware_type = MiddlewareType.TRANSFORMATION
        self.transformations = self.config.get("transformations", {})

    async def process(
        self, data_packet: DataPacket, context: Dict[str, Any]
    ) -> DataPacket:
        start_time = time.time()
        success = True

        try:
            # Apply transformations based on packet tags or metadata
            for condition, transformation in self.transformations.items():
                if self._matches_condition(data_packet, condition):
                    data_packet.data = await self._apply_transformation(
                        data_packet.data, transformation
                    )
                    data_packet.processing_history.append(
                        f"{self.name}:{transformation}"
                    )

            # Update packet metadata
            data_packet.metadata["transformed"] = True
            data_packet.metadata["transformation_count"] = len(
                data_packet.processing_history
            )

        except Exception as e:
            logger.error(f"Error in {self.name}: {str(e)}")
            success = False
            data_packet.metadata["error"] = str(e)

        processing_time = time.time() - start_time
        self.update_metrics(processing_time, success)

        return data_packet

    def _matches_condition(self, data_packet: DataPacket, condition: str) -> bool:
        """Check if packet matches transformation condition."""
        if condition in data_packet.tags:
            return True
        if condition in data_packet.metadata:
            return data_packet.metadata[condition]
        return False

    async def _apply_transformation(self, data: Any, transformation: str) -> Any:
        """Apply the specified transformation to data."""
        if transformation == "json_to_dict" and isinstance(data, str):
            return json.loads(data)
        elif transformation == "dict_to_json" and isinstance(data, dict):
            return json.dumps(data)
        elif transformation == "string_uppercase" and isinstance(data, str):
            return data.upper()
        elif transformation == "string_lowercase" and isinstance(data, str):
            return data.lower()
        # Add more transformations as needed
        return data


class ValidationMiddleware(BaseMiddlewareComponent):
    """Middleware for data validation."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.middleware_type = MiddlewareType.VALIDATION
        self.validation_rules = self.config.get("validation_rules", {})
        self.strict_mode = self.config.get("strict_mode", False)

    async def process(
        self, data_packet: DataPacket, context: Dict[str, Any]
    ) -> DataPacket:
        start_time = time.time()
        success = True

        try:
            validation_errors = []

            # Apply validation rules
            for field, rules in self.validation_rules.items():
                if field in data_packet.metadata:
                    value = data_packet.metadata[field]
                    for rule, constraint in rules.items():
                        if not self._validate_field(value, rule, constraint):
                            error_msg = (
                                f"Validation failed for {field}: {rule} {constraint}"
                            )
                            validation_errors.append(error_msg)

            # Handle validation results
            if validation_errors:
                data_packet.metadata["validation_errors"] = validation_errors
                data_packet.metadata["valid"] = False

                if self.strict_mode:
                    raise ValueError(f"Validation failed: {validation_errors}")
            else:
                data_packet.metadata["valid"] = True
                data_packet.tags.add("validated")

            data_packet.processing_history.append(f"{self.name}:validation")

        except Exception as e:
            logger.error(f"Error in {self.name}: {str(e)}")
            success = False
            data_packet.metadata["error"] = str(e)

        processing_time = time.time() - start_time
        self.update_metrics(processing_time, success)

        return data_packet

    def _validate_field(self, value: Any, rule: str, constraint: Any) -> bool:
        """Validate a field according to the specified rule."""
        if rule == "required":
            return value is not None and value != ""
        elif rule == "min_length" and isinstance(value, str):
            return len(value) >= constraint
        elif rule == "max_length" and isinstance(value, str):
            return len(value) <= constraint
        elif rule == "min_value" and isinstance(value, (int, float)):
            return value >= constraint
        elif rule == "max_value" and isinstance(value, (int, float)):
            return value <= constraint
        elif rule == "type" and constraint == "string":
            return isinstance(value, str)
        elif rule == "type" and constraint == "number":
            return isinstance(value, (int, float))
        return True


class RoutingMiddleware(BaseMiddlewareComponent):
    """Middleware for intelligent data routing."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.middleware_type = MiddlewareType.ROUTING
        self.routing_rules = self.config.get("routing_rules", {})
        self.default_route = self.config.get("default_route", "default")

    async def process(
        self, data_packet: DataPacket, context: Dict[str, Any]
    ) -> DataPacket:
        start_time = time.time()
        success = True

        try:
            # Determine route based on packet characteristics
            route = self._determine_route(data_packet)
            data_packet.metadata["route"] = route
            data_packet.metadata["routed"] = True

            # Add routing tags
            data_packet.tags.add(f"route:{route}")

            # Update destination if not already set
            if not data_packet.destination:
                data_packet.destination = route

            data_packet.processing_history.append(f"{self.name}:{route}")

        except Exception as e:
            logger.error(f"Error in {self.name}: {str(e)}")
            success = False
            data_packet.metadata["error"] = str(e)

        processing_time = time.time() - start_time
        self.update_metrics(processing_time, success)

        return data_packet

    def _determine_route(self, data_packet: DataPacket) -> str:
        """Determine the appropriate route for the data packet."""
        # Check routing rules in order of specificity
        for pattern, route in self.routing_rules.items():
            if self._matches_pattern(data_packet, pattern):
                return route

        return self.default_route

    def _matches_pattern(self, data_packet: DataPacket, pattern: str) -> bool:
        """Check if packet matches routing pattern."""
        if pattern.startswith("tag:"):
            tag = pattern[4:]
            return tag in data_packet.tags
        elif pattern.startswith("metadata:"):
            key_value = pattern[9:].split("=", 1)
            if len(key_value) == 2:
                key, value = key_value
                return data_packet.metadata.get(key) == value
        elif pattern.startswith("source:"):
            source = pattern[7:]
            return data_packet.source == source
        return False


class MiddlewareOrchestrator:
    """Main orchestrator for managing middleware chains and data flow."""

    def __init__(self):
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
                f"Middleware {middleware.name} already registered, overwriting"
            )

        self.middleware_components[middleware.name] = middleware
        logger.info(
            f"Registered middleware: {middleware.name} ({middleware.middleware_type.value})"
        )

    def create_chain(self, chain: MiddlewareChain) -> None:
        """Create a new middleware chain."""
        # Validate chain components
        for middleware_name in chain.middleware_list:
            if middleware_name not in self.middleware_components:
                raise ValueError(
                    f"Middleware '{middleware_name}' not found in chain '{chain.name}'"
                )

        self.middleware_chains.append(chain)
        # Sort by priority
        self.middleware_chains.sort(key=lambda x: x.priority)

        logger.info(
            f"Created middleware chain: {chain.name} with {len(chain.middleware_list)} components"
        )

    async def process_data_packet(
        self, data_packet: DataPacket, chain_name: Optional[str] = None
    ) -> DataPacket:
        """Process a data packet through the appropriate middleware chain."""
        start_time = time.time()

        try:
            # Determine which chain to use
            if chain_name:
                chain = self._find_chain(chain_name)
                if not chain:
                    raise ValueError(f"Chain '{chain_name}' not found")
            else:
                chain = self._select_appropriate_chain(data_packet)

            if not chain or not chain.enabled:
                logger.warning(
                    f"No appropriate chain found for packet {data_packet.id}"
                )
                return data_packet

            # Process through chain
            processed_packet = await self._execute_chain(data_packet, chain, {})

            # Update statistics
            processing_time = time.time() - start_time
            self.total_packets_processed += 1
            self.total_processing_time += processing_time

            # Record in history
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

        except Exception as e:
            logger.error(f"Error processing data packet {data_packet.id}: {str(e)}")
            data_packet.metadata["error"] = str(e)
            data_packet.metadata["processing_failed"] = True
            return data_packet

    def _find_chain(self, chain_name: str) -> Optional[MiddlewareChain]:
        """Find a middleware chain by name."""
        for chain in self.middleware_chains:
            if chain.name == chain_name:
                return chain
        return None

    def _select_appropriate_chain(
        self, data_packet: DataPacket
    ) -> Optional[MiddlewareChain]:
        """Select the most appropriate chain for a data packet."""
        for chain in self.middleware_chains:
            if not chain.enabled:
                continue

            # Check if chain conditions match packet
            if self._chain_matches_packet(chain, data_packet):
                return chain

        return None

    def _chain_matches_packet(
        self, chain: MiddlewareChain, data_packet: DataPacket
    ) -> bool:
        """Check if a chain's conditions match a data packet."""
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
        """Execute a middleware chain on a data packet."""
        current_packet = data_packet

        for middleware_name in chain.middleware_list:
            middleware = self.middleware_components.get(middleware_name)
            if not middleware or not middleware.enabled:
                continue

            if middleware.should_process(current_packet, context):
                try:
                    current_packet = await middleware.process(current_packet, context)
                except Exception as e:
                    logger.error(f"Error in middleware {middleware_name}: {str(e)}")
                    current_packet.metadata["error"] = str(e)
                    current_packet.metadata["failed_middleware"] = middleware_name
                    break

        return current_packet

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get overall performance metrics."""
        uptime = time.time() - self.start_time
        avg_processing_time = (
            self.total_processing_time / self.total_packets_processed
            if self.total_packets_processed > 0
            else 0
        )

        return {
            "uptime_seconds": uptime,
            "total_packets_processed": self.total_packets_processed,
            "total_processing_time": self.total_processing_time,
            "average_processing_time": avg_processing_time,
            "packets_per_second": self.total_packets_processed / uptime
            if uptime > 0
            else 0,
            "middleware_components": len(self.middleware_components),
            "active_chains": len([c for c in self.middleware_chains if c.enabled]),
        }

    def get_middleware_metrics(self) -> List[Dict[str, Any]]:
        """Get metrics for all middleware components."""
        return [
            middleware.get_metrics()
            for middleware in self.middleware_components.values()
        ]

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


# Example usage and testing
async def main():
    """Main function for testing the Middleware Orchestrator."""
    # Create orchestrator
    orchestrator = MiddlewareOrchestrator()

    # Register middleware components
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

    # Create middleware chains
    high_priority_chain = MiddlewareChain(
        name="high_priority_processing",
        middleware_list=["ValidationMiddleware", "RoutingMiddleware"],
        priority=1,
        conditions={"priority": "high"},
        description="High priority packet processing",
    )

    standard_chain = MiddlewareChain(
        name="standard_processing",
        middleware_list=[
            "DataTransformationMiddleware",
            "ValidationMiddleware",
            "RoutingMiddleware",
        ],
        priority=2,
        description="Standard packet processing",
    )

    orchestrator.create_chain(high_priority_chain)
    orchestrator.create_chain(standard_chain)

    # Start orchestrator
    await orchestrator.start()

    # Test data packets
    test_packets = [
        DataPacket(
            id="test1",
            data={"message": "High priority task"},
            metadata={"priority": "high", "source": "agent1"},
            tags={"high_priority", "urgent"},
        ),
        DataPacket(
            id="test2",
            data='{"message": "Standard task"}',
            metadata={"priority": "medium", "source": "agent2"},
            tags={"standard"},
        ),
    ]

    # Process packets
    for packet in test_packets:
        result = await orchestrator.process_data_packet(packet)
        print(f"Processed packet {result.id}: {result.metadata}")

    # Get metrics
    print(
        f"\nPerformance metrics: {json.dumps(orchestrator.get_performance_metrics(), indent=2)}"
    )
    print(
        f"\nMiddleware metrics: {json.dumps(orchestrator.get_middleware_metrics(), indent=2)}"
    )
    print(f"\nChain summary: {json.dumps(orchestrator.get_chain_summary(), indent=2)}")

    await orchestrator.stop()


if __name__ == "__main__":
    asyncio.run(main())
