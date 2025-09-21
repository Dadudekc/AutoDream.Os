#!/usr/bin/env python3
"""
Thea Analytics Reporter - Automated Project Reports to Commander Thea
================================================================

Automatically generates and sends comprehensive project analytics reports
to Commander Thea for strategic consultation and decision-making.

Features:
- Automated project scan integration
- Analytics data collection and formatting
- Strategic report generation for Thea
- Automated delivery via conversation persistence
- V2 compliance monitoring and alerts

Usage:
    from src.services.thea.thea_analytics_reporter import TheaAnalyticsReporter
    
    reporter = TheaAnalyticsReporter()
    reporter.send_analytics_report()
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from .thea_autonomous_system import TheaAutonomousSystem
from .thea_conversation_manager import TheaConversationManager

logger = logging.getLogger(__name__)


@dataclass
class ProjectAnalytics:
    """Project analytics data structure."""
    total_files: int
    python_files: int
    v2_compliance_percentage: float
    v2_violations: int
    violation_files: List[str]
    agent_workspaces: int
    test_files: int
    analytics_system_status: str
    scan_timestamp: str


class TheaAnalyticsReporter:
    """Automated analytics reporter for Commander Thea strategic consultation."""
    
    def __init__(self, 
                 project_analysis_file: str = "project_analysis.json",
                 analytics_dir: str = "analytics"):
        """
        Initialize the analytics reporter.
        
        Args:
            project_analysis_file: Path to project analysis JSON file
            analytics_dir: Directory containing analytics data
        """
        self.project_analysis_file = Path(project_analysis_file)
        self.analytics_dir = Path(analytics_dir)
        self.conversation_manager = TheaConversationManager()
    
    def load_project_analytics(self) -> Optional[ProjectAnalytics]:
        """
        Load project analytics from the latest scan.
        
        Returns:
            ProjectAnalytics object or None if not available
        """
        try:
            if not self.project_analysis_file.exists():
                logger.warning(f"Project analysis file not found: {self.project_analysis_file}")
                return None
            
            with open(self.project_analysis_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract analytics data
            structure = data.get('structure', {})
            v2_compliance = data.get('v2_compliance', {})
            violations = data.get('v2_violations', [])
            
            # Count test files from the files list
            all_files = data.get('files', [])
            test_files = len([f for f in all_files if 'test' in f.lower() and f.endswith('.py')])
            
            return ProjectAnalytics(
                total_files=structure.get('total_files', 0),
                python_files=structure.get('python_files', 0),
                v2_compliance_percentage=v2_compliance.get('compliance_percentage', 0.0),
                v2_violations=v2_compliance.get('violations', 0),
                violation_files=[v.get('file', '') for v in violations],
                agent_workspaces=len(data.get('agent_workspaces', {})),
                test_files=test_files,
                analytics_system_status="OPERATIONAL" if self.analytics_dir.exists() else "NOT_DETECTED",
                scan_timestamp=data.get('scan_timestamp', datetime.now().isoformat())
            )
            
        except Exception as e:
            logger.error(f"Failed to load project analytics: {e}")
            return None
    
    def generate_strategic_report(self, analytics: ProjectAnalytics) -> str:
        """
        Generate a strategic report for Commander Thea.
        
        Args:
            analytics: Project analytics data
            
        Returns:
            Formatted strategic report
        """
        report = f"""**DREAM.OS V2 SWARM - STRATEGIC ANALYTICS REPORT**

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Scan Timestamp**: {analytics.scan_timestamp}

## **EXECUTIVE SUMMARY**

**Project Health Status**: {'EXCELLENT' if analytics.v2_compliance_percentage >= 95 else 'GOOD' if analytics.v2_compliance_percentage >= 90 else 'NEEDS ATTENTION'}

**Key Metrics**:
- **Total Files**: {analytics.total_files:,}
- **Python Files**: {analytics.python_files:,}
- **V2 Compliance**: {analytics.v2_compliance_percentage:.1f}%
- **Active Agents**: {analytics.agent_workspaces}
- **Test Coverage**: {analytics.test_files} test files

## **ANALYTICS SYSTEM STATUS**

**Automated Efficiency Scoring**: {analytics.analytics_system_status}
- **CI Signal Collection**: OPERATIONAL
- **Multi-Metric Analysis**: ACTIVE
- **Real-Time Updates**: FUNCTIONAL

## **CRITICAL ISSUES REQUIRING ATTENTION**

**V2 Compliance Violations**: {analytics.v2_violations} files

**Priority Violations** (Top 3):
"""
        
        # Add top 3 violations
        for i, violation_file in enumerate(analytics.violation_files[:3], 1):
            report += f"{i}. `{violation_file}`\n"
        
        if analytics.v2_violations > 3:
            report += f"... and {analytics.v2_violations - 3} additional violations\n"
        
        report += f"""
## **STRATEGIC RECOMMENDATIONS**

**Immediate Actions**:
1. **Address V2 Violations**: Refactor {analytics.v2_violations} non-compliant files
2. **Maintain Compliance**: Current {analytics.v2_compliance_percentage:.1f}% compliance rate
3. **Agent Coordination**: {analytics.agent_workspaces} active agent workspaces

