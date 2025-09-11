#!/usr/bin/env python3
"""
Agent-5 Core Modules Consolidation Validator
Comprehensive validation of core modules consolidation functionality

This script validates the core modules consolidation process,
ensuring all consolidation targets are met and the system functions properly.

Author: Agent-5 (Business Intelligence & Coordination Specialist)
Date: 2025-09-09
Phase: Consolidation Execution
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent5_core_modules_validator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Agent5CoreModulesValidator:
    """Agent-5 Core Modules Consolidation Validator"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.validation_results = {}
        self.system_status = {}
        self.consolidation_targets = {
            "messaging_system": {
                "current_files": 4,
                "target_files": 1,
                "reduction_percent": 75,
                "files": [
                    "src/core/messaging_core.py",
                    "src/core/messaging_pyautogui.py",
                    "src/services/messaging_core.py",
                    "src/services/messaging_pyautogui.py"
                ],
                "target_file": "src/core/unified_messaging.py"
            },
            "analytics_engine": {
                "current_files": 17,
                "target_files": 5,
                "reduction_percent": 71,
                "directories": [
                    "src/core/analytics/coordinators",
                    "src/core/analytics/engines",
                    "src/core/analytics/intelligence",
                    "src/core/analytics/orchestrators",
                    "src/core/analytics/processors"
                ],
                "target_file": "src/core/analytics/unified_analytics.py"
            },
            "configuration_system": {
                "current_files": 3,
                "target_files": 1,
                "reduction_percent": 67,
                "files": [
                    "src/core/unified_config.py",
                    "src/core/config_core.py",
                    "src/core/env_loader.py"
                ],
                "target_file": "src/core/unified_config.py"
            },
            "coordination_system": {
                "current_files": 15,
                "target_files": 5,
                "reduction_percent": 67,
                "files": [
                    "src/core/coordination_unified.py",
                    "src/core/coordinator_interfaces.py",
                    "src/core/coordinator_models.py",
                    "src/core/coordinator_registry.py",
                    "src/core/coordinator_status_parser.py",
                    "src/core/core_coordination.py"
                ],
                "target_file": "src/core/unified_coordination.py"
            },
            "engine_system": {
                "current_files": 20,
                "target_files": 3,
                "reduction_percent": 85,
                "directory": "src/core/engines",
                "target_file": "src/core/unified_engines.py"
            }
        }
        
    def validate_messaging_system_consolidation(self) -> bool:
        """Validate messaging system consolidation"""
        try:
            logger.info("🔍 Validating messaging system consolidation...")
            
            # Check if target file exists
            target_file = self.project_root / self.consolidation_targets["messaging_system"]["target_file"]
            if not target_file.exists():
                logger.warning("Unified messaging system not found")
                self.validation_results["messaging_system"] = "NOT_CREATED"
                return False
            
            # Check if source files still exist (should be consolidated)
            source_files = self.consolidation_targets["messaging_system"]["files"]
            existing_source_files = []
            
            for file_path in source_files:
                full_path = self.project_root / file_path
                if full_path.exists():
                    existing_source_files.append(file_path)
            
            if len(existing_source_files) > 1:
                logger.warning(f"Multiple messaging files still exist: {existing_source_files}")
                self.validation_results["messaging_system"] = "PARTIAL"
                return False
            
            # Check target file content
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for key messaging functionality
            messaging_keywords = [
                "UnifiedMessagingCore",
                "send_message",
                "broadcast_message",
                "PyAutoGUI",
                "messaging_core"
            ]
            
            found_keywords = sum(1 for keyword in messaging_keywords if keyword in content)
            
            if found_keywords >= 4:
                logger.info("✅ Messaging system consolidation validated")
                self.validation_results["messaging_system"] = "PASS"
                return True
            else:
                logger.warning("⚠️ Messaging system consolidation incomplete")
                self.validation_results["messaging_system"] = "FAIL"
                return False
                
        except Exception as e:
            logger.error(f"Error validating messaging system consolidation: {e}")
            self.validation_results["messaging_system"] = "ERROR"
            return False
    
    def validate_analytics_engine_consolidation(self) -> bool:
        """Validate analytics engine consolidation"""
        try:
            logger.info("🔍 Validating analytics engine consolidation...")
            
            # Check if target file exists
            target_file = self.project_root / self.consolidation_targets["analytics_engine"]["target_file"]
            if not target_file.exists():
                logger.warning("Unified analytics engine not found")
                self.validation_results["analytics_engine"] = "NOT_CREATED"
                return False
            
            # Check source directories
            source_dirs = self.consolidation_targets["analytics_engine"]["directories"]
            total_files = 0
            
            for dir_path in source_dirs:
                full_path = self.project_root / dir_path
                if full_path.exists():
                    files = list(full_path.rglob("*.py"))
                    total_files += len(files)
            
            # Check if consolidation target is met
            target_files = self.consolidation_targets["analytics_engine"]["target_files"]
            if total_files > target_files:
                logger.warning(f"Analytics engine consolidation incomplete: {total_files} files remaining")
                self.validation_results["analytics_engine"] = "PARTIAL"
                return False
            
            # Check target file content
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for key analytics functionality
            analytics_keywords = [
                "UnifiedAnalytics",
                "analytics_engine",
                "intelligence",
                "coordinators",
                "processors"
            ]
            
            found_keywords = sum(1 for keyword in analytics_keywords if keyword in content)
            
            if found_keywords >= 3:
                logger.info("✅ Analytics engine consolidation validated")
                self.validation_results["analytics_engine"] = "PASS"
                return True
            else:
                logger.warning("⚠️ Analytics engine consolidation incomplete")
                self.validation_results["analytics_engine"] = "FAIL"
                return False
                
        except Exception as e:
            logger.error(f"Error validating analytics engine consolidation: {e}")
            self.validation_results["analytics_engine"] = "ERROR"
            return False
    
    def validate_configuration_system_consolidation(self) -> bool:
        """Validate configuration system consolidation"""
        try:
            logger.info("🔍 Validating configuration system consolidation...")
            
            # Check if target file exists
            target_file = self.project_root / self.consolidation_targets["configuration_system"]["target_file"]
            if not target_file.exists():
                logger.warning("Unified configuration system not found")
                self.validation_results["configuration_system"] = "NOT_CREATED"
                return False
            
            # Check if source files are integrated
            source_files = self.consolidation_targets["configuration_system"]["files"]
            existing_source_files = []
            
            for file_path in source_files:
                full_path = self.project_root / file_path
                if full_path.exists():
                    existing_source_files.append(file_path)
            
            # Check target file content
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for key configuration functionality
            config_keywords = [
                "UnifiedConfig",
                "config_core",
                "env_loader",
                "configuration"
            ]
            
            found_keywords = sum(1 for keyword in config_keywords if keyword in content)
            
            if found_keywords >= 3:
                logger.info("✅ Configuration system consolidation validated")
                self.validation_results["configuration_system"] = "PASS"
                return True
            else:
                logger.warning("⚠️ Configuration system consolidation incomplete")
                self.validation_results["configuration_system"] = "FAIL"
                return False
                
        except Exception as e:
            logger.error(f"Error validating configuration system consolidation: {e}")
            self.validation_results["configuration_system"] = "ERROR"
            return False
    
    def validate_coordination_system_consolidation(self) -> bool:
        """Validate coordination system consolidation"""
        try:
            logger.info("🔍 Validating coordination system consolidation...")
            
            # Check if target file exists
            target_file = self.project_root / self.consolidation_targets["coordination_system"]["target_file"]
            if not target_file.exists():
                logger.warning("Unified coordination system not found")
                self.validation_results["coordination_system"] = "NOT_CREATED"
                return False
            
            # Check source files
            source_files = self.consolidation_targets["coordination_system"]["files"]
            existing_source_files = []
            
            for file_path in source_files:
                full_path = self.project_root / file_path
                if full_path.exists():
                    existing_source_files.append(file_path)
            
            # Check if consolidation target is met
            target_files = self.consolidation_targets["coordination_system"]["target_files"]
            if len(existing_source_files) > target_files:
                logger.warning(f"Coordination system consolidation incomplete: {len(existing_source_files)} files remaining")
                self.validation_results["coordination_system"] = "PARTIAL"
                return False
            
            # Check target file content
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for key coordination functionality
            coordination_keywords = [
                "UnifiedCoordination",
                "coordinator",
                "coordination",
                "swarm"
            ]
            
            found_keywords = sum(1 for keyword in coordination_keywords if keyword in content)
            
            if found_keywords >= 3:
                logger.info("✅ Coordination system consolidation validated")
                self.validation_results["coordination_system"] = "PASS"
                return True
            else:
                logger.warning("⚠️ Coordination system consolidation incomplete")
                self.validation_results["coordination_system"] = "FAIL"
                return False
                
        except Exception as e:
            logger.error(f"Error validating coordination system consolidation: {e}")
            self.validation_results["coordination_system"] = "ERROR"
            return False
    
    def validate_engine_system_consolidation(self) -> bool:
        """Validate engine system consolidation"""
        try:
            logger.info("🔍 Validating engine system consolidation...")
            
            # Check if target file exists
            target_file = self.project_root / self.consolidation_targets["engine_system"]["target_file"]
            if not target_file.exists():
                logger.warning("Unified engine system not found")
                self.validation_results["engine_system"] = "NOT_CREATED"
                return False
            
            # Check source directory
            source_dir = self.project_root / self.consolidation_targets["engine_system"]["directory"]
            if source_dir.exists():
                files = list(source_dir.rglob("*.py"))
                total_files = len(files)
                
                # Check if consolidation target is met
                target_files = self.consolidation_targets["engine_system"]["target_files"]
                if total_files > target_files:
                    logger.warning(f"Engine system consolidation incomplete: {total_files} files remaining")
                    self.validation_results["engine_system"] = "PARTIAL"
                    return False
            
            # Check target file content
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for key engine functionality
            engine_keywords = [
                "UnifiedEngines",
                "engine",
                "core_engine",
                "engines"
            ]
            
            found_keywords = sum(1 for keyword in engine_keywords if keyword in content)
            
            if found_keywords >= 3:
                logger.info("✅ Engine system consolidation validated")
                self.validation_results["engine_system"] = "PASS"
                return True
            else:
                logger.warning("⚠️ Engine system consolidation incomplete")
                self.validation_results["engine_system"] = "FAIL"
                return False
                
        except Exception as e:
            logger.error(f"Error validating engine system consolidation: {e}")
            self.validation_results["engine_system"] = "ERROR"
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
    
    def generate_validation_report(self) -> Dict:
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
                "phase": "Consolidation Execution",
                "system": "Core Modules Consolidation",
                "overall_status": overall_status,
                "validation_summary": {
                    "total_checks": total_checks,
                    "passed": passed_checks,
                    "warnings": warning_checks,
                    "failed": failed_checks,
                    "errors": error_checks,
                    "success_rate": f"{(passed_checks/total_checks)*100:.1f}%" if total_checks > 0 else "0%"
                },
                "consolidation_targets": self.consolidation_targets,
                "validation_results": self.validation_results,
                "recommendations": self.generate_recommendations(),
                "next_steps": [
                    "Address any failed or error status checks",
                    "Complete consolidation of remaining modules",
                    "Monitor system performance continuously",
                    "Validate consolidation quality standards"
                ]
            }
            
            # Save validation report
            report_file = self.project_root / "agent5_core_modules_validation_report.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Validation report saved: {report_file}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating validation report: {e}")
            return {}
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        for check, status in self.validation_results.items():
            if status == "FAIL":
                if check == "messaging_system":
                    recommendations.append("Complete messaging system consolidation - merge all messaging files")
                elif check == "analytics_engine":
                    recommendations.append("Complete analytics engine consolidation - merge all analytics modules")
                elif check == "configuration_system":
                    recommendations.append("Complete configuration system consolidation - integrate all config files")
                elif check == "coordination_system":
                    recommendations.append("Complete coordination system consolidation - merge all coordination files")
                elif check == "engine_system":
                    recommendations.append("Complete engine system consolidation - merge all engine files")
            
            elif status == "WARNING":
                if check == "system_performance":
                    recommendations.append("Monitor system resources and optimize performance")
            
            elif status == "ERROR":
                recommendations.append(f"Investigate and resolve {check} validation error")
        
        if not recommendations:
            recommendations.append("Core modules consolidation validation passed - continue monitoring")
        
        return recommendations
    
    def execute_comprehensive_validation(self) -> bool:
        """Execute comprehensive validation of core modules consolidation"""
        try:
            logger.info("🚀 Starting core modules consolidation validation")
            logger.info("🐝 WE ARE SWARM - Agent-5 Validation Active")
            
            # 1. Validate messaging system consolidation
            if not self.validate_messaging_system_consolidation():
                logger.error("Messaging system consolidation validation failed")
            
            # 2. Validate analytics engine consolidation
            if not self.validate_analytics_engine_consolidation():
                logger.error("Analytics engine consolidation validation failed")
            
            # 3. Validate configuration system consolidation
            if not self.validate_configuration_system_consolidation():
                logger.error("Configuration system consolidation validation failed")
            
            # 4. Validate coordination system consolidation
            if not self.validate_coordination_system_consolidation():
                logger.error("Coordination system consolidation validation failed")
            
            # 5. Validate engine system consolidation
            if not self.validate_engine_system_consolidation():
                logger.error("Engine system consolidation validation failed")
            
            # 6. Validate system performance
            if not self.validate_system_performance():
                logger.warning("System performance validation issues")
            
            # 7. Generate validation report
            report = self.generate_validation_report()
            
            # 8. Generate final validation summary
            validation_summary = {
                "timestamp": datetime.now().isoformat(),
                "validator": "Agent-5",
                "phase": "Consolidation Execution",
                "system": "Core Modules Consolidation",
                "status": "VALIDATION_COMPLETE",
                "validation_results": self.validation_results,
                "report": report,
                "next_actions": [
                    "Review validation report for any issues",
                    "Complete consolidation of remaining modules",
                    "Monitor system performance continuously",
                    "Coordinate with all agents for consolidation execution"
                ]
            }
            
            # Save validation summary
            summary_file = self.project_root / "agent5_core_modules_validation_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(validation_summary, f, indent=2)
            
            logger.info("🎉 Core modules consolidation validation completed!")
            logger.info(f"📊 Validation Summary: {summary_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in comprehensive validation: {e}")
            return False

def main():
    """Main execution function"""
    try:
        validator = Agent5CoreModulesValidator()
        
        # Check if we're in the right directory
        if not (Path.cwd() / "src").exists():
            logger.error("Not in project root directory. Please run from project root.")
            return 1
        
        # Execute comprehensive validation
        success = validator.execute_comprehensive_validation()
        
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
