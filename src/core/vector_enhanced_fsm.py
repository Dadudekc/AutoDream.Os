#!/usr/bin/env python3
"""
Vector Enhanced FSM - Agent Cellphone V2
========================================

FSM system enhanced with vector database capabilities for context-aware
state transitions and intelligent agent coordination.

V2 Compliance: < 300 lines, single responsibility, FSM-vector integration.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from ..core.unified_import_system import logging

    FSMContext,
    FSMEvent,
    FSMInstance,
    FSMState,
    create_agent_workflow_fsm,
)


class VectorEnhancedFSM:
    """
    FSM enhanced with vector database capabilities for intelligent state management.

    Provides context-aware state transitions based on historical patterns,
    agent-specific behavior, and similar scenario analysis.
    """

    def __init__(self, agent_id: str, vector_db):
        """
        Initialize vector-enhanced FSM.

        Args:
            agent_id: Agent identifier
            vector_db: Vector database service instance
        """
        self.agent_id = agent_id
        self.vector_db = vector_db
        self.fsm = create_agent_workflow_fsm(agent_id)
        self.logger = logging.getLogger(__name__)

        # Index current FSM state in vector database
        self._index_current_state()

    def _index_current_state(self):
        """Index current FSM state in vector database for context tracking."""
        try:
            current_state = self.fsm.get_current_state()
            context = self.fsm.context

            # Create document for current state
            state_doc = {
                "content": f"Agent {self.agent_id} in state {current_state.value}",
                "metadata": {
                    "agent_id": self.agent_id,
                    "current_state": current_state.value,
                    "previous_state": (
                        context.previous_state.value if context.previous_state else None
                    ),
                    "last_event": (
                        context.last_event.value if context.last_event else None
                    ),
                    "timestamp": (
                        context.timestamp.isoformat()
                        if context.timestamp
                        else datetime.now().isoformat()
                    ),
                    "document_type": "fsm_state",
                },
            }

            # Index in vector database
            self.vector_db.add_document(
                content=state_doc["content"],
                document_type="status",
                metadata=state_doc["metadata"],
                agent_id=self.agent_id,
            )

        except Exception as e:
            self.get_logger(__name__).error(f"Error indexing FSM state: {e}")

    def transition_with_context(self, event: FSMEvent) -> bool:
        """
        Execute state transition with vector database context analysis.

        Args:
            event: FSM event triggering transition

        Returns:
            True if transition successful, False otherwise
        """
        try:
            # Get context from vector database
            context = self._get_transition_context(event)

            # Make intelligent transition decision
            if self._should_transition(context):
                success = self.fsm.transition(event)
                if success:
                    self._index_current_state()
                    self._log_transition(event, context)
                return success

            return False

        except Exception as e:
            self.get_logger(__name__).error(f"Error in context-aware transition: {e}")
            return False

    def _get_transition_context(self, event: FSMEvent) -> Dict[str, Any]:
        """Get context for transition decision from vector database."""
        try:
            current_state = self.fsm.get_current_state()

            # Search for similar transitions
            similar_transitions = self.vector_db.search_documents(
                query=f"agent {self.agent_id} transition {current_state.value} {event.value}",
                filters={"agent_id": self.agent_id, "document_type": "fsm_transition"},
                limit=5,
            )

            # Get agent performance patterns
            performance_patterns = self.vector_db.search_documents(
                query=f"agent {self.agent_id} performance {current_state.value}",
                filters={"agent_id": self.agent_id, "document_type": "performance"},
                limit=3,
            )

            return {
                "similar_transitions": similar_transitions,
                "performance_patterns": performance_patterns,
                "current_state": current_state,
                "event": event,
                "timestamp": datetime.now(),
            }

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting transition context: {e}")
            return {}

    def _should_transition(self, context: Dict[str, Any]) -> bool:
        """Determine if transition should proceed based on context analysis."""
        try:
            # Check if similar transitions were successful
            similar_transitions = context.get("similar_transitions", [])
            if similar_transitions:
                success_rate = sum(
                    1 for t in similar_transitions if t.get("success", False)
                ) / len(similar_transitions)
                if success_rate < 0.5:  # Less than 50% success rate
                    self.get_logger(__name__).warning(
                        f"Low success rate for similar transitions: {success_rate}"
                    )
                    return False

            # Check performance patterns
            performance_patterns = context.get("performance_patterns", [])
            if performance_patterns:
                avg_performance = sum(
                    p.get("performance_score", 0.5) for p in performance_patterns
                ) / len(performance_patterns)
                if avg_performance < 0.3:  # Low performance threshold
                    self.get_logger(__name__).warning(
                        f"Low performance in current state: {avg_performance}"
                    )
                    return False

            return True

        except Exception as e:
            self.get_logger(__name__).error(f"Error in transition decision: {e}")
            return True  # Default to allowing transition

    def _log_transition(self, event: FSMEvent, context: Dict[str, Any]):
        """Log transition for future context analysis."""
        try:
            transition_doc = {
                "content": (
                    f"Agent {self.agent_id} transitioned from {context['current_state'].value} via {event.value}"
                ),
                "metadata": {
                    "agent_id": self.agent_id,
                    "from_state": context["current_state"].value,
                    "to_state": self.fsm.get_current_state().value,
                    "event": event.value,
                    "timestamp": datetime.now().isoformat(),
                    "success": True,
                    "document_type": "fsm_transition",
                    "context_analysis": {
                        "similar_transitions_count": len(
                            context.get("similar_transitions", [])
                        ),
                        "performance_patterns_count": len(
                            context.get("performance_patterns", [])
                        ),
                    },
                },
            }

            self.vector_db.add_document(
                content=transition_doc["content"],
                document_type="status",
                metadata=transition_doc["metadata"],
                agent_id=self.agent_id,
            )

        except Exception as e:
            self.get_logger(__name__).error(f"Error logging transition: {e}")

    def get_optimal_next_states(self) -> List[FSMState]:
        """Get recommended next states based on vector analysis."""
        try:
            current_state = self.fsm.get_current_state()

            # Find similar agents in same state
            similar_agents = self.vector_db.search_documents(
                query=f"agent in state {current_state.value} successful transition",
                filters={"document_type": "fsm_transition"},
                limit=10,
            )

            # Analyze transition patterns
            next_states = {}
            for agent_data in similar_agents:
                to_state = agent_data.get("metadata", {}).get("to_state")
                if to_state:
                    next_states[to_state] = next_states.get(to_state, 0) + 1

            # Rank by frequency
            ranked_states = sorted(
                next_states.items(), key=lambda x: x[1], reverse=True
            )

            # Convert to FSMState objects
            recommended_states = []
            for state_name, count in ranked_states[:3]:  # Top 3 recommendations
                try:
                    state = FSMState(state_name)
                    recommended_states.append(state)
                except ValueError:
                    continue

            return recommended_states

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting optimal next states: {e}")
            return []

    def get_agent_performance_insights(self) -> Dict[str, Any]:
        """Get performance insights for the agent based on FSM patterns."""
        try:
            # Get agent's FSM history
            fsm_history = self.vector_db.search_documents(
                query=f"agent {self.agent_id} FSM state transition",
                filters={"agent_id": self.agent_id, "document_type": "fsm_transition"},
                limit=50,
            )

            if not get_unified_validator().validate_required(fsm_history):
                return {"message": "No FSM history available"}

            # Analyze patterns
            state_times = {}
            transition_success = {}

            for record in fsm_history:
                metadata = record.get("metadata", {})
                state = metadata.get("to_state")
                success = metadata.get("success", True)

                if state:
                    state_times[state] = state_times.get(state, 0) + 1
                    if state not in transition_success:
                        transition_success[state] = []
                    transition_success[state].append(success)

            # Calculate insights
            insights = {
                "total_transitions": len(fsm_history),
                "most_common_states": sorted(
                    state_times.items(), key=lambda x: x[1], reverse=True
                )[:3],
                "success_rate_by_state": {
                    state: sum(successes) / len(successes)
                    for state, successes in transition_success.items()
                },
                "recommendations": self._generate_performance_recommendations(
                    state_times, transition_success
                ),
            }

            return insights

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting performance insights: {e}")
            return {"error": str(e)}

    def _generate_performance_recommendations(
        self, state_times: Dict[str, int], transition_success: Dict[str, List[bool]]
    ) -> List[str]:
        """Generate performance recommendations based on FSM patterns."""
        recommendations = []

        # Check for states with low success rates
        for state, successes in transition_success.items():
            success_rate = sum(successes) / len(successes)
            if success_rate < 0.6:
                recommendations.append(
                    f"Improve performance in {state} state (success rate: {success_rate:.2f})"
                )

        # Check for states with high frequency (potential bottlenecks)
        total_transitions = sum(state_times.values())
        for state, count in state_times.items():
            frequency = count / total_transitions
            if frequency > 0.4:  # More than 40% of time in one state
                recommendations.append(
                    f"Consider optimizing {state} state (frequency: {frequency:.2f})"
                )

        return recommendations

    def get_current_state(self) -> FSMState:
        """Get current FSM state."""
        return self.fsm.get_current_state()

    def is_completed(self) -> bool:
        """Check if FSM is in a final state."""
        return self.fsm.is_completed()

    def can_transition(self, event: FSMEvent) -> bool:
        """Check if transition is allowed."""
        return self.fsm.can_transition(event)


def create_vector_enhanced_fsm(agent_id: str, vector_db) -> VectorEnhancedFSM:
    """Factory function to create vector-enhanced FSM instance."""
    return VectorEnhancedFSM(agent_id, vector_db)
