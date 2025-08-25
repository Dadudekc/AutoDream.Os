"""Utilities for transforming messages to and from storage representations."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Any

from .routing_models import Message


class MessageTransformer:
    """Handle persistence of :class:`~core.routing_models.Message` objects."""

    def to_dict(self, message: Message) -> Dict[str, Any]:
        data = asdict(message)
        data["message_type"] = message.message_type.value
        data["priority"] = message.priority.value
        data["status"] = message.status.value
        return data

    def save(self, message: Message, directory: Path) -> None:
        directory.mkdir(exist_ok=True)
        message_file = directory / f"{message.message_id}.json"
        with open(message_file, "w") as f:
            json.dump(self.to_dict(message), f, indent=2, default=str)
