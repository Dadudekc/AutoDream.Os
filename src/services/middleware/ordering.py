from __future__ import annotations

"""Ordering utilities for middleware chains and execution."""

from typing import Any, Dict, List, Optional

from .base import BaseMiddlewareComponent
from .models import DataPacket, MiddlewareChain
from .errors import handle_middleware_error


def resolve_chain(
    chains: List[MiddlewareChain],
    data_packet: DataPacket,
    chain_name: Optional[str],
) -> Optional[MiddlewareChain]:
    """Resolve which chain should process the given data packet."""
    if chain_name:
        return find_chain(chains, chain_name)
    return select_appropriate_chain(chains, data_packet)


def find_chain(
    chains: List[MiddlewareChain], chain_name: str
) -> Optional[MiddlewareChain]:
    """Find a chain by name."""
    for chain in chains:
        if chain.name == chain_name:
            return chain
    return None


def select_appropriate_chain(
    chains: List[MiddlewareChain],
    data_packet: DataPacket,
) -> Optional[MiddlewareChain]:
    """Select the first enabled chain that matches the packet."""
    for chain in chains:
        if not chain.enabled:
            continue
        if chain_matches_packet(chain, data_packet):
            return chain
    return None


def chain_matches_packet(chain: MiddlewareChain, data_packet: DataPacket) -> bool:
    """Determine if a chain's conditions match the packet."""
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


async def execute_chain(
    components: Dict[str, BaseMiddlewareComponent],
    data_packet: DataPacket,
    chain: MiddlewareChain,
    context: Optional[Dict[str, Any]] = None,
) -> DataPacket:
    """Execute the middleware chain on the data packet."""
    context = context or {}
    current_packet = data_packet
    for middleware_name in chain.middleware_list:
        middleware = components.get(middleware_name)
        if not middleware or not middleware.enabled:
            continue
        if middleware.should_process(current_packet, context):
            try:
                current_packet = await middleware.process(current_packet, context)
            except Exception as exc:  # noqa: BLE001
                handle_middleware_error(current_packet, middleware_name, exc)
                break
    return current_packet
