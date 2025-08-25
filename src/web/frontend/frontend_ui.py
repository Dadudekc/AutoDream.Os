#!/usr/bin/env python3
"""UI component utilities for the frontend application."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

from .frontend_app_core import UIComponent

logger = logging.getLogger(__name__)


def create_component(
    component_type: str, props: Dict[str, Any], children: Optional[List[UIComponent]] = None
) -> UIComponent:
    """Create a new UI component."""
    return UIComponent(
        id=str(uuid.uuid4()),
        type=component_type,
        props=props,
        state={},
        children=children or [],
        event_handlers={},
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def register_default_components(component_registry):
    """Register default UI components."""
    component_registry.register_component(
        "Button",
        lambda props: {"type": "button", "text": props.get("text", "Button")},
        template='<button class="btn btn-primary">{{ text }}</button>',
        style=".btn { padding: 8px 16px; border-radius: 4px; }",
        script='function handleClick() { console.log("Button clicked"); }',
    )

    component_registry.register_component(
        "Card",
        lambda props: {
            "type": "card",
            "title": props.get("title", "Card"),
            "content": props.get("content", ""),
        },
        template='<div class="card"><div class="card-header">{{ title }}</div><div class="card-body">{{ content }}</div></div>',
        style=".card { border: 1px solid #ddd; border-radius: 8px; margin: 8px; }",
        script="",
    )


def process_component_event(state_manager, component_id: str, event_type: str, event_data: Dict[str, Any]):
    """Process component events."""
    logger.info(f"Processing component event: {component_id} - {event_type}")
    if component_id in state_manager.get_state().components:
        component = state_manager.get_state().components[component_id]
        component.state.update(event_data)
        component.updated_at = datetime.now()


__all__ = ["create_component", "register_default_components", "process_component_event"]
