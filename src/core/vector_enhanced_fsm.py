#!/usr/bin/env python3
"""
Vector Enhanced FSM - KISS Simplified
=====================================

Simplified FSM system enhanced with vector database capabilities.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined FSM-vector integration.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-7 - Web Development Specialist
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    from .fsm.fsm_core import (
        FSMContext,
        FSMEvent,
        FSMInstance,
        FSMState,
        create_agent_workflow_fsm,
    )
except ImportError:
    # Fallback for missing imports
    FSMContext = Dict[str, Any]
    FSMEvent = Dict[str, Any]
    FSMInstance = Dict[str, Any]
    FSMState = str
    create_agent_workflow_fsm = lambda x: {}


class VectorEnhancedFSM:
    """
    Simplified FSM enhanced with vector database capabilities.

    Provides context-aware state transitions based on historical patterns
    and agent-specific behavior.
    """

    def __init__(self, agent_id: str, vector_db=None):
        """Initialize vector-enhanced FSM - simplified."""
        self.agent_id = agent_id
        self.vector_db = vector_db
        self.fsm = create_agent_workflow_fsm(agent_id)
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False

    def initialize(self) -> bool:
        """Initialize the FSM - simplified."""
        try:
            if self.vector_db:
                self._index_current_state()
            self.is_initialized = True
            self.logger.info(f"Vector Enhanced FSM initialized for {self.agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Vector Enhanced FSM: {e}")
            return False

    def _index_current_state(self):
        """Index current FSM state in vector database - simplified."""
        try:
            if not self.vector_db:
                return
            
            current_state = self.get_current_state()
            if current_state:
                # Basic state indexing
                state_data = {
                    "agent_id": self.agent_id,
                    "state": current_state,
                    "timestamp": datetime.now().isoformat(),
                    "context": "fsm_state"
                }
                self.vector_db.add_document(state_data)
                
        except Exception as e:
            self.logger.error(f"Error indexing current state: {e}")

    def get_current_state(self) -> Optional[str]:
        """Get current FSM state - simplified."""
        try:
            if hasattr(self.fsm, 'current_state'):
                return self.fsm.current_state
            return "unknown"
        except Exception as e:
            self.logger.error(f"Error getting current state: {e}")
            return None

    def transition_to_state(self, new_state: str, context: Dict[str, Any] = None) -> bool:
        """Transition to new state - simplified."""
        try:
            if not self.is_initialized:
                raise RuntimeError("FSM not initialized")
            
            # Basic state transition
            if hasattr(self.fsm, 'transition_to'):
                self.fsm.transition_to(new_state)
            elif hasattr(self.fsm, 'current_state'):
                self.fsm.current_state = new_state
            
            # Index new state
            if self.vector_db:
                self._index_current_state()
            
            self.logger.info(f"Transitioned to state: {new_state}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error transitioning to state {new_state}: {e}")
            return False

    def get_similar_states(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get similar states from vector database - simplified."""
        try:
            if not self.vector_db:
                return []
            
            # Basic similarity search
            results = self.vector_db.search(query, limit=limit)
            return results if results else []
            
        except Exception as e:
            self.logger.error(f"Error getting similar states: {e}")
            return []

    def get_state_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get state history - simplified."""
        try:
            if not self.vector_db:
                return []
            
            # Basic history retrieval
            history = self.vector_db.get_agent_history(self.agent_id, limit=limit)
            return history if history else []
            
        except Exception as e:
            self.logger.error(f"Error getting state history: {e}")
            return []

    def analyze_state_patterns(self) -> Dict[str, Any]:
        """Analyze state patterns - simplified."""
        try:
            if not self.vector_db:
                return {"patterns": [], "insights": []}
            
            # Basic pattern analysis
            history = self.get_state_history(limit=50)
            if not history:
                return {"patterns": [], "insights": []}
            
            # Count state frequencies
            state_counts = {}
            for entry in history:
                state = entry.get("state", "unknown")
                state_counts[state] = state_counts.get(state, 0) + 1
            
            # Find most common states
            common_states = sorted(state_counts.items(), key=lambda x: x[1], reverse=True)
            
            return {
                "patterns": common_states[:5],
                "insights": [f"Most common state: {common_states[0][0]}" if common_states else "No patterns found"],
                "total_transitions": len(history)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing state patterns: {e}")
            return {"patterns": [], "insights": [], "error": str(e)}

    def get_contextual_recommendations(self, current_context: Dict[str, Any]) -> List[str]:
        """Get contextual recommendations - simplified."""
        try:
            if not self.vector_db:
                return []
            
            # Basic recommendation logic
            recommendations = []
            
            # Check for similar contexts
            similar_states = self.get_similar_states(str(current_context), limit=3)
            if similar_states:
                recommendations.append("Consider similar successful patterns from history")
            
            # Check state patterns
            patterns = self.analyze_state_patterns()
            if patterns.get("patterns"):
                most_common = patterns["patterns"][0][0]
                recommendations.append(f"Consider transitioning to {most_common} based on history")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error getting recommendations: {e}")
            return []

    def update_context(self, context: Dict[str, Any]) -> bool:
        """Update FSM context - simplified."""
        try:
            if not self.is_initialized:
                raise RuntimeError("FSM not initialized")
            
            # Basic context update
            if hasattr(self.fsm, 'context'):
                self.fsm.context.update(context)
            elif hasattr(self.fsm, 'update_context'):
                self.fsm.update_context(context)
            
            # Index updated context
            if self.vector_db:
                self._index_current_state()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating context: {e}")
            return False

    def get_fsm_status(self) -> Dict[str, Any]:
        """Get FSM status - simplified."""
        return {
            "agent_id": self.agent_id,
            "is_initialized": self.is_initialized,
            "current_state": self.get_current_state(),
            "vector_db_available": self.vector_db is not None,
            "fsm_type": "vector_enhanced"
        }

    def shutdown(self) -> bool:
        """Shutdown FSM - simplified."""
        try:
            self.is_initialized = False
            self.logger.info(f"Vector Enhanced FSM shutdown for {self.agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
            return False