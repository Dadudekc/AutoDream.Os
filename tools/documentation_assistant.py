#!/usr/bin/env python3
"""
Documentation Assistant Tool
============================

The tool I wished I had this session!

Automates common documentation tasks:
- Generate mission tracking docs from templates
- Create completion reports with consistent structure
- Generate milestone documentation for agent achievements
- Create enhancement request docs with standard format
- Quick status snapshots

Author: Agent-8 (Documentation Specialist)
Created: 2025-10-11 (During C-055-8 session cleanup)
Purpose: Make documentation faster and more consistent

Usage:
    python tools/documentation_assistant.py mission start --name C-057
    python tools/documentation_assistant.py mission complete --name C-057
    python tools/documentation_assistant.py milestone --agent Agent-7 --achievement "100% V2"
    python tools/documentation_assistant.py enhancement --name "Message Batching" --priority HIGH
    python tools/documentation_assistant.py status-snapshot

V2 Compliance: <400 lines, focused tool
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class DocumentationAssistant:
    """Helper tool for generating consistent documentation."""

    def __init__(self):
        """Initialize documentation assistant."""
        self.templates_dir = Path("docs/templates")
        self.missions_dir = Path("docs/missions")
        self.milestones_dir = Path("docs/milestones")
        self.enhancements_dir = Path("docs/enhancement_requests")

        # Ensure directories exist
        self.missions_dir.mkdir(parents=True, exist_ok=True)
        self.milestones_dir.mkdir(parents=True, exist_ok=True)
        self.enhancements_dir.mkdir(parents=True, exist_ok=True)

    def create_mission_doc(self, mission_name: str) -> Path:
        """Create initial mission tracking document."""
        doc_path = self.missions_dir / f"{mission_name}_TRACKING.md"

        content = f"""# {mission_name} Mission Tracking
## Real-Time Mission Documentation

**Mission:** {mission_name}  
**Start Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Status:** 🔄 IN PROGRESS

---

## 📋 Mission Objectives

### Primary Objectives
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## 👥 Agent Assignments

**Assigned Agents:**
- Agent-X: Role description
- Agent-Y: Role description

---

## 📊 Progress Updates

### {datetime.now().strftime('%Y-%m-%d %H:%M')} - Mission Start
- Mission initiated
- Agent assignments confirmed
- Initial coordination complete

---

## 🏆 Achievements

(Track achievements as they happen)

---

## 🚨 Blockers

(Track blockers in real-time)

---

## 📝 Next Steps

1. Step 1
2. Step 2
3. Step 3

---

*Created by: Documentation Assistant*  
*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

🐝 **WE. ARE. SWARM.** ⚡🔥
"""

        doc_path.write_text(content)
        print(f"✅ Created mission tracking doc: {doc_path}")
        return doc_path

    def create_completion_report(self, mission_name: str) -> Path:
        """Create mission completion report."""
        doc_path = self.missions_dir / f"{mission_name}_COMPLETION_REPORT.md"

        content = f"""# {mission_name} Completion Report
## Mission Summary & Results

**Mission:** {mission_name}  
**Completion Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Status:** ✅ COMPLETE

---

## 🎯 Mission Summary

**Objective:** [Mission objective]  
**Result:** [Mission result]  
**Impact:** [Impact achieved]

---

## ✅ Deliverables

### Primary Deliverables
1. ✅ Deliverable 1
2. ✅ Deliverable 2
3. ✅ Deliverable 3

### Bonus Achievements
- Achievement 1
- Achievement 2

---

## 👥 Agent Contributions

### Agent-X
- Contribution 1
- Contribution 2
- Points Earned: XX

### Agent-Y
- Contribution 1
- Contribution 2
- Points Earned: XX

---

## 📊 Success Metrics

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Metric 1 | Target 1 | Result 1 | ✅ |
| Metric 2 | Target 2 | Result 2 | ✅ |

---

## 💎 Key Learnings

