"""Combined AIManager implementation."""

from .base import AIManagerBase
from .model_ops import ModelOpsMixin
from .workflow_ops import WorkflowOpsMixin
from .api_keys import APIKeyMixin
from .persistence import PersistenceMixin


class AIManager(
    AIManagerBase, ModelOpsMixin, WorkflowOpsMixin, APIKeyMixin, PersistenceMixin
):
    """Central AI management and coordination."""

    pass
