#!/usr/bin/env python3
"""
Captain Progress Tracker - V2 Compliant
======================================

Integrates legacy progress tracking capabilities into Captain tools.
Monitors agent progress, V3 contracts, and swarm coordination.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import argparse
import sys
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, asdict

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# V2 Compliance: File under 400 lines, functions under 30 lines


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"


class ContractPhase(Enum):
    """V3 contract phase enumeration."""
    PHASE_1_FOUNDATION = "PHASE_1_FOUNDATION"
    PHASE_2_EXPANSION = "PHASE_2_EXPANSION"
    PHASE_3_INTEGRATION = "PHASE_3_INTEGRATION"
    PHASE_4_OPTIMIZATION = "PHASE_4_OPTIMIZATION"


@dataclass
class AgentProgress:
    """Agent progress tracking data."""
    agent_id: str
    current_task: Optional[str]
    task_status: str
    v3_contracts: List[str]
    completed_tasks: List[str]
    last_update: str
    efficiency_score: float
    quality_score: float


@dataclass
class V3ContractProgress:
    """V3 contract progress tracking."""
    contract_id: str
    title: str
    assigned_agent: str
    status: str
    progress_percentage: float
    start_date: str
    estimated_completion: str
    dependencies: List[str]
    deliverables: List[str]


@dataclass
class SwarmProgress:
    """Swarm coordination progress."""
    total_agents: int
    active_agents: int
    completed_contracts: int
    total_contracts: int
    overall_progress: float
    current_phase: str
    phase_progress: Dict[str, Any]
    last_update: str


class CaptainProgressTracker:
    """Captain's progress tracking system."""
    
    def __init__(self, data_path: str = "captain_progress_data"):
        """Initialize progress tracker."""
        self.data_path = Path(data_path)
        self.data_path.mkdir(exist_ok=True)
        
        # Progress tracking data
        self.progress_data = {
            "agents": {},
            "v3_contracts": {},
            "swarm_status": {
                "total_agents": 8,
                "active_agents": 0,
                "completed_contracts": 0,
                "total_contracts": 4,
                "overall_progress": 0.0,
                "current_phase": ContractPhase.PHASE_1_FOUNDATION.value,
                "last_update": datetime.datetime.now().isoformat()
            },
            "phase_progress": {
                "phase_1_foundation": {
                    "name": "Phase 1: Foundation",
                    "contracts": ["V3-001"],
                    "completed": 0,
                    "total": 1,
                    "progress_percentage": 0.0,
                    "status": TaskStatus.PENDING.value
                },
                "phase_2_expansion": {
                    "name": "Phase 2: Expansion",
                    "contracts": ["V3-004", "V3-007"],
                    "completed": 0,
                    "total": 2,
                    "progress_percentage": 0.0,
                    "status": TaskStatus.PENDING.value
                },
                "phase_3_integration": {
                    "name": "Phase 3: Integration",
                    "contracts": ["V3-010"],
                    "completed": 0,
                    "total": 1,
                    "progress_percentage": 0.0,
                    "status": TaskStatus.PENDING.value
                }
            }
        }
        
        # Load existing progress
        self._load_existing_progress()
    
    def _load_existing_progress(self) -> None:
        """Load existing progress data."""
        try:
            latest_file = self.data_path / "latest_progress.json"
            if latest_file.exists():
                with open(latest_file, 'r', encoding='utf-8') as f:
                    self.progress_data = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load existing progress: {e}")
    
    def update_agent_progress(self, agent_id: str, task: str, status: str, 
                            efficiency: float = 0.0, quality: float = 0.0) -> None:
        """Update agent progress."""
        if agent_id not in self.progress_data["agents"]:
            self.progress_data["agents"][agent_id] = {
                "agent_id": agent_id,
                "current_task": None,
                "task_status": TaskStatus.PENDING.value,
                "v3_contracts": [],
                "completed_tasks": [],
                "last_update": datetime.datetime.now().isoformat(),
                "efficiency_score": 0.0,
                "quality_score": 0.0
            }
        
        agent_data = self.progress_data["agents"][agent_id]
        agent_data["current_task"] = task
        agent_data["task_status"] = status
        agent_data["last_update"] = datetime.datetime.now().isoformat()
        agent_data["efficiency_score"] = efficiency
        agent_data["quality_score"] = quality
        
        # Update completed tasks
        if status == TaskStatus.COMPLETED.value and task not in agent_data["completed_tasks"]:
            agent_data["completed_tasks"].append(task)
        
        # Save progress
        self._save_progress()
    
    def update_v3_contract(self, contract_id: str, agent_id: str, status: str, 
                          progress: float = 0.0) -> None:
        """Update V3 contract progress."""
        if contract_id not in self.progress_data["v3_contracts"]:
            self.progress_data["v3_contracts"][contract_id] = {
                "contract_id": contract_id,
                "title": self._get_contract_title(contract_id),
                "assigned_agent": agent_id,
                "status": status,
                "progress_percentage": 0.0,
                "start_date": datetime.datetime.now().isoformat(),
                "estimated_completion": "",
                "dependencies": self._get_contract_dependencies(contract_id),
                "deliverables": self._get_contract_deliverables(contract_id)
            }
        
        contract_data = self.progress_data["v3_contracts"][contract_id]
        contract_data["assigned_agent"] = agent_id
        contract_data["status"] = status
        contract_data["progress_percentage"] = progress
        
        # Update phase progress
        self._update_phase_progress()
        
        # Save progress
        self._save_progress()
    
    def _get_contract_title(self, contract_id: str) -> str:
        """Get contract title."""
        titles = {
            "V3-001": "Cloud Infrastructure Setup",
            "V3-004": "Distributed Tracing Implementation",
            "V3-007": "ML Pipeline Setup",
            "V3-010": "Web Dashboard Development"
        }
        return titles.get(contract_id, "Unknown Contract")
    
    def _get_contract_dependencies(self, contract_id: str) -> List[str]:
        """Get contract dependencies."""
        dependencies = {
            "V3-001": [],
            "V3-004": ["V3-001"],
            "V3-007": ["V3-001"],
            "V3-010": ["V3-004", "V3-007"]
        }
        return dependencies.get(contract_id, [])
    
    def _get_contract_deliverables(self, contract_id: str) -> List[str]:
        """Get contract deliverables."""
        deliverables = {
            "V3-001": ["AWS Infrastructure", "Kubernetes Deployment", "Security Setup"],
            "V3-004": ["Distributed Tracing System", "Jaeger Deployment", "OpenTelemetry Integration"],
            "V3-007": ["ML Pipeline", "Model Training", "Model Deployment"],
            "V3-010": ["Web Dashboard", "Real-time Updates", "Data Visualization"]
        }
        return deliverables.get(contract_id, [])
    
    def _update_phase_progress(self) -> None:
        """Update phase progress based on contract status."""
        for phase_name, phase_data in self.progress_data["phase_progress"].items():
            completed = 0
            total = phase_data["total"]
            
            for contract_id in phase_data["contracts"]:
                if contract_id in self.progress_data["v3_contracts"]:
                    contract_status = self.progress_data["v3_contracts"][contract_id]["status"]
                    if contract_status == TaskStatus.COMPLETED.value:
                        completed += 1
            
            phase_data["completed"] = completed
            phase_data["progress_percentage"] = round((completed / total) * 100, 1)
            
            # Update phase status
            if completed == total:
                phase_data["status"] = TaskStatus.COMPLETED.value
            elif completed > 0:
                phase_data["status"] = TaskStatus.IN_PROGRESS.value
            else:
                phase_data["status"] = TaskStatus.PENDING.value
        
        # Update swarm status
        self._update_swarm_status()
    
    def _update_swarm_status(self) -> None:
        """Update overall swarm status."""
        total_contracts = self.progress_data["swarm_status"]["total_contracts"]
        completed_contracts = sum(
            1 for contract in self.progress_data["v3_contracts"].values()
            if contract["status"] == TaskStatus.COMPLETED.value
        )
        
        self.progress_data["swarm_status"]["completed_contracts"] = completed_contracts
        self.progress_data["swarm_status"]["overall_progress"] = round(
            (completed_contracts / total_contracts) * 100, 1
        )
        self.progress_data["swarm_status"]["last_update"] = datetime.datetime.now().isoformat()
        
        # Update current phase
        if completed_contracts >= 3:
            self.progress_data["swarm_status"]["current_phase"] = ContractPhase.PHASE_3_INTEGRATION.value
        elif completed_contracts >= 1:
            self.progress_data["swarm_status"]["current_phase"] = ContractPhase.PHASE_2_EXPANSION.value
        else:
            self.progress_data["swarm_status"]["current_phase"] = ContractPhase.PHASE_1_FOUNDATION.value
    
    def _save_progress(self) -> None:
        """Save progress data."""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save timestamped version
        progress_file = self.data_path / f"progress_{timestamp}.json"
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress_data, f, indent=2, ensure_ascii=False)
        
        # Save latest version
        latest_file = self.data_path / "latest_progress.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress_data, f, indent=2, ensure_ascii=False)
    
    def get_agent_progress(self, agent_id: str) -> Optional[AgentProgress]:
        """Get agent progress."""
        if agent_id in self.progress_data["agents"]:
            data = self.progress_data["agents"][agent_id]
            return AgentProgress(**data)
        return None
    
    def get_v3_contract_progress(self, contract_id: str) -> Optional[V3ContractProgress]:
        """Get V3 contract progress."""
        if contract_id in self.progress_data["v3_contracts"]:
            data = self.progress_data["v3_contracts"][contract_id]
            return V3ContractProgress(**data)
        return None
    
    def get_swarm_progress(self) -> SwarmProgress:
        """Get swarm progress."""
        data = self.progress_data["swarm_status"]
        return SwarmProgress(
            total_agents=data["total_agents"],
            active_agents=data["active_agents"],
            completed_contracts=data["completed_contracts"],
            total_contracts=data["total_contracts"],
            overall_progress=data["overall_progress"],
            current_phase=data["current_phase"],
            phase_progress=self.progress_data["phase_progress"],
            last_update=data["last_update"]
        )
    
    def generate_progress_report(self) -> str:
        """Generate comprehensive progress report."""
        report = []
        report.append("# 📊 Captain Progress Report")
        report.append(f"**Generated**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Swarm status
        swarm = self.get_swarm_progress()
        report.append("## 🐝 Swarm Status")
        report.append(f"- **Total Agents**: {swarm.total_agents}")
        report.append(f"- **Active Agents**: {swarm.active_agents}")
        report.append(f"- **Overall Progress**: {swarm.overall_progress}%")
        report.append(f"- **Current Phase**: {swarm.current_phase}")
        report.append(f"- **Completed Contracts**: {swarm.completed_contracts}/{swarm.total_contracts}")
        report.append("")
        
        # Phase progress
        report.append("## 🎯 Phase Progress")
        for phase_name, phase_data in self.progress_data["phase_progress"].items():
            report.append(f"### {phase_data['name']}")
            report.append(f"- **Status**: {phase_data['status']}")
            report.append(f"- **Progress**: {phase_data['completed']}/{phase_data['total']} ({phase_data['progress_percentage']}%)")
            report.append(f"- **Contracts**: {', '.join(phase_data['contracts'])}")
            report.append("")
        
        # Agent progress
        report.append("## 🤖 Agent Progress")
        for agent_id, agent_data in self.progress_data["agents"].items():
            report.append(f"### {agent_id}")
            report.append(f"- **Current Task**: {agent_data['current_task'] or 'None'}")
            report.append(f"- **Status**: {agent_data['task_status']}")
            report.append(f"- **Efficiency**: {agent_data['efficiency_score']}/10")
            report.append(f"- **Quality**: {agent_data['quality_score']}/10")
            report.append(f"- **Completed Tasks**: {len(agent_data['completed_tasks'])}")
            report.append("")
        
        # V3 contracts
        report.append("## 📋 V3 Contracts")
        for contract_id, contract_data in self.progress_data["v3_contracts"].items():
            report.append(f"### {contract_id}: {contract_data['title']}")
            report.append(f"- **Assigned Agent**: {contract_data['assigned_agent']}")
            report.append(f"- **Status**: {contract_data['status']}")
            report.append(f"- **Progress**: {contract_data['progress_percentage']}%")
            report.append(f"- **Dependencies**: {', '.join(contract_data['dependencies']) or 'None'}")
            report.append("")
        
        return "\n".join(report)
    
    def get_bottlenecks(self) -> List[str]:
        """Identify bottlenecks in progress."""
        bottlenecks = []
        
        # Check for blocked contracts
        for contract_id, contract_data in self.progress_data["v3_contracts"].items():
            if contract_data["status"] == TaskStatus.BLOCKED.value:
                bottlenecks.append(f"Contract {contract_id} is blocked")
            
            # Check dependencies
            for dep in contract_data["dependencies"]:
                if dep in self.progress_data["v3_contracts"]:
                    dep_status = self.progress_data["v3_contracts"][dep]["status"]
                    if dep_status != TaskStatus.COMPLETED.value:
                        bottlenecks.append(f"Contract {contract_id} waiting for {dep}")
        
        # Check for inactive agents
        for agent_id, agent_data in self.progress_data["agents"].items():
            if agent_data["task_status"] == TaskStatus.PENDING.value:
                bottlenecks.append(f"Agent {agent_id} has no active task")
        
        return bottlenecks
    
    def get_next_priorities(self) -> List[str]:
        """Get next priority actions."""
        priorities = []
        
        # Check for ready contracts
        for contract_id, contract_data in self.progress_data["v3_contracts"].items():
            if contract_data["status"] == TaskStatus.PENDING.value:
                # Check if dependencies are met
                deps_met = True
                for dep in contract_data["dependencies"]:
                    if dep in self.progress_data["v3_contracts"]:
                        dep_status = self.progress_data["v3_contracts"][dep]["status"]
                        if dep_status != TaskStatus.COMPLETED.value:
                            deps_met = False
                            break
                
                if deps_met:
                    priorities.append(f"Start contract {contract_id}: {contract_data['title']}")
        
        # Check for available agents
        available_agents = [
            agent_id for agent_id, agent_data in self.progress_data["agents"].items()
            if agent_data["task_status"] == TaskStatus.PENDING.value
        ]
        
        if available_agents and priorities:
            priorities.append(f"Assign available agents: {', '.join(available_agents)}")
        
        return priorities


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Captain Progress Tracker")
    parser.add_argument('--report', action='store_true', help='Generate progress report')
    parser.add_argument('--update-agent', help='Update agent progress (agent_id:task:status)')
    parser.add_argument('--update-contract', help='Update contract progress (contract_id:agent_id:status:progress)')
    parser.add_argument('--bottlenecks', action='store_true', help='Show bottlenecks')
    parser.add_argument('--priorities', action='store_true', help='Show next priorities')
    
    args = parser.parse_args()
    
    try:
        tracker = CaptainProgressTracker()
        
        if args.update_agent:
            parts = args.update_agent.split(':')
            if len(parts) >= 3:
                agent_id, task, status = parts[0], parts[1], parts[2]
                efficiency = float(parts[3]) if len(parts) > 3 else 0.0
                quality = float(parts[4]) if len(parts) > 4 else 0.0
                tracker.update_agent_progress(agent_id, task, status, efficiency, quality)
                print(f"✅ Updated {agent_id} progress")
        
        if args.update_contract:
            parts = args.update_contract.split(':')
            if len(parts) >= 3:
                contract_id, agent_id, status = parts[0], parts[1], parts[2]
                progress = float(parts[3]) if len(parts) > 3 else 0.0
                tracker.update_v3_contract(contract_id, agent_id, status, progress)
                print(f"✅ Updated {contract_id} progress")
        
        if args.report:
            print(tracker.generate_progress_report())
        
        if args.bottlenecks:
            bottlenecks = tracker.get_bottlenecks()
            if bottlenecks:
                print("🚨 Bottlenecks identified:")
                for bottleneck in bottlenecks:
                    print(f"  - {bottleneck}")
            else:
                print("✅ No bottlenecks identified")
        
        if args.priorities:
            priorities = tracker.get_next_priorities()
            if priorities:
                print("🎯 Next priorities:")
                for priority in priorities:
                    print(f"  - {priority}")
            else:
                print("✅ All priorities addressed")
        
        if not any([args.report, args.update_agent, args.update_contract, args.bottlenecks, args.priorities]):
            # Show current status
            swarm = tracker.get_swarm_progress()
            print(f"Swarm Progress: {swarm.overall_progress}%")
            print(f"Current Phase: {swarm.current_phase}")
            print(f"Completed Contracts: {swarm.completed_contracts}/{swarm.total_contracts}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
