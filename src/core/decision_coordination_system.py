#!/usr/bin/env python3
"""
Decision Coordination System - Agent Cellphone V2
================================================

Coordinates collaborative decision-making across agent swarm.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import time
import json
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
from .decision import DecisionMakingEngine, DecisionType, DecisionRequest


class CoordinationMode(Enum):
    """Decision coordination modes"""
    CONSENSUS = "consensus"
    MAJORITY = "majority"
    EXPERT_OPINION = "expert_opinion"
    HIERARCHICAL = "hierarchical"
    COLLABORATIVE = "collaborative"


@dataclass
class CoordinationSession:
    """Decision coordination session data"""
    session_id: str
    decision_id: str
    mode: CoordinationMode
    participants: List[str]
    start_time: float
    end_time: Optional[float]
    status: str
    consensus_reached: bool
    final_decision: Optional[Any]


class DecisionCoordinationSystem:
    """
    Coordinates collaborative decision-making across agent swarm
    
    Responsibilities:
    - Manage decision coordination sessions
    - Facilitate agent collaboration on decisions
    - Implement coordination protocols
    - Track decision coordination progress
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.DecisionCoordinationSystem")
        self.workspace_path = Path("agent_workspaces")
        self.decision_engine = DecisionMakingEngine()
        self.active_sessions: Dict[str, CoordinationSession] = {}
        self.session_history: List[CoordinationSession] = []
        self.coordination_protocols: Dict[CoordinationMode, Dict] = {}
        
        # Ensure workspace exists
        self.workspace_path.mkdir(exist_ok=True)
        
        # Initialize coordination protocols
        self._initialize_coordination_protocols()
    
    def _initialize_coordination_protocols(self):
        """Initialize coordination protocols for different modes"""
        self.coordination_protocols = {
            CoordinationMode.CONSENSUS: {
                "description": "All participants must agree",
                "threshold": 1.0,
                "timeout": 300,  # 5 minutes
                "retry_attempts": 3
            },
            CoordinationMode.MAJORITY: {
                "description": "Majority vote decides",
                "threshold": 0.51,
                "timeout": 180,  # 3 minutes
                "retry_attempts": 2
            },
            CoordinationMode.EXPERT_OPINION: {
                "description": "Expert agent makes final decision",
                "threshold": 0.8,
                "timeout": 120,  # 2 minutes
                "retry_attempts": 1
            },
            CoordinationMode.HIERARCHICAL: {
                "description": "Hierarchical decision structure",
                "threshold": 0.7,
                "timeout": 240,  # 4 minutes
                "retry_attempts": 2
            },
            CoordinationMode.COLLABORATIVE: {
                "description": "Full collaborative decision-making",
                "threshold": 0.6,
                "timeout": 360,  # 6 minutes
                "retry_attempts": 3
            }
        }
    
    def initiate_coordination_session(self, decision_id: str, mode: CoordinationMode,
                                   participants: Optional[List[str]] = None) -> str:
        """Initiate a new decision coordination session"""
        session_id = f"session_{mode.value}_{decision_id}_{int(time.time())}"
        
        # Discover participants if not specified
        if not participants:
            participants = self._discover_available_agents()
        
        session = CoordinationSession(
            session_id=session_id,
            decision_id=decision_id,
            mode=mode,
            participants=participants,
            start_time=time.time(),
            end_time=None,
            status="active",
            consensus_reached=False,
            final_decision=None
        )
        
        self.active_sessions[session_id] = session
        
        # Notify all participants
        self._notify_session_participants(session)
        
        # Start coordination process
        self._start_coordination_process(session)
        
        self.logger.info(f"Coordination session initiated: {session_id} with {len(participants)} participants")
        return session_id
    
    def _start_coordination_process(self, session: CoordinationSession):
        """Start the coordination process for a session"""
        protocol = self.coordination_protocols[session.mode]
        
        # Create coordination thread
        coord_thread = threading.Thread(
            target=self._run_coordination_process,
            args=(session, protocol),
            daemon=True
        )
        coord_thread.start()
    
    def _run_coordination_process(self, session: CoordinationSession, protocol: Dict):
        """Run the coordination process"""
        try:
            # Phase 1: Information gathering
            self._gather_agent_inputs(session)
            
            # Phase 2: Decision deliberation
            self._deliberate_decision(session, protocol)
            
            # Phase 3: Consensus building
            consensus_reached = self._build_consensus(session, protocol)
            
            # Phase 4: Final decision
            if consensus_reached:
                self._finalize_decision(session)
            else:
                self._handle_no_consensus(session, protocol)
            
        except Exception as e:
            self.logger.error(f"Coordination process failed for session {session.session_id}: {e}")
            session.status = "failed"
            session.end_time = time.time()
    
    def _gather_agent_inputs(self, session: CoordinationSession):
        """Gather inputs from all participating agents"""
        session.status = "gathering_inputs"
        
        for participant in session.participants:
            # Send input request
            self._send_input_request(session, participant)
        
        # Wait for inputs (with timeout)
        timeout = time.time() + 60  # 1 minute timeout
        while time.time() < timeout:
            if self._all_inputs_received(session):
                break
            time.sleep(1)
        
        session.status = "inputs_gathered"
    
    def _deliberate_decision(self, session: CoordinationSession, protocol: Dict):
        """Deliberate on the decision based on gathered inputs"""
        session.status = "deliberating"
        
        # Analyze agent inputs
        inputs = self._collect_agent_inputs(session)
        
        # Apply coordination mode logic
        if session.mode == CoordinationMode.CONSENSUS:
            deliberation_result = self._apply_consensus_logic(inputs)
        elif session.mode == CoordinationMode.MAJORITY:
            deliberation_result = self._apply_majority_logic(inputs)
        elif session.mode == CoordinationMode.EXPERT_OPINION:
            deliberation_result = self._apply_expert_logic(inputs)
        elif session.mode == CoordinationMode.HIERARCHICAL:
            deliberation_result = self._apply_hierarchical_logic(inputs)
        else:  # COLLABORATIVE
            deliberation_result = self._apply_collaborative_logic(inputs)
        
        session.status = "deliberation_complete"
        return deliberation_result
    
    def _build_consensus(self, session: CoordinationSession, protocol: Dict) -> bool:
        """Build consensus among participants"""
        session.status = "building_consensus"
        
        # Check if consensus threshold is met
        consensus_score = self._calculate_consensus_score(session)
        threshold = protocol["threshold"]
        
        consensus_reached = consensus_score >= threshold
        session.consensus_reached = consensus_reached
        
        if consensus_reached:
            session.status = "consensus_reached"
        else:
            session.status = "consensus_failed"
        
        return consensus_reached
    
    def _finalize_decision(self, session: CoordinationSession):
        """Finalize the decision after consensus"""
        session.status = "finalizing"
        
        # Get the final decision from the decision engine
        try:
            result = self.decision_engine.process_decision(session.decision_id)
            session.final_decision = result.decision
            
            # Notify all participants of final decision
            self._notify_final_decision(session, result)
            
            session.status = "completed"
            
        except Exception as e:
            self.logger.error(f"Failed to finalize decision: {e}")
            session.status = "failed"
        
        session.end_time = time.time()
        
        # Move to history
        self.session_history.append(session)
        del self.active_sessions[session.session_id]
    
    def _handle_no_consensus(self, session: CoordinationSession, protocol: Dict):
        """Handle cases where no consensus is reached"""
        session.status = "no_consensus"
        
        # Check retry attempts
        retry_count = getattr(session, 'retry_count', 0)
        max_retries = protocol["retry_attempts"]
        
        if retry_count < max_retries:
            # Retry with modified approach
            session.retry_count = retry_count + 1
            session.status = "retrying"
            self._start_coordination_process(session)
        else:
            # Final failure
            session.status = "failed"
            session.end_time = time.time()
            
            # Move to history
            self.session_history.append(session)
            del self.active_sessions[session.session_id]
    
    def _apply_consensus_logic(self, inputs: List[Dict]) -> Dict:
        """Apply consensus-based decision logic"""
        # All inputs must be similar for consensus
        if len(set(str(input) for input in inputs)) == 1:
            return {"decision": inputs[0], "method": "consensus", "confidence": 1.0}
        else:
            return {"decision": None, "method": "consensus", "confidence": 0.0}
    
    def _apply_majority_logic(self, inputs: List[Dict]) -> Dict:
        """Apply majority-based decision logic"""
        # Count similar inputs
        input_counts = {}
        for input_data in inputs:
            input_str = str(input_data)
            input_counts[input_str] = input_counts.get(input_str, 0) + 1
        
        # Find majority
        majority_input = max(input_counts.items(), key=lambda x: x[1])
        majority_count = majority_input[1]
        total_count = len(inputs)
        
        confidence = majority_count / total_count
        return {"decision": eval(majority_input[0]), "method": "majority", "confidence": confidence}
    
    def _apply_expert_logic(self, inputs: List[Dict]) -> Dict:
        """Apply expert opinion-based decision logic"""
        # Find agent with highest expertise score
        expert_input = max(inputs, key=lambda x: x.get("expertise_score", 0))
        return {"decision": expert_input, "method": "expert_opinion", "confidence": 0.8}
    
    def _apply_hierarchical_logic(self, inputs: List[Dict]) -> Dict:
        """Apply hierarchical decision logic"""
        # Sort by hierarchy level and take highest
        hierarchical_input = max(inputs, key=lambda x: x.get("hierarchy_level", 0))
        return {"decision": hierarchical_input, "method": "hierarchical", "confidence": 0.7}
    
    def _apply_collaborative_logic(self, inputs: List[Dict]) -> Dict:
        """Apply collaborative decision logic"""
        # Combine all inputs for collaborative decision
        combined_decision = {
            "collaborative_inputs": inputs,
            "combined_score": sum(input.get("score", 0) for input in inputs),
            "participant_count": len(inputs)
        }
        return {"decision": combined_decision, "method": "collaborative", "confidence": 0.6}
    
    def _calculate_consensus_score(self, session: CoordinationSession) -> float:
        """Calculate consensus score among participants"""
        # Simple consensus calculation
        # In production, implement more sophisticated consensus metrics
        return 0.8  # Placeholder - implement actual consensus calculation
    
    def _discover_available_agents(self) -> List[str]:
        """Discover available agents for coordination"""
        agents = []
        if self.workspace_path.exists():
            for agent_dir in self.workspace_path.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    agents.append(agent_dir.name)
        return agents
    
    def _notify_session_participants(self, session: CoordinationSession):
        """Notify all participants about coordination session"""
        for participant in session.participants:
            self._send_session_notification(session, participant)
    
    def _send_session_notification(self, session: CoordinationSession, participant: str):
        """Send session notification to participant"""
        message = {
            "type": "coordination_session",
            "from": "DecisionCoordinationSystem",
            "to": participant,
            "timestamp": time.time(),
            "session_id": session.session_id,
            "decision_id": session.decision_id,
            "mode": session.mode.value,
            "action": "join_coordination_session"
        }
        
        # Send to agent's inbox
        agent_inbox = self.workspace_path / participant / "inbox"
        agent_inbox.mkdir(exist_ok=True)
        
        message_file = agent_inbox / f"coordination_session_{session.session_id}.json"
        with open(message_file, 'w') as f:
            json.dump(message, f, indent=2)
    
    def _send_input_request(self, session: CoordinationSession, participant: str):
        """Send input request to participant"""
        message = {
            "type": "input_request",
            "from": "DecisionCoordinationSystem",
            "to": participant,
            "timestamp": time.time(),
            "session_id": session.session_id,
            "decision_id": session.decision_id,
            "action": "provide_decision_input",
            "deadline": time.time() + 60
        }
        
        # Send to agent's inbox
        agent_inbox = self.workspace_path / participant / "inbox"
        agent_inbox.mkdir(exist_ok=True)
        
        message_file = agent_inbox / f"input_request_{session.session_id}.json"
        with open(message_file, 'w') as f:
            json.dump(message, f, indent=2)
    
    def _all_inputs_received(self, session: CoordinationSession) -> bool:
        """Check if all inputs have been received"""
        # Check inbox for input responses from all participants
        for participant in session.participants:
            input_file = self.workspace_path / participant / "inbox" / f"input_response_{session.session_id}.json"
            if not input_file.exists():
                return False
        return True
    
    def _collect_agent_inputs(self, session: CoordinationSession) -> List[Dict]:
        """Collect all agent inputs for the session"""
        inputs = []
        
        for participant in session.participants:
            input_file = self.workspace_path / participant / "inbox" / f"input_response_{session.session_id}.json"
            if input_file.exists():
                try:
                    with open(input_file, 'r') as f:
                        input_data = json.load(f)
                        inputs.append(input_data)
                except Exception as e:
                    self.logger.error(f"Failed to read input from {participant}: {e}")
        
        return inputs
    
    def _notify_final_decision(self, session: CoordinationSession, result):
        """Notify all participants of final decision"""
        for participant in session.participants:
            message = {
                "type": "final_decision",
                "from": "DecisionCoordinationSystem",
                "to": participant,
                "timestamp": time.time(),
                "session_id": session.session_id,
                "decision_id": session.decision_id,
                "decision": session.final_decision,
                "status": "completed"
            }
            
            # Send to agent's inbox
            agent_inbox = self.workspace_path / participant / "inbox"
            agent_inbox.mkdir(exist_ok=True)
            
            message_file = agent_inbox / f"final_decision_{session.session_id}.json"
            with open(message_file, 'w') as f:
                json.dump(message, f, indent=2)
    
    def get_coordination_status(self) -> Dict[str, Any]:
        """Get current coordination system status"""
        return {
            "active_sessions": len(self.active_sessions),
            "completed_sessions": len(self.session_history),
            "total_participants": sum(len(s.participants) for s in self.active_sessions.values()),
            "coordination_modes": [mode.value for mode in CoordinationMode],
            "status": "DECISION_COORDINATION_ACTIVE"
        }
    
    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific coordination session"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            return {
                "session_id": session.session_id,
                "status": session.status,
                "mode": session.mode.value,
                "participants": session.participants,
                "consensus_reached": session.consensus_reached,
                "duration": time.time() - session.start_time
            }
        return None


