"""Combined ModelManager implementation."""

from .base import ModelManagerBase
from .registry import RegistryMixin
from .api_keys import APIKeyMixin
from .persistence import PersistenceMixin


class ModelManager(ModelManagerBase, RegistryMixin, APIKeyMixin, PersistenceMixin):
    """Manages AI/ML models and their lifecycle."""

    pass
