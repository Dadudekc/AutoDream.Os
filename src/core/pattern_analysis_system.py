"""
Pattern Analysis System for Strategic Decision Making

This module provides advanced pattern analysis capabilities for:
- Mission success pattern recognition
- Strategic decision optimization
- Cross-mission learning and adaptation
- Predictive analytics based on historical data

Key Features:
- Success/failure pattern identification
- Cross-domain pattern correlation
- Real-time pattern adaptation
- Strategic recommendation generation

Author: Agent-3 (Pattern Analysis System)
"""

from datetime import datetime



@dataclass
class MissionPattern:
    """Mission pattern structure for analysis."""

    pattern_id: str
    pattern_type: str
    mission_type: str
    success_indicators: List[str] = field(default_factory=list)
    failure_indicators: List[str] = field(default_factory=list)
    optimal_conditions: Dict[str, Any] = field(default_factory=dict)
    risk_factors: List[str] = field(default_factory=list)
    success_rate: float = 0.0
    average_duration: float = 0.0
    confidence_score: float = 0.0
    usage_count: int = 0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class PatternCorrelation:
    """Pattern correlation structure."""

    correlation_id: str
    pattern_a: str
    pattern_b: str
    correlation_strength: float
    correlation_type: str  # "success", "failure", "resource", "time"
    evidence_count: int = 0
    confidence_level: float = 0.0


@dataclass
class StrategicRecommendation:
    """Strategic recommendation structure."""

    recommendation_id: str
    mission_context: str
    recommendation_type: str
    confidence_score: float
    expected_impact: str
    implementation_steps: List[str] = field(default_factory=list)
    risk_assessment: str = "medium"
    generated_at: datetime = field(default_factory=datetime.now)


