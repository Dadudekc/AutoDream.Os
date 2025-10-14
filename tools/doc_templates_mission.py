#!/usr/bin/env python3
"""
Documentation Templates - Mission Documentation
================================================

Mission tracking and completion report templates.
Extracted from documentation_assistant.py for V2 compliance.

Author: Agent-8 (original), Agent-6 (refactor)
Created: 2025-10-14
License: MIT
"""

from datetime import datetime
from pathlib import Path


def create_mission_tracking_template(mission_name: str) -> str:
    """Generate mission tracking document template."""
    return f"""# {mission_name} Mission Tracking
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


def create_completion_report_template(mission_name: str) -> str:
    """Generate mission completion report template."""
    return f"""# {mission_name} Completion Report
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


__all__ = ["create_mission_tracking_template", "create_completion_report_template"]

