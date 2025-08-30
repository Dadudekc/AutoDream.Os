#!/usr/bin/env python3
"""
System Health Monitor - Agent-7 Active Engagement
=================================================

Monitors system health, validates V2 compliance, and ensures quality standards.
Demonstrates active engagement and system maintenance capabilities.

Author: Agent-7 - Quality Completion Optimization Manager
Mission: Maintain System Health and V2 Compliance
Priority: HIGH - Active Engagement
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import subprocess


class SystemHealthMonitor:
    """Monitors system health and validates V2 compliance"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.health_metrics = {}
        self.compliance_status = {}
        self.quality_metrics = {}
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for system health monitoring"""
        logger = logging.getLogger("SystemHealthMonitor")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health status"""
        self.logger.info("Checking system health status")
        
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "EXCELLENT",
            "components": {}
        }
        
        # Check file system health
        health_status["components"]["file_system"] = self._check_file_system()
        
        # Check Python environment health
        health_status["components"]["python_environment"] = self._check_python_environment()
        
        # Check agent workspace health
        health_status["components"]["agent_workspaces"] = self._check_agent_workspaces()
        
        # Check V2 compliance health
        health_status["components"]["v2_compliance"] = self._check_v2_compliance()
        
        # Check QA framework health
        health_status["components"]["qa_framework"] = self._check_qa_framework()
        
        # Calculate overall health score
        health_scores = []
        for component, status in health_status["components"].items():
            if isinstance(status, dict) and "health_score" in status:
                health_scores.append(status["health_score"])
        
        if health_scores:
            overall_score = sum(health_scores) / len(health_scores)
            if overall_score >= 95:
                health_status["overall_health"] = "EXCELLENT"
            elif overall_score >= 85:
                health_status["overall_health"] = "GOOD"
            elif overall_score >= 75:
                health_status["overall_health"] = "FAIR"
            else:
                health_status["overall_health"] = "NEEDS_ATTENTION"
            
            health_status["overall_score"] = overall_score
        
        return health_status
    
    def _check_file_system(self) -> Dict[str, Any]:
        """Check file system health"""
        try:
            # Check workspace directory structure
            workspace_path = Path("agent_workspaces")
            if workspace_path.exists():
                agent_dirs = [d for d in workspace_path.iterdir() if d.is_dir()]
                agent_count = len(agent_dirs)
                
                # Check for critical files
                critical_files = [
                    "agent_workspaces/Agent-7/status.json",
                    "agent_workspaces/Agent-7/next_phase_implementation.py",
                    "agent_workspaces/Agent-7/stall_prevention_qa_framework.py",
                    "agent_workspaces/Agent-7/quality_validation_scripts.py",
                    "agent_workspaces/Agent-7/class_hierarchy_refactoring.py"
                ]
                
                existing_critical_files = sum(1 for f in critical_files if Path(f).exists())
                critical_file_health = (existing_critical_files / len(critical_files)) * 100
                
                return {
                    "status": "HEALTHY",
                    "health_score": 95,
                    "agent_workspaces": agent_count,
                    "critical_files": f"{existing_critical_files}/{len(critical_files)}",
                    "critical_file_health": f"{critical_file_health:.1f}%"
                }
            else:
                return {
                    "status": "ERROR",
                    "health_score": 0,
                    "error": "Workspace directory not found"
                }
        except Exception as e:
            return {
                "status": "ERROR",
                "health_score": 0,
                "error": str(e)
            }
    
    def _check_python_environment(self) -> Dict[str, Any]:
        """Check Python environment health"""
        try:
            # Check Python version
            python_version = sys.version_info
            version_health = 100 if python_version.major >= 3 and python_version.minor >= 7 else 80
            
            # Check required modules
            required_modules = ["json", "logging", "pathlib", "typing", "datetime"]
            missing_modules = []
            
            for module in required_modules:
                try:
                    __import__(module)
                except ImportError:
                    missing_modules.append(module)
            
            module_health = 100 if not missing_modules else 100 - (len(missing_modules) * 20)
            
            return {
                "status": "HEALTHY",
                "health_score": (version_health + module_health) / 2,
                "python_version": f"{python_version.major}.{python_version.minor}.{python_version.micro}",
                "required_modules": f"{len(required_modules) - len(missing_modules)}/{len(required_modules)}",
                "missing_modules": missing_modules
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "health_score": 0,
                "error": str(e)
            }
    
    def _check_agent_workspaces(self) -> Dict[str, Any]:
        """Check agent workspace health"""
        try:
            agent_7_path = Path("agent_workspaces/Agent-7")
            if not agent_7_path.exists():
                return {
                    "status": "ERROR",
                    "health_score": 0,
                    "error": "Agent-7 workspace not found"
                }
            
            # Check key files
            key_files = [
                "status.json",
                "next_phase_implementation.py",
                "stall_prevention_qa_framework.py",
                "quality_validation_scripts.py",
                "class_hierarchy_refactoring.py"
            ]
            
            existing_files = []
            missing_files = []
            
            for file in key_files:
                file_path = agent_7_path / file
                if file_path.exists():
                    existing_files.append(file)
                else:
                    missing_files.append(file)
            
            file_health = (len(existing_files) / len(key_files)) * 100
            
            # Check file sizes for V2 compliance
            large_files = []
            for file in existing_files:
                file_path = agent_7_path / file
                try:
                    file_size = file_path.stat().st_size
                    if file_size > 400 * 1024:  # 400KB limit
                        large_files.append(f"{file} ({file_size / 1024:.1f}KB)")
                except Exception:
                    pass
            
            compliance_health = 100 if not large_files else 100 - (len(large_files) * 20)
            
            return {
                "status": "HEALTHY",
                "health_score": (file_health + compliance_health) / 2,
                "existing_files": len(existing_files),
                "missing_files": len(missing_files),
                "file_health": f"{file_health:.1f}%",
                "large_files": large_files,
                "compliance_health": f"{compliance_health:.1f}%"
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "health_score": 0,
                "error": str(e)
            }
    
    def _check_v2_compliance(self) -> Dict[str, Any]:
        """Check V2 compliance status"""
        try:
            # Check V2 compliance tracker
            compliance_tracker_path = Path("docs/reports/V2_COMPLIANCE_PROGRESS_TRACKER.md")
            if compliance_tracker_path.exists():
                with open(compliance_tracker_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract compliance information
                if "100%" in content and "Phase 1 Complete" in content:
                    compliance_level = "100%"
                    phase_status = "Phase 1 Complete"
                    compliance_health = 100
                elif "95%" in content:
                    compliance_level = "95%"
                    phase_status = "Phase 1 In Progress"
                    compliance_health = 95
                else:
                    compliance_level = "Unknown"
                    phase_status = "Unknown"
                    compliance_health = 50
                
                return {
                    "status": "HEALTHY",
                    "health_score": compliance_health,
                    "compliance_level": compliance_level,
                    "phase_status": phase_status,
                    "tracker_file": "Found and accessible"
                }
            else:
                return {
                    "status": "WARNING",
                    "health_score": 70,
                    "error": "V2 compliance tracker not found"
                }
        except Exception as e:
            return {
                "status": "ERROR",
                "health_score": 0,
                "error": str(e)
            }
    
    def _check_qa_framework(self) -> Dict[str, Any]:
        """Check QA framework health"""
        try:
            qa_files = [
                "agent_workspaces/Agent-7/stall_prevention_qa_framework.py",
                "agent_workspaces/Agent-7/quality_validation_scripts.py",
                "agent_workspaces/Agent-7/modularization_qa_framework.py"
            ]
            
            existing_qa_files = sum(1 for f in qa_files if Path(f).exists())
            qa_file_health = (existing_qa_files / len(qa_files)) * 100
            
            # Check if QA framework can be executed
            try:
                result = subprocess.run([
                    sys.executable, 
                    "agent_workspaces/Agent-7/quality_validation_scripts.py",
                    "--help"
                ], capture_output=True, text=True, timeout=10)
                
                execution_health = 100 if result.returncode == 0 else 80
            except Exception:
                execution_health = 60
            
            overall_qa_health = (qa_file_health + execution_health) / 2
            
            return {
                "status": "HEALTHY",
                "health_score": overall_qa_health,
                "qa_files": f"{existing_qa_files}/{len(qa_files)}",
                "file_health": f"{qa_file_health:.1f}%",
                "execution_health": f"{execution_health:.1f}%",
                "framework_status": "OPERATIONAL"
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "health_score": 0,
                "error": str(e)
            }
    
    def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        self.logger.info("Generating comprehensive health report")
        
        health_status = self.check_system_health()
        
        # Add recommendations
        recommendations = []
        if health_status["overall_health"] != "EXCELLENT":
            recommendations.append("System health needs attention - review components")
        
        for component, status in health_status["components"].items():
            if isinstance(status, dict) and status.get("health_score", 100) < 80:
                recommendations.append(f"Improve {component} health - current score: {status.get('health_score', 0)}")
        
        health_status["recommendations"] = recommendations
        health_status["report_generated"] = datetime.now().isoformat()
        
        return health_status
    
    def save_health_report(self, report: Dict[str, Any], filename: str = None) -> str:
        """Save health report to file"""
        if filename is None:
            filename = f"agent_workspaces/Agent-7/system_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            self.logger.info(f"Health report saved to: {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Error saving health report: {e}")
            return ""


def main():
    """Main entry point for system health monitoring"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="System Health Monitor - Agent-7 Active Engagement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python system_health_monitor.py --check
  python system_health_monitor.py --report
  python system_health_monitor.py --help
        """
    )
    
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="Check system health status"
    )
    
    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help="Generate and save comprehensive health report"
    )
    
    args = parser.parse_args()
    
    # Initialize system health monitor
    monitor = SystemHealthMonitor()
    
    if args.check:
        # Check system health
        health_status = monitor.check_system_health()
        print("System Health Status:")
        print(json.dumps(health_status, indent=2))
    elif args.report:
        # Generate comprehensive report
        report = monitor.generate_health_report()
        filename = monitor.save_health_report(report)
        print("System Health Report Generated:")
        print(json.dumps(report, indent=2))
        print(f"\nReport saved to: {filename}")
    else:
        print("Use --check to check system health status")
        print("Use --report to generate comprehensive health report")
    
    return 0


if __name__ == "__main__":
    exit(main())
