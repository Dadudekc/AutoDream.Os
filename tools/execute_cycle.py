#!/usr/bin/env python3
"""
Execute Cycle
=============

Helper script to execute agent cycles with validation and progress tracking.

Usage:
    python tools/execute_cycle.py --cycle c001 --agent Agent-3
    python tools/execute_cycle.py --list-available
    python tools/execute_cycle.py --status
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime


class CycleExecutor:
    """Execute and validate agent cycles."""

    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.devlogs_dir = Path("devlogs")
        self.devlogs_dir.mkdir(exist_ok=True)

    def list_available_cycles(self):
        """List all available cycles by phase."""
        phases = {
            "phase1_discovery": "Discovery (C1-C8)",
            "phase2_cleanup": "Cleanup (C9-C20)",
            "phase3_enhancement": "Enhancement (C21-C40)",
            "phase4_documentation": "Documentation (C41-C55)",
            "phase5_testing": "Testing (C56-C70)",
        }

        print("🎯 Available Cycles by Phase")
        print("=" * 50)

        for phase_dir, phase_name in phases.items():
            phase_path = self.prompts_dir / phase_dir
            if phase_path.exists():
                cycles = sorted([f.stem for f in phase_path.glob("c*.md")])
                print(f"\n📁 {phase_name}")
                for cycle in cycles:
                    print(f"   • {cycle}")
            else:
                print(f"\n📁 {phase_name} - Not found")

    def get_cycle_info(self, cycle_id: str):
        """Get information about a specific cycle."""
        cycle_file = None
        
        # Search for cycle file across all phases
        for phase_dir in self.prompts_dir.iterdir():
            if phase_dir.is_dir():
                potential_file = phase_dir / f"{cycle_id}.md"
                if potential_file.exists():
                    cycle_file = potential_file
                    break
        
        if not cycle_file:
            print(f"❌ Cycle {cycle_id} not found")
            return None
        
        try:
            content = cycle_file.read_text(encoding="utf-8")
            
            # Extract key information
            lines = content.split('\n')
            title = lines[0] if lines else "Unknown"
            agent = "Unknown"
            time_est = "Unknown"
            priority = "Unknown"
            
            for line in lines:
                if line.startswith("**AGENT:**"):
                    agent = line.replace("**AGENT:**", "").strip()
                elif line.startswith("**ESTIMATED TIME:**"):
                    time_est = line.replace("**ESTIMATED TIME:**", "").strip()
                elif line.startswith("**PRIORITY:**"):
                    priority = line.replace("**PRIORITY:**", "").strip()
            
            return {
                "file": cycle_file,
                "title": title,
                "agent": agent,
                "time_est": time_est,
                "priority": priority,
                "content": content
            }
        except Exception as e:
            print(f"❌ Error reading cycle {cycle_id}: {e}")
            return None

    def execute_cycle(self, cycle_id: str, agent: str = None, dry_run: bool = False):
        """Execute a specific cycle."""
        cycle_info = self.get_cycle_info(cycle_id)
        if not cycle_info:
            return False
        
        print(f"🚀 Executing {cycle_id}")
        print(f"📋 {cycle_info['title']}")
        print(f"🤖 Agent: {cycle_info['agent']}")
        print(f"⏰ Estimated Time: {cycle_info['time_est']}")
        print(f"🎯 Priority: {cycle_info['priority']}")
        print("=" * 60)
        
        if dry_run:
            print("🔍 DRY RUN - Would execute the following:")
            print(cycle_info['content'])
            return True
        
        # Create agent devlog if it doesn't exist
        agent_devlog = self.devlogs_dir / f"{agent or 'unknown'}.md"
        if not agent_devlog.exists():
            agent_devlog.write_text(f"# {agent or 'Unknown'} Devlog\n\n", encoding="utf-8")
        
        # Log cycle start
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        start_log = f"\n## CYCLE START: {cycle_id} - {timestamp}\n\n"
        agent_devlog.write_text(agent_devlog.read_text() + start_log, encoding="utf-8")
        
        print(f"📝 Cycle started - logged to {agent_devlog}")
        print(f"⏰ Start time: {timestamp}")
        print("\n📋 Cycle Instructions:")
        print(cycle_info['content'])
        
        print(f"\n💡 To mark completion, add this to {agent_devlog}:")
        print(f"CYCLE_DONE {agent or 'Agent-X'} {cycle_id} [\"metric1\", \"metric2\", \"metric3\", \"metric4\"] \"Summary of completion\"")
        
        return True

    def get_system_status(self):
        """Get overall system status."""
        print("🎯 V2_SWARM System Status")
        print("=" * 40)
        
        # Check progress tracker
        try:
            result = subprocess.run([sys.executable, "tools/cycle_progress_tracker.py", "--format", "summary"], 
                                  capture_output=True, text=True, cwd=".")
            if result.returncode == 0:
                print(result.stdout)
            else:
                print("⚠️ Progress tracker not available")
        except Exception as e:
            print(f"⚠️ Error running progress tracker: {e}")
        
        # Check devlogs
        if self.devlogs_dir.exists():
            devlog_files = list(self.devlogs_dir.glob("*.md"))
            print(f"\n📝 Devlogs: {len(devlog_files)} files")
            for devlog in sorted(devlog_files):
                print(f"   • {devlog.name}")
        else:
            print("\n📝 Devlogs: No devlog directory found")
        
        # Check prompts
        total_prompts = 0
        for phase_dir in self.prompts_dir.iterdir():
            if phase_dir.is_dir():
                prompts = list(phase_dir.glob("c*.md"))
                total_prompts += len(prompts)
        
        print(f"\n📋 Prompts: {total_prompts} total")
        
        return True


def main():
    parser = argparse.ArgumentParser(description="Execute agent cycles")
    parser.add_argument("--cycle", help="Cycle ID to execute (e.g., c001)")
    parser.add_argument("--agent", help="Agent executing the cycle")
    parser.add_argument("--list-available", action="store_true", help="List all available cycles")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be executed without running")
    parser.add_argument("--prompts-dir", default="prompts", help="Prompts directory path")
    
    args = parser.parse_args()
    
    executor = CycleExecutor(args.prompts_dir)
    
    if args.list_available:
        executor.list_available_cycles()
    elif args.status:
        executor.get_system_status()
    elif args.cycle:
        executor.execute_cycle(args.cycle, args.agent, args.dry_run)
    else:
        print("❌ Please specify --cycle, --list-available, or --status")
        parser.print_help()


if __name__ == "__main__":
    main()

