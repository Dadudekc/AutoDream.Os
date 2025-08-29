#!/usr/bin/env python3
"""
Unified Learning System - Agent Cellphone V2
============================================

CONSOLIDATED learning system eliminating duplication.
Follows V2 standards: 400 LOC, OOP design, SRP.

**Author:** V2 Consolidation Specialist
**Created:** Current Sprint
**Status:** ACTIVE - CONSOLIDATION IN PROGRESS
"""

from .unified_learning_engine import UnifiedLearningEngine
from .learning_manager import LearningManager
# ARCHITECTURE CORRECTED: Decision manager moved to decision module
from .models import (
    LearningData,
    LearningGoal,
    LearningProgress,
    LearningMode,
    IntelligenceLevel,
    LearningManagerConfig,
    LearningEngineConfig,
)

__all__ = [
    # Core Engine
    "UnifiedLearningEngine",
    
    # Specialized Managers
    "LearningManager",
    
    # Learning Models
    "LearningData",
    "LearningGoal",
    "LearningProgress",
    "LearningMode",
    "IntelligenceLevel",
    "LearningManagerConfig",
    "LearningEngineConfig",
]

# Version information
__version__ = "2.0.0"
__author__ = "V2 Consolidation Specialist"
__status__ = "ACTIVE - CONSOLIDATION IN PROGRESS"
