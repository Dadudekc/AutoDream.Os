"""
Enhanced Project Scanner Report Generator
========================================

Report generation with merging capabilities and agent categorization.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class EnhancedReportGenerator:
    """Enhanced report generator with merging capabilities and agent categorization."""
    
    def __init__(self, project_root: Path, analysis: Dict[str, Dict[str, Any]]):
        """Initialize report generator."""
        self.project_root = project_root
        self.analysis = analysis
        self.output_dir = project_root / "analysis"
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_enhanced_reports(self):
        """Generate all enhanced reports with merging capabilities."""
        self.save_project_analysis()
        self.save_test_analysis()
        self.save_agent_analysis()
        self.save_architecture_overview()
        self.export_chatgpt_context()
    
    def save_project_analysis(self):
        """Save enhanced project analysis with merging."""
        report_path = self.project_root / "project_analysis.json"
        existing = self._load_existing_report(report_path)
        
        # Merge new analysis with existing
        merged = {**existing, **self.analysis}
        
        with report_path.open("w", encoding="utf-8") as f:
            json.dump(merged, f, indent=4)
        
        logger.info(f"✅ Enhanced project analysis saved to {report_path}")
    
    def save_test_analysis(self):
        """Save test analysis with enhanced categorization."""
        test_report_path = self.project_root / "test_analysis.json"
        existing_tests = self._load_existing_report(test_report_path)
        
        # Separate test files
        test_files = {}
        for file_path, analysis in self.analysis.items():
            if "test" in file_path.lower() or "tests" in file_path.lower():
                test_files[file_path] = analysis
        
        merged_tests = {**existing_tests, **test_files}
        
        with test_report_path.open("w", encoding="utf-8") as f:
            json.dump(merged_tests, f, indent=4)
        
        logger.info(f"✅ Enhanced test analysis saved to {test_report_path}")
    
    def save_agent_analysis(self):
        """Save enhanced agent analysis with categorization."""
        agent_data = {
            "agent_categories": {},
            "maturity_distribution": {},
            "agent_types": {},
            "swarm_coordination": {
                "total_agents": 8,
                "active_agents": 8,
                "coordination_method": "PyAutoGUI automation",
                "physical_positions": {
                    "Monitor 1": [(-1269, 481), (-308, 480), (-1269, 1001), (-308, 1000)],
                    "Monitor 2": [(652, 421), (1612, 419), (920, 851), (1611, 941)]
                }
            }
        }
        
        # Categorize agents from analysis
        for file_path, analysis in self.analysis.items():
            if analysis.get("language") == ".py":
                for class_name, class_data in analysis.get("classes", {}).items():
                    agent_type = class_data.get("agent_type", "Unknown")
                    maturity = class_data.get("maturity", "Unknown")
                    
                    if agent_type not in agent_data["agent_categories"]:
                        agent_data["agent_categories"][agent_type] = []
                    
                    agent_data["agent_categories"][agent_type].append({
                        "class": class_name,
                        "file": file_path,
                        "maturity": maturity,
                        "methods": len(class_data.get("methods", [])),
                        "complexity": analysis.get("complexity", 0)
                    })
                    
                    # Update distributions
                    agent_data["maturity_distribution"][maturity] = agent_data["maturity_distribution"].get(maturity, 0) + 1
                    agent_data["agent_types"][agent_type] = agent_data["agent_types"].get(agent_type, 0) + 1
        
        agent_report_path = self.output_dir / "enhanced_agent_analysis.json"
        with agent_report_path.open("w", encoding="utf-8") as f:
            json.dump(agent_data, f, indent=4)
        
        logger.info(f"✅ Enhanced agent analysis saved to {agent_report_path}")
    
    def save_architecture_overview(self):
        """Save enhanced architecture overview."""
        architecture_data = {
            "system_architecture": {
                "pattern": "Enhanced Modular Agent System with Swarm Intelligence",
                "components": [
                    "Enhanced Project Scanner",
                    "Agent Registry with Categorization",
                    "PyAutoGUI Communication Services",
                    "V2 Compliance Engine",
                    "Advanced Language Analysis",
                    "Intelligent Caching System"
                ],
                "enhancements": [
                    "Tree-sitter AST parsing for multiple languages",
                    "Advanced route detection for web frameworks",
                    "Agent maturity and type categorization",
                    "File movement detection and cache optimization",
                    "Enhanced complexity analysis",
                    "Automatic __init__.py generation"
                ]
            },
            "quality_metrics": {
                "total_files_analyzed": len(self.analysis),
                "languages_supported": list(set(a.get("language", "unknown") for a in self.analysis.values())),
                "average_complexity": sum(a.get("complexity", 0) for a in self.analysis.values()) / max(len(self.analysis), 1),
                "agent_distribution": self._calculate_agent_distribution()
            },
            "v2_compliance": {
                "compliant_files": sum(1 for a in self.analysis.values() if a.get("file_size", 0) <= 400),
                "violation_files": sum(1 for a in self.analysis.values() if a.get("file_size", 0) > 400),
                "compliance_rate": 0.0  # Will be calculated
            }
        }
        
        # Calculate compliance rate
        total_files = len(self.analysis)
        if total_files > 0:
            compliant = architecture_data["v2_compliance"]["compliant_files"]
            architecture_data["v2_compliance"]["compliance_rate"] = (compliant / total_files) * 100
        
        arch_report_path = self.output_dir / "enhanced_architecture_overview.json"
        with arch_report_path.open("w", encoding="utf-8") as f:
            json.dump(architecture_data, f, indent=4)
        
        logger.info(f"✅ Enhanced architecture overview saved to {arch_report_path}")
    
    def export_chatgpt_context(self):
        """Export enhanced ChatGPT context with agent categorization."""
        context_path = self.project_root / "chatgpt_project_context.json"
        existing_context = self._load_existing_report(context_path)
        
        enhanced_context = {
            "project_root": str(self.project_root),
            "scan_timestamp": time.time(),
            "enhanced_features": [
                "Advanced language analysis with tree-sitter",
                "Agent categorization and maturity assessment",
                "Enhanced route detection",
                "Intelligent caching with file movement detection",
                "V2 compliance monitoring",
                "Swarm coordination analysis"
            ],
            "analysis_summary": {
                "total_files": len(self.analysis),
                "languages": list(set(a.get("language", "unknown") for a in self.analysis.values())),
                "total_complexity": sum(a.get("complexity", 0) for a in self.analysis.values()),
                "agent_types": self._calculate_agent_distribution(),
                "maturity_levels": self._calculate_maturity_distribution()
            },
            "swarm_intelligence": {
                "coordination_method": "PyAutoGUI automation across dual monitors",
                "agent_positions": "8 agents positioned at specific pixel coordinates",
                "communication_protocol": "Real-time agent-to-agent messaging",
                "achievements": ["8-agent debate coordination", "Multi-monitor architecture", "Physical swarm automation"]
            },
            "analysis_details": self.analysis
        }
        
        # Merge with existing context
        merged_context = {**existing_context, **enhanced_context}
        
        with context_path.open("w", encoding="utf-8") as f:
            json.dump(merged_context, f, indent=4)
        
        logger.info(f"✅ Enhanced ChatGPT context exported to {context_path}")
    
    def generate_init_files(self, overwrite: bool = True):
        """Generate __init__.py files for Python packages."""
        from collections import defaultdict
        
        package_modules = defaultdict(list)
        
        for rel_path in self.analysis.keys():
            if rel_path.endswith(".py") and not rel_path.endswith("__init__.py"):
                file_path = Path(rel_path)
                package_dir = file_path.parent
                module_name = file_path.stem
                package_modules[str(package_dir)].append(module_name)
        
        for package, modules in package_modules.items():
            package_path = self.project_root / package
            init_file = package_path / "__init__.py"
            package_path.mkdir(parents=True, exist_ok=True)
            
            if overwrite or not init_file.exists():
                lines = [
                    "# AUTO-GENERATED __init__.py",
                    "# Enhanced Project Scanner - DO NOT EDIT MANUALLY\n"
                ]
                
                for module in sorted(modules):
                    lines.append(f"from . import {module}")
                
                lines.extend([
                    "",
                    "__all__ = ["
                ])
                
                for module in sorted(modules):
                    lines.append(f"    '{module}',")
                
                lines.append("]\n")
                
                content = "\n".join(lines)
                
                with init_file.open("w", encoding="utf-8") as f:
                    f.write(content)
                
                logger.info(f"✅ Generated enhanced __init__.py in {package_path}")
    
    def _load_existing_report(self, report_path: Path) -> Dict[str, Any]:
        """Load existing report to preserve data during merging."""
        if report_path.exists():
            try:
                with report_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading existing report {report_path}: {e}")
        return {}
    
    def _calculate_agent_distribution(self) -> Dict[str, int]:
        """Calculate distribution of agent types."""
        distribution = {}
        
        for analysis in self.analysis.values():
            if analysis.get("language") == ".py":
                for class_data in analysis.get("classes", {}).values():
                    agent_type = class_data.get("agent_type", "Unknown")
                    distribution[agent_type] = distribution.get(agent_type, 0) + 1
        
        return distribution
    
    def _calculate_maturity_distribution(self) -> Dict[str, int]:
        """Calculate distribution of maturity levels."""
        distribution = {}
        
        for analysis in self.analysis.values():
            if analysis.get("language") == ".py":
                for class_data in analysis.get("classes", {}).values():
                    maturity = class_data.get("maturity", "Unknown")
                    distribution[maturity] = distribution.get(maturity, 0) + 1
        
        return distribution