class PatternAnalysisSystem:
    """
    Pattern Analysis System for Strategic Decision Making.

    This system analyzes historical mission data to identify patterns,
    correlations, and optimal strategies for future mission success.
    """

    def __init__(self, ssot_indexer: VectorDatabaseSSOTIndexer):
        """Initialize the pattern analysis system."""
        self.ssot_indexer = ssot_indexer
        self.mission_patterns: Dict[str, MissionPattern] = {}
        self.pattern_correlations: List[PatternCorrelation] = []
        self.strategic_recommendations: List[StrategicRecommendation] = []

        # Initialize with known patterns
        self._initialize_base_patterns()

    def _initialize_base_patterns(self):
        """Initialize base patterns from historical data."""
        base_patterns = [
            MissionPattern(
                pattern_id="coordination_efficiency",
                pattern_type="coordination",
                mission_type="general",
                success_indicators=["clear_communication", "resource_optimization", "timeline_adherence"],
                failure_indicators=["communication_gaps", "resource_conflicts", "timeline_delays"],
                optimal_conditions={"agent_count": "4-6", "communication_frequency": "high"},
                risk_factors=["unclear_objectives", "resource_shortage"],
                success_rate=0.85,
                average_duration=120.0,  # minutes
                confidence_score=0.9
            ),
            MissionPattern(
                pattern_id="emergency_response",
                pattern_type="emergency",
                mission_type="intervention",
                success_indicators=["rapid_response", "clear_escalation", "resource_reallocation"],
                failure_indicators=["delayed_response", "unclear_chain_of_command", "resource_confusion"],
                optimal_conditions={"response_time": "<5_min", "escalation_path": "clear"},
                risk_factors=["unclear_emergency_criteria", "insufficient_backup_resources"],
                success_rate=0.75,
                average_duration=15.0,  # minutes
                confidence_score=0.85
            ),
            MissionPattern(
                pattern_id="resource_optimization",
                pattern_type="resource",
                mission_type="general",
                success_indicators=["balanced_workload", "skill_matching", "efficient_utilization"],
                failure_indicators=["workload_imbalance", "skill_mismatch", "resource_waste"],
                optimal_conditions={"workload_distribution": "balanced", "skill_utilization": ">80%"},
                risk_factors=["inadequate_resource_assessment", "changing_requirements"],
                success_rate=0.8,
                average_duration=90.0,  # minutes
                confidence_score=0.88
            )
        ]

        for pattern in base_patterns:
            self.mission_patterns[pattern.pattern_id] = pattern

    def analyze_mission_patterns(self, mission_context: MissionContext) -> Dict[str, Any]:
        """
        Analyze patterns for a given mission context.

        Args:
            mission_context: Current mission context

        Returns:
            Pattern analysis results with insights and recommendations
        """
        # Identify relevant patterns
        relevant_patterns = self._identify_relevant_patterns(mission_context)

        # Calculate pattern effectiveness
        pattern_effectiveness = self._calculate_pattern_effectiveness(relevant_patterns, mission_context)

        # Generate pattern-based recommendations
        pattern_recommendations = self._generate_pattern_recommendations(relevant_patterns, mission_context)

        # Identify potential risks based on patterns
        pattern_risks = self._identify_pattern_based_risks(relevant_patterns, mission_context)

        # Calculate success probability based on patterns
        success_probability = self._calculate_pattern_based_success_probability(
            relevant_patterns, mission_context
        )

        return {
            "mission_id": mission_context.mission_id,
            "relevant_patterns": [pattern.pattern_id for pattern in relevant_patterns],
            "pattern_effectiveness": pattern_effectiveness,
            "pattern_recommendations": pattern_recommendations,
            "pattern_based_risks": pattern_risks,
            "pattern_success_probability": success_probability,
            "analysis_confidence": self._calculate_analysis_confidence(relevant_patterns),
            "generated_at": datetime.now().isoformat()
        }

    def _identify_relevant_patterns(self, mission_context: MissionContext) -> List[MissionPattern]:
        """Identify patterns relevant to the current mission context."""
        relevant_patterns = []

        # Match by mission type
        for pattern in self.mission_patterns.values():
            if pattern.mission_type == mission_context.mission_type or pattern.mission_type == "general":
                relevance_score = self._calculate_pattern_relevance(pattern, mission_context)
                if relevance_score > 0.6:  # Threshold for relevance
                    relevant_patterns.append(pattern)

        # Sort by relevance (could be enhanced with more sophisticated scoring)
        relevant_patterns.sort(key=lambda p: p.success_rate, reverse=True)

        return relevant_patterns[:5]  # Return top 5 most relevant patterns

    def _calculate_pattern_relevance(self, pattern: MissionPattern, mission_context: MissionContext) -> float:
        """Calculate how relevant a pattern is to the current mission context."""
        relevance_score = 0.0

        # Mission type match
        if pattern.mission_type == mission_context.mission_type:
            relevance_score += 0.4
        elif pattern.mission_type == "general":
            relevance_score += 0.2

        # Current phase alignment
        if mission_context.current_phase in ["execution", "critical"]:
            relevance_score += 0.2

        # Risk factor alignment
        mission_risks = set(mission_context.risk_factors)
        pattern_risks = set(pattern.risk_factors)
        risk_overlap = len(mission_risks & pattern_risks)
        relevance_score += min(0.3, risk_overlap * 0.1)

        # Agent count consideration
        agent_count = len(mission_context.agent_assignments)
        if "agent_count" in pattern.optimal_conditions:
            optimal_range = pattern.optimal_conditions["agent_count"]
            if optimal_range == "4-6" and 4 <= agent_count <= 6:
                relevance_score += 0.1

        return min(1.0, relevance_score)

    def _calculate_pattern_effectiveness(self, patterns: List[MissionPattern],
                                       mission_context: MissionContext) -> Dict[str, Any]:
        """Calculate overall effectiveness of identified patterns."""
        if not get_unified_validator().validate_required(patterns):
            return {"overall_effectiveness": 0.0, "confidence_level": 0.0}

        # Calculate weighted effectiveness
        total_weight = 0
        weighted_effectiveness = 0

        for pattern in patterns:
            weight = pattern.confidence_score * pattern.usage_count
            weighted_effectiveness += pattern.success_rate * weight
            total_weight += weight

        overall_effectiveness = weighted_effectiveness / total_weight if total_weight > 0 else 0.0

        # Calculate confidence based on pattern consensus
        success_rates = [p.success_rate for p in patterns]
        confidence_level = statistics.stdev(success_rates) if len(success_rates) > 1 else 0.5
        confidence_level = max(0.1, 1.0 - confidence_level)  # Invert so higher consensus = higher confidence

        return {
            "overall_effectiveness": round(overall_effectiveness, 3),
            "confidence_level": round(confidence_level, 3),
            "pattern_count": len(patterns),
            "average_success_rate": round(statistics.mean(success_rates), 3) if success_rates else 0.0
        }

    def _generate_pattern_recommendations(self, patterns: List[MissionPattern],
                                        mission_context: MissionContext) -> List[Dict[str, Any]]:
        """Generate pattern-based recommendations for mission success."""
        recommendations = []

        for pattern in patterns:
            if pattern.success_rate > 0.7:  # Only recommend from high-success patterns
                recommendation = {
                    "pattern_id": pattern.pattern_id,
                    "recommendation_type": "adopt_success_factors",
                    "description": f"Adopt {pattern.pattern_type} pattern with {pattern.success_rate:.1%} success rate",
                    "success_indicators": pattern.success_indicators[:3],
                    "implementation_priority": "high" if pattern.success_rate > 0.85 else "medium",
                    "expected_impact": "significant" if pattern.confidence_score > 0.8 else "moderate"
                }
                recommendations.append(recommendation)

        # Sort by expected impact and success rate
        recommendations.sort(key=lambda r: (r["expected_impact"], r.get("success_indicators", [])), reverse=True)

        return recommendations[:5]  # Return top 5 recommendations

    def _identify_pattern_based_risks(self, patterns: List[MissionPattern],
                                    mission_context: MissionContext) -> List[Dict[str, Any]]:
        """Identify risks based on pattern analysis."""
        risks = []

        # Analyze failure indicators from patterns
        failure_indicators = set()
        for pattern in patterns:
            failure_indicators.update(pattern.failure_indicators)

        # Check current mission against failure indicators
        mission_description = f"{mission_context.mission_type} {mission_context.current_phase}"
        for indicator in failure_indicators:
            if self._matches_failure_indicator(mission_description, mission_context.risk_factors, indicator):
                risk = {
                    "risk_type": "pattern_based",
                    "indicator": indicator,
                    "severity": "high" if any(pattern.success_rate < 0.7 for pattern in patterns) else "medium",
                    "mitigation_strategy": self._generate_mitigation_strategy(indicator)
                }
                risks.append(risk)

        return risks[:3]  # Return top 3 risks

    def _matches_failure_indicator(self, mission_desc: str, risk_factors: List[str], indicator: str) -> bool:
        """Check if current mission matches a failure indicator."""
        # Simple keyword matching (could be enhanced with NLP)
        mission_text = (mission_desc + " " + " ".join(risk_factors)).lower()
        indicator_keywords = indicator.lower().replace("_", " ")

        # Check for keyword matches
        keywords = indicator_keywords.split()
        matches = sum(1 for keyword in keywords if keyword in mission_text)

        return matches >= len(keywords) * 0.6  # 60% keyword match threshold

    def _generate_mitigation_strategy(self, indicator: str) -> str:
        """Generate mitigation strategy for a failure indicator."""
        mitigation_map = {
            "communication_gaps": "Establish clear communication protocols and regular check-ins",
            "resource_conflicts": "Implement resource allocation planning and conflict resolution procedures",
            "timeline_delays": "Create detailed timeline with buffer time and milestone tracking",
            "unclear_objectives": "Define clear objectives, success criteria, and deliverables upfront",
            "resource_shortage": "Develop resource contingency plans and backup allocation strategies"
        }

        return mitigation_map.get(indicator, f"Monitor and address {indicator.replace('_', ' ')} proactively")

    def _calculate_pattern_based_success_probability(self, patterns: List[MissionPattern],
                                                  mission_context: MissionContext) -> float:
        """Calculate success probability based on pattern analysis."""
        if not get_unified_validator().validate_required(patterns):
            return 50.0  # Default neutral probability

        # Base probability from pattern success rates
        success_rates = [p.success_rate for p in patterns]
        base_probability = statistics.mean(success_rates) * 100

        # Adjust for pattern relevance
        relevance_adjustment = 0
        for pattern in patterns:
            relevance = self._calculate_pattern_relevance(pattern, mission_context)
            relevance_adjustment += (relevance - 0.5) * 10  # +/- 10% based on relevance

        # Adjust for risk factors
        risk_penalty = len(mission_context.risk_factors) * 5  # 5% penalty per risk factor

        # Adjust for agent coverage
        agent_coverage = len(mission_context.agent_assignments) / max(len(mission_context.critical_path), 1)
        coverage_bonus = (agent_coverage - 0.8) * 20 if agent_coverage > 0.8 else (0.8 - agent_coverage) * 30

        final_probability = base_probability + relevance_adjustment - risk_penalty + coverage_bonus

        return max(5.0, min(95.0, final_probability))  # Clamp between 5% and 95%

    def _calculate_analysis_confidence(self, patterns: List[MissionPattern]) -> float:
        """Calculate confidence level of the pattern analysis."""
        if not get_unified_validator().validate_required(patterns):
            return 0.0

        # Confidence based on pattern usage and consistency
        usage_scores = [p.usage_count for p in patterns]
        avg_usage = statistics.mean(usage_scores) if usage_scores else 0

        # Confidence based on success rate consistency
        success_rates = [p.success_rate for p in patterns]
        consistency_score = 1.0 - (statistics.stdev(success_rates) if len(success_rates) > 1 else 0)

        # Combined confidence score
        confidence = (avg_usage / 10 + consistency_score) / 2  # Normalize usage to 0-1 scale

        return min(1.0, confidence)

    def update_pattern_from_mission_outcome(self, mission_context: MissionContext,
                                          outcome: str, duration: float) -> None:
        """
        Update patterns based on mission outcomes for continuous learning.

        Args:
            mission_context: Completed mission context
            outcome: Mission outcome ("success" or "failure")
            duration: Mission duration in minutes
        """
        # Identify relevant patterns for this mission
        relevant_patterns = self._identify_relevant_patterns(mission_context)

        for pattern in relevant_patterns:
            # Update usage count
            pattern.usage_count += 1

            # Update success rate using exponential moving average
            outcome_value = 1.0 if outcome == "success" else 0.0
            alpha = 0.1  # Learning rate
            pattern.success_rate = (1 - alpha) * pattern.success_rate + alpha * outcome_value

            # Update average duration
            pattern.average_duration = (pattern.average_duration + duration) / 2

            # Update confidence score based on usage
            pattern.confidence_score = min(1.0, pattern.usage_count / 20)

            # Update last updated timestamp
            pattern.last_updated = datetime.now()

            # Store updated pattern
            self.mission_patterns[pattern.pattern_id] = pattern

    def find_pattern_correlations(self) -> List[Dict[str, Any]]:
        """
        Find correlations between different patterns for strategic insights.

        Returns:
            List of pattern correlations with insights
        """
        correlations = []

        # Analyze success pattern correlations
        success_patterns = [p for p in self.mission_patterns.values() if p.success_rate > 0.8]

        for i, pattern_a in enumerate(success_patterns):
            for pattern_b in success_patterns[i+1:]:
                # Calculate correlation based on shared success indicators
                shared_indicators = set(pattern_a.success_indicators) & set(pattern_b.success_indicators)
                correlation_strength = len(shared_indicators) / max(len(pattern_a.success_indicators), 1)

                if correlation_strength > 0.3:  # Significant correlation threshold
                    correlation = {
                        "pattern_a": pattern_a.pattern_id,
                        "pattern_b": pattern_b.pattern_id,
                        "correlation_type": "success_indicators",
                        "correlation_strength": round(correlation_strength, 3),
                        "shared_indicators": list(shared_indicators),
                        "combined_success_rate": round((pattern_a.success_rate + pattern_b.success_rate) / 2, 3)
                    }
                    correlations.append(correlation)

        return correlations

    def generate_strategic_insights(self, mission_context: MissionContext) -> List[StrategicRecommendation]:
        """
        Generate strategic insights and recommendations for mission optimization.

        Args:
            mission_context: Current mission context

        Returns:
            List of strategic recommendations
        """
        insights = []

        # Pattern-based insights
        pattern_analysis = self.analyze_mission_patterns(mission_context)

        if pattern_analysis["pattern_success_probability"] > 80:
            insight = StrategicRecommendation(
                recommendation_id=f"pattern_success_{mission_context.mission_id}",
                mission_context=mission_context.mission_id,
                recommendation_type="pattern_adoption",
                confidence_score=pattern_analysis["analysis_confidence"],
                expected_impact="high",
                implementation_steps=[
                    "Adopt identified success patterns",
                    "Implement recommended coordination strategies",
                    "Monitor pattern effectiveness during execution"
                ],
                risk_assessment="low"
            )
            insights.append(insight)

        # Correlation-based insights
        correlations = self.find_pattern_correlations()
        if correlations:
            top_correlation = max(correlations, key=lambda c: c["correlation_strength"])
            if top_correlation["correlation_strength"] > 0.5:
                insight = StrategicRecommendation(
                    recommendation_id=f"correlation_optimization_{mission_context.mission_id}",
                    mission_context=mission_context.mission_id,
                    recommendation_type="correlation_leverage",
                    confidence_score=top_correlation["correlation_strength"],
                    expected_impact="medium",
                    implementation_steps=[
                        f"Combine {top_correlation['pattern_a']} and {top_correlation['pattern_b']} approaches",
                        "Leverage shared success indicators",
                        "Monitor combined pattern effectiveness"
                    ],
                    risk_assessment="medium"
                )
                insights.append(insight)

        # Risk mitigation insights
        if pattern_analysis["pattern_based_risks"]:
            insight = StrategicRecommendation(
                recommendation_id=f"risk_mitigation_{mission_context.mission_id}",
                mission_context=mission_context.mission_id,
                recommendation_type="risk_mitigation",
                confidence_score=0.8,
                expected_impact="high",
                implementation_steps=[
                    "Implement identified mitigation strategies",
                    "Monitor risk indicators continuously",
                    "Prepare contingency plans for high-risk scenarios"
                ],
                risk_assessment="low"
            )
            insights.append(insight)

        return insights

    def get_pattern_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics for the pattern analysis system."""
        total_patterns = len(self.mission_patterns)
        active_patterns = sum(1 for p in self.mission_patterns.values() if p.usage_count > 0)

        success_rates = [p.success_rate for p in self.mission_patterns.values()]
        avg_success_rate = statistics.mean(success_rates) if success_rates else 0.0

        confidence_scores = [p.confidence_score for p in self.mission_patterns.values()]
        avg_confidence = statistics.mean(confidence_scores) if confidence_scores else 0.0

        # Pattern effectiveness distribution
        high_effective = sum(1 for p in self.mission_patterns.values() if p.success_rate > 0.8)
        medium_effective = sum(1 for p in self.mission_patterns.values() if 0.6 <= p.success_rate <= 0.8)
        low_effective = sum(1 for p in self.mission_patterns.values() if p.success_rate < 0.6)

        return {
            "total_patterns": total_patterns,
            "active_patterns": active_patterns,
            "average_success_rate": round(avg_success_rate, 3),
            "average_confidence": round(avg_confidence, 3),
            "pattern_effectiveness_distribution": {
                "high_effective": high_effective,
                "medium_effective": medium_effective,
                "low_effective": low_effective
            },
            "pattern_usage_distribution": sorted(
                [(p.pattern_id, p.usage_count) for p in self.mission_patterns.values()],
                key=lambda x: x[1],
                reverse=True
            )[:10],  # Top 10 most used patterns
            "last_updated": datetime.now().isoformat()
        }
