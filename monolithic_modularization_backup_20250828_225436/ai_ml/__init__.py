"""
AI/ML Core Package - Duplication-Free Architecture
Captain Agent-3: Emergency Cleanup Implementation
"""

__version__ = "2.0.0"
__author__ = "Captain Agent-3"
__status__ = "DUPLICATION_FREE"

from .core.ai_ml_engine import ai_ml_engine
from .managers.base_manager import BaseManager
from .integrations.base_integration import BaseIntegration
from .utilities.common_utils import generate_hash, validate_config, format_response

__all__ = [
    "ai_ml_engine",
    "BaseManager", 
    "BaseIntegration",
    "generate_hash",
    "validate_config",
    "format_response"
]

# Single entry point - no duplication
def get_ai_ml_engine():
    """Get the unified AI/ML engine"""
    return ai_ml_engine
