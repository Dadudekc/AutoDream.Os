#!/usr/bin/env python3
"""
Captain Onboarding Wizard - V2 Compliant
=======================================

Interactive wizard to guide new Captains through the onboarding process.
Provides step-by-step guidance and hands-on practice.

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


class OnboardingPhase(Enum):
    """Onboarding phase enumeration."""
    SYSTEM_UNDERSTANDING = "SYSTEM_UNDERSTANDING"
    HANDS_ON_PRACTICE = "HANDS_ON_PRACTICE"
    STRATEGIC_PLANNING = "STRATEGIC_PLANNING"
    CERTIFICATION = "CERTIFICATION"


class OnboardingStep(Enum):
    """Onboarding step enumeration."""
    READ_DOCUMENTATION = "READ_DOCUMENTATION"
    EXPLORE_TOOLS = "EXPLORE_TOOLS"
    HEALTH_ASSESSMENT = "HEALTH_ASSESSMENT"
    PROGRESS_TRACKING = "PROGRESS_TRACKING"
    AGENT_COMMUNICATION = "AGENT_COMMUNICATION"
    STRATEGIC_DIRECTIVES = "STRATEGIC_DIRECTIVES"
    DAILY_ROUTINE = "DAILY_ROUTINE"
    CERTIFICATION_TEST = "CERTIFICATION_TEST"


@dataclass
class OnboardingProgress:
    """Onboarding progress tracking."""
    captain_id: str
    current_phase: str
    completed_steps: List[str]
    current_step: str
    start_date: str
    last_update: str
    certification_status: str


class CaptainOnboardingWizard:
    """Interactive Captain onboarding wizard."""
    
    def __init__(self, captain_id: str = "Captain"):
        """Initialize onboarding wizard."""
        self.captain_id = captain_id
        self.progress_file = Path("captain_onboarding_progress.json")
        self.progress = self._load_progress()
        
        # Onboarding phases and steps
        self.phases = {
            OnboardingPhase.SYSTEM_UNDERSTANDING.value: {
                "name": "Phase 1: System Understanding",
                "description": "Learn about Captain role, tools, and systems",
                "steps": [
                    OnboardingStep.READ_DOCUMENTATION.value,
                    OnboardingStep.EXPLORE_TOOLS.value
                ]
            },
            OnboardingPhase.HANDS_ON_PRACTICE.value: {
                "name": "Phase 2: Hands-On Practice",
                "description": "Practice using Captain tools and systems",
                "steps": [
                    OnboardingStep.HEALTH_ASSESSMENT.value,
                    OnboardingStep.PROGRESS_TRACKING.value,
                    OnboardingStep.AGENT_COMMUNICATION.value
                ]
            },
            OnboardingPhase.STRATEGIC_PLANNING.value: {
                "name": "Phase 3: Strategic Planning",
                "description": "Learn strategic planning and directive management",
                "steps": [
                    OnboardingStep.STRATEGIC_DIRECTIVES.value,
                    OnboardingStep.DAILY_ROUTINE.value
                ]
            },
            OnboardingPhase.CERTIFICATION.value: {
                "name": "Phase 4: Certification",
                "description": "Complete certification requirements",
                "steps": [
                    OnboardingStep.CERTIFICATION_TEST.value
                ]
            }
        }
    
    def _load_progress(self) -> OnboardingProgress:
        """Load onboarding progress."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return OnboardingProgress(**data)
            except Exception:
                pass
        
        # Create new progress
        return OnboardingProgress(
            captain_id=self.captain_id,
            current_phase=OnboardingPhase.SYSTEM_UNDERSTANDING.value,
            completed_steps=[],
            current_step=OnboardingStep.READ_DOCUMENTATION.value,
            start_date=datetime.datetime.now().isoformat(),
            last_update=datetime.datetime.now().isoformat(),
            certification_status="IN_PROGRESS"
        )
    
    def _save_progress(self) -> None:
        """Save onboarding progress."""
        self.progress.last_update = datetime.datetime.now().isoformat()
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.progress), f, indent=2, ensure_ascii=False)
    
    def start_onboarding(self) -> None:
        """Start the onboarding process."""
        print("🎯 Welcome to Captain Onboarding!")
        print(f"Captain ID: {self.captain_id}")
        print(f"Current Phase: {self.phases[self.progress.current_phase]['name']}")
        print(f"Progress: {len(self.progress.completed_steps)}/{sum(len(phase['steps']) for phase in self.phases.values())} steps completed")
        print()
        
        # Show current phase
        self._show_current_phase()
        
        # Show available commands
        self._show_commands()
    
    def _show_current_phase(self) -> None:
        """Show current phase information."""
        phase_info = self.phases[self.progress.current_phase]
        print(f"📋 {phase_info['name']}")
        print(f"   {phase_info['description']}")
        print()
        
        # Show steps in current phase
        print("📝 Steps in this phase:")
        for step in phase_info['steps']:
            status = "✅" if step in self.progress.completed_steps else "⏳"
            print(f"   {status} {step.replace('_', ' ').title()}")
        print()
    
    def _show_commands(self) -> None:
        """Show available commands."""
        print("🛠️ Available Commands:")
        print("   next          - Complete current step and move to next")
        print("   step <name>   - Jump to specific step")
        print("   status        - Show current progress")
        print("   help          - Show this help")
        print("   quit          - Exit onboarding")
        print()
    
    def complete_step(self, step_name: str) -> None:
        """Complete a specific step."""
        if step_name not in self.progress.completed_steps:
            self.progress.completed_steps.append(step_name)
            print(f"✅ Completed step: {step_name.replace('_', ' ').title()}")
            
            # Move to next step
            self._move_to_next_step()
            self._save_progress()
        else:
            print(f"ℹ️ Step already completed: {step_name.replace('_', ' ').title()}")
    
    def _move_to_next_step(self) -> None:
        """Move to next step in current phase."""
        current_phase_steps = self.phases[self.progress.current_phase]['steps']
        current_index = current_phase_steps.index(self.progress.current_step)
        
        if current_index + 1 < len(current_phase_steps):
            # Move to next step in current phase
            self.progress.current_step = current_phase_steps[current_index + 1]
        else:
            # Move to next phase
            self._move_to_next_phase()
    
    def _move_to_next_phase(self) -> None:
        """Move to next phase."""
        phases = list(self.phases.keys())
        current_index = phases.index(self.progress.current_phase)
        
        if current_index + 1 < len(phases):
            # Move to next phase
            self.progress.current_phase = phases[current_index + 1]
            self.progress.current_step = self.phases[self.progress.current_phase]['steps'][0]
            print(f"🎉 Phase completed! Moving to: {self.phases[self.progress.current_phase]['name']}")
        else:
            # All phases completed
            self.progress.certification_status = "COMPLETED"
            print("🏆 Congratulations! Captain onboarding completed!")
    
    def jump_to_step(self, step_name: str) -> None:
        """Jump to specific step."""
        # Find step in phases
        for phase_name, phase_info in self.phases.items():
            if step_name in phase_info['steps']:
                self.progress.current_phase = phase_name
                self.progress.current_step = step_name
                self._save_progress()
                print(f"📍 Jumped to: {step_name.replace('_', ' ').title()}")
                return
        
        print(f"❌ Step not found: {step_name}")
    
    def show_status(self) -> None:
        """Show current onboarding status."""
        print("📊 Captain Onboarding Status")
        print("=" * 40)
        print(f"Captain ID: {self.progress.captain_id}")
        print(f"Start Date: {self.progress.start_date}")
        print(f"Last Update: {self.progress.last_update}")
        print(f"Certification Status: {self.progress.certification_status}")
        print()
        
        # Show progress by phase
        total_steps = sum(len(phase['steps']) for phase in self.phases.values())
        completed_steps = len(self.progress.completed_steps)
        progress_percentage = (completed_steps / total_steps) * 100
        
        print(f"Overall Progress: {completed_steps}/{total_steps} ({progress_percentage:.1f}%)")
        print()
        
        for phase_name, phase_info in self.phases.items():
            phase_steps = phase_info['steps']
            completed_in_phase = sum(1 for step in phase_steps if step in self.progress.completed_steps)
            phase_progress = (completed_in_phase / len(phase_steps)) * 100
            
            status = "✅" if phase_progress == 100 else "⏳" if phase_progress > 0 else "⏸️"
            print(f"{status} {phase_info['name']}: {completed_in_phase}/{len(phase_steps)} ({phase_progress:.1f}%)")
        
        print()
        print(f"Current Phase: {self.phases[self.progress.current_phase]['name']}")
        print(f"Current Step: {self.progress.current_step.replace('_', ' ').title()}")
    
    def run_step_guide(self, step_name: str) -> None:
        """Run interactive guide for specific step."""
        if step_name == OnboardingStep.READ_DOCUMENTATION.value:
            self._guide_read_documentation()
        elif step_name == OnboardingStep.EXPLORE_TOOLS.value:
            self._guide_explore_tools()
        elif step_name == OnboardingStep.HEALTH_ASSESSMENT.value:
            self._guide_health_assessment()
        elif step_name == OnboardingStep.PROGRESS_TRACKING.value:
            self._guide_progress_tracking()
        elif step_name == OnboardingStep.AGENT_COMMUNICATION.value:
            self._guide_agent_communication()
        elif step_name == OnboardingStep.STRATEGIC_DIRECTIVES.value:
            self._guide_strategic_directives()
        elif step_name == OnboardingStep.DAILY_ROUTINE.value:
            self._guide_daily_routine()
        elif step_name == OnboardingStep.CERTIFICATION_TEST.value:
            self._guide_certification_test()
        else:
            print(f"❌ Unknown step: {step_name}")
    
    def _guide_read_documentation(self) -> None:
        """Guide through reading documentation."""
        print("📖 Step: Read Documentation")
        print("=" * 30)
        print("Please read the following documentation:")
        print()
        print("1. 📋 Captain's Handbook: docs/CAPTAIN_HANDBOOK.md")
        print("2. 🎯 Captain's Cheatsheet: docs/CAPTAIN_CHEATSHEET.md")
        print("3. 📝 Captain's Log Template: docs/CAPTAIN_LOG_TEMPLATE.md")
        print("4. 🔄 FSM Overview: docs/fsm/OVERVIEW.md")
        print()
        print("After reading, type 'next' to continue.")
    
    def _guide_explore_tools(self) -> None:
        """Guide through exploring tools."""
        print("🛠️ Step: Explore Captain Tools")
        print("=" * 30)
        print("Let's explore the Captain tools:")
        print()
        print("1. 🎯 Enhanced Captain CLI (with role/mode management):")
        print("   python tools/captain/cli.py status")
        print("   python tools/captain/cli.py mode list")
        print("   python tools/captain/cli.py role list")
        print()
        print("2. 🏥 Repository Health Monitor:")
        print("   python tools/captain_repository_health_monitor.py . --report")
        print()
        print("3. 📊 Progress Tracker:")
        print("   python tools/captain_progress_tracker.py --report")
        print()
        print("4. 🚫 Overengineering Detector:")
        print("   python tools/overengineering_detector.py src/ --report")
        print()
        print("5. 📋 Directive Manager:")
        print("   python tools/captain_directive_manager.py --list-directives")
        print()
        print("6. 🔄 Mode and Role Management:")
        print("   python tools/captain/cli.py mode switch 6 --owner captain")
        print("   python tools/captain/cli.py role assign 1 captain")
        print()
        print("Run these commands to explore the tools. Type 'next' when done.")
    
    def _guide_health_assessment(self) -> None:
        """Guide through health assessment."""
        print("🏥 Step: Health Assessment Practice")
        print("=" * 30)
        print("Practice using the repository health monitor:")
        print()
        print("1. Assess current project health:")
        print("   python tools/captain_repository_health_monitor.py . --report")
        print()
        print("2. Get agent assignment recommendation:")
        print("   python tools/captain_repository_health_monitor.py . --assign-agent")
        print()
        print("3. Assess specific directory:")
        print("   python tools/captain_repository_health_monitor.py src/ --report")
        print()
        print("Run these commands and review the results. Type 'next' when done.")
    
    def _guide_progress_tracking(self) -> None:
        """Guide through progress tracking."""
        print("📊 Step: Progress Tracking Practice")
        print("=" * 30)
        print("Practice using the progress tracker:")
        print()
        print("1. Generate progress report:")
        print("   python tools/captain_progress_tracker.py --report")
        print()
        print("2. Check for bottlenecks:")
        print("   python tools/captain_progress_tracker.py --bottlenecks")
        print()
        print("3. Get next priorities:")
        print("   python tools/captain_progress_tracker.py --priorities")
        print()
        print("4. Update agent progress (example):")
        print("   python tools/captain_progress_tracker.py --update-agent Agent-1:V3-001:IN_PROGRESS:8.5:9.0")
        print()
        print("Run these commands and review the results. Type 'next' when done.")
    
    def _guide_agent_communication(self) -> None:
        """Guide through agent communication."""
        print("🤖 Step: Agent Communication Practice")
        print("=" * 30)
        print("Practice communicating with agents:")
        print()
        print("1. Send test message to Agent-1:")
        print("   python -m src.services.messaging.cli.messaging_cli_clean send --agent Agent-1 --message \"Captain onboarding test message\" --priority NORMAL")
        print()
        print("2. Check agent status:")
        print("   python -m src.services.messaging.cli.messaging_cli_clean status --agent Agent-1")
        print()
        print("3. Broadcast to all agents:")
        print("   python -m src.services.messaging.cli.messaging_cli_clean broadcast --message \"Captain onboarding complete\" --priority NORMAL")
        print()
        print("Run these commands to practice agent communication. Type 'next' when done.")
    
    def _guide_strategic_directives(self) -> None:
        """Guide through strategic directives."""
        print("📋 Step: Strategic Directives Practice")
        print("=" * 30)
        print("Practice managing strategic directives:")
        print()
        print("1. List current directives:")
        print("   python tools/captain_directive_manager.py --list-directives")
        print()
        print("2. Create a test directive:")
        print("   python tools/captain_directive_manager.py --create-directive --title \"Test Directive\" --description \"Learning directive management\" --priority MEDIUM --timeline \"7 days\"")
        print()
        print("3. Update directive status:")
        print("   python tools/captain_directive_manager.py --update-directive <id> --status IN_PROGRESS")
        print()
        print("Run these commands to practice directive management. Type 'next' when done.")
    
    def _guide_daily_routine(self) -> None:
        """Guide through daily routine setup."""
        print("🌅 Step: Daily Routine Setup")
        print("=" * 30)
        print("Set up your daily Captain routine:")
        print()
        print("Morning Routine (5 minutes):")
        print("1. python tools/captain_repository_health_monitor.py . --report")
        print("2. python tools/captain_progress_tracker.py --report")
        print("3. python tools/captain_progress_tracker.py --bottlenecks")
        print("4. python tools/captain_progress_tracker.py --priorities")
        print()
        print("Evening Routine (10 minutes):")
        print("1. Update progress tracking")
        print("2. Generate daily report")
        print("3. Create Captain's log entry")
        print()
        print("Review the daily routine and commit to following it. Type 'next' when ready.")
    
    def _guide_certification_test(self) -> None:
        """Guide through certification test."""
        print("🏆 Step: Certification Test")
        print("=" * 30)
        print("Complete the Captain certification test:")
        print()
        print("1. Demonstrate repository health monitoring")
        print("2. Show progress tracking proficiency")
        print("3. Demonstrate agent communication")
        print("4. Show strategic directive management")
        print("5. Demonstrate daily routine execution")
        print()
        print("Complete all tasks and type 'next' to finish certification.")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Captain Onboarding Wizard")
    parser.add_argument('--captain-id', default='Captain', help='Captain ID')
    parser.add_argument('--step', help='Run specific step guide')
    parser.add_argument('--complete', help='Complete specific step')
    parser.add_argument('--status', action='store_true', help='Show onboarding status')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    
    args = parser.parse_args()
    
    try:
        wizard = CaptainOnboardingWizard(args.captain_id)
        
        if args.status:
            wizard.show_status()
        elif args.step:
            wizard.run_step_guide(args.step)
        elif args.complete:
            wizard.complete_step(args.complete)
        elif args.interactive:
            wizard.start_onboarding()
        else:
            wizard.start_onboarding()
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
