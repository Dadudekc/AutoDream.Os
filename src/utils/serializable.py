"""Serializable mixin providing dataclass to_dict capability."""
from dataclasses import asdict
from typing import Any, Dict


class SerializableMixin:
    """Mixin that adds a ``to_dict`` method using :func:`dataclasses.asdict`.

    Data model classes can inherit from this mixin to avoid redefining
    simple serialization logic.
    """

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the dataclass."""
        return asdict(self)
