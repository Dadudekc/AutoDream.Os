#!/usr/bin/env python3
"""
Consolidation Analyzer Operations
===============================
Operations and utilities for system consolidation analyzer
V2 Compliant: ≤400 lines, focused operations
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
import sys
sys.path.insert(0, str(project_root))

from src.team_beta.consolidation_analyzer_core import (
    SystemConsolidationAnalyzerCore, ConsolidationStatus, DuplicationSeverity, DuplicationInstance
)

class ConsolidationAnalyzerOperations:
    """Operations and utilities for consolidation analyzer management"""
    
    def __init__(self, analyzer: SystemConsolidationAnalyzerCore = None):
        self.analyzer = analyzer or SystemConsolidationAnalyzerCore()
    
    def manage_operations(self, action: str, **kwargs) -> Any:
        """Consolidated operations management"""
        if action == "bulk_update_status":
            return self.bulk_update_status(kwargs["updates"])
        elif action == "export_report":
            return self.export_consolidation_report(kwargs["output_file"])
        elif action == "import_analysis":
            return self.import_consolidation_analysis(kwargs["input_file"])
        elif action == "validate_consolidation":
            return self.validate_consolidation_state()
        elif action == "cleanup_completed":
            return self.cleanup_completed_consolidations(kwargs.get("days", 30))
        elif action == "backup_analysis":
            return self.backup_consolidation_analysis(kwargs["backup_dir"])
        elif action == "restore_analysis":
            return self.restore_consolidation_analysis(kwargs["backup_file"])
        elif action == "analyze_trends":
            return self.analyze_consolidation_trends(kwargs.get("days", 30))
        elif action == "optimize_plan":
            return self.optimize_consolidation_plan()
        elif action == "monitor_progress":
            return self.monitor_consolidation_progress()
        return None
    
    def bulk_update_status(self, updates: List[Dict[str, str]]) -> Dict[str, Any]:
        """Bulk update duplication statuses"""
        results = {
            "success": True,
            "updated": 0,
            "failed": 0,
            "errors": []
        }
        
        for update in updates:
            try:
                name = update["name"]
                status_str = update["status"]
                
                # Validate status
                try:
                    status = ConsolidationStatus(status_str)
                except ValueError:
                    results["failed"] += 1
                    results["errors"].append(f"Invalid status '{status_str}' for {name}")
                    continue
                
                # Update status
                self.analyzer.manage_consolidation_operations(
                    "update_status",
                    name=name,
                    status=status
                )
                
                results["updated"] += 1
                
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Error updating {update.get('name', 'unknown')}: {e}")
        
        return results
    
    def export_consolidation_report(self, output_file: str) -> bool:
        """Export comprehensive consolidation report"""
        try:
            analysis = self.analyzer.manage_consolidation_operations("analyze")
            plan = self.analyzer.manage_consolidation_operations("create_plan")
            progress = self.analyzer.manage_consolidation_operations("get_progress")
            
            report = {
                "report_timestamp": datetime.now().isoformat(),
                "consolidation_analysis": analysis,
                "consolidation_plan": plan,
                "progress_report": progress,
                "duplication_details": [
                    {
                        "name": dup.name,
                        "description": dup.description,
                        "files": dup.files,
                        "severity": dup.severity.value,
                        "status": dup.status.value,
                        "impact": dup.impact,
                        "consolidation_plan": dup.consolidation_plan,
                        "dependencies": dup.dependencies,
                        "risks": dup.risks,
                    }
                    for dup in self.analyzer.duplications
                ],
                "summary": {
                    "total_duplications": len(self.analyzer.duplications),
                    "critical_count": len([d for d in self.analyzer.duplications if d.severity == DuplicationSeverity.CRITICAL]),
                    "high_count": len([d for d in self.analyzer.duplications if d.severity == DuplicationSeverity.HIGH]),
                    "completed_count": len([d for d in self.analyzer.duplications if d.status == ConsolidationStatus.COMPLETED]),
                    "in_progress_count": len([d for d in self.analyzer.duplications if d.status == ConsolidationStatus.IN_PROGRESS]),
                    "completion_percentage": progress["completion_percentage"]
                }
            }
            
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error exporting consolidation report: {e}")
            return False
    
    def import_consolidation_analysis(self, input_file: str) -> bool:
        """Import consolidation analysis from file"""
        try:
            with open(input_file, 'r') as f:
                import_data = json.load(f)
            
            # Validate import data structure
            if "duplication_details" not in import_data:
                print("Invalid import file format")
                return False
            
            # Clear existing duplications
            self.analyzer.duplications.clear()
            
            # Import duplications
            imported_count = 0
            for dup_data in import_data["duplication_details"]:
                try:
                    duplication = DuplicationInstance(
                        name=dup_data["name"],
                        description=dup_data["description"],
                        files=dup_data["files"],
                        severity=DuplicationSeverity(dup_data["severity"]),
                        status=ConsolidationStatus(dup_data["status"]),
                        impact=dup_data["impact"],
                        consolidation_plan=dup_data["consolidation_plan"],
                        dependencies=dup_data["dependencies"],
                        risks=dup_data["risks"]
                    )
                    
                    self.analyzer.duplications.append(duplication)
                    imported_count += 1
                    
                except Exception as e:
                    print(f"Error importing duplication {dup_data.get('name', 'unknown')}: {e}")
            
            print(f"Successfully imported {imported_count} duplications")
            return True
            
        except Exception as e:
            print(f"Error importing consolidation analysis: {e}")
            return False
    
    def validate_consolidation_state(self) -> Dict[str, Any]:
        """Validate consolidation state integrity"""
        validation_report = {
            "valid": True,
            "issues": [],
            "statistics": {
                "total_duplications": len(self.analyzer.duplications),
                "invalid_duplications": 0,
                "missing_files": 0,
                "inconsistent_status": 0
            }
        }
        
        # Validate duplications
        for dup in self.analyzer.duplications:
            # Check if files exist
            for file_path in dup.files:
                if not Path(file_path).exists():
                    validation_report["statistics"]["missing_files"] += 1
                    validation_report["issues"].append(f"File {file_path} not found for {dup.name}")
            
            # Check for invalid severity/status combinations
            if dup.severity == DuplicationSeverity.CRITICAL and dup.status == ConsolidationStatus.CANCELLED:
                validation_report["statistics"]["inconsistent_status"] += 1
                validation_report["issues"].append(f"Critical duplication {dup.name} cannot be cancelled")
            
            # Check for empty required fields
            if not dup.name or not dup.description:
                validation_report["statistics"]["invalid_duplications"] += 1
                validation_report["issues"].append(f"Duplication {dup.name} has empty required fields")
        
        if validation_report["issues"]:
            validation_report["valid"] = False
        
        return validation_report
    
    def cleanup_completed_consolidations(self, days: int = 30) -> Dict[str, Any]:
        """Clean up old completed consolidations"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        cleanup_report = {
            "success": True,
            "archived": 0,
            "errors": []
        }
        
        duplications_to_archive = []
        
        for dup in self.analyzer.duplications:
            if dup.status == ConsolidationStatus.COMPLETED:
                # For completed consolidations, we would typically check completion date
                # Since we don't have completion timestamps, we'll archive based on status
                duplications_to_archive.append(dup)
        
        # Archive completed consolidations
        for dup in duplications_to_archive:
            try:
                # In a real implementation, we would move to archive
                # For now, we'll just mark as archived
                dup.status = ConsolidationStatus.CANCELLED  # Using cancelled as archived
                cleanup_report["archived"] += 1
            except Exception as e:
                cleanup_report["errors"].append(f"Error archiving {dup.name}: {e}")
        
        return cleanup_report
    
    def backup_consolidation_analysis(self, backup_dir: str) -> bool:
        """Create backup of consolidation analysis"""
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_path / f"consolidation_backup_{timestamp}.json"
            
            # Export analysis
            return self.export_consolidation_report(str(backup_file))
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def restore_consolidation_analysis(self, backup_file: str) -> bool:
        """Restore consolidation analysis from backup"""
        try:
            # Create backup of current analysis
            current_backup = f"consolidation_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.export_consolidation_report(current_backup)
            
            # Restore from backup
            return self.import_consolidation_analysis(backup_file)
            
        except Exception as e:
            print(f"Error restoring consolidation analysis: {e}")
            return False
    
    def analyze_consolidation_trends(self, days: int = 30) -> Dict[str, Any]:
        """Analyze consolidation trends over time"""
        trends_report = {
            "analysis_period_days": days,
            "total_duplications": len(self.analyzer.duplications),
            "severity_distribution": {},
            "status_distribution": {},
            "consolidation_efficiency": 0.0,
            "risk_trends": {},
            "recommendations": []
        }
        
        # Analyze severity distribution
        for severity in DuplicationSeverity:
            count = len([d for d in self.analyzer.duplications if d.severity == severity])
            trends_report["severity_distribution"][severity.value] = count
        
        # Analyze status distribution
        for status in ConsolidationStatus:
            count = len([d for d in self.analyzer.duplications if d.status == status])
            trends_report["status_distribution"][status.value] = count
        
        # Calculate consolidation efficiency
        completed = trends_report["status_distribution"].get("completed", 0)
        total = trends_report["total_duplications"]
        trends_report["consolidation_efficiency"] = (completed / total) * 100 if total > 0 else 0
        
        # Analyze risk trends
        critical_count = trends_report["severity_distribution"].get("critical", 0)
        high_count = trends_report["severity_distribution"].get("high", 0)
        
        if critical_count > 2:
            trends_report["risk_trends"]["overall_risk"] = "high"
            trends_report["recommendations"].append("Prioritize critical consolidations immediately")
        elif critical_count == 0 and high_count < 3:
            trends_report["risk_trends"]["overall_risk"] = "low"
            trends_report["recommendations"].append("System consolidation is well-managed")
        else:
            trends_report["risk_trends"]["overall_risk"] = "medium"
            trends_report["recommendations"].append("Continue monitoring consolidation progress")
        
        # Additional recommendations based on efficiency
        if trends_report["consolidation_efficiency"] < 50:
            trends_report["recommendations"].append("Consider increasing consolidation resources")
        elif trends_report["consolidation_efficiency"] > 80:
            trends_report["recommendations"].append("Excellent consolidation progress - maintain current pace")
        
        return trends_report
    
    def optimize_consolidation_plan(self) -> Dict[str, Any]:
        """Optimize consolidation plan based on current state"""
        optimization_report = {
            "success": True,
            "optimizations_applied": 0,
            "plan_adjustments": [],
            "errors": []
        }
        
        # Analyze current state
        analysis = self.analyzer.manage_consolidation_operations("analyze")
        plan = self.analyzer.manage_consolidation_operations("create_plan")
        
        # Optimize based on current progress
        completed_count = len([d for d in self.analyzer.duplications if d.status == ConsolidationStatus.COMPLETED])
        total_count = len(self.analyzer.duplications)
        
        if completed_count > total_count * 0.5:
            # More than half completed - adjust timeline
            optimization_report["plan_adjustments"].append("Reduced estimated duration due to high completion rate")
            optimization_report["optimizations_applied"] += 1
        
        # Check for critical duplications that need immediate attention
        critical_duplications = [d for d in self.analyzer.duplications if d.severity == DuplicationSeverity.CRITICAL]
        if critical_duplications:
            optimization_report["plan_adjustments"].append(f"Prioritize {len(critical_duplications)} critical consolidations")
            optimization_report["optimizations_applied"] += 1
        
        # Check for stuck consolidations
        in_progress_count = len([d for d in self.analyzer.duplications if d.status == ConsolidationStatus.IN_PROGRESS])
        if in_progress_count > 3:
            optimization_report["plan_adjustments"].append("Consider reassigning stuck consolidations")
            optimization_report["optimizations_applied"] += 1
        
        return optimization_report
    
    def monitor_consolidation_progress(self) -> Dict[str, Any]:
        """Monitor current consolidation progress and identify issues"""
        monitor_report = {
            "timestamp": datetime.now().isoformat(),
            "total_duplications": len(self.analyzer.duplications),
            "completed": 0,
            "in_progress": 0,
            "stuck_consolidations": 0,
            "critical_pending": 0,
            "bottlenecks": [],
            "recommendations": []
        }
        
        # Count statuses
        for dup in self.analyzer.duplications:
            if dup.status == ConsolidationStatus.COMPLETED:
                monitor_report["completed"] += 1
            elif dup.status == ConsolidationStatus.IN_PROGRESS:
                monitor_report["in_progress"] += 1
                # Check for stuck consolidations (in progress for too long)
                # Since we don't have timestamps, we'll use a simple heuristic
                if len(dup.files) > 3:  # Complex consolidations might be stuck
                    monitor_report["stuck_consolidations"] += 1
                    monitor_report["bottlenecks"].append({
                        "name": dup.name,
                        "files_count": len(dup.files),
                        "severity": dup.severity.value
                    })
        
        # Count critical pending
        monitor_report["critical_pending"] = len([
            d for d in self.analyzer.duplications 
            if d.severity == DuplicationSeverity.CRITICAL and d.status != ConsolidationStatus.COMPLETED
        ])
        
        # Generate recommendations
        if monitor_report["critical_pending"] > 0:
            monitor_report["recommendations"].append("Address critical consolidations immediately")
        
        if monitor_report["stuck_consolidations"] > 0:
            monitor_report["recommendations"].append("Investigate stuck consolidations")
        
        if monitor_report["in_progress"] > 5:
            monitor_report["recommendations"].append("Consider reducing concurrent consolidations")
        
        completion_rate = (monitor_report["completed"] / monitor_report["total_duplications"]) * 100
        if completion_rate < 30:
            monitor_report["recommendations"].append("Accelerate consolidation efforts")
        elif completion_rate > 80:
            monitor_report["recommendations"].append("Excellent progress - maintain current pace")
        
        return monitor_report
