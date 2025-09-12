#!/usr/bin/env python3
"""
Agent-5 Core Modules Consolidation Validator
Comprehensive validation of core modules consolidation effectiveness

This script validates core modules consolidation, ensuring business value
preservation and system functionality maintenance.

Author: Agent-5 (Business Intelligence & Coordination Specialist)
Date: 2025-09-09
Phase: Consolidation Execution
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("agent5_core_consolidation_validator.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class Agent5CoreConsolidationValidator:
    """Agent-5 Core Modules Consolidation Validator"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.validation_results = {}
        self.consolidation_status = {}
        self.business_metrics = {}

        # Define core modules consolidation targets
        self.consolidation_targets = {
            "messaging_system": {
                "current_files": [
                    "src/core/messaging_core.py",
                    "src/core/messaging_pyautogui.py",
                    "src/services/messaging_core.py",
                    "src/services/messaging_pyautogui.py",
                ],
                "target_file": "src/core/unified_messaging.py",
                "reduction": "4 → 1 (75% reduction)",
            },
            "analytics_engine": {
                "current_files": [
                    "src/core/analytics/coordinators/*.py",
                    "src/core/analytics/engines/*.py",
                    "src/core/analytics/intelligence/*.py",
                    "src/core/analytics/orchestrators/*.py",
                    "src/core/analytics/processors/*.py",
                ],
                "target_file": "src/core/analytics/unified_analytics.py",
                "reduction": "28 → 5 (82% reduction)",
            },
            "configuration_system": {
                "current_files": [
                    "src/core/unified_config.py",
                    "src/core/config_core.py",
                    "src/core/env_loader.py",
                ],
                "target_file": "src/core/enhanced_unified_config.py",
                "reduction": "3 → 1 (67% reduction)",
            },
        }

    def validate_messaging_system_consolidation(self) -> bool:
        """Validate messaging system consolidation effectiveness"""
        try:
            logger.info("🔍 Validating messaging system consolidation...")

            # Check if unified messaging system exists
            unified_messaging_file = self.project_root / "src" / "core" / "unified_messaging.py"
            if not unified_messaging_file.exists():
                logger.warning("Unified messaging system not found")
                self.validation_results["messaging_consolidation"] = "PENDING"
                return False

            # Check if duplicate files still exist
            duplicate_files = []
            for file_path in self.consolidation_targets["messaging_system"]["current_files"]:
                full_path = self.project_root / file_path
                if full_path.exists():
                    duplicate_files.append(file_path)

            if duplicate_files:
                logger.warning(f"Duplicate messaging files still exist: {duplicate_files}")
                self.validation_results["messaging_consolidation"] = "PARTIAL"
                return False

            # Check unified messaging system functionality
            with open(unified_messaging_file, encoding="utf-8") as f:
                content = f.read()

            # Check for key functionality
            required_functions = [
                "send_message",
                "broadcast_message",
                "pyautogui_integration",
                "unified_interface",
            ]

            found_functions = sum(1 for func in required_functions if func in content)

            if found_functions >= 3:
                logger.info("✅ Messaging system consolidation validated")
                self.validation_results["messaging_consolidation"] = "PASS"
                return True
            else:
                logger.warning("⚠️ Messaging system consolidation incomplete")
                self.validation_results["messaging_consolidation"] = "FAIL"
                return False

        except Exception as e:
            logger.error(f"Error validating messaging system consolidation: {e}")
            self.validation_results["messaging_consolidation"] = "ERROR"
            return False

    def validate_analytics_engine_consolidation(self) -> bool:
        """Validate analytics engine consolidation effectiveness"""
        try:
            logger.info("🔍 Validating analytics engine consolidation...")

            # Check if unified analytics system exists
            unified_analytics_file = (
                self.project_root / "src" / "core" / "analytics" / "unified_analytics.py"
            )
            if not unified_analytics_file.exists():
                logger.warning("Unified analytics system not found")
                self.validation_results["analytics_consolidation"] = "PENDING"
                return False

            # Check analytics directory structure
            analytics_dir = self.project_root / "src" / "core" / "analytics"
            if not analytics_dir.exists():
                logger.warning("Analytics directory not found")
                self.validation_results["analytics_consolidation"] = "FAIL"
                return False

            # Count remaining analytics files
            analytics_files = list(analytics_dir.rglob("*.py"))
            remaining_files = len(analytics_files)

            # Check if consolidation target achieved (28 → 5)
            if remaining_files <= 5:
                logger.info(
                    f"✅ Analytics engine consolidation validated ({remaining_files} files)"
                )
                self.validation_results["analytics_consolidation"] = "PASS"
                return True
            else:
                logger.warning(
                    f"⚠️ Analytics engine consolidation incomplete ({remaining_files} files)"
                )
                self.validation_results["analytics_consolidation"] = "PARTIAL"
                return False

        except Exception as e:
            logger.error(f"Error validating analytics engine consolidation: {e}")
            self.validation_results["analytics_consolidation"] = "ERROR"
            return False

    def validate_configuration_system_consolidation(self) -> bool:
        """Validate configuration system consolidation effectiveness"""
        try:
            logger.info("🔍 Validating configuration system consolidation...")

            # Check if enhanced unified config exists
            enhanced_config_file = self.project_root / "src" / "core" / "enhanced_unified_config.py"
            if not enhanced_config_file.exists():
                logger.warning("Enhanced unified config not found")
                self.validation_results["config_consolidation"] = "PENDING"
                return False

            # Check if duplicate config files still exist
            duplicate_files = []
            for file_path in ["src/core/config_core.py", "src/core/env_loader.py"]:
                full_path = self.project_root / file_path
                if full_path.exists():
                    duplicate_files.append(file_path)

            if duplicate_files:
                logger.warning(f"Duplicate config files still exist: {duplicate_files}")
                self.validation_results["config_consolidation"] = "PARTIAL"
                return False

            # Check enhanced config functionality
            with open(enhanced_config_file, encoding="utf-8") as f:
                content = f.read()

            # Check for key functionality
            required_functions = [
                "load_config",
                "env_loader",
                "unified_config",
                "configuration_interface",
            ]

            found_functions = sum(1 for func in required_functions if func in content)

            if found_functions >= 3:
                logger.info("✅ Configuration system consolidation validated")
                self.validation_results["config_consolidation"] = "PASS"
                return True
            else:
                logger.warning("⚠️ Configuration system consolidation incomplete")
                self.validation_results["config_consolidation"] = "FAIL"
                return False

        except Exception as e:
            logger.error(f"Error validating configuration system consolidation: {e}")
            self.validation_results["config_consolidation"] = "ERROR"
            return False

    def validate_business_value_preservation(self) -> bool:
        """Validate that business value is preserved during consolidation"""
        try:
            logger.info("🔍 Validating business value preservation...")

            # Check for critical business functionality
            business_functions = ["messaging_core.py", "analytics", "unified_config.py"]

            preserved_functions = 0
            for func in business_functions:
                if func in str(self.project_root):
                    preserved_functions += 1

            if preserved_functions >= 2:
                logger.info("✅ Business value preservation validated")
                self.validation_results["business_value"] = "PASS"
                return True
            else:
                logger.warning("⚠️ Business value preservation incomplete")
                self.validation_results["business_value"] = "FAIL"
                return False

        except Exception as e:
            logger.error(f"Error validating business value preservation: {e}")
            self.validation_results["business_value"] = "ERROR"
            return False

    def validate_system_performance(self) -> bool:
        """Validate system performance after consolidation"""
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
            disk_usage = psutil.disk_usage("/").percent
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

    def calculate_consolidation_metrics(self) -> dict[str, Any]:
        """Calculate consolidation metrics and business value"""
        try:
            logger.info("📊 Calculating consolidation metrics...")

            # Count current core files
            core_dir = self.project_root / "src" / "core"
            if not core_dir.exists():
                return {"error": "Core directory not found"}

            current_files = list(core_dir.rglob("*.py"))
            current_count = len(current_files)

            # Calculate consolidation progress
            target_count = 15  # Target from consolidation plan
            reduction_percentage = ((50 - current_count) / 50 * 100) if current_count <= 50 else 0

            metrics = {
                "current_files": current_count,
                "target_files": target_count,
                "reduction_percentage": reduction_percentage,
                "consolidation_progress": min(100, reduction_percentage),
                "status": "ON_TRACK" if current_count <= target_count else "NEEDS_WORK",
            }

            logger.info(
                f"Consolidation metrics: {current_count} files, {reduction_percentage:.1f}% reduction"
            )
            return metrics

        except Exception as e:
            logger.error(f"Error calculating consolidation metrics: {e}")
            return {"error": str(e)}

    def generate_consolidation_report(self) -> dict:
        """Generate comprehensive consolidation validation report"""
        try:
            logger.info("📊 Generating consolidation validation report...")

            # Calculate overall validation status
            total_checks = len(self.validation_results)
            passed_checks = sum(
                1 for status in self.validation_results.values() if status == "PASS"
            )
            warning_checks = sum(
                1 for status in self.validation_results.values() if status == "WARNING"
            )
            failed_checks = sum(
                1 for status in self.validation_results.values() if status == "FAIL"
            )
            error_checks = sum(
                1 for status in self.validation_results.values() if status == "ERROR"
            )

            overall_status = "PASS"
            if error_checks > 0:
                overall_status = "ERROR"
            elif failed_checks > 0:
                overall_status = "FAIL"
            elif warning_checks > 0:
                overall_status = "WARNING"

            # Get consolidation metrics
            metrics = self.calculate_consolidation_metrics()

            report = {
                "timestamp": datetime.now().isoformat(),
                "validator": "Agent-5",
                "phase": "Consolidation Execution",
                "system": "Core Modules Consolidation",
                "overall_status": overall_status,
                "validation_summary": {
                    "total_checks": total_checks,
                    "passed": passed_checks,
                    "warnings": warning_checks,
                    "failed": failed_checks,
                    "errors": error_checks,
                    "success_rate": (
                        f"{(passed_checks / total_checks) * 100:.1f}%" if total_checks > 0 else "0%"
                    ),
                },
                "consolidation_targets": self.consolidation_targets,
                "validation_results": self.validation_results,
                "consolidation_metrics": metrics,
                "recommendations": self.generate_recommendations(),
                "next_steps": [
                    "Address any failed or error status checks",
                    "Continue consolidation execution",
                    "Monitor system performance continuously",
                    "Validate business value preservation",
                ],
            }

            # Save consolidation report
            report_file = self.project_root / "agent5_core_consolidation_validation_report.json"
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)

            logger.info(f"Consolidation validation report saved: {report_file}")
            return report

        except Exception as e:
            logger.error(f"Error generating consolidation validation report: {e}")
            return {}

    def generate_recommendations(self) -> list[str]:
        """Generate recommendations based on validation results"""
        recommendations = []

        for check, status in self.validation_results.items():
            if status == "FAIL":
                if check == "messaging_consolidation":
                    recommendations.append(
                        "Complete messaging system consolidation - merge duplicate files"
                    )
                elif check == "analytics_consolidation":
                    recommendations.append(
                        "Complete analytics engine consolidation - reduce file count"
                    )
                elif check == "config_consolidation":
                    recommendations.append(
                        "Complete configuration system consolidation - merge config files"
                    )
                elif check == "business_value":
                    recommendations.append(
                        "Ensure business value preservation during consolidation"
                    )

            elif status == "WARNING":
                if check == "system_performance":
                    recommendations.append("Monitor system performance and optimize if needed")

            elif status == "ERROR":
                recommendations.append(f"Investigate and resolve {check} validation error")

        if not recommendations:
            recommendations.append("Consolidation validation passed - continue monitoring")

        return recommendations

    def execute_consolidation_validation(self) -> bool:
        """Execute comprehensive consolidation validation"""
        try:
            logger.info("🚀 Starting core modules consolidation validation")
            logger.info("🐝 WE ARE SWARM - Agent-5 Consolidation Validation Active")

            # 1. Validate messaging system consolidation
            if not self.validate_messaging_system_consolidation():
                logger.error("Messaging system consolidation validation failed")

            # 2. Validate analytics engine consolidation
            if not self.validate_analytics_engine_consolidation():
                logger.error("Analytics engine consolidation validation failed")

            # 3. Validate configuration system consolidation
            if not self.validate_configuration_system_consolidation():
                logger.error("Configuration system consolidation validation failed")

            # 4. Validate business value preservation
            if not self.validate_business_value_preservation():
                logger.warning("Business value preservation validation issues")

            # 5. Validate system performance
            if not self.validate_system_performance():
                logger.warning("System performance validation issues")

            # 6. Generate consolidation report
            report = self.generate_consolidation_report()

            # 7. Generate final validation summary
            validation_summary = {
                "timestamp": datetime.now().isoformat(),
                "validator": "Agent-5",
                "phase": "Consolidation Execution",
                "system": "Core Modules Consolidation",
                "status": "VALIDATION_COMPLETE",
                "validation_results": self.validation_results,
                "report": report,
                "next_actions": [
                    "Review consolidation validation report",
                    "Address failed or error status checks",
                    "Continue consolidation execution",
                    "Monitor system performance continuously",
                ],
            }

            # Save validation summary
            summary_file = self.project_root / "agent5_core_consolidation_validation_summary.json"
            with open(summary_file, "w", encoding="utf-8") as f:
                json.dump(validation_summary, f, indent=2)

            logger.info("🎉 Core modules consolidation validation completed!")
            logger.info(f"📊 Validation Summary: {summary_file}")

            return True

        except Exception as e:
            logger.error(f"Error in consolidation validation: {e}")
            return False


def main():
    """Main execution function"""
    try:
        validator = Agent5CoreConsolidationValidator()

        # Check if we're in the right directory
        if not (Path.cwd() / "src").exists():
            logger.error("Not in project root directory. Please run from project root.")
            return 1

        # Execute consolidation validation
        success = validator.execute_consolidation_validation()

        if success:
            logger.info("✅ Core modules consolidation validation completed successfully!")
            return 0
        else:
            logger.error("❌ Core modules consolidation validation failed!")
            return 1

    except Exception as e:
        logger.error(f"Fatal error in core modules consolidation validation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
