"""
Intelligent Context Retrieval System for Strategic Oversight

This module provides advanced context retrieval capabilities for:
- Mission coordination and strategic decision making
- Emergency intervention based on historical patterns
- Agent capability matching and task optimization
- Pattern analysis for predictive insights

Key Features:
- Multi-modal context search (semantic, keyword, pattern-based)
- Real-time context adaptation based on mission status
- Emergency intervention pattern recognition
- Agent capability optimization recommendations

Author: Agent-3 (Intelligent Context Retrieval System)
"""

from datetime import datetime



@dataclass
class MissionContext:
    """Mission context structure for intelligent retrieval."""

    mission_id: str
    mission_type: str
    current_phase: str
    agent_assignments: Dict[str, str] = field(default_factory=dict)
    critical_path: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class AgentCapability:
    """Agent capability structure for matching and optimization."""

    agent_id: str
    primary_role: str
    skills: Set[str] = field(default_factory=set)
    experience_level: str = "intermediate"
    current_workload: int = 0
    success_rate: float = 0.8
    specialization: List[str] = field(default_factory=list)
    availability_status: str = "available"


@dataclass
class StrategicInsight:
    """Strategic insight structure for decision making."""

    insight_type: str
    content: str
    confidence_score: float
    source_documents: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    risk_assessment: str = "medium"
    generated_at: datetime = field(default_factory=datetime.now)


