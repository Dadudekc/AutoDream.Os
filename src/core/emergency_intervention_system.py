"""
Emergency Intervention System for Strategic Oversight

This module provides emergency intervention capabilities for:
- Real-time emergency detection and classification
- Automated intervention protocol activation
- Historical pattern-based response optimization
- Captain Agent-4 emergency coordination support

Key Features:
- Emergency pattern recognition and classification
- Automated escalation protocols
- Historical success pattern utilization
- Real-time intervention coordination

Author: Agent-3 (Emergency Intervention System)
"""

from datetime import datetime



class EmergencySeverity(Enum):
    """Emergency severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmergencyType(Enum):
    """Types of emergencies that can occur."""

    AGENT_FAILURE = "agent_failure"
    MISSION_BLOCKED = "mission_blocked"
    RESOURCE_SHORTAGE = "resource_shortage"
    DEADLINE_PRESSURE = "deadline_pressure"
    COMMUNICATION_BREAKDOWN = "communication_breakdown"
    QUALITY_DEGRADATION = "quality_degradation"
    SYSTEM_OVERLOAD = "system_overload"
    SECURITY_INCIDENT = "security_incident"


@dataclass
class EmergencyEvent:
    """Emergency event structure."""

    event_id: str
    emergency_type: EmergencyType
    severity: EmergencySeverity
    description: str
    affected_mission: Optional[str] = None
    affected_agents: List[str] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.now)
    escalated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    intervention_steps: List[str] = field(default_factory=list)
    outcome: Optional[str] = None
    response_time_seconds: Optional[float] = None


@dataclass
class InterventionProtocol:
    """Intervention protocol structure."""

    protocol_id: str
    emergency_type: EmergencyType
    severity_threshold: EmergencySeverity
    activation_criteria: List[str] = field(default_factory=list)
    intervention_steps: List[str] = field(default_factory=list)
    required_resources: Dict[str, int] = field(default_factory=dict)
    estimated_duration_minutes: int = 30
    success_rate: float = 0.0
    usage_count: int = 0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class InterventionResult:
    """Intervention result structure."""

    intervention_id: str
    emergency_event: EmergencyEvent
    protocol_used: InterventionProtocol
    success_score: float
    actual_duration_minutes: float
    resources_used: Dict[str, int] = field(default_factory=dict)
    lessons_learned: List[str] = field(default_factory=list)
    completed_at: datetime = field(default_factory=datetime.now)


class EmergencyInterventionSystem:
    """
    Emergency Intervention System for Strategic Oversight.

    This system provides automated emergency detection, classification,
    and intervention capabilities based on historical patterns and
    real-time mission monitoring.
    """

    def __init__(self, ssot_indexer: VectorDatabaseSSOTIndexer,
                 context_retrieval: IntelligentContextRetrieval,
                 pattern_analysis: PatternAnalysisSystem,
                 messaging_core: Optional[UnifiedMessagingCore] = None):
        """Initialize the emergency intervention system."""
        self.ssot_indexer = ssot_indexer
        self.context_retrieval = context_retrieval
        self.pattern_analysis = pattern_analysis
        self.messaging_core = messaging_core

        # Emergency tracking
        self.active_emergencies: Dict[str, EmergencyEvent] = {}
        self.intervention_history: List[InterventionResult] = []

        # Intervention protocols
        self.intervention_protocols: Dict[str, InterventionProtocol] = {}
        self._initialize_base_protocols()

        # Emergency detection patterns
        self.emergency_patterns = self._initialize_emergency_patterns()

        # Monitoring state
        self.monitoring_active = False
        self.monitoring_task: Optional[asyncio.Task] = None

    def _initialize_base_protocols(self):
        """Initialize base intervention protocols."""
        base_protocols = [
            InterventionProtocol(
                protocol_id="agent_failure_recovery",
                emergency_type=EmergencyType.AGENT_FAILURE,
                severity_threshold=EmergencySeverity.HIGH,
                activation_criteria=[
                    "agent unresponsive for >5 minutes",
                    "critical task blocked",
                    "no backup agent available"
                ],
                intervention_steps=[
                    "Assess agent failure scope and impact",
                    "Identify backup agent with similar capabilities",
                    "Reassign critical tasks to backup agent",
                    "Notify Captain Agent-4 of intervention",
                    "Monitor reassignment effectiveness"
                ],
                required_resources={"backup_agents": 1, "communication_channels": 1},
                estimated_duration_minutes=15,
                success_rate=0.85
            ),
            InterventionProtocol(
                protocol_id="mission_blockage_resolution",
                emergency_type=EmergencyType.MISSION_BLOCKED,
                severity_threshold=EmergencySeverity.CRITICAL,
                activation_criteria=[
                    "mission stalled for >30 minutes",
                    "critical path blocked",
                    "deadline approaching within 2 hours"
                ],
                intervention_steps=[
                    "Analyze blockage root cause",
                    "Identify alternative approaches from pattern analysis",
                    "Reallocate resources to unblock critical path",
                    "Implement parallel processing where possible",
                    "Escalate to Captain Agent-4 if unresolved"
                ],
                required_resources={"analysis_agents": 2, "coordination_support": 1},
                estimated_duration_minutes=45,
                success_rate=0.75
            ),
            InterventionProtocol(
                protocol_id="resource_shortage_mitigation",
                emergency_type=EmergencyType.RESOURCE_SHORTAGE,
                severity_threshold=EmergencySeverity.MEDIUM,
                activation_criteria=[
                    "resource utilization >90%",
                    "no available backup resources",
                    "mission timeline at risk"
                ],
                intervention_steps=[
                    "Audit current resource utilization",
                    "Identify resource optimization opportunities",
                    "Reallocate resources from low-priority tasks",
                    "Implement resource sharing protocols",
                    "Monitor resource utilization post-intervention"
                ],
                required_resources={"resource_auditor": 1, "coordination_agent": 1},
                estimated_duration_minutes=30,
                success_rate=0.80
            ),
            InterventionProtocol(
                protocol_id="deadline_pressure_management",
                emergency_type=EmergencyType.DEADLINE_PRESSURE,
                severity_threshold=EmergencySeverity.HIGH,
                activation_criteria=[
                    "deadline within 4 hours",
                    "completion rate <70% of target",
                    "scope creep detected"
                ],
                intervention_steps=[
                    "Assess current completion status",
                    "Prioritize remaining tasks by impact",
                    "Implement focused execution mode",
                    "Reduce non-essential activities",
                    "Provide Captain Agent-4 status update"
                ],
                required_resources={"coordination_agent": 1, "execution_support": 2},
                estimated_duration_minutes=60,
                success_rate=0.70
            )
        ]

        for protocol in base_protocols:
            self.intervention_protocols[protocol.protocol_id] = protocol

    def _initialize_emergency_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize emergency detection patterns."""
        return {
            "agent_unresponsive": {
                "keywords": ["unresponsive", "no response", "timeout", "failed"],
                "severity_mapping": {"high": EmergencySeverity.HIGH, "critical": EmergencySeverity.CRITICAL},
                "emergency_type": EmergencyType.AGENT_FAILURE
            },
            "mission_blocked": {
                "keywords": ["blocked", "stalled", "stuck", "cannot proceed", "deadlock"],
                "severity_mapping": {"medium": EmergencySeverity.MEDIUM, "high": EmergencySeverity.HIGH},
                "emergency_type": EmergencyType.MISSION_BLOCKED
            },
            "resource_critical": {
                "keywords": ["resource shortage", "out of resources", "capacity exceeded", "overload"],
                "severity_mapping": {"medium": EmergencySeverity.MEDIUM, "high": EmergencySeverity.CRITICAL},
                "emergency_type": EmergencyType.RESOURCE_SHORTAGE
            },
            "deadline_crisis": {
                "keywords": ["deadline approaching", "running out of time", "time critical", "urgent"],
                "severity_mapping": {"medium": EmergencySeverity.MEDIUM, "high": EmergencySeverity.CRITICAL},
                "emergency_type": EmergencyType.DEADLINE_PRESSURE
            },
            "communication_failure": {
                "keywords": ["communication breakdown", "cannot reach", "coordination failure"],
                "severity_mapping": {"medium": EmergencySeverity.MEDIUM, "high": EmergencySeverity.HIGH},
                "emergency_type": EmergencyType.COMMUNICATION_BREAKDOWN
            }
        }

    async def detect_emergency(self, mission_context: MissionContext,
                             system_status: Dict[str, Any]) -> Optional[EmergencyEvent]:
        """
        Detect potential emergencies based on mission context and system status.

        Args:
            mission_context: Current mission context
            system_status: Current system status information

        Returns:
            EmergencyEvent if emergency detected, None otherwise
        """
        # Analyze mission context for emergency indicators
        emergency_indicators = self._analyze_mission_for_emergencies(mission_context, system_status)

        if not get_unified_validator().validate_required(emergency_indicators):
            return None

        # Determine most critical emergency
        most_critical = max(emergency_indicators, key=lambda e: self._get_severity_score(e["severity"]))

        # Create emergency event
        emergency_event = EmergencyEvent(
            event_id=f"emergency_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            emergency_type=most_critical["type"],
            severity=most_critical["severity"],
            description=most_critical["description"],
            affected_mission=mission_context.mission_id,
            affected_agents=list(mission_context.agent_assignments.keys())
        )

        # Store active emergency
        self.active_emergencies[emergency_event.event_id] = emergency_event

        return emergency_event

    def _analyze_mission_for_emergencies(self, mission_context: MissionContext,
                                       system_status: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze mission context for emergency indicators."""
        emergency_indicators = []

        # Check agent responsiveness
        unresponsive_agents = self._get_unified_validator().check_agent_responsiveness(system_status)
        if unresponsive_agents:
            emergency_indicators.append({
                "type": EmergencyType.AGENT_FAILURE,
                "severity": EmergencySeverity.HIGH if len(unresponsive_agents) > 1 else EmergencySeverity.MEDIUM,
                "description": f"Agents unresponsive: {', '.join(unresponsive_agents)}"
            })

        # Check mission progress
        progress_status = self._analyze_mission_progress(mission_context)
        if progress_status["is_emergency"]:
            emergency_indicators.append({
                "type": EmergencyType.MISSION_BLOCKED,
                "severity": progress_status["severity"],
                "description": progress_status["description"]
            })

        # Check resource utilization
        resource_status = self._analyze_resource_utilization(system_status)
        if resource_status["is_emergency"]:
            emergency_indicators.append({
                "type": EmergencyType.RESOURCE_SHORTAGE,
                "severity": resource_status["severity"],
                "description": resource_status["description"]
            })

        # Check deadline pressure
        deadline_status = self._analyze_deadline_pressure(mission_context)
        if deadline_status["is_emergency"]:
            emergency_indicators.append({
                "type": EmergencyType.DEADLINE_PRESSURE,
                "severity": deadline_status["severity"],
                "description": deadline_status["description"]
            })

        return emergency_indicators

    def _get_unified_validator().check_agent_responsiveness(self, system_status: Dict[str, Any]) -> List[str]:
        """Check for unresponsive agents."""
        unresponsive = []
        agent_status = system_status.get("agent_status", {})

        for agent_id, status in agent_status.items():
            last_seen = status.get("last_seen")
            if last_seen:
                time_since_last_seen = datetime.now() - datetime.fromisoformat(last_seen)
                if time_since_last_seen.total_seconds() > 300:  # 5 minutes
                    unresponsive.append(agent_id)

        return unresponsive

    def _analyze_mission_progress(self, mission_context: MissionContext) -> Dict[str, Any]:
        """Analyze mission progress for potential blockages."""
        # This is a simplified analysis - in practice, this would be more sophisticated
        time_elapsed = (datetime.now() - mission_context.created_at).total_seconds() / 3600  # hours

        # Simple heuristic: if mission has been running for >2 hours and still in planning/early execution
        if time_elapsed > 2 and mission_context.current_phase in ["planning", "execution"]:
            return {
                "is_emergency": True,
                "severity": EmergencySeverity.MEDIUM,
                "description": f"Mission {mission_context.mission_id} appears stalled in {mission_context.current_phase} phase"
            }

        return {"is_emergency": False}

    def _analyze_resource_utilization(self, system_status: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze resource utilization for shortages."""
        resource_usage = system_status.get("resource_usage", {})

        for resource_type, usage_percent in resource_usage.items():
            if usage_percent > 90:
                return {
                    "is_emergency": True,
                    "severity": EmergencySeverity.HIGH,
                    "description": f"Critical resource shortage: {resource_type} at {usage_percent}% utilization"
                }

        return {"is_emergency": False}

    def _analyze_deadline_pressure(self, mission_context: MissionContext) -> Dict[str, Any]:
        """Analyze deadline pressure for emergencies."""
        # Check if any risk factors indicate deadline pressure
        deadline_risks = [risk for risk in mission_context.risk_factors
                         if "deadline" in risk.lower() or "time" in risk.lower()]

        if deadline_risks and mission_context.current_phase in ["critical", "final"]:
            return {
                "is_emergency": True,
                "severity": EmergencySeverity.HIGH,
                "description": f"Deadline pressure detected with risks: {', '.join(deadline_risks)}"
            }

        return {"is_emergency": False}

    def _get_severity_score(self, severity: EmergencySeverity) -> int:
        """Get numerical score for severity level."""
        severity_scores = {
            EmergencySeverity.LOW: 1,
            EmergencySeverity.MEDIUM: 2,
            EmergencySeverity.HIGH: 3,
            EmergencySeverity.CRITICAL: 4
        }
        return severity_scores.get(severity, 0)

    async def activate_intervention_protocol(self, emergency_event: EmergencyEvent) -> Dict[str, Any]:
        """
        Activate appropriate intervention protocol for emergency.

        Args:
            emergency_event: The emergency event requiring intervention

        Returns:
            Intervention activation results
        """
        # Find appropriate protocol
        protocol = self._select_intervention_protocol(emergency_event)

        if not get_unified_validator().validate_required(protocol):
            return {
                "success": False,
                "error": "No suitable intervention protocol found",
                "emergency_id": emergency_event.event_id
            }

        # Mark emergency as escalated
        emergency_event.escalated_at = datetime.now()
        emergency_event.intervention_steps = protocol.intervention_steps

        # Execute intervention steps
        intervention_start = time.time()
        intervention_result = await self._execute_intervention_steps(emergency_event, protocol)
        intervention_duration = (time.time() - intervention_start) / 60  # minutes

        # Create intervention result
        result = InterventionResult(
            intervention_id=f"intervention_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            emergency_event=emergency_event,
            protocol_used=protocol,
            success_score=intervention_result["success_score"],
            actual_duration_minutes=intervention_duration,
            resources_used=intervention_result.get("resources_used", {}),
            lessons_learned=intervention_result.get("lessons_learned", [])
        )

        # Store intervention result
        self.intervention_history.append(result)

        # Update protocol success rate
        self._update_protocol_success_rate(protocol, intervention_result["success_score"])

        # Notify Captain Agent-4
        await self._notify_captain_intervention(emergency_event, intervention_result)

        return {
            "success": intervention_result["success_score"] > 0.5,
            "intervention_id": result.intervention_id,
            "protocol_used": protocol.protocol_id,
            "success_score": intervention_result["success_score"],
            "duration_minutes": intervention_duration,
            "emergency_id": emergency_event.event_id
        }

    def _select_intervention_protocol(self, emergency_event: EmergencyEvent) -> Optional[InterventionProtocol]:
        """Select the most appropriate intervention protocol."""
        candidate_protocols = []

        for protocol in self.intervention_protocols.values():
            if (protocol.emergency_type == emergency_event.emergency_type and
                self._get_severity_score(emergency_event.severity) >= self._get_severity_score(protocol.severity_threshold)):
                candidate_protocols.append(protocol)

        if not get_unified_validator().validate_required(candidate_protocols):
            return None

        # Select protocol with highest success rate
        return max(candidate_protocols, key=lambda p: p.success_rate)

    async def _execute_intervention_steps(self, emergency_event: EmergencyEvent,
                                        protocol: InterventionProtocol) -> Dict[str, Any]:
        """Execute intervention protocol steps."""
        success_score = 1.0
        resources_used = {}
        lessons_learned = []

        for step in protocol.intervention_steps:
            try:
                # Simulate step execution (in real implementation, this would be actual execution)
                await asyncio.sleep(0.1)  # Brief delay to simulate processing

                # Assess step success (simplified)
                step_success = self._assess_step_success(step, emergency_event)

                if not get_unified_validator().validate_required(step_success):
                    success_score *= 0.8  # Reduce overall success score
                    lessons_learned.append(f"Step failed: {step}")
                else:
                    lessons_learned.append(f"Step completed successfully: {step}")

            except Exception as e:
                success_score *= 0.5
                lessons_learned.append(f"Step error: {step} - {str(e)}")

        # Track resource usage
        resources_used = protocol.required_resources.copy()

        return {
            "success_score": success_score,
            "resources_used": resources_used,
            "lessons_learned": lessons_learned
        }

    def _assess_step_success(self, step: str, emergency_event: EmergencyEvent) -> bool:
        """Assess success of an intervention step (simplified implementation)."""
        # This would be more sophisticated in a real implementation
        # For now, return success based on step type and emergency context

        success_indicators = {
            "assess": True,  # Assessment steps usually succeed
            "identify": emergency_event.affected_agents,  # Identification depends on available data
            "reassign": len(emergency_event.affected_agents) > 0,
            "notify": True,  # Notification steps usually succeed
            "monitor": True,  # Monitoring steps usually succeed
            "analyze": True,  # Analysis steps usually succeed
            "implement": emergency_event.severity != EmergencySeverity.CRITICAL,
            "escalate": True  # Escalation steps usually succeed
        }

        for indicator, success in success_indicators.items():
            if indicator in step.lower():
                return success

        return True  # Default to success for unknown steps

    def _update_protocol_success_rate(self, protocol: InterventionProtocol, new_success_score: float):
        """Update protocol success rate based on new intervention result."""
        protocol.usage_count += 1

        # Exponential moving average update
        alpha = 0.1  # Learning rate
        protocol.success_rate = (1 - alpha) * protocol.success_rate + alpha * new_success_score

        protocol.last_updated = datetime.now()

    async def _notify_captain_intervention(self, emergency_event: EmergencyEvent,
                                         intervention_result: Dict[str, Any]):
        """Notify Captain Agent-4 of emergency intervention."""
        if not self.messaging_core:
            return

        notification_message = f"""
🚨 **EMERGENCY INTERVENTION ACTIVATED** 🚨

**Emergency Event**: {emergency_event.event_id}
**Type**: {emergency_event.emergency_type.value}
**Severity**: {emergency_event.severity.value}
**Description**: {emergency_event.description}

**Intervention Results**:
- Protocol Used: {intervention_result.get('protocol_used', 'N/A')}
- Success Score: {intervention_result.get('success_score', 0):.1%}
- Duration: {intervention_result.get('duration_minutes', 0):.1f} minutes

**Affected Mission**: {emergency_event.affected_mission or 'N/A'}
**Affected Agents**: {', '.join(emergency_event.affected_agents) if emergency_event.affected_agents else 'None'}

**Next Steps**: Monitoring intervention effectiveness and preparing contingency plans.

**WE. ARE. SWARM.** ⚡️🔥🧠
"""

        try:
            await self.messaging_core.send_message_to_agent(
                message=notification_message,
                agent_id="captain_agent_4",
                message_type="emergency_intervention",
                priority="urgent"
            )
        except Exception as e:
            get_logger(__name__).info(f"Warning: Failed to notify Captain Agent-4: {e}")

    def get_emergency_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive emergency status report."""
        active_count = len(self.active_emergencies)
        resolved_today = len([
            e for e in self.intervention_history
            if e.completed_at.date() == datetime.now().date()
        ])

        # Emergency type distribution
        type_distribution = Counter(
            e.emergency_type.value for e in self.active_emergencies.values()
        )

        # Severity distribution
        severity_distribution = Counter(
            e.severity.value for e in self.active_emergencies.values()
        )

        # Intervention success rates
        if self.intervention_history:
            success_scores = [r.success_score for r in self.intervention_history]
            avg_success_rate = sum(success_scores) / len(success_scores)
            recent_success_rate = sum(success_scores[-10:]) / min(10, len(success_scores))
        else:
            avg_success_rate = 0.0
            recent_success_rate = 0.0

        return {
            "active_emergencies": active_count,
            "resolved_today": resolved_today,
            "type_distribution": dict(type_distribution),
            "severity_distribution": dict(severity_distribution),
            "average_success_rate": round(avg_success_rate, 3),
            "recent_success_rate": round(recent_success_rate, 3),
            "total_interventions": len(self.intervention_history),
            "most_common_emergency_type": type_distribution.most_common(1)[0][0] if type_distribution else "none",
            "generated_at": datetime.now().isoformat()
        }

    def get_emergency_response_patterns(self) -> Dict[str, Any]:
        """Get patterns and insights from emergency response history."""
        if not self.intervention_history:
            return {"error": "No intervention history available"}

        # Analyze response times by emergency type
        response_times_by_type = defaultdict(list)
        success_rates_by_type = defaultdict(list)

        for intervention in self.intervention_history:
            emergency_type = intervention.emergency_event.emergency_type.value
            response_times_by_type[emergency_type].append(intervention.actual_duration_minutes)
            success_rates_by_type[emergency_type].append(intervention.success_score)

        # Calculate averages
        avg_response_times = {}
        avg_success_rates = {}

        for emergency_type, times in response_times_by_type.items():
            avg_response_times[emergency_type] = round(sum(times) / len(times), 1)

        for emergency_type, scores in success_rates_by_type.items():
            avg_success_rates[emergency_type] = round(sum(scores) / len(scores), 3)

        # Identify most effective protocols
        protocol_effectiveness = Counter()
        for intervention in self.intervention_history:
            protocol_id = intervention.protocol_used.protocol_id
            effectiveness_score = intervention.success_score * (1 / max(intervention.actual_duration_minutes, 1))
            protocol_effectiveness[protocol_id] = effectiveness_score

        most_effective_protocols = protocol_effectiveness.most_common(3)

        return {
            "average_response_times_by_type": avg_response_times,
            "average_success_rates_by_type": avg_success_rates,
            "most_effective_protocols": [
                {"protocol": protocol, "effectiveness_score": round(score, 3)}
                for protocol, score in most_effective_protocols
            ],
            "total_emergency_responses": len(self.intervention_history),
            "analysis_period_days": (datetime.now() - min(r.completed_at for r in self.intervention_history)).days,
            "generated_at": datetime.now().isoformat()
        }

    async def start_monitoring(self, get_unified_validator().check_interval_seconds: int = 60):
        """Start continuous emergency monitoring."""
        if self.monitoring_active:
            return

        self.monitoring_active = True

        async def monitoring_loop():
            while self.monitoring_active:
                try:
                    # In a real implementation, this would monitor actual mission contexts
                    # For now, we'll simulate periodic checks
                    await asyncio.sleep(get_unified_validator().check_interval_seconds)

                    # Placeholder for actual monitoring logic
                    # This would check mission statuses, agent responsiveness, etc.

                except Exception as e:
                    get_logger(__name__).info(f"Emergency monitoring error: {e}")
                    await asyncio.sleep(get_unified_validator().check_interval_seconds)

        self.monitoring_task = asyncio.create_task(monitoring_loop())

    async def stop_monitoring(self):
        """Stop emergency monitoring."""
        self.monitoring_active = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
