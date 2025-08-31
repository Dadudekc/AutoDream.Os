#!/usr/bin/env python3
"""
Side Mission Tracker
Tracks and manages multiple side missions for V2 compliance
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class SideMissionTracker:
    def __init__(self):
        self.missions_file = "reports/side_missions_tracker.json"
        self.missions = {
            'active_missions': [],
            'completed_missions': [],
            'failed_missions': [],
            'total_missions': 0,
            'success_rate': 0.0
        }
    
    def add_mission(self, mission_id: str, description: str, priority: str = "MEDIUM") -> bool:
        """Add a new side mission"""
        mission = {
            'id': mission_id,
            'description': description,
            'priority': priority,
            'status': 'ACTIVE',
            'created_at': datetime.now().isoformat(),
            'completed_at': None,
            'progress': 0.0
        }
        
        self.missions['active_missions'].append(mission)
        self.missions['total_missions'] += 1
        self.save_missions()
        
        print(f"✅ Added mission: {mission_id}")
        return True
    
    def complete_mission(self, mission_id: str, results: Dict[str, Any] = None) -> bool:
        """Mark a mission as completed"""
        for mission in self.missions['active_missions']:
            if mission['id'] == mission_id:
                mission['status'] = 'COMPLETED'
                mission['completed_at'] = datetime.now().isoformat()
                mission['progress'] = 100.0
                mission['results'] = results or {}
                
                self.missions['completed_missions'].append(mission)
                self.missions['active_missions'].remove(mission)
                
                self.update_success_rate()
                self.save_missions()
                
                print(f"🎉 Mission completed: {mission_id}")
                return True
        
        print(f"❌ Mission not found: {mission_id}")
        return False
    
    def update_success_rate(self):
        """Update mission success rate"""
        total_completed = len(self.missions['completed_missions'])
        total_failed = len(self.missions['failed_missions'])
        total = total_completed + total_failed
        
        if total > 0:
            self.missions['success_rate'] = (total_completed / total) * 100
    
    def save_missions(self):
        """Save missions to file"""
        os.makedirs("reports", exist_ok=True)
        with open(self.missions_file, 'w', encoding='utf-8') as f:
            json.dump(self.missions, f, indent=2)
    
    def load_missions(self):
        """Load missions from file"""
        if os.path.exists(self.missions_file):
            with open(self.missions_file, 'r', encoding='utf-8') as f:
                self.missions = json.load(f)
    
    def generate_report(self) -> str:
        """Generate side mission report"""
        report = f"""# Side Mission Tracker Report

## 📊 **MISSION SUMMARY**

**Generated:** {datetime.now()}
**Total Missions:** {self.missions['total_missions']}
**Active Missions:** {len(self.missions['active_missions'])}
**Completed Missions:** {len(self.missions['completed_missions'])}
**Success Rate:** {self.missions['success_rate']:.1f}%

## 🎯 **ACTIVE MISSIONS**

"""
        
        for mission in self.missions['active_missions']:
            report += f"- **{mission['id']}**: {mission['description']} ({mission['priority']})
"
            report += f"  - Progress: {mission['progress']:.1f}%
"
        
        report += "
## ✅ **COMPLETED MISSIONS**
"
        
        for mission in self.missions['completed_missions']:
            report += f"- **{mission['id']}**: {mission['description']}
"
            report += f"  - Completed: {mission['completed_at']}
"
        
        return report

def main():
    """Main tracker function"""
    tracker = SideMissionTracker()
    tracker.load_missions()
    
    # Add some example missions
    tracker.add_mission("CLEANUP-001", "Remove duplicate directories", "HIGH")
    tracker.add_mission("CLEANUP-002", "Clean temporary files", "MEDIUM")
    tracker.add_mission("CLEANUP-003", "Update import statements", "HIGH")
    tracker.add_mission("MONITOR-001", "Create V2 compliance monitor", "HIGH")
    
    # Generate report
    report = tracker.generate_report()
    print(report)
    
    # Save report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = f"reports/SIDE_MISSIONS_REPORT_{timestamp}.md"
    
    os.makedirs("reports", exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📋 Side mission report saved: {report_path}")

if __name__ == "__main__":
    main()
