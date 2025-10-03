#!/usr/bin/env python3
"""
Swarm Intelligence Workflow Coordinator
======================================

V2 Compliant: ≤400 lines, implements swarm intelligence
workflow coordination for autonomous agent development.

This module coordinates workflows using swarm intelligence
principles with emergent collective intelligence.

🐝 WE ARE SWARM - Workflow Innovation Initiative
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List
import logging
from datetime import datetime
import random
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SwarmIntelligenceCoordinator:
    """Coordinates workflows using swarm intelligence principles."""
    
    def __init__(self, project_root: str = "."):
        """Initialize swarm intelligence coordinator."""
        self.project_root = Path(project_root)
        self.swarm_dir = self.project_root / "swarm_intelligence"
        self.swarm_dir.mkdir(exist_ok=True)
        
        # Swarm parameters
        self.swarm_size = 8  # Number of agents in swarm
        self.coordination_radius = 5.0  # Coordination influence radius
        self.emergent_threshold = 0.8  # Threshold for emergent behavior
        
        # Agent positions and states
        self.agent_positions = {}
        self.agent_states = {}
        self.swarm_center = {"x": 0, "y": 0}
        
        # Swarm intelligence rules
        self.swarm_rules = {
            "separation": 0.5,  # Avoid crowding
            "alignment": 0.3,   # Match velocity
            "cohesion": 0.2     # Move toward center
        }
        
        # Workflow coordination log
        self.coordination_log = []
        
    def coordinate_swarm_workflow(self, workflow_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Coordinate workflow using swarm intelligence."""
        logger.info("Starting swarm intelligence workflow coordination")
        
        coordination_results = {
            "coordination_id": f"SWARM_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "swarm_size": self.swarm_size,
            "tasks_distributed": [],
            "emergent_behaviors": [],
            "coordination_efficiency": 0.0
        }
        
        # Initialize swarm
        self._initialize_swarm()
        
        # Distribute tasks using swarm intelligence
        for task in workflow_tasks:
            task_assignment = self._assign_task_swarm_intelligence(task)
            coordination_results["tasks_distributed"].append(task_assignment)
        
        # Detect emergent behaviors
        emergent_behaviors = self._detect_emergent_behaviors()
        coordination_results["emergent_behaviors"] = emergent_behaviors
        
        # Calculate coordination efficiency
        coordination_results["coordination_efficiency"] = self._calculate_coordination_efficiency()
        
        # Log coordination
        self.coordination_log.append(coordination_results)
        self._save_coordination_log()
        
        logger.info(f"Swarm coordination complete. Efficiency: {coordination_results['coordination_efficiency']:.2f}")
        return coordination_results
    
    def _initialize_swarm(self):
        """Initialize swarm with random positions and states."""
        logger.info("Initializing swarm")
        
        for i in range(self.swarm_size):
            agent_id = f"Agent-{i+1}"
            
            # Random position
            self.agent_positions[agent_id] = {
                "x": random.uniform(-10, 10),
                "y": random.uniform(-10, 10)
            }
            
            # Random state
            self.agent_states[agent_id] = {
                "velocity_x": random.uniform(-1, 1),
                "velocity_y": random.uniform(-1, 1),
                "workload": random.uniform(0, 1),
                "capability": random.uniform(0.5, 1.0)
            }
        
        # Calculate swarm center
        self._update_swarm_center()
    
    def _assign_task_swarm_intelligence(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Assign task using swarm intelligence principles."""
        task_assignment = {
            "task_id": task.get("id", "unknown"),
            "assigned_agent": None,
            "assignment_confidence": 0.0,
            "swarm_consensus": 0.0
        }
        
        # Calculate assignment scores for all agents
        assignment_scores = {}
        for agent_id in self.agent_positions.keys():
            score = self._calculate_assignment_score(agent_id, task)
            assignment_scores[agent_id] = score
        
        # Select best agent based on swarm intelligence
        best_agent = max(assignment_scores, key=assignment_scores.get)
        task_assignment["assigned_agent"] = best_agent
        task_assignment["assignment_confidence"] = assignment_scores[best_agent]
        
        # Calculate swarm consensus
        task_assignment["swarm_consensus"] = self._calculate_swarm_consensus(assignment_scores)
        
        # Update agent state after assignment
        self._update_agent_state(best_agent, task)
        
        return task_assignment
    
    def _calculate_assignment_score(self, agent_id: str, task: Dict[str, Any]) -> float:
        """Calculate assignment score using swarm intelligence."""
        agent_pos = self.agent_positions[agent_id]
        agent_state = self.agent_states[agent_id]
        
        # Base score from agent capability
        base_score = agent_state["capability"]
        
        # Adjust for workload (lower workload = higher score)
        workload_factor = 1.0 - agent_state["workload"]
        
        # Adjust for distance from swarm center (closer = higher score)
        distance_from_center = math.sqrt(
            (agent_pos["x"] - self.swarm_center["x"])**2 + 
            (agent_pos["y"] - self.swarm_center["y"])**2
        )
        distance_factor = 1.0 / (1.0 + distance_from_center)
        
        # Calculate final score
        final_score = base_score * workload_factor * distance_factor
        
        return final_score
    
    def _calculate_swarm_consensus(self, assignment_scores: Dict[str, float]) -> float:
        """Calculate swarm consensus on task assignment."""
        if not assignment_scores:
            return 0.0
        
        scores = list(assignment_scores.values())
        max_score = max(scores)
        min_score = min(scores)
        
        # Consensus is high when scores are close together
        if max_score == min_score:
            return 1.0
        
        consensus = 1.0 - ((max_score - min_score) / max_score)
        return max(0.0, consensus)
    
    def _detect_emergent_behaviors(self) -> List[Dict[str, Any]]:
        """Detect emergent behaviors in the swarm."""
        emergent_behaviors = []
        
        # Check for collective task completion
        total_workload = sum(agent["workload"] for agent in self.agent_states.values())
        if total_workload > self.emergent_threshold:
            emergent_behaviors.append({
                "behavior_type": "collective_task_completion",
                "description": "Swarm collectively completing tasks",
                "strength": total_workload
            })
        
        # Check for coordinated movement
        velocity_alignment = self._calculate_velocity_alignment()
        if velocity_alignment > self.emergent_threshold:
            emergent_behaviors.append({
                "behavior_type": "coordinated_movement",
                "description": "Agents moving in coordinated patterns",
                "strength": velocity_alignment
            })
        
        # Check for workload balancing
        workload_variance = self._calculate_workload_variance()
        if workload_variance < 0.1:  # Low variance = good balancing
            emergent_behaviors.append({
                "behavior_type": "workload_balancing",
                "description": "Automatic workload distribution",
                "strength": 1.0 - workload_variance
            })
        
        return emergent_behaviors
    
    def _calculate_velocity_alignment(self) -> float:
        """Calculate how aligned agent velocities are."""
        if not self.agent_states:
            return 0.0
        
        velocities = []
        for agent_state in self.agent_states.values():
            velocity_magnitude = math.sqrt(
                agent_state["velocity_x"]**2 + agent_state["velocity_y"]**2
            )
            velocities.append(velocity_magnitude)
        
        if not velocities:
            return 0.0
        
        # Calculate variance in velocities (lower = more aligned)
        mean_velocity = sum(velocities) / len(velocities)
        variance = sum((v - mean_velocity)**2 for v in velocities) / len(velocities)
        
        # Convert variance to alignment score (0-1)
        alignment = 1.0 / (1.0 + variance)
        return alignment
    
    def _calculate_workload_variance(self) -> float:
        """Calculate variance in agent workloads."""
        if not self.agent_states:
            return 0.0
        
        workloads = [agent["workload"] for agent in self.agent_states.values()]
        mean_workload = sum(workloads) / len(workloads)
        variance = sum((w - mean_workload)**2 for w in workloads) / len(workloads)
        
        return variance
    
    def _calculate_coordination_efficiency(self) -> float:
        """Calculate overall coordination efficiency."""
        # Combine multiple factors
        velocity_alignment = self._calculate_velocity_alignment()
        workload_balance = 1.0 - self._calculate_workload_variance()
        swarm_cohesion = self._calculate_swarm_cohesion()
        
        # Weighted average
        efficiency = (
            velocity_alignment * 0.3 +
            workload_balance * 0.4 +
            swarm_cohesion * 0.3
        )
        
        return efficiency
    
    def _calculate_swarm_cohesion(self) -> float:
        """Calculate how cohesive the swarm is."""
        if not self.agent_positions:
            return 0.0
        
        # Calculate average distance from swarm center
        total_distance = 0
        for agent_pos in self.agent_positions.values():
            distance = math.sqrt(
                (agent_pos["x"] - self.swarm_center["x"])**2 + 
                (agent_pos["y"] - self.swarm_center["y"])**2
            )
            total_distance += distance
        
        average_distance = total_distance / len(self.agent_positions)
        
        # Convert to cohesion score (closer = more cohesive)
        cohesion = 1.0 / (1.0 + average_distance)
        return cohesion
    
    def _update_swarm_center(self):
        """Update swarm center based on agent positions."""
        if not self.agent_positions:
            return
        
        total_x = sum(pos["x"] for pos in self.agent_positions.values())
        total_y = sum(pos["y"] for pos in self.agent_positions.values())
        
        self.swarm_center = {
            "x": total_x / len(self.agent_positions),
            "y": total_y / len(self.agent_positions)
        }
    
    def _update_agent_state(self, agent_id: str, task: Dict[str, Any]):
        """Update agent state after task assignment."""
        if agent_id not in self.agent_states:
            return
        
        # Increase workload
        self.agent_states[agent_id]["workload"] = min(1.0, 
            self.agent_states[agent_id]["workload"] + 0.1)
        
        # Update position based on swarm rules
        self._apply_swarm_rules(agent_id)
    
    def _apply_swarm_rules(self, agent_id: str):
        """Apply swarm intelligence rules to agent."""
        if agent_id not in self.agent_positions or agent_id not in self.agent_states:
            return
        
        # Apply separation, alignment, and cohesion rules
        # This is a simplified implementation
        agent_pos = self.agent_positions[agent_id]
        agent_state = self.agent_states[agent_id]
        
        # Move toward swarm center (cohesion)
        dx = self.swarm_center["x"] - agent_pos["x"]
        dy = self.swarm_center["y"] - agent_pos["y"]
        
        agent_state["velocity_x"] += dx * self.swarm_rules["cohesion"]
        agent_state["velocity_y"] += dy * self.swarm_rules["cohesion"]
        
        # Update position
        agent_pos["x"] += agent_state["velocity_x"] * 0.1
        agent_pos["y"] += agent_state["velocity_y"] * 0.1
    
    def _save_coordination_log(self):
        """Save coordination log to file."""
        log_file = self.swarm_dir / "coordination_log.json"
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(self.coordination_log, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving coordination log: {e}")
    
    def get_swarm_status(self) -> Dict[str, Any]:
        """Get current swarm status."""
        return {
            "swarm_size": self.swarm_size,
            "coordination_efficiency": self._calculate_coordination_efficiency(),
            "emergent_behaviors": len(self._detect_emergent_behaviors()),
            "swarm_center": self.swarm_center,
            "total_coordinations": len(self.coordination_log)
        }

def main():
    """Main execution function."""
    coordinator = SwarmIntelligenceCoordinator()
    
    # Test swarm coordination
    test_tasks = [
        {"id": "task_1", "type": "configuration_sync", "priority": "high"},
        {"id": "task_2", "type": "role_validation", "priority": "medium"},
        {"id": "task_3", "type": "ssot_validation", "priority": "high"}
    ]
    
    results = coordinator.coordinate_swarm_workflow(test_tasks)
    print(f"Swarm coordination results:")
    print(f"  Tasks distributed: {len(results['tasks_distributed'])}")
    print(f"  Emergent behaviors: {len(results['emergent_behaviors'])}")
    print(f"  Coordination efficiency: {results['coordination_efficiency']:.2f}")
    
    # Get swarm status
    status = coordinator.get_swarm_status()
    print(f"Swarm status: {status}")

if __name__ == "__main__":
    main()
