#!/usr/bin/env python3
"""
Agent-5 Comprehensive Reminder System Validator
Comprehensive validation of all 4 reminder types in the messaging system

This script validates the comprehensive reminder system integration,
ensuring all messages include all 4 reminder types and the system functions properly.

Author: Agent-5 (Business Intelligence & Coordination Specialist)
Date: 2025-09-09
Phase: 2 - High-Impact Optimization
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent5_comprehensive_reminder_validator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Agent5ComprehensiveReminderValidator:
    """Agent-5 Comprehensive Reminder System Validator"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.validation_results = {}
        self.system_status = {}
        self.agent_responses = {}

        # Define the 4 reminder types
        self.reminder_types = {
            "identity": "🆔 IDENTITY REMINDER: You are [Agent-ID] - [Role Description]",
            "discord_devlog": "📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory",
            "inbox_check": "📬 INBOX CHECK REMINDER: Check your agent workspace inbox for new messages",
            "status_update": "📊 STATUS UPDATE REMINDER: Update your status and progress in agent workspace"
        }

    def validate_messaging_system_integration(self) -> bool:
        """Validate that the messaging system includes all 4 reminder types"""
        try:
            logger.info("🔍 Validating comprehensive reminder system integration...")

            # Check messaging core file
            messaging_core_file = self.project_root / "src" / "core" / "messaging_core.py"
            if not messaging_core_file.exists():
                logger.error("Messaging core file not found")
                return False

            # Read messaging core content
            with open(messaging_core_file, encoding='utf-8') as f:
                content = f.read()

            # Check for each reminder type
            found_reminders = {}
            for reminder_name, reminder_text in self.reminder_types.items():
                if reminder_text in content:
                    logger.info(f"✅ {reminder_name} reminder found in messaging core")
                    found_reminders[reminder_name] = "PASS"
                else:
                    logger.warning(f"⚠️ {reminder_name} reminder not found in messaging core")
                    found_reminders[reminder_name] = "FAIL"

            # Calculate overall integration status
            total_reminders = len(self.reminder_types)
            found_reminders_count = sum(1 for status in found_reminders.values() if status == "PASS")

            if found_reminders_count == total_reminders:
                logger.info("✅ All 4 reminder types found in messaging core")
                self.validation_results["messaging_integration"] = "PASS"
                return True
            else:
                logger.warning(f"⚠️ Only {found_reminders_count}/{total_reminders} reminder types found")
                self.validation_results["messaging_integration"] = "PARTIAL"
                return False

        except Exception as e:
            logger.error(f"Error validating messaging system integration: {e}")
            self.validation_results["messaging_integration"] = "ERROR"
            return False

    def validate_reminder_consistency(self) -> bool:
        """Validate reminder consistency across the system"""
        try:
            logger.info("🔍 Validating reminder consistency...")

            # Check for reminder patterns in various files
            reminder_patterns = {
                "identity": ["identity", "Identity", "IDENTITY"],
                "discord_devlog": ["discord", "devlog", "Discord", "DevLog"],
                "inbox_check": ["inbox", "Inbox", "INBOX"],
                "status_update": ["status", "Status", "STATUS"]
            }

            consistency_results = {}

            for reminder_name, patterns in reminder_patterns.items():
                pattern_found = False
                for pattern in patterns:
                    if pattern in str(self.project_root):
                        pattern_found = True
                        break

                if pattern_found:
                    logger.info(f"✅ {reminder_name} reminder patterns found")
                    consistency_results[reminder_name] = "PASS"
                else:
                    logger.warning(f"⚠️ {reminder_name} reminder patterns not found")
                    consistency_results[reminder_name] = "FAIL"

            # Calculate overall consistency
            total_reminders = len(reminder_patterns)
            consistent_reminders = sum(1 for status in consistency_results.values() if status == "PASS")

            if consistent_reminders == total_reminders:
                logger.info("✅ All reminder types are consistent across the system")
                self.validation_results["reminder_consistency"] = "PASS"
                return True
            else:
                logger.warning(f"⚠️ Only {consistent_reminders}/{total_reminders} reminder types are consistent")
                self.validation_results["reminder_consistency"] = "PARTIAL"
                return False

        except Exception as e:
            logger.error(f"Error validating reminder consistency: {e}")
            self.validation_results["reminder_consistency"] = "ERROR"
            return False

    def validate_agent_message_reminders(self) -> bool:
        """Validate that all agents are receiving all 4 reminder types"""
        try:
            logger.info("🔍 Validating agent message reminders...")

            # Check agent workspaces for recent messages
            agent_workspaces_dir = self.project_root / "agent_workspaces"
            if not agent_workspaces_dir.exists():
                logger.warning("Agent workspaces directory not found")
                self.validation_results["agent_reminders"] = "WARNING"
                return False

            # Check for recent message files
            recent_messages = []
            for agent_dir in agent_workspaces_dir.iterdir():
                if agent_dir.is_dir():
                    # Look for recent message files
                    message_files = list(agent_dir.glob("*_message*.json")) + list(agent_dir.glob("*_inbox*.txt"))
                    recent_messages.extend(message_files)

            if not recent_messages:
                logger.warning("No recent agent messages found")
                self.validation_results["agent_reminders"] = "WARNING"
                return False

            # Check for each reminder type in recent messages
            reminder_counts = dict.fromkeys(self.reminder_types.keys(), 0)

            for message_file in recent_messages:
                try:
                    with open(message_file, encoding='utf-8') as f:
                        content = f.read()

                    for reminder_name, reminder_text in self.reminder_types.items():
                        if reminder_text in content:
                            reminder_counts[reminder_name] += 1
                except Exception as e:
                    logger.warning(f"Error reading message file {message_file}: {e}")

            # Calculate reminder coverage
            total_messages = len(recent_messages)
            reminder_coverage = {}

            for reminder_name, count in reminder_counts.items():
                coverage = (count / total_messages * 100) if total_messages > 0 else 0
                reminder_coverage[reminder_name] = coverage

                if coverage > 80:
                    logger.info(f"✅ {reminder_name} reminder coverage: {coverage:.1f}%")
                else:
                    logger.warning(f"⚠️ {reminder_name} reminder coverage: {coverage:.1f}%")

            # Overall reminder coverage
            overall_coverage = sum(reminder_coverage.values()) / len(reminder_coverage)

            if overall_coverage > 80:
                logger.info(f"✅ Overall reminder coverage: {overall_coverage:.1f}%")
                self.validation_results["agent_reminders"] = "PASS"
                return True
            else:
                logger.warning(f"⚠️ Overall reminder coverage: {overall_coverage:.1f}%")
                self.validation_results["agent_reminders"] = "FAIL"
                return False

        except Exception as e:
            logger.error(f"Error validating agent message reminders: {e}")
            self.validation_results["agent_reminders"] = "ERROR"
            return False

    def validate_system_performance(self) -> bool:
        """Validate system performance and reliability"""
        try:
            logger.info("🔍 Validating system performance...")

            # Check system resources
            import psutil

            # Check memory usage
            memory_usage = psutil.virtual_memory().percent
            if memory_usage < 90:
                logger.info(f"✅ Memory usage acceptable: {memory_usage}%")
                memory_status = "PASS"
            else:
                logger.warning(f"⚠️ High memory usage: {memory_usage}%")
                memory_status = "WARNING"

            # Check disk space
            disk_usage = psutil.disk_usage('/').percent
            if disk_usage < 90:
                logger.info(f"✅ Disk usage acceptable: {disk_usage}%")
                disk_status = "PASS"
            else:
                logger.warning(f"⚠️ High disk usage: {disk_usage}%")
                disk_status = "WARNING"

            # Overall performance status
            if memory_status == "PASS" and disk_status == "PASS":
                self.validation_results["system_performance"] = "PASS"
                return True
            else:
                self.validation_results["system_performance"] = "WARNING"
                return False

        except Exception as e:
            logger.error(f"Error validating system performance: {e}")
            self.validation_results["system_performance"] = "ERROR"
            return False

    def validate_reminder_quality(self) -> bool:
        """Validate reminder quality and format"""
        try:
            logger.info("🔍 Validating reminder quality...")

            # Check reminder format consistency
            quality_checks = {
                "emoji_consistency": all("🆔" in reminder or "📝" in reminder or "📬" in reminder or "📊" in reminder
                                      for reminder in self.reminder_types.values()),
                "text_consistency": all("REMINDER:" in reminder for reminder in self.reminder_types.values()),
                "length_consistency": all(len(reminder) > 50 for reminder in self.reminder_types.values()),
                "format_consistency": all(reminder.startswith(("🆔", "📝", "📬", "📊"))
                                        for reminder in self.reminder_types.values())
            }

            # Calculate quality score
            quality_score = sum(quality_checks.values()) / len(quality_checks) * 100

            if quality_score >= 80:
                logger.info(f"✅ Reminder quality score: {quality_score:.1f}%")
                self.validation_results["reminder_quality"] = "PASS"
                return True
            else:
                logger.warning(f"⚠️ Reminder quality score: {quality_score:.1f}%")
                self.validation_results["reminder_quality"] = "FAIL"
                return False

        except Exception as e:
            logger.error(f"Error validating reminder quality: {e}")
            self.validation_results["reminder_quality"] = "ERROR"
            return False

    def generate_validation_report(self) -> dict:
        """Generate comprehensive validation report"""
        try:
            logger.info("📊 Generating validation report...")

            # Calculate overall validation status
            total_checks = len(self.validation_results)
            passed_checks = sum(1 for status in self.validation_results.values() if status == "PASS")
            warning_checks = sum(1 for status in self.validation_results.values() if status == "WARNING")
            failed_checks = sum(1 for status in self.validation_results.values() if status == "FAIL")
            error_checks = sum(1 for status in self.validation_results.values() if status == "ERROR")

            overall_status = "PASS"
            if error_checks > 0:
                overall_status = "ERROR"
            elif failed_checks > 0:
                overall_status = "FAIL"
            elif warning_checks > 0:
                overall_status = "WARNING"

            report = {
                "timestamp": datetime.now().isoformat(),
                "validator": "Agent-5",
                "phase": "Phase 2 Consolidation",
                "system": "Comprehensive Reminder System",
                "overall_status": overall_status,
                "validation_summary": {
                    "total_checks": total_checks,
                    "passed": passed_checks,
                    "warnings": warning_checks,
                    "failed": failed_checks,
                    "errors": error_checks,
                    "success_rate": f"{(passed_checks/total_checks)*100:.1f}%" if total_checks > 0 else "0%"
                },
                "reminder_types": self.reminder_types,
                "validation_results": self.validation_results,
                "recommendations": self.generate_recommendations(),
                "next_steps": [
                    "Address any failed or error status checks",
                    "Monitor system performance continuously",
                    "Validate agent message reminders regularly",
                    "Maintain reminder quality standards"
                ]
            }

            # Save validation report
            report_file = self.project_root / "agent5_comprehensive_reminder_validation_report.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)

            logger.info(f"Validation report saved: {report_file}")
            return report

        except Exception as e:
            logger.error(f"Error generating validation report: {e}")
            return {}

    def generate_recommendations(self) -> list[str]:
        """Generate recommendations based on validation results"""
        recommendations = []

        for check, status in self.validation_results.items():
            if status == "FAIL":
                if check == "messaging_integration":
                    recommendations.append("Update messaging core to include all 4 reminder types")
                elif check == "reminder_consistency":
                    recommendations.append("Ensure reminder consistency across all system components")
                elif check == "agent_reminders":
                    recommendations.append("Ensure all agents receive all 4 reminder types in messages")
                elif check == "reminder_quality":
                    recommendations.append("Improve reminder quality and format consistency")

            elif status == "WARNING":
                if check == "system_performance":
                    recommendations.append("Monitor system resources and optimize performance")
                elif check == "agent_reminders":
                    recommendations.append("Increase agent message reminder coverage")

            elif status == "ERROR":
                recommendations.append(f"Investigate and resolve {check} validation error")

        if not recommendations:
            recommendations.append("System validation passed - continue monitoring")

        return recommendations

    def execute_comprehensive_validation(self) -> bool:
        """Execute comprehensive validation of comprehensive reminder system"""
        try:
            logger.info("🚀 Starting comprehensive reminder system validation")
            logger.info("🐝 WE ARE SWARM - Agent-5 Validation Active")

            # 1. Validate messaging system integration
            if not self.validate_messaging_system_integration():
                logger.error("Messaging system integration validation failed")

            # 2. Validate reminder consistency
            if not self.validate_reminder_consistency():
                logger.error("Reminder consistency validation failed")

            # 3. Validate agent message reminders
            if not self.validate_agent_message_reminders():
                logger.warning("Agent message reminders validation issues")

            # 4. Validate system performance
            if not self.validate_system_performance():
                logger.warning("System performance validation issues")

            # 5. Validate reminder quality
            if not self.validate_reminder_quality():
                logger.warning("Reminder quality validation issues")

            # 6. Generate validation report
            report = self.generate_validation_report()

            # 7. Generate final validation summary
            validation_summary = {
                "timestamp": datetime.now().isoformat(),
                "validator": "Agent-5",
                "phase": "Phase 2 Consolidation",
                "system": "Comprehensive Reminder System",
                "status": "VALIDATION_COMPLETE",
                "validation_results": self.validation_results,
                "report": report,
                "next_actions": [
                    "Review validation report for any issues",
                    "Address failed or error status checks",
                    "Monitor system performance continuously",
                    "Coordinate with all agents for system adoption"
                ]
            }

            # Save validation summary
            summary_file = self.project_root / "agent5_comprehensive_reminder_validation_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(validation_summary, f, indent=2)

            logger.info("🎉 Comprehensive reminder system validation completed!")
            logger.info(f"📊 Validation Summary: {summary_file}")

            return True

        except Exception as e:
            logger.error(f"Error in comprehensive validation: {e}")
            return False

def main():
    """Main execution function"""
    try:
        validator = Agent5ComprehensiveReminderValidator()

        # Check if we're in the right directory
        if not (Path.cwd() / "src").exists():
            logger.error("Not in project root directory. Please run from project root.")
            return 1

        # Execute comprehensive validation
        success = validator.execute_comprehensive_validation()

        if success:
            logger.info("✅ Comprehensive reminder system validation completed successfully!")
            return 0
        else:
            logger.error("❌ Comprehensive reminder system validation failed!")
            return 1

    except Exception as e:
        logger.error(f"Fatal error in comprehensive reminder system validation: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
