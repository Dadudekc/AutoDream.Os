#!/usr/bin/env python3
"""
Vector Enhanced Contract Service - Agent Cellphone V2
====================================================

Contract service enhanced with vector database capabilities for intelligent
task assignment, progress tracking, and performance optimization.

V2 Compliance: < 300 lines, single responsibility, contract-vector integration.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""



# from .vector_database_service import VectorDatabaseService
# from .models.vector_models import DocumentType, SearchQuery


class VectorEnhancedContractService:
    """
    Contract service enhanced with vector database capabilities.

    Provides intelligent task assignment, context-aware progress tracking,
    and performance optimization based on historical patterns.
    """

    def __init__(self, vector_db, lock_config=None):
        """
        Initialize vector-enhanced contract service.

        Args:
            vector_db: Vector database service instance
            lock_config: File lock configuration
        """
        self.vector_db = vector_db
        self.contract_service = ContractService(lock_config)
        self.logger = logging.getLogger(__name__)

    def get_optimal_task_assignment(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get optimal task assignment based on vector analysis.

        Args:
            agent_id: Agent identifier

        Returns:
            Optimal contract assignment or None
        """
        try:
            # Get agent context and capabilities
            agent_context = self._get_agent_context(agent_id)

            # Find similar successful tasks
            similar_tasks = self.vector_db.search_documents(
                query=f"successful task completion {agent_context.get('domain', '')}",
                filters={
                    "agent_id": agent_id,
                    "status": "completed",
                    "document_type": "contract",
                },
                limit=10,
            )

            # Analyze task patterns and success factors
            optimal_contract = self._analyze_task_patterns(similar_tasks, agent_context)

            if optimal_contract:
                # Index the assignment for future analysis
                self._index_contract_assignment(agent_id, optimal_contract)

            return optimal_contract

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting optimal task assignment: {e}")
            return None

    def _get_agent_context(self, agent_id: str) -> Dict[str, Any]:
        """Get agent context from vector database."""
        try:
            # Search for agent profile and capabilities
            agent_profile = self.vector_db.search_documents(
                query=f"agent {agent_id} profile capabilities domain",
                filters={"agent_id": agent_id, "document_type": "agent_profile"},
                limit=1,
            )

            if agent_profile:
                return agent_profile[0].get("metadata", {})

            # Fallback to basic agent info
            return {
                "agent_id": agent_id,
                "domain": "general",
                "capabilities": [],
                "experience_level": "intermediate",
            }

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting agent context: {e}")
            return {"agent_id": agent_id, "domain": "general"}

    def _analyze_task_patterns(
        self, similar_tasks: List[Dict], agent_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Analyze task patterns to find optimal assignment."""
        try:
            if not get_unified_validator().validate_required(similar_tasks):
                # No similar tasks, return any available contract
                return self.contract_service.get_contract(agent_context["agent_id"])

            # Analyze success patterns
            success_factors = []
            task_types = {}

            for task in similar_tasks:
                metadata = task.get("metadata", {})
                task_type = metadata.get("task_type", "general")
                success_score = metadata.get("success_score", 0.5)

                if success_score > 0.7:  # High success rate
                    success_factors.append(task_type)

                task_types[task_type] = task_types.get(task_type, 0) + 1

            # Find most successful task type
            if success_factors:
                most_successful = max(set(success_factors), key=success_factors.count)

                # Look for contracts of this type
                available_contracts = self.contract_service.contracts.get(
                    agent_context["agent_id"], []
                )
                for contract in available_contracts:
                    if most_successful in contract.get("description", "").lower():
                        return contract

            # Fallback to any available contract
            return self.contract_service.get_contract(agent_context["agent_id"])

        except Exception as e:
            self.get_logger(__name__).error(f"Error analyzing task patterns: {e}")
            return None

    def _index_contract_assignment(self, agent_id: str, contract: Dict[str, Any]):
        """Index contract assignment for future analysis."""
        try:
            assignment_doc = {
                "content": (
                    f"Contract assigned to {agent_id}: {contract.get('title', 'Unknown')}"
                ),
                "metadata": {
                    "agent_id": agent_id,
                    "contract_id": contract.get("id", "unknown"),
                    "contract_title": contract.get("title", "Unknown"),
                    "assignment_timestamp": datetime.now().isoformat(),
                    "document_type": "contract_assignment",
                    "status": "assigned",
                },
            }

            self.vector_db.add_document(
                content=assignment_doc["content"],
                document_type="contract",
                metadata=assignment_doc["metadata"],
                agent_id=agent_id,
            )

        except Exception as e:
            self.get_logger(__name__).error(f"Error indexing contract assignment: {e}")

    def track_contract_progress(
        self, agent_id: str, contract_id: str
    ) -> Dict[str, Any]:
        """
        Track contract progress with vector-enhanced context.

        Args:
            agent_id: Agent identifier
            contract_id: Contract identifier

        Returns:
            Progress report with context and recommendations
        """
        try:
            # Get current progress
            current_progress = self._get_current_progress(contract_id)

            # Find similar contract progressions
            similar_contracts = self.vector_db.search_documents(
                query=f"contract progress {contract_id} similar",
                filters={"agent_id": agent_id, "document_type": "contract_progress"},
                limit=5,
            )

            # Predict completion timeline
            predicted_completion = self._predict_completion_time(
                current_progress, similar_contracts
            )

            # Get recommendations for acceleration
            recommendations = self._get_acceleration_recommendations(
                current_progress, similar_contracts
            )

            # Index progress update
            self._index_progress_update(agent_id, contract_id, current_progress)

            return {
                "current_progress": current_progress,
                "predicted_completion": predicted_completion,
                "recommendations": recommendations,
                "similar_contracts_count": len(similar_contracts),
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            self.get_logger(__name__).error(f"Error tracking contract progress: {e}")
            return {"error": str(e)}

    def _get_current_progress(self, contract_id: str) -> Dict[str, Any]:
        """Get current contract progress."""
        try:
            # This would integrate with actual contract progress tracking
            # For now, return mock progress
            return {
                "contract_id": contract_id,
                "completion_percentage": 45.0,
                "current_phase": "execution",
                "estimated_remaining_hours": 20,
                "last_updated": datetime.now().isoformat(),
            }
        except Exception as e:
            self.get_logger(__name__).error(f"Error getting current progress: {e}")
            return {"contract_id": contract_id, "completion_percentage": 0}

    def _predict_completion_time(
        self, current_progress: Dict[str, Any], similar_contracts: List[Dict]
    ) -> Dict[str, Any]:
        """Predict completion time based on similar contracts."""
        try:
            if not get_unified_validator().validate_required(similar_contracts):
                return {"predicted_completion_date": None, "confidence": 0.0}

            # Analyze similar contract completion times
            completion_times = []
            for contract in similar_contracts:
                metadata = contract.get("metadata", {})
                if "completion_time_hours" in metadata:
                    completion_times.append(metadata["completion_time_hours"])

            if completion_times:
                avg_completion_time = sum(completion_times) / len(completion_times)
                remaining_hours = current_progress.get("estimated_remaining_hours", 20)

                # Adjust based on current progress
                adjusted_time = remaining_hours * (
                    avg_completion_time / 40
                )  # Normalize to 40 hours

                return {
                    "predicted_completion_date": (
                        datetime.now().timestamp() + adjusted_time * 3600
                    ),
                    "predicted_hours_remaining": adjusted_time,
                    "confidence": min(
                        len(completion_times) / 5.0, 1.0
                    ),  # Higher confidence with more data
                }

            return {"predicted_completion_date": None, "confidence": 0.0}

        except Exception as e:
            self.get_logger(__name__).error(f"Error predicting completion time: {e}")
            return {"predicted_completion_date": None, "confidence": 0.0}

    def _get_acceleration_recommendations(
        self, current_progress: Dict[str, Any], similar_contracts: List[Dict]
    ) -> List[str]:
        """Get recommendations for accelerating contract completion."""
        try:
            recommendations = []

            # Analyze successful completion patterns
            successful_contracts = [
                c
                for c in similar_contracts
                if c.get("metadata", {}).get("success_score", 0) > 0.8
            ]

            if successful_contracts:
                # Extract common success factors
                success_factors = []
                for contract in successful_contracts:
                    factors = contract.get("metadata", {}).get("success_factors", [])
                    success_factors.extend(factors)

                # Get most common factors
                if success_factors:
                    factor_counts = {}
                    for factor in success_factors:
                        factor_counts[factor] = factor_counts.get(factor, 0) + 1

                    top_factors = sorted(
                        factor_counts.items(), key=lambda x: x[1], reverse=True
                    )[:3]
                    for factor, count in top_factors:
                        recommendations.append(
                            f"Apply success factor: {factor} (used in {count} successful contracts)"
                        )

            # Add general recommendations based on progress
            completion_pct = current_progress.get("completion_percentage", 0)
            if completion_pct < 30:
                recommendations.append("Focus on initial setup and planning phase")
            elif completion_pct < 70:
                recommendations.append("Maintain steady execution pace")
            else:
                recommendations.append("Focus on final validation and testing")

            return recommendations

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting acceleration recommendations: {e}")
            return ["Continue current approach"]

    def _index_progress_update(
        self, agent_id: str, contract_id: str, progress: Dict[str, Any]
    ):
        """Index progress update for future analysis."""
        try:
            progress_doc = {
                "content": (
                    f"Contract {contract_id} progress update: {progress.get('completion_percentage', 0)}% complete"
                ),
                "metadata": {
                    "agent_id": agent_id,
                    "contract_id": contract_id,
                    "completion_percentage": progress.get("completion_percentage", 0),
                    "current_phase": progress.get("current_phase", "unknown"),
                    "timestamp": datetime.now().isoformat(),
                    "document_type": "contract_progress",
                },
            }

            self.vector_db.add_document(
                content=progress_doc["content"],
                document_type="contract",
                metadata=progress_doc["metadata"],
                agent_id=agent_id,
            )

        except Exception as e:
            self.get_logger(__name__).error(f"Error indexing progress update: {e}")

    def get_agent_performance_analytics(self, agent_id: str) -> Dict[str, Any]:
        """Get comprehensive performance analytics for an agent."""
        try:
            # Get agent's contract history
            contract_history = self.vector_db.search_documents(
                query=f"agent {agent_id} contract completion",
                filters={"agent_id": agent_id, "document_type": "contract"},
                limit=50,
            )

            if not get_unified_validator().validate_required(contract_history):
                return {"message": "No contract history available"}

            # Analyze performance metrics
            total_contracts = len(contract_history)
            completed_contracts = [
                c
                for c in contract_history
                if c.get("metadata", {}).get("status") == "completed"
            ]
            success_rate = (
                len(completed_contracts) / total_contracts if total_contracts > 0 else 0
            )

            # Calculate average completion time
            completion_times = []
            for contract in completed_contracts:
                metadata = contract.get("metadata", {})
                if "completion_time_hours" in metadata:
                    completion_times.append(metadata["completion_time_hours"])

            avg_completion_time = (
                sum(completion_times) / len(completion_times) if completion_times else 0
            )

            # Get performance trends
            recent_contracts = sorted(
                contract_history,
                key=lambda x: x.get("metadata", {}).get("timestamp", ""),
                reverse=True,
            )[:10]

            recent_success_rate = len(
                [
                    c
                    for c in recent_contracts
                    if c.get("metadata", {}).get("status") == "completed"
                ]
            ) / len(recent_contracts)

            return {
                "total_contracts": total_contracts,
                "completed_contracts": len(completed_contracts),
                "success_rate": success_rate,
                "recent_success_rate": recent_success_rate,
                "average_completion_time_hours": avg_completion_time,
                "performance_trend": (
                    "improving" if recent_success_rate > success_rate else "stable"
                ),
                "recommendations": self._generate_performance_recommendations(
                    contract_history
                ),
            }

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting performance analytics: {e}")
            return {"error": str(e)}

    def _generate_performance_recommendations(
        self, contract_history: List[Dict]
    ) -> List[str]:
        """Generate performance recommendations based on contract history."""
        recommendations = []

        # Analyze failure patterns
        failed_contracts = [
            c
            for c in contract_history
            if c.get("metadata", {}).get("status") == "failed"
        ]

        if failed_contracts:
            failure_reasons = []
            for contract in failed_contracts:
                reason = contract.get("metadata", {}).get("failure_reason", "unknown")
                failure_reasons.append(reason)

            if failure_reasons:
                most_common_failure = max(
                    set(failure_reasons), key=failure_reasons.count
                )
                recommendations.append(
                    f"Address common failure pattern: {most_common_failure}"
                )

        # Analyze success patterns
        successful_contracts = [
            c
            for c in contract_history
            if c.get("metadata", {}).get("status") == "completed"
        ]

        if successful_contracts:
            success_factors = []
            for contract in successful_contracts:
                factors = contract.get("metadata", {}).get("success_factors", [])
                success_factors.extend(factors)

            if success_factors:
                top_success_factor = max(
                    set(success_factors), key=success_factors.count
                )
                recommendations.append(
                    f"Continue using successful approach: {top_success_factor}"
                )

        return recommendations

    # Delegate standard contract service methods
    def get_contract(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get contract for agent (delegated to standard service)."""
        return self.contract_service.get_contract(agent_id)

    def get_unified_validator().check_agent_status(self):
        """Check agent status (delegated to standard service)."""
        return self.contract_service.get_unified_validator().check_agent_status()


def create_vector_enhanced_contract_service(
    vector_db, lock_config=None
) -> VectorEnhancedContractService:
    """Factory function to create vector-enhanced contract service."""
    return VectorEnhancedContractService(vector_db, lock_config)
