"""
Vector Database Web Interface Routes - V2 Compliance
===================================================

Refactored Flask routes for the vector database web interface.
V2 Compliance: Modular architecture with clean separation of concerns.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
Target: 447 lines → < 300 lines (ACHIEVED: 15 lines)
"""

# Import the modular blueprint
from .vector_database import vector_db_bp

# Export the blueprint for backward compatibility
__all__ = ['vector_db_bp']