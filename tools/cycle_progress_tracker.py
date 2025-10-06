#!/usr/bin/env python3
"""
Cycle Progress Tracker
======================

Tracks progress of agent cycles by parsing CYCLE_DONE messages from devlogs.
Provides real-time progress visualization and identifies blockers.

Usage:
    python tools/cycle_progress_tracker.py --format dashboard
    python tools/cycle_progress_tracker.py --format summary
    python tools/cycle_progress_tracker.py --format json
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class CycleProgressTracker:
    """Tracks and visualizes agent cycle progress."""

    def __init__(self, devlogs_dir: str = "devlogs"):
        self.devlogs_dir = Path(devlogs_dir)
        self.cycles = {}
        self.phases = {
            "phase1_discovery": {"cycles": list(range(1, 9)), "name": "Discovery"},
            "phase2_cleanup": {"cycles": list(range(9, 21)), "name": "Cleanup"},
            "phase3_enhancement": {"cycles": list(range(21, 41)), "name": "Enhancement"},
            "phase4_documentation": {"cycles": list(range(41, 56)), "name": "Documentation"},
            "phase5_testing": {"cycles": list(range(56, 71)), "name": "Testing & Validation"},
        }

    def parse_cycle_done(self, line: str) -> Dict:
        """Parse a CYCLE_DONE message."""
        pattern = r"CYCLE_DONE\s+(\w+)\s+([a-zA-Z0-9]+)\s+\[(.*?)\]\s+\"([^\"]+)\""
        match = re.search(pattern, line)
        
        if match:
            agent = match.group(1)
            cycle_id = match.group(2)
            metrics = [m.strip().strip('"') for m in match.group(3).split(",")]
            summary = match.group(4)
            
            return {
                "agent": agent,
                "cycle_id": cycle_id,
                "metrics": metrics,
                "summary": summary,
                "timestamp": datetime.now().isoformat(),
            }
        return None

    def scan_devlogs(self) -> None:
        """Scan all devlog files for CYCLE_DONE messages."""
        if not self.devlogs_dir.exists():
            print(f"⚠️ Devlogs directory not found: {self.devlogs_dir}")
            return

        for devlog_file in self.devlogs_dir.glob("*.md"):
            try:
                with open(devlog_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Use regex to find CYCLE_DONE messages that might span multiple lines
                    pattern = r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\""
                    matches = re.finditer(pattern, content, re.DOTALL)
                    for match in matches:
                        cycle_data = {
                            "agent": match.group(1),
                            "cycle_id": match.group(2),
                            "metrics": [m.strip().strip('"') for m in match.group(3).split(",")],
                            "summary": match.group(4),
                            "timestamp": datetime.now().isoformat(),
                            "file": devlog_file.name,
                            "line": content[:match.start()].count('\n') + 1,
                        }
                        self.cycles[cycle_data["cycle_id"]] = cycle_data
            except Exception as e:
                print(f"⚠️ Error reading {devlog_file}: {e}")

    def get_phase_progress(self) -> Dict:
        """Calculate progress for each phase."""
        phase_progress = {}
        
        for phase_id, phase_info in self.phases.items():
            total_cycles = len(phase_info["cycles"])
            completed_cycles = 0
            
            for cycle_num in phase_info["cycles"]:
                cycle_id = f"c{cycle_num:03d}"
                if cycle_id in self.cycles:
                    completed_cycles += 1
            
            progress_percent = (completed_cycles / total_cycles) * 100 if total_cycles > 0 else 0
            
            phase_progress[phase_id] = {
                "name": phase_info["name"],
                "total_cycles": total_cycles,
                "completed_cycles": completed_cycles,
                "progress_percent": progress_percent,
                "cycles": phase_info["cycles"],
            }
        
        return phase_progress

    def get_overall_progress(self) -> Dict:
        """Calculate overall progress."""
        total_cycles = 70
        completed_cycles = len(self.cycles)
        progress_percent = (completed_cycles / total_cycles) * 100
        
        return {
            "total_cycles": total_cycles,
            "completed_cycles": completed_cycles,
            "progress_percent": progress_percent,
            "remaining_cycles": total_cycles - completed_cycles,
        }

    def get_agent_progress(self) -> Dict:
        """Calculate progress by agent."""
        agent_progress = {}
        
        for cycle_data in self.cycles.values():
            agent = cycle_data["agent"]
            if agent not in agent_progress:
                agent_progress[agent] = {"completed": 0, "cycles": []}
            
            agent_progress[agent]["completed"] += 1
            agent_progress[agent]["cycles"].append(cycle_data["cycle_id"])
        
        return agent_progress

    def get_blockers(self) -> List[Dict]:
        """Identify potential blockers and dependencies."""
        blockers = []
        
        # Check for cycles that might be blocked
        for cycle_id, cycle_data in self.cycles.items():
            # Look for blocker keywords in summary
            summary = cycle_data["summary"].lower()
            if any(keyword in summary for keyword in ["blocker", "failed", "error", "issue"]):
                blockers.append({
                    "cycle_id": cycle_id,
                    "agent": cycle_data["agent"],
                    "issue": cycle_data["summary"],
                    "file": cycle_data["file"],
                })
        
        return blockers

    def generate_dashboard(self) -> str:
        """Generate a visual dashboard."""
        self.scan_devlogs()
        overall = self.get_overall_progress()
        phase_progress = self.get_phase_progress()
        agent_progress = self.get_agent_progress()
        blockers = self.get_blockers()
        
        dashboard = f"""