### Success Factors
1. Factor 1
2. Factor 2

### Challenges Overcome
1. Challenge 1
2. Challenge 2

### Recommendations
1. Recommendation 1
2. Recommendation 2

---

## 🚀 Impact

**Immediate Impact:**
- Impact 1
- Impact 2

**Long-Term Impact:**
- Impact 1
- Impact 2

---

**Status:** ✅ MISSION COMPLETE  
**Quality:** 🏆 [Rating]  
**Next:** [Next steps]

---

*Compiled by: Documentation Assistant*  
*Date: {datetime.now().strftime('%Y-%m-%d')}*

🐝 **WE. ARE. SWARM.** ⚡🔥
"""

        doc_path.write_text(content)
        print(f"✅ Created completion report: {doc_path}")
        return doc_path

    def create_milestone_doc(self, agent_id: str, achievement: str) -> Path:
        """Create agent milestone documentation."""
        safe_achievement = achievement.lower().replace(" ", "_")
        doc_path = self.milestones_dir / f"{agent_id}_{safe_achievement}.md"

        content = f"""# 🏆 {agent_id} Milestone: {achievement}
## Achievement Documentation

**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Agent:** {agent_id}  
**Achievement:** {achievement}  
**Status:** ✅ ACHIEVED

---

## 🎯 Achievement Summary

**What Was Achieved:**
[Description of achievement]

**Why This Matters:**
[Significance and impact]

---

## 📊 Achievement Details

### Metrics
- Metric 1: Value
- Metric 2: Value
- Metric 3: Value

### Deliverables
1. Deliverable 1
2. Deliverable 2
3. Deliverable 3

---

## 🏆 Recognition

**{agent_id} demonstrates:**
- Quality 1
- Quality 2
- Quality 3

**Impact:**
- Impact 1
- Impact 2

---

## 💎 Lessons Learned

### Success Factors
1. Factor 1
2. Factor 2

### For Other Agents
- Lesson 1
- Lesson 2

---

## 🐝 Swarm Impact

**This achievement:**
- Inspires other agents
- Raises swarm standards
- Demonstrates what's possible

---

**Achievement:** 🏆 LEGENDARY  
**Agent:** {agent_id}  
**Impact:** SIGNIFICANT

---

*Documented by: Documentation Assistant*  
*Date: {datetime.now().strftime('%Y-%m-%d')}*

🐝 **WE. ARE. SWARM.** ⚡🔥
"""

        doc_path.write_text(content)
        print(f"✅ Created milestone doc: {doc_path}")
        return doc_path

    def create_enhancement_request(self, name: str, priority: str = "MEDIUM") -> Path:
        """Create enhancement request document."""
        safe_name = name.upper().replace(" ", "_")
        doc_path = self.enhancements_dir / f"{safe_name}.md"

        content = f"""# Enhancement Request: {name}
## System Improvement Proposal

**Request ID:** ENH-XXX  
**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Requested By:** [Agent/Team]  
**Priority:** {priority}  
**Status:** 📝 PROPOSED

---

## 🎯 Problem Statement

**Current Issue:**
[Description of current pain point]

**Example Scenario:**
[Concrete example of the problem]

---

## 💡 Proposed Solution

**High-Level Approach:**
[Overview of proposed solution]

**Key Features:**
1. Feature 1
2. Feature 2
3. Feature 3

---

## 🔧 Technical Design

### Implementation Details
```
[Technical specifications]
```

### Requirements
- Requirement 1
- Requirement 2

---

## 💪 Benefits

### For Users
- Benefit 1
- Benefit 2

### For System
- Benefit 1
- Benefit 2

---

## ⚠️ Considerations

### Potential Issues
1. Issue 1
2. Issue 2

### Backward Compatibility
[Compatibility considerations]

---

## 🚀 Implementation Plan

### Phase 1: Core (X cycles)
- [ ] Task 1
- [ ] Task 2

