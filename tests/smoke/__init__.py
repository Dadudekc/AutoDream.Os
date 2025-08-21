"""
🧪 SMOKE TESTS - AGENT_CELLPHONE_V2
Foundation & Testing Specialist - TDD Integration Project

This package contains smoke tests for all components, ensuring basic functionality
and V2 coding standards compliance.
"""

__version__ = "1.0.0"
__author__ = "Foundation & Testing Specialist"
__status__ = "ACTIVE"

# Smoke test modules
from .test_core_components import *  # noqa: F403, F401
from .test_service_components import *  # noqa: F403, F401
from .test_launcher_components import *  # noqa: F403, F401
from .test_utility_components import *  # noqa: F403, F401
