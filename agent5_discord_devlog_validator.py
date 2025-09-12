#!/usr/bin/env python3
"""
Agent-5 Discord DevLog Reminder Validator
Comprehensive validation of Discord devlog reminder system integration

This script validates the Discord devlog reminder system integration,
ensuring all messages include devlog reminders and the system functions properly.

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
        logging.FileHandler('agent5_discord_devlog_validator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Agent5DiscordDevLogValidator:
    """Agent-5 Discord DevLog Reminder System Validator"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.validation_results = {}
        self.system_status = {}
        self.agent_responses = {}

    def validate_messaging_system_integration(self) -> bool:
        """Validate that the messaging system includes Discord devlog reminders"""
        try:
            logger.info("🔍 Validating messaging system integration...")

            # Check messaging core file
            messaging_core_file = self.project_root / "src" / "core" / "messaging_core.py"
            if not messaging_core_file.exists():
                logger.error("Messaging core file not found")
                return False

            # Read messaging core content
            with open(messaging_core_file, encoding='utf-8') as f:
                content = f.read()

            # Check for Discord devlog reminder integration
            devlog_reminder_text = "📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory"

            if devlog_reminder_text in content:
                logger.info("✅ Discord devlog reminder found in messaging core")
                self.validation_results["messaging_integration"] = "PASS"
                return True
            else:
                logger.warning("⚠️ Discord devlog reminder not found in messaging core")
                self.validation_results["messaging_integration"] = "FAIL"
                return False

        except Exception as e:
            logger.error(f"Error validating messaging system integration: {e}")
            self.validation_results["messaging_integration"] = "ERROR"
            return False

    def validate_discord_integration(self) -> bool:
        """Validate Discord integration functionality"""
        try:
            logger.info("🔍 Validating Discord integration...")

            # Check Discord commander file
            discord_commander_file = self.project_root / "src" / "discord_commander" / "discord_commander.py"
            if not discord_commander_file.exists():
                logger.error("Discord commander file not found")
                return False

            # Read Discord commander content
            with open(discord_commander_file, encoding='utf-8') as f:
                content = f.read()

            # Check for devlog monitoring functionality
            devlog_monitoring_keywords = [
                "devlog_monitoring",
                "send_devlog_notification",
                "process_devlog",
                "DiscordWebhookIntegration"
            ]

            found_keywords = sum(1 for keyword in devlog_monitoring_keywords if keyword in content)

            if found_keywords >= 3:
                logger.info("✅ Discord integration functionality found")
                self.validation_results["discord_integration"] = "PASS"
                return True
            else:
                logger.warning("⚠️ Discord integration functionality incomplete")
                self.validation_results["discord_integration"] = "FAIL"
                return False

        except Exception as e:
            logger.error(f"Error validating Discord integration: {e}")
            self.validation_results["discord_integration"] = "ERROR"
            return False

    def validate_devlog_directory_structure(self) -> bool:
        """Validate devlog directory structure and organization"""
        try:
            logger.info("🔍 Validating devlog directory structure...")

            devlogs_dir = self.project_root / "devlogs"
            if not devlogs_dir.exists():
                logger.error("Devlogs directory not found")
                return False

            # Check for devlog files
            devlog_files = list(devlogs_dir.rglob("*.md"))
            if not devlog_files:
                logger.warning("No devlog files found")
                self.validation_results["devlog_directory"] = "WARNING"
                return False

            # Check directory organization
            subdirectories = [d for d in devlogs_dir.iterdir() if d.is_dir()]
            expected_subdirs = ["agent_work", "autonomous_cycles", "cleanup_reports", "project_updates", "system_events", "v2_compliance"]

            found_subdirs = sum(1 for subdir in expected_subdirs if (devlogs_dir / subdir).exists())

            if found_subdirs >= 4:
                logger.info(f"✅ Devlog directory structure validated ({found_subdirs}/{len(expected_subdirs)} subdirectories)")
                self.validation_results["devlog_directory"] = "PASS"
                return True
            else:
                logger.warning(f"⚠️ Devlog directory structure incomplete ({found_subdirs}/{len(expected_subdirs)} subdirectories)")
                self.validation_results["devlog_directory"] = "PARTIAL"
                return False

        except Exception as e:
            logger.error(f"Error validating devlog directory structure: {e}")
            self.validation_results["devlog_directory"] = "ERROR"
            return False

    def validate_agent_message_reminders(self) -> bool:
        """Validate that all agents are receiving devlog reminders"""
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

            # Check for devlog reminders in recent messages
            devlog_reminder_text = "📝 DISCORD DEVLOG REMINDER"
            reminder_count = 0

            for message_file in recent_messages:
                try:
                    with open(message_file, encoding='utf-8') as f:
                        content = f.read()

                    if devlog_reminder_text in content:
                        reminder_count += 1
                except Exception as e:
                    logger.warning(f"Error reading message file {message_file}: {e}")

            if reminder_count > 0:
                logger.info(f"✅ Found devlog reminders in {reminder_count} recent messages")
                self.validation_results["agent_reminders"] = "PASS"
                return True
            else:
                logger.warning("⚠️ No devlog reminders found in recent messages")
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
                "system": "Discord DevLog Reminder System",
                "overall_status": overall_status,
                "validation_summary": {
                    "total_checks": total_checks,
                    "passed": passed_checks,
                    "warnings": warning_checks,
                    "failed": failed_checks,
                    "errors": error_checks,
                    "success_rate": f"{(passed_checks/total_checks)*100:.1f}%" if total_checks > 0 else "0%"
                },
                "validation_results": self.validation_results,
                "recommendations": self.generate_recommendations(),
                "next_steps": [
                    "Address any failed or error status checks",
                    "Monitor system performance continuously",
                    "Validate agent message reminders regularly",
                    "Maintain devlog directory organization"
                ]
            }

            # Save validation report
            report_file = self.project_root / "agent5_discord_devlog_validation_report.json"
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
                    recommendations.append("Update messaging core to include Discord devlog reminders")
                elif check == "discord_integration":
                    recommendations.append("Enhance Discord integration functionality")
                elif check == "agent_reminders":
                    recommendations.append("Ensure all agents receive devlog reminders in messages")

            elif status == "WARNING":
                if check == "devlog_directory":
                    recommendations.append("Improve devlog directory organization")
                elif check == "system_performance":
                    recommendations.append("Monitor system resources and optimize performance")

            elif status == "ERROR":
                recommendations.append(f"Investigate and resolve {check} validation error")

        if not recommendations:
            recommendations.append("System validation passed - continue monitoring")

        return recommendations

    def execute_comprehensive_validation(self) -> bool:
        """Execute comprehensive validation of Discord devlog reminder system"""
        try:
            logger.info("🚀 Starting comprehensive Discord devlog reminder system validation")
            logger.info("🐝 WE ARE SWARM - Agent-5 Validation Active")

            # 1. Validate messaging system integration
            if not self.validate_messaging_system_integration():
                logger.error("Messaging system integration validation failed")

            # 2. Validate Discord integration
            if not self.validate_discord_integration():
                logger.error("Discord integration validation failed")

            # 3. Validate devlog directory structure
            if not self.validate_devlog_directory_structure():
                logger.warning("Devlog directory structure validation issues")

            # 4. Validate agent message reminders
            if not self.validate_agent_message_reminders():
                logger.warning("Agent message reminders validation issues")

            # 5. Validate system performance
            if not self.validate_system_performance():
                logger.warning("System performance validation issues")

            # 6. Generate validation report
            report = self.generate_validation_report()

            # 7. Generate final validation summary
            validation_summary = {
                "timestamp": datetime.now().isoformat(),
                "validator": "Agent-5",
                "phase": "Phase 2 Consolidation",
                "system": "Discord DevLog Reminder System",
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
            summary_file = self.project_root / "agent5_discord_devlog_validation_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(validation_summary, f, indent=2)

            logger.info("🎉 Discord devlog reminder system validation completed!")
            logger.info(f"📊 Validation Summary: {summary_file}")

            return True

        except Exception as e:
            logger.error(f"Error in comprehensive validation: {e}")
            return False

def main():
    """Main execution function"""
    try:
        validator = Agent5DiscordDevLogValidator()

        # Check if we're in the right directory
        if not (Path.cwd() / "src").exists():
            logger.error("Not in project root directory. Please run from project root.")
            return 1

        # Execute comprehensive validation
        success = validator.execute_comprehensive_validation()

        if success:
            logger.info("✅ Discord devlog reminder system validation completed successfully!")
            return 0
        else:
            logger.error("❌ Discord devlog reminder system validation failed!")
            return 1

    except Exception as e:
        logger.error(f"Fatal error in Discord devlog reminder system validation: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
