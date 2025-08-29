#!/usr/bin/env python3
"""Emergency Documentation Module - Extracted from emergency_response_system.py
Agent-3: Monolithic File Modularization Contract

This module handles emergency documentation, reporting, and history tracking.
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from .emergency_types import EmergencyEvent, EmergencyType, EmergencyLevel
from .utils import load_template, ensure_directory

logger = logging.getLogger(__name__)


class EmergencyDocumentation:
    """Handles emergency documentation and reporting"""

    def __init__(self, reports_dir: str = "reports/emergency"):
        """Initialize emergency documentation"""
        self.reports_dir = Path(reports_dir)
        ensure_directory(self.reports_dir)
        self.documentation_history: List[Dict[str, Any]] = []
        self.report_templates = self._load_report_templates()

    def _load_report_templates(self) -> Dict[str, str]:
        """Load report templates from disk."""
        return {
            "incident_report": load_template("incident_report"),
            "recovery_log": load_template("recovery_log"),
            "lessons_learned": load_template("lessons_learned"),
            "summary_report": load_template("summary_report"),
        }

    def generate_emergency_documentation(
        self,
        emergency: EmergencyEvent,
        response_data: Dict[str, Any],
        recovery_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, str]:
        """Generate comprehensive emergency documentation"""
        try:
            logger.info(f"Generating documentation for emergency: {emergency.id}")

            generated_files = {}

            # Generate incident report
            incident_report = self._generate_incident_report(emergency, response_data)
            incident_file = self._save_incident_report(emergency.id, incident_report)
            if incident_file:
                generated_files["incident_report"] = incident_file

            # Generate recovery log if recovery data available
            if recovery_data:
                recovery_log = self._generate_recovery_log(emergency, recovery_data)
                recovery_file = self._save_recovery_log(emergency.id, recovery_log)
                if recovery_file:
                    generated_files["recovery_log"] = recovery_file

            # Generate lessons learned
            lessons_learned = self._generate_lessons_learned(
                emergency, response_data, recovery_data
            )
            lessons_file = self._save_lessons_learned(emergency.id, lessons_learned)
            if lessons_file:
                generated_files["lessons_learned"] = lessons_file

            # Generate summary report
            summary_report = self._generate_summary_report(emergency, generated_files)
            summary_file = self._save_summary_report(emergency.id, summary_report)
            if summary_file:
                generated_files["summary_report"] = summary_file

            # Record documentation generation
            self.documentation_history.append(
                {
                    "emergency_id": emergency.id,
                    "action": "documentation_generated",
                    "timestamp": datetime.now().isoformat(),
                    "files_generated": list(generated_files.keys()),
                    "file_paths": generated_files,
                }
            )

            logger.info(
                f"Documentation generated successfully: {len(generated_files)} files"
            )
            return generated_files

        except Exception as e:
            logger.error(f"Error generating emergency documentation: {e}")
            return {}

    def _generate_incident_report(
        self, emergency: EmergencyEvent, response_data: Dict[str, Any]
    ) -> str:
        """Generate incident report"""
        try:
            # Calculate duration
            duration = "Unknown"
            if emergency.resolution_time:
                duration = str(emergency.resolution_time - emergency.timestamp)

            # Format impact assessment
            impact_assessment = self._format_impact_assessment(
                emergency.impact_assessment
            )

            # Format response actions
            response_actions = self._format_response_actions(
                response_data.get("actions_taken", [])
            )

            # Format lessons learned
            lessons_learned = self._format_lessons_learned(emergency.lessons_learned)

            # Generate recommendations
            recommendations = self._generate_recommendations(emergency, response_data)

            # Fill template
            report = self.report_templates["incident_report"].format(
                emergency_id=emergency.id,
                emergency_type=emergency.type.value,
                emergency_level=emergency.level.value,
                description=emergency.description,
                timestamp=emergency.timestamp.isoformat(),
                source=emergency.source,
                impact_assessment=impact_assessment,
                response_actions=response_actions,
                status=emergency.status,
                resolution_time=emergency.resolution_time.isoformat()
                if emergency.resolution_time
                else "Not resolved",
                duration=duration,
                lessons_learned=lessons_learned,
                recommendations=recommendations,
                generated_timestamp=datetime.now().isoformat(),
            )

            return report

        except Exception as e:
            logger.error(f"Error generating incident report: {e}")
            return f"Error generating incident report: {e}"

    def _generate_recovery_log(
        self, emergency: EmergencyEvent, recovery_data: Dict[str, Any]
    ) -> str:
        """Generate recovery log"""
        try:
            # Format recovery timeline
            recovery_timeline = self._format_recovery_timeline(recovery_data)

            # Format actions taken
            actions_taken = self._format_recovery_actions(
                recovery_data.get("completed_steps", [])
            )

            # Format resources used
            resources_used = self._format_resources_used(recovery_data)

            # Format validation results
            validation_results = self._format_validation_results(recovery_data)

            # Fill template
            report = self.report_templates["recovery_log"].format(
                emergency_id=emergency.id,
                emergency_type=emergency.type.value,
                emergency_level=emergency.level.value,
                recovery_timeline=recovery_timeline,
                actions_taken=actions_taken,
                resources_used=resources_used,
                success_rate=f"{recovery_data.get('success_rate', 0):.1f}%",
                total_duration=f"{recovery_data.get('duration', 0):.1f}s",
                steps_completed=len(recovery_data.get("completed_steps", [])),
                steps_failed=len(recovery_data.get("failed_steps", [])),
                validation_results=validation_results,
                generated_timestamp=datetime.now().isoformat(),
            )

            return report

        except Exception as e:
            logger.error(f"Error generating recovery log: {e}")
            return f"Error generating recovery log: {e}"

    def _generate_lessons_learned(
        self,
        emergency: EmergencyEvent,
        response_data: Dict[str, Any],
        recovery_data: Optional[Dict[str, Any]],
    ) -> str:
        """Generate lessons learned summary"""
        try:
            # Extract key learnings
            key_learnings = self._extract_key_learnings(
                emergency, response_data, recovery_data
            )

            # Identify what went well
            what_went_well = self._identify_successes(response_data, recovery_data)

            # Identify improvements
            what_could_improve = self._identify_improvements(
                response_data, recovery_data
            )

            # Generate action items
            action_items = self._generate_action_items(
                emergency, response_data, recovery_data
            )

            # Generate prevention strategies
            prevention_strategies = self._generate_prevention_strategies(emergency)

            # Fill template
            report = self.report_templates["lessons_learned"].format(
                emergency_id=emergency.id,
                emergency_type=emergency.type.value,
                date=emergency.timestamp.strftime("%Y-%m-%d"),
                key_learnings=key_learnings,
                what_went_well=what_went_well,
                what_could_improve=what_could_improve,
                action_items=action_items,
                prevention_strategies=prevention_strategies,
                generated_timestamp=datetime.now().isoformat(),
            )

            return report

        except Exception as e:
            logger.error(f"Error generating lessons learned: {e}")
            return f"Error generating lessons learned: {e}"

    def _generate_summary_report(
        self, emergency: EmergencyEvent, generated_files: Dict[str, str]
    ) -> str:
        """Generate summary report"""
        try:
            template = self.report_templates["summary_report"]
            summary = template.format(
                emergency_id=emergency.id,
                emergency_type=emergency.type.value,
                emergency_level=emergency.level.value,
                status=emergency.status,
                duration=emergency.resolution_time - emergency.timestamp
                if emergency.resolution_time
                else "Ongoing",
                generated_files=self._format_generated_files(generated_files),
                response_time=self._calculate_response_time(emergency),
                resolution_time=self._calculate_resolution_time(emergency),
                documentation_completeness=f"{len(generated_files)}/4 files",
                generated_timestamp=datetime.now().isoformat(),
            )

            return summary
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
            return f"Error generating summary report: {e}"

    # Helper methods for formatting
    def _format_impact_assessment(self, impact: Dict[str, Any]) -> str:
        """Format impact assessment for report"""
        if not impact:
            return "No impact assessment available"

        formatted = []
        for key, value in impact.items():
            formatted.append(f"- **{key}**: {value}")

        return "\n".join(formatted) if formatted else "No impact assessment available"

    def _format_response_actions(self, actions: List[str]) -> str:
        """Format response actions for report"""
        if not actions:
            return "No response actions recorded"

        formatted = []
        for i, action in enumerate(actions, 1):
            formatted.append(f"{i}. {action}")

        return "\n".join(formatted)

    def _format_lessons_learned(self, lessons: List[str]) -> str:
        """Format lessons learned for report"""
        if not lessons:
            return "No lessons learned recorded"

        formatted = []
        for i, lesson in enumerate(lessons, 1):
            formatted.append(f"{i}. {lesson}")

        return "\n".join(formatted)

    def _format_recovery_timeline(self, recovery_data: Dict[str, Any]) -> str:
        """Format recovery timeline for report"""
        if not recovery_data:
            return "No recovery timeline available"

        timeline = []
        if "start_time" in recovery_data:
            timeline.append(f"- **Start**: {recovery_data['start_time']}")
        if "completion_time" in recovery_data:
            timeline.append(f"- **Completion**: {recovery_data['completion_time']}")
        if "duration" in recovery_data:
            timeline.append(f"- **Duration**: {recovery_data['duration']:.1f} seconds")

        return "\n".join(timeline) if timeline else "No recovery timeline available"

    def _format_recovery_actions(self, actions: List[str]) -> str:
        """Format recovery actions for report"""
        if not actions:
            return "No recovery actions recorded"

        formatted = []
        for i, action in enumerate(actions, 1):
            formatted.append(f"{i}. {action}")

        return "\n".join(formatted)

    def _format_resources_used(self, recovery_data: Dict[str, Any]) -> str:
        """Format resources used for report"""
        return "Standard recovery procedures and system resources"

    def _format_validation_results(self, recovery_data: Dict[str, Any]) -> str:
        """Format validation results for report"""
        if not recovery_data:
            return "No validation results available"

        success_rate = recovery_data.get("success_rate", 0)
        if success_rate >= 80:
            return f"✅ Recovery successful (Success rate: {success_rate:.1f}%)"
        elif success_rate >= 60:
            return (
                f"⚠️ Recovery partially successful (Success rate: {success_rate:.1f}%)"
            )
        else:
            return f"❌ Recovery failed (Success rate: {success_rate:.1f}%)"

    def _extract_key_learnings(
        self,
        emergency: EmergencyEvent,
        response_data: Dict[str, Any],
        recovery_data: Optional[Dict[str, Any]],
    ) -> str:
        """Extract key learnings from emergency response"""
        learnings = []

        if emergency.lessons_learned:
            learnings.extend(emergency.lessons_learned)

        if recovery_data and recovery_data.get("lessons_learned"):
            learnings.extend(recovery_data["lessons_learned"])

        if not learnings:
            learnings.append("Emergency response completed successfully")
            learnings.append("Standard procedures were effective")

        return self._format_lessons_learned(learnings)

    def _identify_successes(
        self, response_data: Dict[str, Any], recovery_data: Optional[Dict[str, Any]]
    ) -> str:
        """Identify what went well during response"""
        successes = []

        if response_data.get("actions_taken"):
            successes.append("All planned response actions were executed")

        if recovery_data and recovery_data.get("success_rate", 0) >= 80:
            successes.append("Recovery procedures were highly effective")

        if not successes:
            successes.append("Emergency was identified and responded to promptly")

        return self._format_lessons_learned(successes)

    def _identify_improvements(
        self, response_data: Dict[str, Any], recovery_data: Optional[Dict[str, Any]]
    ) -> str:
        """Identify areas for improvement"""
        improvements = []

        if recovery_data and recovery_data.get("failed_steps"):
            improvements.append(
                f"Recovery step failures: {', '.join(recovery_data['failed_steps'])}"
            )

        if recovery_data and recovery_data.get("duration", 0) > 1800:
            improvements.append(
                "Recovery time exceeded 30 minutes - optimize procedures"
            )

        if not improvements:
            improvements.append(
                "Consider reducing response time for future emergencies"
            )
            improvements.append("Review and update emergency procedures regularly")

        return self._format_lessons_learned(improvements)

    def _generate_action_items(
        self,
        emergency: EmergencyEvent,
        response_data: Dict[str, Any],
        recovery_data: Optional[Dict[str, Any]],
    ) -> str:
        """Generate action items from emergency response"""
        actions = []

        actions.append("Review and update emergency response procedures")
        actions.append("Conduct post-incident review meeting")
        actions.append("Update emergency contact lists if needed")

        if recovery_data and recovery_data.get("failed_steps"):
            actions.append("Investigate and fix failed recovery procedures")

        if emergency.level in [EmergencyLevel.CRITICAL, EmergencyLevel.CODE_BLACK]:
            actions.append("Schedule emergency response team training")

        return self._format_lessons_learned(actions)

    def _generate_prevention_strategies(self, emergency: EmergencyEvent) -> str:
        """Generate prevention strategies"""
        strategies = []

        if emergency.type == EmergencyType.SYSTEM_FAILURE:
            strategies.append("Implement proactive system monitoring")
            strategies.append("Regular system health checks")

        if emergency.type == EmergencyType.WORKFLOW_STALL:
            strategies.append("Implement workflow timeout mechanisms")
            strategies.append("Add workflow progress monitoring")

        if emergency.type == EmergencyType.DATA_CORRUPTION:
            strategies.append("Regular data integrity checks")
            strategies.append("Implement data backup validation")

        if not strategies:
            strategies.append("Regular emergency response drills")
            strategies.append("Continuous improvement of procedures")

        return self._format_lessons_learned(strategies)

    def _format_generated_files(self, generated_files: Dict[str, str]) -> str:
        """Format generated files list for report"""
        if not generated_files:
            return "No documentation files generated"

        formatted = []
        for file_type, file_path in generated_files.items():
            formatted.append(
                f"- **{file_type.replace('_', ' ').title()}**: {file_path}"
            )

        return "\n".join(formatted)

    def _calculate_response_time(self, emergency: EmergencyEvent) -> str:
        """Calculate response time"""
        # This would typically calculate from emergency detection to first response
        return "Immediate"

    def _calculate_resolution_time(self, emergency: EmergencyEvent) -> str:
        """Calculate resolution time"""
        if emergency.resolution_time:
            duration = emergency.resolution_time - emergency.timestamp
            return f"{duration.total_seconds():.1f} seconds"
        return "Not resolved"

    # File saving methods
    def _save_incident_report(self, emergency_id: str, content: str) -> Optional[str]:
        """Save incident report to file"""
        try:
            filename = f"incident_report_{emergency_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            filepath = self.reports_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info(f"Incident report saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error saving incident report: {e}")
            return None

    def _save_recovery_log(self, emergency_id: str, content: str) -> Optional[str]:
        """Save recovery log to file"""
        try:
            filename = f"recovery_log_{emergency_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            filepath = self.reports_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info(f"Recovery log saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error saving recovery log: {e}")
            return None

    def _save_lessons_learned(self, emergency_id: str, content: str) -> Optional[str]:
        """Save lessons learned to file"""
        try:
            filename = f"lessons_learned_{emergency_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            filepath = self.reports_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info(f"Lessons learned saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error saving lessons learned: {e}")
            return None

    def _save_summary_report(self, emergency_id: str, content: str) -> Optional[str]:
        """Save summary report to file"""
        try:
            filename = f"summary_report_{emergency_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            filepath = self.reports_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info(f"Summary report saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error saving summary report: {e}")
            return None

    def save_emergency_report(self, report: Dict[str, Any]) -> bool:
        """Save emergency report data"""
        try:
            filename = (
                f"emergency_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            filepath = self.reports_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            logger.info(f"Emergency report saved: {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error saving emergency report: {e}")
            return False

    def get_emergency_history(self) -> List[Dict[str, Any]]:
        """Get emergency history from documentation"""
        try:
            history = []

            # Scan reports directory for emergency files
            for filepath in self.reports_dir.glob("*.json"):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        history.append(data)
                except Exception as e:
                    logger.warning(f"Error reading report file {filepath}: {e}")

            # Sort by timestamp
            history.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

            return history

        except Exception as e:
            logger.error(f"Error getting emergency history: {e}")
            return []

    def get_documentation_status(self) -> Dict[str, Any]:
        """Get documentation status"""
        return {
            "reports_directory": str(self.reports_dir),
            "total_files": len(list(self.reports_dir.glob("*"))),
            "documentation_history_count": len(self.documentation_history),
            "last_generated": self.documentation_history[-1]["timestamp"]
            if self.documentation_history
            else None,
        }