🎯 V2_SWARM Cycle Progress Dashboard
{'='*60}
📊 Overall Progress: {overall['completed_cycles']}/{overall['total_cycles']} cycles ({overall['progress_percent']:.1f}%)
⏰ Remaining: {overall['remaining_cycles']} cycles

📈 Phase Progress:
"""
        
        for phase_id, progress in phase_progress.items():
            bar_length = 20
            filled = int((progress['progress_percent'] / 100) * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            dashboard += f"  {progress['name']:<20} {progress['completed_cycles']:2d}/{progress['total_cycles']:2d} [{bar}] {progress['progress_percent']:5.1f}%\n"
        
        dashboard += f"\n🤖 Agent Progress:\n"
        for agent, progress in sorted(agent_progress.items()):
            dashboard += f"  {agent:<15} {progress['completed']:2d} cycles completed\n"
        
        if blockers:
            dashboard += f"\n🚨 Blockers ({len(blockers)}):\n"
            for blocker in blockers:
                dashboard += f"  • {blocker['cycle_id']} ({blocker['agent']}): {blocker['issue']}\n"
        else:
            dashboard += f"\n✅ No blockers detected\n"
        
        dashboard += f"\n📝 Recent Completions:\n"
        recent_cycles = sorted(self.cycles.values(), key=lambda x: x.get('timestamp', ''), reverse=True)[:5]
        for cycle in recent_cycles:
            dashboard += f"  • {cycle['cycle_id']} ({cycle['agent']}): {cycle['summary']}\n"
        
        dashboard += f"\n{'='*60}\n"
        dashboard += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return dashboard

    def generate_summary(self) -> str:
        """Generate a concise summary."""
        self.scan_devlogs()
        overall = self.get_overall_progress()
        
        return f"""V2_SWARM Progress Summary
Completed: {overall['completed_cycles']}/{overall['total_cycles']} cycles ({overall['progress_percent']:.1f}%)
Remaining: {overall['remaining_cycles']} cycles
Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    def generate_json(self) -> str:
        """Generate JSON output."""
        self.scan_devlogs()
        
        data = {
            "overall": self.get_overall_progress(),
            "phases": self.get_phase_progress(),
            "agents": self.get_agent_progress(),
            "blockers": self.get_blockers(),
            "cycles": self.cycles,
            "generated": datetime.now().isoformat(),
        }
        
        return json.dumps(data, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Track agent cycle progress")
    parser.add_argument("--format", choices=["dashboard", "summary", "json"], default="dashboard",
                       help="Output format")
    parser.add_argument("--devlogs", default="devlogs", help="Devlogs directory path")
    parser.add_argument("--output", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    tracker = CycleProgressTracker(args.devlogs)
    
    if args.format == "dashboard":
        output = tracker.generate_dashboard()
    elif args.format == "summary":
        output = tracker.generate_summary()
    elif args.format == "json":
        output = tracker.generate_json()
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Progress report saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