class IntelligentContextRetrieval:
    """
    Intelligent Context Retrieval System for Strategic Oversight.

    This system provides advanced context retrieval and analysis capabilities
    for enhanced mission coordination and emergency intervention.
    """

    def __init__(self, ssot_indexer: VectorDatabaseSSOTIndexer):
        """Initialize the intelligent context retrieval system."""
        self.ssot_indexer = ssot_indexer
        self.active_missions: Dict[str, MissionContext] = {}
        self.agent_capabilities: Dict[str, AgentCapability] = {}
        self.strategic_patterns: Dict[str, List[StrategicInsight]] = defaultdict(list)

    def update_mission_context(self, mission_context: MissionContext):
        """Update active mission context for intelligent retrieval."""
        self.active_missions[mission_context.mission_id] = mission_context

    def update_agent_capabilities(self, agent_data: Dict[str, Any]):
        """Update agent capabilities for optimization recommendations."""
        for agent_id, data in agent_data.items():
            capability = AgentCapability(
                agent_id=agent_id,
                primary_role=data.get("primary_role", "general"),
                skills=set(data.get("skills", [])),
                experience_level=data.get("experience_level", "intermediate"),
                current_workload=data.get("current_workload", 0),
                success_rate=data.get("success_rate", 0.8),
                specialization=data.get("specialization", []),
                availability_status=data.get("availability_status", "available")
            )
            self.agent_capabilities[agent_id] = capability

    def retrieve_mission_context(self, mission_id: str, context_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Retrieve intelligent context for mission coordination.

        Args:
            mission_id: Mission identifier
            context_type: Type of context (comprehensive, strategic, operational, emergency)

        Returns:
            Intelligent mission context with insights and recommendations
        """
        if mission_id not in self.active_missions:
            return {"error": f"Mission {mission_id} not found"}

        mission = self.active_missions[mission_id]

        # Get strategic insights
        strategic_insights = self.ssot_indexer.get_strategic_insights(
            f"{mission.mission_type} {mission.current_phase}",
            {agent_id: vars(cap) for agent_id, cap in self.agent_capabilities.items()}
        )

        # Get emergency preparedness
        emergency_context = self._get_emergency_context(mission)

        # Get agent optimization recommendations
        agent_recommendations = self._optimize_agent_assignment(mission)

        # Get pattern analysis
        pattern_analysis = self._analyze_success_patterns(mission)

        context = {
            "mission_id": mission_id,
            "mission_type": mission.mission_type,
            "current_phase": mission.current_phase,
            "strategic_insights": strategic_insights,
            "emergency_context": emergency_context,
            "agent_recommendations": agent_recommendations,
            "pattern_analysis": pattern_analysis,
            "risk_assessment": self._assess_mission_risks(mission),
            "success_probability": self._calculate_success_probability(mission, agent_recommendations),
            "generated_at": datetime.now().isoformat()
        }

        if context_type == "strategic":
            return {k: v for k, v in context.items() if k in ["strategic_insights", "pattern_analysis", "success_probability"]}
        elif context_type == "operational":
            return {k: v for k, v in context.items() if k in ["agent_recommendations", "current_phase", "risk_assessment"]}
        elif context_type == "emergency":
            return {k: v for k, v in context.items() if k in ["emergency_context", "risk_assessment"]}

        return context

    def _get_emergency_context(self, mission: MissionContext) -> Dict[str, Any]:
        """Get emergency context and intervention readiness."""
        emergency_types = ["agent_failure", "mission_blocked", "resource_shortage", "deadline_pressure"]

        emergency_readiness = {}
        for emergency_type in emergency_types:
            emergency_data = self.ssot_indexer.get_emergency_intervention(
                emergency_type,
                {"mission_phase": mission.current_phase, "agent_count": len(mission.agent_assignments)}
            )
            emergency_readiness[emergency_type] = {
                "preparedness_score": len(emergency_data.get("intervention_patterns", [])) / 10,
                "estimated_response_time": emergency_data.get("estimated_response_time", 300),
                "available_patterns": len(emergency_data.get("intervention_patterns", []))
            }

        return {
            "emergency_readiness": emergency_readiness,
            "high_risk_scenarios": [risk for risk in mission.risk_factors if self._is_high_risk(risk)],
            "intervention_protocols": self._get_intervention_protocols(mission)
        }

    def _is_high_risk(self, risk_factor: str) -> bool:
        """Determine if a risk factor is considered high risk."""
        high_risk_keywords = ["failure", "blockage", "shortage", "deadline", "critical", "emergency"]
        return any(keyword in risk_factor.lower() for keyword in high_risk_keywords)

    def _get_intervention_protocols(self, mission: MissionContext) -> List[str]:
        """Get relevant intervention protocols for the mission."""
        protocols = []

        if len(mission.agent_assignments) < 3:
            protocols.append("Agent reallocation protocol - insufficient agent coverage")

        if any(self._is_high_risk(risk) for risk in mission.risk_factors):
            protocols.append("Emergency escalation protocol - high risk factors detected")

        if mission.current_phase in ["critical", "final"]:
            protocols.append("Phase acceleration protocol - time-sensitive operations")

        return protocols

    def _optimize_agent_assignment(self, mission: MissionContext) -> Dict[str, Any]:
        """Optimize agent assignment based on capabilities and mission requirements."""
        available_agents = {aid: cap for aid, cap in self.agent_capabilities.items()
                          if cap.availability_status == "available"}

        # Calculate capability scores for each agent
        capability_scores = {}
        for agent_id, capability in available_agents.items():
            score = self._calculate_agent_score(capability, mission)
            capability_scores[agent_id] = score

        # Sort agents by capability score
        sorted_agents = sorted(capability_scores.items(), key=lambda x: x[1], reverse=True)

        recommendations = []
        assigned_agents = set(mission.agent_assignments.keys())

        for agent_id, score in sorted_agents[:5]:  # Top 5 recommendations
            if agent_id not in assigned_agents:
                agent = available_agents[agent_id]
                recommendations.append({
                    "agent_id": agent_id,
                    "capability_score": score,
                    "primary_role": agent.primary_role,
                    "specialization_match": self._calculate_specialization_match(agent, mission),
                    "workload_impact": "low" if agent.current_workload < 3 else "medium"
                })

        return {
            "top_recommendations": recommendations[:3],
            "capability_distribution": self._analyze_capability_distribution(available_agents, mission),
            "optimization_score": sum(score for _, score in sorted_agents[:len(mission.critical_path)]) / max(len(mission.critical_path), 1)
        }

    def _calculate_agent_score(self, capability: AgentCapability, mission: MissionContext) -> float:
        """Calculate capability score for agent-mission matching."""
        base_score = capability.success_rate * 100

        # Specialization bonus
        specialization_bonus = len(set(capability.specialization) & set(mission.critical_path)) * 20

        # Experience bonus
        experience_multipliers = {"beginner": 0.8, "intermediate": 1.0, "expert": 1.2, "master": 1.4}
        experience_bonus = experience_multipliers.get(capability.experience_level, 1.0)

        # Workload penalty
        workload_penalty = max(0, (capability.current_workload - 2) * 10)

        return (base_score + specialization_bonus) * experience_bonus - workload_penalty

    def _calculate_specialization_match(self, capability: AgentCapability, mission: MissionContext) -> str:
        """Calculate specialization match quality."""
        mission_skills = set(mission.critical_path)
        agent_skills = set(capability.specialization)

        if not get_unified_validator().validate_required(mission_skills):
            return "unknown"

        match_ratio = len(agent_skills & mission_skills) / len(mission_skills)

        if match_ratio >= 0.8:
            return "excellent"
        elif match_ratio >= 0.6:
            return "good"
        elif match_ratio >= 0.4:
            return "fair"
        else:
            return "poor"

    def _analyze_capability_distribution(self, available_agents: Dict[str, AgentCapability],
                                       mission: MissionContext) -> Dict[str, int]:
        """Analyze capability distribution across available agents."""
        role_distribution = Counter(agent.primary_role for agent in available_agents.values())

        specialization_coverage = set()
        for agent in available_agents.values():
            specialization_coverage.update(agent.specialization)

        return {
            "role_distribution": dict(role_distribution),
            "unique_specializations": len(specialization_coverage),
            "specialization_coverage": len(specialization_coverage & set(mission.critical_path)) / max(len(mission.critical_path), 1)
        }

    def _analyze_success_patterns(self, mission: MissionContext) -> Dict[str, Any]:
        """Analyze success patterns for the current mission type."""
        # Search for similar successful missions
        similar_missions = self.ssot_indexer.search_intelligent_context(
            f"successful {mission.mission_type} missions",
            context_type="mission",
            limit=5
        )

        # Extract common success factors
        success_factors = self._extract_success_factors(similar_missions)

        # Identify potential pitfalls
        pitfalls = self._identify_potential_pitfalls(mission, similar_missions)

        return {
            "similar_successful_missions": len(similar_missions),
            "common_success_factors": success_factors[:5],  # Top 5
            "potential_pitfalls": pitfalls[:3],  # Top 3
            "pattern_confidence": len(similar_missions) / 10  # Simple confidence metric
        }

    def _extract_success_factors(self, similar_missions: List[SearchResult]) -> List[str]:
        """Extract common success factors from similar missions."""
        success_keywords = ["efficient", "coordinated", "optimal", "successful", "completed", "excellent"]
        factors = []

        for result in similar_missions:
            content = result.content.lower()
            for keyword in success_keywords:
                if keyword in content:
                    # Extract sentence containing the keyword
                    sentences = content.split('.')
                    for sentence in sentences:
                        if keyword in sentence:
                            factors.append(sentence.strip().capitalize())
                            break
                    break

        return list(set(factors))  # Remove duplicates

    def _identify_potential_pitfalls(self, mission: MissionContext, similar_missions: List[SearchResult]) -> List[str]:
        """Identify potential pitfalls based on historical data."""
        pitfalls = []

        # Check for common failure patterns
        failure_patterns = ["delayed", "blocked", "failed", "insufficient", "mismatched", "overloaded"]

        for result in similar_missions:
            content = result.content.lower()
            for pattern in failure_patterns:
                if pattern in content:
                    pitfalls.append(f"Avoid {pattern} situations based on historical data")
                    break

        # Add mission-specific pitfalls
        if len(mission.agent_assignments) < len(mission.critical_path):
            pitfalls.append("Potential resource shortage - insufficient agent coverage")

        if any("deadline" in risk.lower() for risk in mission.risk_factors):
            pitfalls.append("Time pressure may lead to quality compromises")

        return list(set(pitfalls))  # Remove duplicates

    def _assess_mission_risks(self, mission: MissionContext) -> Dict[str, Any]:
        """Assess overall mission risks."""
        risk_score = len(mission.risk_factors) * 20  # Base risk from identified factors

        # Adjust based on agent coverage
        agent_coverage = len(mission.agent_assignments) / max(len(mission.critical_path), 1)
        if agent_coverage < 0.8:
            risk_score += 30

        # Adjust based on phase
        phase_risks = {"planning": 10, "execution": 20, "critical": 40, "final": 30}
        risk_score += phase_risks.get(mission.current_phase, 15)

        risk_level = "low" if risk_score < 30 else "medium" if risk_score < 60 else "high"

        return {
            "risk_score": min(risk_score, 100),
            "risk_level": risk_level,
            "primary_risk_factors": mission.risk_factors[:3],
            "mitigation_recommendations": self._generate_risk_mitigations(risk_level, mission)
        }

    def _generate_risk_mitigations(self, risk_level: str, mission: MissionContext) -> List[str]:
        """Generate risk mitigation recommendations."""
        mitigations = []

        if risk_level == "high":
            mitigations.extend([
                "Implement emergency escalation protocols",
                "Increase monitoring frequency",
                "Prepare contingency agent assignments"
            ])
        elif risk_level == "medium":
            mitigations.extend([
                "Regular progress check-ins",
                "Resource availability monitoring",
                "Early warning system activation"
            ])
        else:
            mitigations.extend([
                "Standard monitoring protocols",
                "Regular status updates"
            ])

        # Mission-specific mitigations
        if len(mission.agent_assignments) < 3:
            mitigations.append("Consider additional agent allocation")

        return mitigations

    def _calculate_success_probability(self, mission: MissionContext, agent_recommendations: Dict[str, Any]) -> float:
        """Calculate estimated success probability."""
        base_probability = 70.0  # Base success rate

        # Adjust based on agent optimization
        optimization_bonus = agent_recommendations.get("optimization_score", 50) / 2
        base_probability += optimization_bonus

        # Adjust based on risk level
        risk_penalty = 0
        risk_assessment = self._assess_mission_risks(mission)
        if risk_assessment["risk_level"] == "high":
            risk_penalty = 25
        elif risk_assessment["risk_level"] == "medium":
            risk_penalty = 10

        success_probability = max(10, min(95, base_probability - risk_penalty))

        return round(success_probability, 1)

    def get_predictive_insights(self, mission_id: str, prediction_horizon: int = 24) -> Dict[str, Any]:
        """
        Generate predictive insights for mission outcomes.

        Args:
            mission_id: Mission identifier
            prediction_horizon: Hours to predict ahead

        Returns:
            Predictive insights and recommendations
        """
        if mission_id not in self.active_missions:
            return {"error": f"Mission {mission_id} not found"}

        mission = self.active_missions[mission_id]

        # Get historical patterns for similar missions
        historical_patterns = self.ssot_indexer.search_intelligent_context(
            f"mission patterns for {mission.mission_type} over {prediction_horizon} hours",
            context_type="mission",
            limit=3
        )

        # Analyze current trajectory
        current_trajectory = self._analyze_current_trajectory(mission)

        # Generate predictions
        predictions = self._generate_predictions(mission, historical_patterns, prediction_horizon)

        return {
            "mission_id": mission_id,
            "prediction_horizon_hours": prediction_horizon,
            "current_trajectory": current_trajectory,
            "predictions": predictions,
            "recommended_actions": self._generate_predictive_actions(predictions),
            "generated_at": datetime.now().isoformat()
        }

    def _analyze_current_trajectory(self, mission: MissionContext) -> Dict[str, Any]:
        """Analyze current mission trajectory."""
        # Simple trajectory analysis based on phase and assignments
        phase_progress = {
            "planning": 0.2,
            "execution": 0.5,
            "critical": 0.8,
            "final": 0.95
        }

        progress_score = phase_progress.get(mission.current_phase, 0.5)
        agent_efficiency = len(mission.agent_assignments) / max(len(mission.critical_path), 1)

        return {
            "progress_score": progress_score,
            "agent_efficiency": agent_efficiency,
            "overall_trajectory": "on_track" if progress_score > 0.7 and agent_efficiency > 0.8 else "needs_attention"
        }

    def _generate_predictions(self, mission: MissionContext, historical_patterns: List[SearchResult],
                            prediction_horizon: int) -> Dict[str, Any]:
        """Generate predictions based on historical patterns."""
        # Simple prediction logic
        success_probability = self._calculate_success_probability(mission, self._optimize_agent_assignment(mission))

        time_to_completion = prediction_horizon * (1 + (1 - success_probability / 100))

        risk_trend = "stable"
        if len(mission.risk_factors) > 2:
            risk_trend = "increasing"
        elif len(mission.risk_factors) == 0:
            risk_trend = "decreasing"

        return {
            "estimated_completion_time_hours": round(time_to_completion, 1),
            "success_probability": success_probability,
            "risk_trend": risk_trend,
            "bottlenecks": self._identify_bottlenecks(mission),
            "confidence_level": len(historical_patterns) / 5  # Based on available historical data
        }

    def _identify_bottlenecks(self, mission: MissionContext) -> List[str]:
        """Identify potential bottlenecks in mission execution."""
        bottlenecks = []

        if len(mission.agent_assignments) < len(mission.critical_path):
            bottlenecks.append("Insufficient agent coverage for critical path tasks")

        if mission.current_phase == "critical" and len(mission.risk_factors) > 0:
            bottlenecks.append("High-risk operations in critical phase")

        if any("deadline" in risk.lower() for risk in mission.risk_factors):
            bottlenecks.append("Time pressure may cause quality bottlenecks")

        return bottlenecks

    def _generate_predictive_actions(self, predictions: Dict[str, Any]) -> List[str]:
        """Generate predictive action recommendations."""
        actions = []

        if predictions["success_probability"] < 70:
            actions.append("Consider additional resource allocation to improve success probability")

        if predictions["risk_trend"] == "increasing":
            actions.append("Implement additional risk monitoring and mitigation strategies")

        if predictions["estimated_completion_time_hours"] > predictions.get("prediction_horizon_hours", 24):
            actions.append("Consider timeline extension or acceleration strategies")

        if predictions["bottlenecks"]:
            actions.append("Address identified bottlenecks proactively")

        return actions
