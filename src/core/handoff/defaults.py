"""Default handoff procedures."""




def get_default_procedures() -> List[HandoffProcedure]:
    """Return built-in handoff procedures."""
    return [
        HandoffProcedure(
            procedure_id="PHASE_TRANSITION_STANDARD",
            name="Standard Phase Transition",
            description="Minimal phase transition",
            steps=[
                {
                    "step_id": 1,
                    "name": "Phase completion check",
                    "action": "validate_phase_completion",
                    "timeout": 30.0,
                },
                {
                    "step_id": 2,
                    "name": "Handoff validation",
                    "action": "validate_handoff",
                    "timeout": 30.0,
                },
            ],
            validation_rules=[
                {
                    "rule_id": "VR001",
                    "name": "Phase completion",
                    "condition": "source_phase_completed",
                    "severity": "critical",
                }
            ],
            rollback_procedures=[
                {
                    "rollback_id": "RB001",
                    "name": "Resource rollback",
                    "action": "rollback_resources",
                    "timeout": 30.0,
                }
            ],
            estimated_duration=60.0,
        )
    ]
