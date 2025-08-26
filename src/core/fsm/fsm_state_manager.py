"""
FSM State Manager - Agent Cellphone V2
Manages FSM state updates and task completion tracking
"""

import os
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import threading


@dataclass
class FSMState:
    """Represents a state in the FSM"""
    state_id: str
    state_name: str
    status: str  # PENDING, ACTIVE, COMPLETED, FAILED
    agent_id: str
    task_id: str
    start_time: datetime
    completion_time: Optional[datetime] = None
    progress_percentage: float = 0.0
    deliverables: List[str] = None
    dependencies: List[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class FSMTransition:
    """Represents a transition between FSM states"""
    transition_id: str
    timestamp: datetime
    from_state: str
    to_state: str
    trigger: str
    agent_id: str
    task_id: str
    metadata: Dict[str, Any] = None


class FSMStateManager:
    """Manages FSM state updates and task completion tracking"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.states: Dict[str, FSMState] = {}
        self.transitions: List[FSMTransition] = []
        self.completed_tasks: List[str] = []
        self.active_tasks: List[str] = []
        self.pending_tasks: List[str] = []
        self.fsm_file = "fsm_state.json"
        self.lock = threading.Lock()
        
        # Load existing FSM state
        self._load_fsm_state()
        
    def _load_fsm_state(self):
        """Load existing FSM state from file"""
        if os.path.exists(self.fsm_file):
            try:
                with open(self.fsm_file, 'r') as f:
                    data = json.load(f)
                    
                    # Reconstruct states
                    for state_data in data.get("states", {}).values():
                        state = FSMState(
                            state_id=state_data["state_id"],
                            state_name=state_data["state_name"],
                            status=state_data["status"],
                            agent_id=state_data["agent_id"],
                            task_id=state_data["task_id"],
                            start_time=datetime.fromisoformat(state_data["start_time"]),
                            completion_time=datetime.fromisoformat(state_data["completion_time"]) if state_data.get("completion_time") else None,
                            progress_percentage=state_data.get("progress_percentage", 0.0),
                            deliverables=state_data.get("deliverables", []),
                            dependencies=state_data.get("dependencies", []),
                            metadata=state_data.get("metadata", {})
                        )
                        self.states[state.state_id] = state
                        
                        # Update task lists
                        if state.status == "COMPLETED":
                            self.completed_tasks.append(state.task_id)
                        elif state.status == "ACTIVE":
                            self.active_tasks.append(state.task_id)
                        elif state.status == "PENDING":
                            self.pending_tasks.append(state.task_id)
                    
                    # Reconstruct transitions
                    for trans_data in data.get("transitions", []):
                        transition = FSMTransition(
                            transition_id=trans_data["transition_id"],
                            timestamp=datetime.fromisoformat(trans_data["timestamp"]),
                            from_state=trans_data["from_state"],
                            to_state=trans_data["to_state"],
                            trigger=trans_data["trigger"],
                            agent_id=trans_data["agent_id"],
                            task_id=trans_data["task_id"],
                            metadata=trans_data.get("metadata", {})
                        )
                        self.transitions.append(transition)
                        
            except Exception as e:
                print(f"Error loading FSM state: {e}")
    
    def _save_fsm_state(self):
        """Save current FSM state to file"""
        try:
            data = {
                "states": {state_id: asdict(state) for state_id, state in self.states.items()},
                "transitions": [asdict(trans) for trans in self.transitions],
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.fsm_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            print(f"Error saving FSM state: {e}")
    
    def create_state(self, state_id: str, state_name: str, agent_id: str, task_id: str, 
                    deliverables: List[str] = None, dependencies: List[str] = None) -> FSMState:
        """Create a new FSM state"""
        with self.lock:
            state = FSMState(
                state_id=state_id,
                state_name=state_name,
                status="PENDING",
                agent_id=agent_id,
                task_id=task_id,
                start_time=datetime.now(),
                deliverables=deliverables or [],
                dependencies=dependencies or [],
                metadata={}
            )
            
            self.states[state_id] = state
            self.pending_tasks.append(task_id)
            self._save_fsm_state()
            
            return state
    
    def activate_state(self, state_id: str) -> bool:
        """Activate a pending state"""
        with self.lock:
            if state_id in self.states and self.states[state_id].status == "PENDING":
                self.states[state_id].status = "ACTIVE"
                self.states[state_id].start_time = datetime.now()
                
                # Move from pending to active
                if self.states[state_id].task_id in self.pending_tasks:
                    self.pending_tasks.remove(self.states[state_id].task_id)
                self.active_tasks.append(self.states[state_id].task_id)
                
                # Record transition
                transition = FSMTransition(
                    transition_id=f"trans_{int(time.time())}",
                    timestamp=datetime.now(),
                    from_state="PENDING",
                    to_state="ACTIVE",
                    trigger="MANUAL_ACTIVATION",
                    agent_id=self.states[state_id].agent_id,
                    task_id=self.states[state_id].task_id
                )
                self.transitions.append(transition)
                
                self._save_fsm_state()
                return True
            return False
    
    def complete_state(self, state_id: str, deliverables: List[str] = None) -> bool:
        """Mark a state as completed"""
        with self.lock:
            if state_id in self.states and self.states[state_id].status == "ACTIVE":
                self.states[state_id].status = "COMPLETED"
                self.states[state_id].completion_time = datetime.now()
                self.states[state_id].progress_percentage = 100.0
                
                if deliverables:
                    self.states[state_id].deliverables = deliverables
                
                # Move from active to completed
                if self.states[state_id].task_id in self.active_tasks:
                    self.active_tasks.remove(self.states[state_id].task_id)
                self.completed_tasks.append(self.states[state_id].task_id)
                
                # Record transition
                transition = FSMTransition(
                    transition_id=f"trans_{int(time.time())}",
                    timestamp=datetime.now(),
                    from_state="ACTIVE",
                    to_state="COMPLETED",
                    trigger="TASK_COMPLETION",
                    agent_id=self.states[state_id].agent_id,
                    task_id=self.states[state_id].task_id
                )
                self.transitions.append(transition)
                
                self._save_fsm_state()
                return True
            return False
    
    def update_progress(self, state_id: str, progress_percentage: float) -> bool:
        """Update progress for an active state"""
        with self.lock:
            if state_id in self.states and self.states[state_id].status == "ACTIVE":
                self.states[state_id].progress_percentage = progress_percentage
                self._save_fsm_state()
                return True
            return False
    
    def get_fsm_report(self) -> Dict:
        """Generate comprehensive FSM report"""
        total_states = len(self.states)
        completed_states = len([s for s in self.states.values() if s.status == "COMPLETED"])
        active_states = len([s for s in self.states.values() if s.status == "ACTIVE"])
        pending_states = len([s for s in self.states.values() if s.status == "PENDING"])
        
        # Convert datetime objects to strings for JSON serialization
        recent_transitions = []
        for t in self.transitions[-10:]:
            trans_dict = asdict(t)
            trans_dict['timestamp'] = trans_dict['timestamp'].isoformat()
            recent_transitions.append(trans_dict)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_states": total_states,
            "completed_states": completed_states,
            "active_states": active_states,
            "pending_states": pending_states,
            "completion_rate": (completed_states / total_states * 100) if total_states > 0 else 0,
            "recent_transitions": recent_transitions,
            "active_tasks": self.active_tasks,
            "pending_tasks": self.pending_tasks,
            "completed_tasks": self.completed_tasks
        }
    
    def get_available_tasks(self) -> List[Dict]:
        """Get list of available tasks that can be assigned"""
        available_tasks = []
        
        for state in self.states.values():
            if state.status == "PENDING":
                # Check if dependencies are met
                dependencies_met = True
                if state.dependencies:
                    for dep in state.dependencies:
                        if not any(s.task_id == dep and s.status == "COMPLETED" for s in self.states.values()):
                            dependencies_met = False
                            break
                
                if dependencies_met:
                    available_tasks.append({
                        "state_id": state.state_id,
                        "task_id": state.task_id,
                        "state_name": state.state_name,
                        "agent_id": state.agent_id,
                        "deliverables": state.deliverables,
                        "dependencies": state.dependencies
                    })
        
        return available_tasks
    
    def get_agent_workload(self, agent_id: str) -> Dict:
        """Get workload summary for a specific agent"""
        agent_states = [s for s in self.states.values() if s.agent_id == agent_id]
        
        return {
            "agent_id": agent_id,
            "total_tasks": len(agent_states),
            "completed_tasks": len([s for s in agent_states if s.status == "COMPLETED"]),
            "active_tasks": len([s for s in agent_states if s.status == "ACTIVE"]),
            "pending_tasks": len([s for s in agent_states if s.status == "PENDING"]),
            "current_workload": [s.task_id for s in agent_states if s.status == "ACTIVE"]
        }


# CLI interface for the FSM state manager
def main():
    """CLI interface for FSM state manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FSM State Manager")
    parser.add_argument("--create-state", help="Create new state (JSON format)")
    parser.add_argument("--activate-state", help="Activate a state by ID")
    parser.add_argument("--complete-state", help="Complete a state by ID")
    parser.add_argument("--update-progress", help="Update progress (state_id:percentage)")
    parser.add_argument("--report", action="store_true", help="Generate FSM report")
    parser.add_argument("--available-tasks", action="store_true", help="Show available tasks")
    parser.add_argument("--agent-workload", help="Show workload for specific agent")
    
    args = parser.parse_args()
    
    fsm = FSMStateManager()
    
    if args.create_state:
        try:
            state_data = json.loads(args.create_state)
            state = fsm.create_state(
                state_data["state_id"],
                state_data["state_name"],
                state_data["agent_id"],
                state_data["task_id"],
                state_data.get("deliverables"),
                state_data.get("dependencies")
            )
            print(f"State created: {state.state_id}")
        except Exception as e:
            print(f"Error creating state: {e}")
    
    if args.activate_state:
        if fsm.activate_state(args.activate_state):
            print(f"State {args.activate_state} activated")
        else:
            print(f"Failed to activate state {args.activate_state}")
    
    if args.complete_state:
        if fsm.complete_state(args.complete_state):
            print(f"State {args.complete_state} completed")
        else:
            print(f"Failed to complete state {args.complete_state}")
    
    if args.update_progress:
        try:
            state_id, percentage = args.update_progress.split(":")
            if fsm.update_progress(state_id, float(percentage)):
                print(f"Progress updated for {state_id}: {percentage}%")
            else:
                print(f"Failed to update progress for {state_id}")
        except Exception as e:
            print(f"Error updating progress: {e}")
    
    if args.report:
        report = fsm.get_fsm_report()
        print(json.dumps(report, indent=2))
    
    if args.available_tasks:
        tasks = fsm.get_available_tasks()
        print(json.dumps(tasks, indent=2))
    
    if args.agent_workload:
        workload = fsm.get_agent_workload(args.agent_workload)
        print(json.dumps(workload, indent=2))


if __name__ == "__main__":
    main()
