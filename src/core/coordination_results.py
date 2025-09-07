#!/usr/bin/env python3
"""Result aggregation utilities for decision coordination."""

import json
import time
from typing import Dict, List

from .coordination_status import CoordinationMode, CoordinationStatus


def apply_consensus_logic(inputs: List[Dict]) -> Dict:
    """Apply consensus-based decision logic."""
    if len({str(inp) for inp in inputs}) == 1 and inputs:
        return {"decision": inputs[0], "method": "consensus", "confidence": 1.0}
    return {"decision": None, "method": "consensus", "confidence": 0.0}


def apply_majority_logic(inputs: List[Dict]) -> Dict:
    """Apply majority-based decision logic."""
    counts: Dict[str, int] = {}
    for data in inputs:
        key = str(data)
        counts[key] = counts.get(key, 0) + 1
    majority = max(counts.items(), key=lambda x: x[1])
    confidence = majority[1] / len(inputs) if inputs else 0.0
    return {"decision": majority[0], "method": "majority", "confidence": confidence}


def apply_expert_logic(inputs: List[Dict]) -> Dict:
    """Apply expert opinion logic."""
    expert = max(inputs, key=lambda x: x.get("expertise_score", 0))
    return {"decision": expert, "method": "expert_opinion", "confidence": 0.8}


def apply_hierarchical_logic(inputs: List[Dict]) -> Dict:
    """Apply hierarchical decision logic."""
    highest = max(inputs, key=lambda x: x.get("hierarchy_level", 0))
    return {"decision": highest, "method": "hierarchical", "confidence": 0.7}


def apply_collaborative_logic(inputs: List[Dict]) -> Dict:
    """Apply collaborative decision logic."""
    combined = {
        "collaborative_inputs": inputs,
        "combined_score": sum(i.get("score", 0) for i in inputs),
        "participant_count": len(inputs),
    }
    return {"decision": combined, "method": "collaborative", "confidence": 0.6}


def calculate_consensus_score(session) -> float:
    """Calculate consensus score among participants."""
    return 0.8  # Placeholder for future implementation


def collect_agent_inputs(system, session) -> List[Dict]:
    """Collect agent inputs for a session."""
    inputs: List[Dict] = []
    for participant in session.participants:
        input_file = (
            system.workspace_path
            / participant
            / "inbox"
            / f"input_response_{session.session_id}.json"
        )
        if input_file.exists():
            try:
                with open(input_file, "r") as f:
                    inputs.append(json.load(f))
            except Exception:
                pass
    return inputs


def deliberate_decision(system, session, protocol) -> Dict:
    """Deliberate on the decision based on gathered inputs."""
    session.status = CoordinationStatus.DELIBERATING.value
    inputs = collect_agent_inputs(system, session)
    if session.mode == CoordinationMode.CONSENSUS:
        result = apply_consensus_logic(inputs)
    elif session.mode == CoordinationMode.MAJORITY:
        result = apply_majority_logic(inputs)
    elif session.mode == CoordinationMode.EXPERT_OPINION:
        result = apply_expert_logic(inputs)
    elif session.mode == CoordinationMode.HIERARCHICAL:
        result = apply_hierarchical_logic(inputs)
    else:
        result = apply_collaborative_logic(inputs)
    session.status = CoordinationStatus.DELIBERATION_COMPLETE.value
    return result


def build_consensus(system, session, protocol) -> bool:
    """Build consensus among participants."""
    session.status = CoordinationStatus.BUILDING_CONSENSUS.value
    score = calculate_consensus_score(session)
    threshold = protocol["threshold"]
    reached = score >= threshold
    session.consensus_reached = reached
    session.status = (
        CoordinationStatus.CONSENSUS_REACHED if reached else CoordinationStatus.CONSENSUS_FAILED
    ).value
    return reached


def finalize_decision(system, session) -> None:
    """Finalize decision after consensus."""
    session.status = CoordinationStatus.FINALIZING.value
    result = system.decision_engine.process_decision(session.decision_id)
    session.final_decision = result.decision
    system._notify_final_decision(session, result)
    session.status = CoordinationStatus.COMPLETED.value
    session.end_time = time.time()
    system.session_history.append(session)
    del system.active_sessions[session.session_id]


def handle_no_consensus(system, session, protocol) -> None:
    """Handle cases where no consensus is reached."""
    session.status = CoordinationStatus.NO_CONSENSUS.value
    retry = getattr(session, "retry_count", 0)
    if retry < protocol["retry_attempts"]:
        session.retry_count = retry + 1
        session.status = CoordinationStatus.RETRYING.value
        system.scheduler.start(system, session, protocol)
    else:
        session.status = CoordinationStatus.FAILED.value
        session.end_time = time.time()
        system.session_history.append(session)
        del system.active_sessions[session.session_id]


def gather_agent_inputs(system, session) -> None:
    """Gather inputs from all participants."""
    session.status = CoordinationStatus.GATHERING_INPUTS.value
    for participant in session.participants:
        system._send_input_request(session, participant)
    timeout = time.time() + 60
    while time.time() < timeout:
        if system._all_inputs_received(session):
            break
        time.sleep(1)
    session.status = CoordinationStatus.INPUTS_GATHERED.value