### Phase 2: Enhanced (X cycles)
- [ ] Task 1
- [ ] Task 2

**Estimated Total:** X cycles

---

## 📊 Success Metrics

**Target Improvements:**
- Metric 1: Target
- Metric 2: Target

---

**Status:** 📝 Proposed  
**Priority:** {priority}  
**Next:** Review and prioritization

---

*Enhancement request by: Documentation Assistant*  
*Date: {datetime.now().strftime('%Y-%m-%d')}*

🐝 **WE. ARE. SWARM.** ⚡🔥
"""

        doc_path.write_text(content)
        print(f"✅ Created enhancement request: {doc_path}")
        return doc_path

    def create_status_snapshot(self) -> dict[str, Any]:
        """Generate quick status snapshot."""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "swarm_status": {
                "active_agents": self._count_active_agents(),
                "recent_missions": self._list_recent_missions(),
                "recent_milestones": self._list_recent_milestones(),
            },
            "documentation_health": {
                "missions_tracked": len(list(self.missions_dir.glob("*_TRACKING.md"))),
                "completed_missions": len(list(self.missions_dir.glob("*_COMPLETION*.md"))),
                "milestones_documented": len(list(self.milestones_dir.glob("*.md"))),
                "enhancements_proposed": len(list(self.enhancements_dir.glob("*.md"))),
            },
        }

        print(json.dumps(snapshot, indent=2))
        return snapshot

    def _count_active_agents(self) -> int:
        """Count active agents based on recent activity."""
        workspaces = Path("agent_workspaces")
        if not workspaces.exists():
            return 0
        return len([d for d in workspaces.iterdir() if d.is_dir() and d.name.startswith("Agent-")])

    def _list_recent_missions(self, limit: int = 5) -> list:
        """List recent mission docs."""
        missions = sorted(
            self.missions_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True
        )
        return [m.stem for m in missions[:limit]]

    def _list_recent_milestones(self, limit: int = 5) -> list:
        """List recent milestone docs."""
        milestones = sorted(
            self.milestones_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True
        )
        return [m.stem for m in milestones[:limit]]


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Documentation Assistant - Automate common documentation tasks"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Mission subcommand
    mission_parser = subparsers.add_parser("mission", help="Mission documentation")
    mission_sub = mission_parser.add_subparsers(dest="action")

    start_p = mission_sub.add_parser("start", help="Create mission tracking doc")
    start_p.add_argument("--name", required=True, help="Mission name (e.g., C-057)")

    complete_p = mission_sub.add_parser("complete", help="Create completion report")
    complete_p.add_argument("--name", required=True, help="Mission name")

    # Milestone subcommand
    milestone_parser = subparsers.add_parser("milestone", help="Milestone documentation")
    milestone_parser.add_argument("--agent", required=True, help="Agent ID")
    milestone_parser.add_argument("--achievement", required=True, help="Achievement description")

    # Enhancement subcommand
    enhance_parser = subparsers.add_parser("enhancement", help="Enhancement request")
    enhance_parser.add_argument("--name", required=True, help="Enhancement name")
    enhance_parser.add_argument(
        "--priority", choices=["LOW", "MEDIUM", "HIGH"], default="MEDIUM", help="Priority level"
    )

    # Status snapshot
    subparsers.add_parser("status-snapshot", help="Generate status snapshot")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    assistant = DocumentationAssistant()

    try:
        if args.command == "mission":
            if args.action == "start":
                assistant.create_mission_doc(args.name)
            elif args.action == "complete":
                assistant.create_completion_report(args.name)

        elif args.command == "milestone":
            assistant.create_milestone_doc(args.agent, args.achievement)

        elif args.command == "enhancement":
            assistant.create_enhancement_request(args.name, args.priority)

        elif args.command == "status-snapshot":
            assistant.create_status_snapshot()

        print("\n🐝 WE. ARE. SWARM. ⚡🔥")
        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
