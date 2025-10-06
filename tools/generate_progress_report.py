#!/usr/bin/env python3
"""
Generate Progress Report
========================

Generates comprehensive progress reports from CYCLE_DONE messages.
Supports multiple output formats and detailed analysis.

Usage:
    python tools/generate_progress_report.py --format markdown > reports/progress_YYYYMMDD.md
    python tools/generate_progress_report.py --format html --output reports/progress.html
"""

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple


class ProgressReportGenerator:
    """Generates comprehensive progress reports."""

    def __init__(self, devlogs_dir: str = "devlogs"):
        self.devlogs_dir = Path(devlogs_dir)
        self.cycles = {}
        self.phases = {
            "phase1_discovery": {"cycles": list(range(1, 9)), "name": "Discovery", "target_hours": 6},
            "phase2_cleanup": {"cycles": list(range(9, 21)), "name": "Cleanup", "target_hours": 8},
            "phase3_enhancement": {"cycles": list(range(21, 41)), "name": "Enhancement", "target_hours": 20},
            "phase4_documentation": {"cycles": list(range(41, 56)), "name": "Documentation", "target_hours": 19},
            "phase5_testing": {"cycles": list(range(56, 71)), "name": "Testing & Validation", "target_hours": 13},
        }

    def parse_cycle_done(self, line: str) -> Dict:
        """Parse a CYCLE_DONE message."""
        pattern = r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\""
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
            return

        for devlog_file in self.devlogs_dir.glob("*.md"):
            try:
                with open(devlog_file, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        cycle_data = self.parse_cycle_done(line)
                        if cycle_data:
                            cycle_data["file"] = devlog_file.name
                            cycle_data["line"] = line_num
                            self.cycles[cycle_data["cycle_id"]] = cycle_data
            except Exception as e:
                print(f"⚠️ Error reading {devlog_file}: {e}")

    def get_phase_progress(self) -> Dict:
        """Calculate detailed progress for each phase."""
        phase_progress = {}
        
        for phase_id, phase_info in self.phases.items():
            total_cycles = len(phase_info["cycles"])
            completed_cycles = 0
            completed_agents = set()
            total_time_estimated = 0
            
            for cycle_num in phase_info["cycles"]:
                cycle_id = f"c{cycle_num:03d}"
                if cycle_id in self.cycles:
                    completed_cycles += 1
                    completed_agents.add(self.cycles[cycle_id]["agent"])
                    # Estimate time from cycle (simplified)
                    total_time_estimated += 45  # Average 45 minutes per cycle
            
            progress_percent = (completed_cycles / total_cycles) * 100 if total_cycles > 0 else 0
            time_progress = (total_time_estimated / 60) / phase_info["target_hours"] * 100
            
            phase_progress[phase_id] = {
                "name": phase_info["name"],
                "total_cycles": total_cycles,
                "completed_cycles": completed_cycles,
                "progress_percent": progress_percent,
                "target_hours": phase_info["target_hours"],
                "estimated_hours": total_time_estimated / 60,
                "time_progress": time_progress,
                "completed_agents": list(completed_agents),
                "cycles": phase_info["cycles"],
            }
        
        return phase_progress

    def get_overall_progress(self) -> Dict:
        """Calculate overall progress with time estimates."""
        total_cycles = 70
        completed_cycles = len(self.cycles)
        progress_percent = (completed_cycles / total_cycles) * 100
        
        # Calculate time estimates
        total_estimated_hours = completed_cycles * 0.75  # 45 minutes average
        total_target_hours = 66  # From plan
        
        # Calculate velocity
        recent_cycles = sorted(self.cycles.values(), key=lambda x: x.get('timestamp', ''), reverse=True)[:10]
        velocity_per_hour = len(recent_cycles) / 8  # Assuming 8-hour work day
        
        return {
            "total_cycles": total_cycles,
            "completed_cycles": completed_cycles,
            "progress_percent": progress_percent,
            "remaining_cycles": total_cycles - completed_cycles,
            "estimated_hours": total_estimated_hours,
            "target_hours": total_target_hours,
            "time_progress": (total_estimated_hours / total_target_hours) * 100,
            "velocity_per_hour": velocity_per_hour,
            "estimated_completion": self._estimate_completion_time(),
        }

    def _estimate_completion_time(self) -> str:
        """Estimate completion time based on current velocity."""
        remaining_cycles = 70 - len(self.cycles)
        if remaining_cycles <= 0:
            return "Completed"
        
        # Simple estimation: 45 minutes per cycle, 8 hours per day
        estimated_hours = remaining_cycles * 0.75
        estimated_days = estimated_hours / 8
        
        if estimated_days < 1:
            return f"{int(estimated_hours * 60)} minutes"
        elif estimated_days < 7:
            return f"{estimated_days:.1f} days"
        else:
            return f"{estimated_days / 7:.1f} weeks"

    def get_agent_progress(self) -> Dict:
        """Calculate detailed progress by agent."""
        agent_progress = {}
        
        for cycle_data in self.cycles.values():
            agent = cycle_data["agent"]
            if agent not in agent_progress:
                agent_progress[agent] = {
                    "completed": 0, 
                    "cycles": [],
                    "total_time": 0,
                    "recent_activity": []
                }
            
            agent_progress[agent]["completed"] += 1
            agent_progress[agent]["cycles"].append(cycle_data["cycle_id"])
            agent_progress[agent]["total_time"] += 45  # 45 minutes per cycle
            agent_progress[agent]["recent_activity"].append({
                "cycle": cycle_data["cycle_id"],
                "summary": cycle_data["summary"],
                "timestamp": cycle_data.get("timestamp", "")
            })
        
        # Sort recent activity by timestamp
        for agent in agent_progress:
            agent_progress[agent]["recent_activity"].sort(
                key=lambda x: x["timestamp"], reverse=True
            )
            # Keep only last 5 activities
            agent_progress[agent]["recent_activity"] = agent_progress[agent]["recent_activity"][:5]
        
        return agent_progress

    def get_blockers_and_risks(self) -> Dict:
        """Identify blockers, risks, and dependencies."""
        blockers = []
        risks = []
        dependencies = []
        
        for cycle_id, cycle_data in self.cycles.items():
            summary = cycle_data["summary"].lower()
            
            # Check for blockers
            if any(keyword in summary for keyword in ["blocker", "failed", "error", "issue", "broken"]):
                blockers.append({
                    "cycle_id": cycle_id,
                    "agent": cycle_data["agent"],
                    "issue": cycle_data["summary"],
                    "severity": "HIGH" if any(word in summary for word in ["failed", "broken", "critical"]) else "MEDIUM",
                    "file": cycle_data.get("file", ""),
                })
            
            # Check for risks
            if any(keyword in summary for keyword in ["warning", "concern", "risk", "uncertain"]):
                risks.append({
                    "cycle_id": cycle_id,
                    "agent": cycle_data["agent"],
                    "risk": cycle_data["summary"],
                    "file": cycle_data.get("file", ""),
                })
        
        # Identify dependency risks
        completed_cycles = set(self.cycles.keys())
        for phase_id, phase_info in self.phases.items():
            phase_cycles = [f"c{i:03d}" for i in phase_info["cycles"]]
            missing_cycles = [c for c in phase_cycles if c not in completed_cycles]
            
            if missing_cycles:
                dependencies.append({
                    "phase": phase_info["name"],
                    "missing_cycles": missing_cycles,
                    "impact": "HIGH" if len(missing_cycles) > phase_info["total_cycles"] * 0.5 else "MEDIUM",
                })
        
        return {
            "blockers": blockers,
            "risks": risks,
            "dependencies": dependencies,
        }

    def generate_markdown_report(self) -> str:
        """Generate comprehensive markdown report."""
        self.scan_devlogs()
        overall = self.get_overall_progress()
        phase_progress = self.get_phase_progress()
        agent_progress = self.get_agent_progress()
        blockers_risks = self.get_blockers_and_risks()
        
        report = f"""# V2_SWARM Production Readiness Progress Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Report Period:** Since project start  
**Total Cycles:** 70 (Agent Coordination System)

## 🎯 Executive Summary

**Overall Progress:** {overall['completed_cycles']}/{overall['total_cycles']} cycles ({overall['progress_percent']:.1f}%)  
**Time Progress:** {overall['estimated_hours']:.1f}/{overall['target_hours']} hours ({overall['time_progress']:.1f}%)  
**Estimated Completion:** {overall['estimated_completion']}  
**Current Velocity:** {overall['velocity_per_hour']:.1f} cycles/hour  

## 📊 Phase Progress

"""
        
        for phase_id, progress in phase_progress.items():
            bar_length = 20
            filled = int((progress['progress_percent'] / 100) * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            report += f"""### {progress['name']} Phase
- **Progress:** {progress['completed_cycles']}/{progress['total_cycles']} cycles [{bar}] {progress['progress_percent']:.1f}%
- **Time:** {progress['estimated_hours']:.1f}/{progress['target_hours']} hours ({progress['time_progress']:.1f}%)
- **Active Agents:** {', '.join(progress['completed_agents']) if progress['completed_agents'] else 'None'}

"""
        
        report += f"""## 🤖 Agent Performance

"""
        for agent, progress in sorted(agent_progress.items()):
            report += f"""### {agent}
- **Completed Cycles:** {progress['completed']}
- **Total Time:** {progress['total_time']} minutes
- **Recent Activity:**
"""
            for activity in progress['recent_activity'][:3]:
                report += f"  - {activity['cycle']}: {activity['summary'][:60]}{'...' if len(activity['summary']) > 60 else ''}\n"
            report += "\n"
        
        if blockers_risks['blockers']:
            report += f"""## 🚨 Critical Blockers ({len(blockers_risks['blockers'])})

"""
            for blocker in blockers_risks['blockers']:
                report += f"""### {blocker['cycle_id']} - {blocker['severity']} Severity
- **Agent:** {blocker['agent']}
- **Issue:** {blocker['issue']}
- **Source:** {blocker['file']}

"""
        
        if blockers_risks['risks']:
            report += f"""## ⚠️ Risks & Concerns ({len(blockers_risks['risks'])})

"""
            for risk in blockers_risks['risks']:
                report += f"""- **{risk['cycle_id']}** ({risk['agent']}): {risk['risk']}

"""
        
        if blockers_risks['dependencies']:
            report += f"""## 🔗 Dependency Analysis

"""
            for dep in blockers_risks['dependencies']:
                report += f"""### {dep['phase']} - {dep['impact']} Impact
- **Missing Cycles:** {', '.join(dep['missing_cycles'])}
- **Impact:** {dep['impact']}

"""
        
        report += f"""## 📈 Metrics & KPIs

### Cycle Completion Rate
- **Target:** 100% (70/70 cycles)
- **Current:** {overall['progress_percent']:.1f}% ({overall['completed_cycles']}/70)
- **Remaining:** {overall['remaining_cycles']} cycles

### Time Performance
- **Target:** 66 hours total
- **Current:** {overall['estimated_hours']:.1f} hours completed
- **Efficiency:** {overall['time_progress']:.1f}% of target time

### Agent Utilization
- **Active Agents:** {len(agent_progress)}
- **Most Active:** {max(agent_progress.items(), key=lambda x: x[1]['completed'])[0] if agent_progress else 'None'}
- **Least Active:** {min(agent_progress.items(), key=lambda x: x[1]['completed'])[0] if agent_progress else 'None'}

## 🎯 Recommendations

"""
        
        if blockers_risks['blockers']:
            report += f"""1. **Address Critical Blockers:** {len(blockers_risks['blockers'])} blockers need immediate attention
2. **Escalate High-Severity Issues:** Focus on failed cycles first
3. **Coordinate Agent Response:** Ensure proper handoff between agents

"""
        
        if overall['progress_percent'] < 50:
            report += f"""4. **Accelerate Execution:** Current progress suggests need for increased velocity
5. **Review Dependencies:** Ensure prerequisite cycles are completed before dependent cycles

"""
        
        report += f"""## 📝 Next Steps

1. **Review this report** with all agents
2. **Address blockers** identified above
3. **Continue cycle execution** according to phase priorities
4. **Update progress** daily via CYCLE_DONE messages
5. **Generate next report** in 24 hours

---

**Report Generated by:** V2_SWARM Progress Report Generator  
**Next Update:** {datetime.now() + timedelta(hours=24):%Y-%m-%d %H:%M:%S}  
**Contact:** Agent-4 (Captain) for questions or issues
"""
        
        return report

    def generate_html_report(self) -> str:
        """Generate HTML report with styling."""
        markdown_content = self.generate_markdown_report()
        
        # Convert markdown to HTML (simplified)
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>V2_SWARM Progress Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #7f8c8d; }}
        .metric {{ background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .blocker {{ background: #e74c3c; color: white; padding: 10px; margin: 5px 0; border-radius: 5px; }}
        .risk {{ background: #f39c12; color: white; padding: 10px; margin: 5px 0; border-radius: 5px; }}
        .success {{ background: #27ae60; color: white; padding: 10px; margin: 5px 0; border-radius: 5px; }}
        code {{ background: #f8f9fa; padding: 2px 5px; border-radius: 3px; }}
        pre {{ background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="container">
        {markdown_content.replace(chr(10), '<br>').replace('**', '<strong>').replace('**', '</strong>')}
    </div>
</body>
</html>"""
        
        return html

    def generate_json_report(self) -> str:
        """Generate JSON report for programmatic consumption."""
        self.scan_devlogs()
        
        data = {
            "report_metadata": {
                "generated": datetime.now().isoformat(),
                "total_cycles": 70,
                "report_type": "comprehensive_progress_report"
            },
            "overall_progress": self.get_overall_progress(),
            "phase_progress": self.get_phase_progress(),
            "agent_progress": self.get_agent_progress(),
            "blockers_and_risks": self.get_blockers_and_risks(),
            "completed_cycles": self.cycles,
        }
        
        return json.dumps(data, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive progress reports")
    parser.add_argument("--format", choices=["markdown", "html", "json"], default="markdown",
                       help="Output format")
    parser.add_argument("--devlogs", default="devlogs", help="Devlogs directory path")
    parser.add_argument("--output", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    generator = ProgressReportGenerator(args.devlogs)
    
    if args.format == "markdown":
        output = generator.generate_markdown_report()
    elif args.format == "html":
        output = generator.generate_html_report()
    elif args.format == "json":
        output = generator.generate_json_report()
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Progress report saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()