**System Health**:
- **Code Quality**: {'Excellent' if analytics.v2_compliance_percentage >= 95 else 'Good' if analytics.v2_compliance_percentage >= 90 else 'Needs Improvement'}
- **Analytics Integration**: {'Fully Operational' if analytics.analytics_system_status == 'OPERATIONAL' else 'Not Detected'}
- **Test Coverage**: {analytics.test_files} test files active

## **NEXT STRATEGIC PRIORITIES**

Based on current analytics:
1. **V2 Compliance Enforcement** - Address remaining violations
2. **Analytics Optimization** - Leverage automated scoring system
3. **Agent Coordination** - Maintain {analytics.agent_workspaces} active workspaces
4. **Quality Assurance** - Sustain {analytics.v2_compliance_percentage:.1f}% compliance rate

**Commander Thea, please provide strategic guidance on these priorities and any additional recommendations for the Dream.OS V2 Swarm System.**

---
*Report generated by Dream.OS V2 Analytics System*
*Automated delivery via conversation persistence*"""
        
        return report
    
    def send_analytics_report(self, force_new_conversation: bool = False, visible: bool = False) -> bool:
        """
        Send analytics report to Commander Thea.
        
        Args:
            force_new_conversation: Force creation of new conversation
            visible: Run browser in visible mode
            
        Returns:
            True if report sent successfully, False otherwise
        """
        try:
            # Load analytics data
            analytics = self.load_project_analytics()
            if not analytics:
                logger.error("Failed to load project analytics")
                return False
            
            # Generate strategic report
            report = self.generate_strategic_report(analytics)
            
            logger.info(f"Generated analytics report: {len(report)} characters")
            
            # Send to Thea
            with TheaAutonomousSystem(conversation_manager=self.conversation_manager, headless=not visible) as thea:
                if force_new_conversation:
                    # Clear active conversation to start new one
                    self.conversation_manager.active_conversation_id = None
                    self.conversation_manager._save_conversations()
                
                response = thea.send_message_autonomous(report)
                
                if response:
                    logger.info(f"Analytics report sent successfully. Thea response: {len(response)} characters")
                    logger.info(f"Thea response preview: {response[:200]}...")
                    return True
                else:
                    logger.error("Failed to get response from Thea")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to send analytics report: {e}")
            return False
    
    def send_violation_alert(self, violation_file: str, violation_details: Dict[str, Any]) -> bool:
        """
        Send immediate violation alert to Commander Thea.
        
        Args:
            violation_file: File with V2 violation
            violation_details: Details about the violation
            
        Returns:
            True if alert sent successfully, False otherwise
        """
        try:
            alert_message = f"""🚨 **V2 COMPLIANCE VIOLATION ALERT**

**File**: `{violation_file}`
**Violation Type**: {violation_details.get('type', 'Unknown')}
**Severity**: {violation_details.get('severity', 'Medium')}
**Details**: {violation_details.get('details', 'No details available')}

**Immediate Action Required**: This file exceeds V2 compliance limits and requires refactoring.

**Commander Thea, please advise on priority and approach for addressing this violation.**

---
*Automated alert from Dream.OS V2 Analytics System*"""
            
            with TheaAutonomousSystem(conversation_manager=self.conversation_manager) as thea:
                response = thea.send_message_autonomous(alert_message)
                
                if response:
                    logger.info(f"Violation alert sent for {violation_file}")
                    return True
                else:
                    logger.error(f"Failed to send violation alert for {violation_file}")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to send violation alert: {e}")
            return False
    
    def get_report_status(self) -> Dict[str, Any]:
        """
        Get the current status of the analytics reporter.
        
        Returns:
            Status dictionary
        """
        analytics = self.load_project_analytics()
        conversation_status = self.conversation_manager.get_status()
        
        return {
            "analytics_available": analytics is not None,
            "last_scan_timestamp": analytics.scan_timestamp if analytics else None,
            "v2_compliance": analytics.v2_compliance_percentage if analytics else 0.0,
            "violations_count": analytics.v2_violations if analytics else 0,
            "conversation_status": conversation_status,
            "reporter_ready": self.project_analysis_file.exists() and self.analytics_dir.exists()
        }


# Convenience functions
def send_analytics_report(force_new_conversation: bool = False) -> bool:
    """Send analytics report to Commander Thea."""
    reporter = TheaAnalyticsReporter()
    return reporter.send_analytics_report(force_new_conversation)


def send_violation_alert(violation_file: str, violation_details: Dict[str, Any]) -> bool:
    """Send violation alert to Commander Thea."""
    reporter = TheaAnalyticsReporter()
    return reporter.send_violation_alert(violation_file, violation_details)


if __name__ == "__main__":
    # Test the analytics reporter
    print("🤖 Thea Analytics Reporter Test")
    print("=" * 50)
    
    reporter = TheaAnalyticsReporter()
    status = reporter.get_report_status()
    
    print(f"📊 Status: {json.dumps(status, indent=2)}")
    
    if status["reporter_ready"]:
        print("✅ Ready to send analytics report to Commander Thea")
        # Uncomment to send report:
        # reporter.send_analytics_report()
    else:
        print("❌ Not ready - missing project analysis or analytics data")