def main():
    """CLI interface for Decision Coordination System"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Decision Coordination System CLI")
    parser.add_argument("--initiate", "-i", help="Initiate coordination session for decision ID")
    parser.add_argument("--mode", "-m", default="collaborative", help="Coordination mode")
    parser.add_argument("--status", "-s", help="Get session status by ID")
    parser.add_argument("--system-status", action="store_true", help="Show system status")
    
    args = parser.parse_args()
    
    system = DecisionCoordinationSystem()
    
    if args.initiate:
        try:
            mode = CoordinationMode(args.mode)
            session_id = system.initiate_coordination_session(args.initiate, mode)
            print(f"✅ Coordination session initiated: {session_id}")
            print(f"📋 Mode: {mode.value}")
            
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    elif args.status:
        status = system.get_session_status(args.status)
        if status:
            print(f"📊 Session Status: {status['status']}")
            print(f"  Mode: {status['mode']}")
            print(f"  Participants: {status['participants']}")
            print(f"  Consensus: {status['consensus_reached']}")
            print(f"  Duration: {status['duration']:.1f}s")
        else:
            print(f"❌ Session {args.status} not found")
    
    elif args.system_status:
        status = system.get_coordination_status()
        print("📊 Decision Coordination System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    else:
        print("Decision Coordination System - Use --help for options")


if __name__ == "__main__":
    main()
