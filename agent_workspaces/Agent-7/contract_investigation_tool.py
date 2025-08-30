#!/usr/bin/env python3
"""
Contract Investigation Tool - Agent-7 Active Engagement
======================================================

Investigates contract claiming system discrepancies and identifies available contracts.
Demonstrates active engagement and system troubleshooting capabilities.

Author: Agent-7 - Quality Completion Optimization Manager
Mission: Investigate Contract System and Identify Available Work
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


class ContractInvestigationTool:
    """Investigates contract claiming system and identifies available work"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.contract_system_status = {}
        self.available_contracts = []
        self.contract_discrepancies = []
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for contract investigation"""
        logger = logging.getLogger("ContractInvestigationTool")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def investigate_contract_system(self) -> Dict[str, Any]:
        """Investigate the contract claiming system"""
        self.logger.info("Investigating contract claiming system")
        
        investigation_results = {
            "timestamp": datetime.now().isoformat(),
            "system_status": "INVESTIGATING",
            "findings": {},
            "discrepancies": [],
            "recommendations": []
        }
        
        # Check contract claiming system
        investigation_results["findings"]["contract_system"] = self._check_contract_system()
        
        # Check task list for available contracts
        investigation_results["findings"]["task_list"] = self._check_task_list()
        
        # Check for contract discrepancies
        investigation_results["findings"]["discrepancies"] = self._identify_discrepancies()
        
        # Check contract claiming system files
        investigation_results["findings"]["system_files"] = self._check_system_files()
        
        # Generate recommendations
        investigation_results["recommendations"] = self._generate_recommendations(
            investigation_results["findings"]
        )
        
        return investigation_results
    
    def _check_contract_system(self) -> Dict[str, Any]:
        """Check the contract claiming system status"""
        try:
            # Check if the contract claiming system exists
            contract_system_path = Path("agent_workspaces/meeting/contract_claiming_system.py")
            if not contract_system_path.exists():
                return {
                    "status": "ERROR",
                    "error": "Contract claiming system not found",
                    "path": str(contract_system_path)
                }
            
            # Check if the system can be executed
            try:
                result = subprocess.run([
                    sys.executable,
                    "agent_workspaces/meeting/contract_claiming_system.py",
                    "--help"
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    system_status = "OPERATIONAL"
                    help_available = True
                else:
                    system_status = "ERROR"
                    help_available = False
            except Exception as e:
                system_status = "ERROR"
                help_available = False
                error_msg = str(e)
            
            # Check system statistics
            try:
                stats_result = subprocess.run([
                    sys.executable,
                    "agent_workspaces/meeting/contract_claiming_system.py",
                    "--stats"
                ], capture_output=True, text=True, timeout=10)
                
                if stats_result.returncode == 0:
                    stats_available = True
                    stats_output = stats_result.stdout
                else:
                    stats_available = False
                    stats_output = "Error getting stats"
            except Exception as e:
                stats_available = False
                stats_output = f"Exception: {str(e)}"
            
            return {
                "status": system_status,
                "file_exists": True,
                "executable": help_available,
                "stats_available": stats_available,
                "stats_output": stats_output,
                "system_path": str(contract_system_path)
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e)
            }
    
    def _check_task_list(self) -> Dict[str, Any]:
        """Check the task list for available contracts"""
        try:
            task_list_path = Path("agent_workspaces/meeting/task_list.json")
            if not task_list_path.exists():
                return {
                    "status": "ERROR",
                    "error": "Task list not found",
                    "path": str(task_list_path)
                }
            
            # Read task list
            with open(task_list_path, 'r', encoding='utf-8') as f:
                task_list = json.load(f)
            
            # Extract contract information
            total_contracts = task_list.get("total_contracts", 0)
            available_contracts = task_list.get("available_contracts", 0)
            claimed_contracts = task_list.get("claimed_contracts", 0)
            completed_contracts = task_list.get("completed_contracts", 0)
            
            # Find available contracts
            available_contract_list = []
            if "contracts" in task_list:
                for category, category_data in task_list["contracts"].items():
                    if "contracts" in category_data:
                        for contract in category_data["contracts"]:
                            if contract.get("status") == "AVAILABLE":
                                available_contract_list.append({
                                    "contract_id": contract.get("contract_id"),
                                    "title": contract.get("title"),
                                    "category": contract.get("category"),
                                    "difficulty": contract.get("difficulty"),
                                    "estimated_time": contract.get("estimated_time"),
                                    "extra_credit_points": contract.get("extra_credit_points")
                                })
            
            return {
                "status": "HEALTHY",
                "file_exists": True,
                "total_contracts": total_contracts,
                "available_contracts": available_contracts,
                "claimed_contracts": claimed_contracts,
                "completed_contracts": completed_contracts,
                "available_contract_list": available_contract_list,
                "file_path": str(task_list_path)
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e)
            }
    
    def _identify_discrepancies(self) -> List[Dict[str, Any]]:
        """Identify discrepancies in the contract system"""
        discrepancies = []
        
        try:
            # Check if stats show available contracts but claiming fails
            contract_system = self._check_contract_system()
            task_list = self._check_task_list()
            
            if (contract_system.get("status") == "OPERATIONAL" and 
                task_list.get("status") == "HEALTHY"):
                
                # Check for discrepancy between stats and actual availability
                if (task_list.get("available_contracts", 0) > 0 and 
                    len(task_list.get("available_contract_list", [])) > 0):
                    
                    # Try to claim one of the available contracts
                    test_contract = task_list["available_contract_list"][0]
                    test_contract_id = test_contract["contract_id"]
                    
                    try:
                        claim_result = subprocess.run([
                            sys.executable,
                            "agent_workspaces/meeting/contract_claiming_system.py",
                            "--claim", test_contract_id,
                            "--agent", "Agent-7"
                        ], capture_output=True, text=True, timeout=10)
                        
                        if claim_result.returncode != 0:
                            discrepancies.append({
                                "type": "CLAIMING_FAILURE",
                                "contract_id": test_contract_id,
                                "expected_status": "AVAILABLE",
                                "actual_status": "UNAVAILABLE",
                                "error_message": claim_result.stderr.strip(),
                                "recommendation": "Investigate contract status synchronization"
                            })
                    except Exception as e:
                        discrepancies.append({
                            "type": "CLAIMING_EXCEPTION",
                            "contract_id": test_contract_id,
                            "error": str(e),
                            "recommendation": "Check contract claiming system stability"
                        })
        except Exception as e:
            discrepancies.append({
                "type": "INVESTIGATION_ERROR",
                "error": str(e),
                "recommendation": "Review contract investigation process"
            })
        
        return discrepancies
    
    def _check_system_files(self) -> Dict[str, Any]:
        """Check contract system related files"""
        try:
            system_files = {
                "contract_claiming_system": "agent_workspaces/meeting/contract_claiming_system.py",
                "task_list": "agent_workspaces/meeting/task_list.json",
                "meeting": "agent_workspaces/meeting/meeting.json"
            }
            
            file_status = {}
            for name, path in system_files.items():
                file_path = Path(path)
                if file_path.exists():
                    try:
                        file_size = file_path.stat().st_size
                        file_status[name] = {
                            "exists": True,
                            "size": f"{file_size} bytes",
                            "path": str(file_path)
                        }
                    except Exception as e:
                        file_status[name] = {
                            "exists": True,
                            "error": str(e),
                            "path": str(file_path)
                        }
                else:
                    file_status[name] = {
                        "exists": False,
                        "path": str(file_path)
                    }
            
            return {
                "status": "HEALTHY",
                "files": file_status
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e)
            }
    
    def _generate_recommendations(self, findings: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on investigation findings"""
        recommendations = []
        
        # Check for contract system issues
        if findings.get("contract_system", {}).get("status") != "OPERATIONAL":
            recommendations.append("Fix contract claiming system - system not operational")
        
        # Check for discrepancies
        if findings.get("discrepancies"):
            recommendations.append("Resolve contract status discrepancies - claiming system out of sync")
        
        # Check for available contracts
        task_list = findings.get("task_list", {})
        if task_list.get("available_contracts", 0) > 0:
            recommendations.append(f"Investigate why {task_list['available_contracts']} available contracts cannot be claimed")
        
        # Check system file integrity
        system_files = findings.get("system_files", {})
        if system_files.get("status") != "HEALTHY":
            recommendations.append("Review contract system file integrity")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Contract system appears healthy - continue monitoring")
        
        return recommendations
    
    def generate_investigation_report(self) -> Dict[str, Any]:
        """Generate comprehensive investigation report"""
        self.logger.info("Generating comprehensive investigation report")
        
        investigation_results = self.investigate_contract_system()
        
        # Add summary
        summary = {
            "total_discrepancies": len(investigation_results.get("discrepancies", [])),
            "system_health": "HEALTHY" if not investigation_results.get("discrepancies") else "NEEDS_ATTENTION",
            "available_contracts": investigation_results.get("findings", {}).get("task_list", {}).get("available_contracts", 0),
            "investigation_complete": True
        }
        
        investigation_results["summary"] = summary
        investigation_results["report_generated"] = datetime.now().isoformat()
        
        return investigation_results
    
    def save_investigation_report(self, report: Dict[str, Any], filename: str = None) -> str:
        """Save investigation report to file"""
        if filename is None:
            filename = f"agent_workspaces/Agent-7/contract_investigation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            self.logger.info(f"Investigation report saved to: {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Error saving investigation report: {e}")
            return ""


def main():
    """Main entry point for contract investigation"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Contract Investigation Tool - Agent-7 Active Engagement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python contract_investigation_tool.py --investigate
  python contract_investigation_tool.py --report
  python contract_investigation_tool.py --help
        """
    )
    
    parser.add_argument(
        "--investigate", "-i",
        action="store_true",
        help="Investigate contract claiming system"
    )
    
    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help="Generate and save comprehensive investigation report"
    )
    
    args = parser.parse_args()
    
    # Initialize contract investigation tool
    investigator = ContractInvestigationTool()
    
    if args.investigate:
        # Investigate contract system
        investigation_results = investigator.investigate_contract_system()
        print("Contract System Investigation Results:")
        print(json.dumps(investigation_results, indent=2))
    elif args.report:
        # Generate comprehensive report
        report = investigator.generate_investigation_report()
        filename = investigator.save_investigation_report(report)
        print("Contract Investigation Report Generated:")
        print(json.dumps(report, indent=2))
        print(f"\nReport saved to: {filename}")
    else:
        print("Use --investigate to investigate contract claiming system")
        print("Use --report to generate comprehensive investigation report")
    
    return 0


if __name__ == "__main__":
    exit(main())
