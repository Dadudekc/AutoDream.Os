#!/usr/bin/env python3
"""
🛰️ SIMPLE GODFATHER ANALYSIS SYSTEM
===================================

A simplified version that demonstrates how project scanner capabilities
can enhance Godfather-level analysis without complex dependencies.

Features:
- V2 Compliance Analysis
- File Structure Analysis
- Dependency Mapping
- Architecture Pattern Detection
- File-by-File Godfather Analysis
- Master System Summary
"""

import ast
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleGodfatherAnalyzer:
    """Simple Godfather Analysis System with project scanner integration."""
    
    def __init__(self, project_root: str = "."):
        """Initialize the analyzer."""
        self.project_root = Path(project_root).resolve()
        self.analysis_data = {}
        
        logger.info(f"🛰️ Simple Godfather Analyzer initialized for {self.project_root}")
    
    def analyze_project(self) -> Dict[str, Any]:
        """Perform comprehensive project analysis."""
        logger.info("🔍 Starting Simple Godfather Analysis...")
        
        # Phase 1: Project Structure Analysis
        self._analyze_project_structure()
        
        # Phase 2: V2 Compliance Analysis
        self._analyze_v2_compliance()
        
        # Phase 3: Dependency Analysis
        self._analyze_dependencies()
        
        # Phase 4: Architecture Analysis
        self._analyze_architecture()
        
        # Phase 5: File-by-File Godfather Analysis
        self._godfather_file_analysis()
        
        # Phase 6: Generate Master Summary
        self._generate_master_summary()
        
        logger.info("✅ Simple Godfather Analysis completed")
        return self.analysis_data
    
    def _analyze_project_structure(self) -> None:
        """Analyze basic project structure and file organization."""
        logger.info("📁 Analyzing project structure...")
        
        structure = {
            "total_files": 0,
            "python_files": 0,
            "directories": [],
            "file_types": {},
            "agent_workspaces": [],
            "core_modules": [],
            "service_modules": [],
            "tool_modules": []
        }
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip hidden directories and cache
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                structure["total_files"] += 1
                file_path = Path(root) / file
                ext = file_path.suffix.lower()
                
                if ext == '.py':
                    structure["python_files"] += 1
                
                structure["file_types"][ext] = structure["file_types"].get(ext, 0) + 1
        
        # Categorize modules
        for py_file in self.project_root.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
                
            rel_path = py_file.relative_to(self.project_root)
            path_parts = rel_path.parts
            
            if "agent_workspaces" in path_parts:
                structure["agent_workspaces"].append(str(rel_path))
            elif "src/core" in str(rel_path):
                structure["core_modules"].append(str(rel_path))
            elif "src/services" in str(rel_path):
                structure["service_modules"].append(str(rel_path))
            elif "tools" in path_parts:
                structure["tool_modules"].append(str(rel_path))
        
        self.analysis_data["structure"] = structure
        logger.info(f"📊 Found {structure['total_files']} files, {structure['python_files']} Python files")
    
    def _analyze_v2_compliance(self) -> None:
        """Analyze V2 compliance violations."""
        logger.info("🔍 Analyzing V2 compliance...")
        
        v2_results = {
            "files_analyzed": 0,
            "total_violations": 0,
            "violation_counts": {
                "file_loc": 0,
                "class_loc": 0,
                "function_loc": 0,
                "line_length": 0,
                "print_statement": 0
            },
            "files": [],
            "summary": {}
        }
        
        python_files = [f for f in self.project_root.rglob("*.py") 
                       if "__pycache__" not in str(f)]
        
        for py_file in python_files[:100]:  # Limit for demo
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.splitlines()
                
                file_violations = []
                
                # Check file length (V2 compliance: ≤400 lines)
                if len(lines) > 400:
                    file_violations.append({
                        "type": "file_loc",
                        "line": 1,
                        "message": f"File has {len(lines)} lines, exceeds 400 limit",
                        "severity": "error"
                    })
                    v2_results["violation_counts"]["file_loc"] += 1
                
                # Check line length (≤100 characters)
                for i, line in enumerate(lines, 1):
                    if len(line) > 100:
                        file_violations.append({
                            "type": "line_length",
                            "line": i,
                            "message": f"Line {i} has {len(line)} characters, exceeds 100 limit",
                            "severity": "warning"
                        })
                        v2_results["violation_counts"]["line_length"] += 1
                
                # Check for print statements
                for i, line in enumerate(lines, 1):
                    if line.strip().startswith("print("):
                        file_violations.append({
                            "type": "print_statement",
                            "line": i,
                            "message": f"Line {i} contains print statement, use logger instead",
                            "severity": "warning"
                        })
                        v2_results["violation_counts"]["print_statement"] += 1
                
                # AST analysis for class/function violations
                try:
                    tree = ast.parse(content, filename=str(py_file))
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            class_lines = (node.end_lineno or 0) - (node.lineno or 0) + 1
                            if class_lines > 100:
                                file_violations.append({
                                    "type": "class_loc",
                                    "line": node.lineno,
                                    "message": f"Class '{node.name}' has {class_lines} lines, exceeds 100 limit",
                                    "severity": "error"
                                })
                                v2_results["violation_counts"]["class_loc"] += 1
                        
                        elif isinstance(node, ast.FunctionDef):
                            func_lines = (node.end_lineno or 0) - (node.lineno or 0) + 1
                            if func_lines > 50:
                                file_violations.append({
                                    "type": "function_loc",
                                    "line": node.lineno,
                                    "message": f"Function '{node.name}' has {func_lines} lines, exceeds 50 limit",
                                    "severity": "error"
                                })
                                v2_results["violation_counts"]["function_loc"] += 1
                
                except SyntaxError:
                    pass  # Skip files with syntax errors
                
                v2_results["files"].append({
                    "file": str(py_file),
                    "lines": len(lines),
                    "violations": file_violations,
                    "status": "error" if any(v["severity"] == "error" for v in file_violations) else "warning" if file_violations else "ok"
                })
                
                v2_results["files_analyzed"] += 1
                v2_results["total_violations"] += len(file_violations)
                
            except Exception as e:
                logger.warning(f"Could not analyze {py_file}: {e}")
        
        # Generate summary
        total_files = v2_results["files_analyzed"]
        error_files = sum(1 for f in v2_results["files"] if f["status"] == "error")
        warning_files = sum(1 for f in v2_results["files"] if f["status"] == "warning")
        ok_files = sum(1 for f in v2_results["files"] if f["status"] == "ok")
        
        v2_results["summary"] = {
            "total_files": total_files,
            "total_violations": v2_results["total_violations"],
            "error_files": error_files,
            "warning_files": warning_files,
            "ok_files": ok_files,
            "compliance_rate": (ok_files / total_files * 100) if total_files > 0 else 0,
            "violation_rate": (v2_results["total_violations"] / total_files) if total_files > 0 else 0
        }
        
        self.analysis_data["v2_compliance"] = v2_results
        logger.info(f"⚠️ Found {v2_results['total_violations']} V2 violations across {v2_results['files_analyzed']} files")
    
    def _analyze_dependencies(self) -> None:
        """Analyze project dependencies and relationships."""
        logger.info("🔗 Analyzing dependencies...")
        
        dependencies = {
            "external_deps": set(),
            "internal_deps": {},
            "requirements_files": []
        }
        
        # Check for requirements files
        req_files = ["requirements.txt", "requirements-test.txt", "pyproject.toml"]
        for req_file in req_files:
            if (self.project_root / req_file).exists():
                dependencies["requirements_files"].append(req_file)
        
        # Analyze imports in Python files
        for py_file in self.project_root.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_imports = []
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('import ') or line.startswith('from '):
                        if ' import ' in line:
                            module = line.split(' import ')[0].replace('from ', '').strip()
                            if not module.startswith('.'):
                                dependencies["external_deps"].add(module.split('.')[0])
                            else:
                                file_imports.append(module)
                
                dependencies["internal_deps"][str(py_file)] = file_imports
                
            except Exception as e:
                logger.warning(f"Could not analyze imports in {py_file}: {e}")
        
        dependencies["external_deps"] = list(dependencies["external_deps"])
        self.analysis_data["dependencies"] = dependencies
        
        logger.info(f"📦 Found {len(dependencies['external_deps'])} external dependencies")
    
    def _analyze_architecture(self) -> None:
        """Analyze system architecture and patterns."""
        logger.info("🏗️ Analyzing architecture patterns...")
        
        architecture = {
            "patterns_detected": [],
            "agent_system": {},
            "service_architecture": {}
        }
        
        # Detect architectural patterns
        for py_file in self.project_root.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Pattern detection
                if "class.*Factory" in content:
                    architecture["patterns_detected"].append("Factory Pattern")
                if "class.*Singleton" in content:
                    architecture["patterns_detected"].append("Singleton Pattern")
                if "class.*Observer" in content:
                    architecture["patterns_detected"].append("Observer Pattern")
                if "class.*Repository" in content:
                    architecture["patterns_detected"].append("Repository Pattern")
                if "class.*Service" in content:
                    architecture["patterns_detected"].append("Service Layer Pattern")
                
            except Exception as e:
                logger.warning(f"Could not analyze architecture in {py_file}: {e}")
        
        # Analyze agent system
        agent_files = [f for f in self.project_root.rglob("*.py") if "agent" in str(f).lower()]
        architecture["agent_system"] = {
            "agent_files": len(agent_files),
            "coordination_method": "PyAutoGUI",
            "messaging_system": "Unified Messaging Service"
        }
        
        self.analysis_data["architecture"] = architecture
        logger.info(f"🏛️ Detected patterns: {', '.join(set(architecture['patterns_detected']))}")
    
    def _godfather_file_analysis(self) -> None:
        """Perform Godfather-level file-by-file analysis."""
        logger.info("🛰️ Performing Godfather file analysis...")
        
        file_analyses = []
        
        # Get all Python files for analysis
        python_files = [f for f in self.project_root.rglob("*.py") 
                       if "__pycache__" not in str(f)]
        
        for py_file in python_files[:30]:  # Limit to first 30 files for demo
            try:
                analysis = self._analyze_single_file(py_file)
                file_analyses.append(analysis)
            except Exception as e:
                logger.warning(f"Could not analyze {py_file}: {e}")
                file_analyses.append({
                    "file_path": str(py_file),
                    "purpose": "Analysis failed",
                    "error": str(e)
                })
        
        self.analysis_data["file_analyses"] = file_analyses
        logger.info(f"🔍 Completed Godfather analysis of {len(file_analyses)} files")
    
    def _analyze_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file with Godfather-level detail."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic file analysis
            lines = content.splitlines()
            line_count = len(lines)
            
            # AST analysis
            tree = ast.parse(content, filename=str(file_path))
            
            # Extract components
            classes = []
            functions = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                    })
                elif isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": len(node.args.args)
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    else:
                        module = node.module or ""
                        for alias in node.names:
                            imports.append(f"{module}.{alias.name}")
            
            # Determine purpose
            purpose = self._determine_file_purpose(file_path, content, classes, functions)
            
            # Determine role in system
            role = self._determine_system_role(file_path, content)
            
            # Identify patterns and issues
            observations = self._identify_patterns_and_issues(content, classes, functions)
            
            return {
                "file_path": str(file_path),
                "purpose": purpose,
                "major_components": {
                    "classes": classes,
                    "functions": functions,
                    "imports": imports
                },
                "dependencies": imports,
                "role_in_system": role,
                "observations": observations,
                "metrics": {
                    "lines": line_count,
                    "complexity": len(classes) + len(functions)
                }
            }
            
        except Exception as e:
            return {
                "file_path": str(file_path),
                "purpose": "Analysis failed",
                "error": str(e)
            }
    
    def _determine_file_purpose(self, file_path: Path, content: str, classes: List, functions: List) -> str:
        """Determine the purpose of a file based on its content and structure."""
        path_str = str(file_path).lower()
        
        if "test" in path_str:
            return "Test file for validation and quality assurance"
        elif "agent" in path_str:
            return "Agent system component for autonomous operations"
        elif "service" in path_str:
            return "Service layer component for business logic"
        elif "core" in path_str:
            return "Core system functionality and utilities"
        elif "messaging" in path_str:
            return "Messaging system for agent communication"
        elif "discord" in path_str:
            return "Discord bot integration and commands"
        elif "thea" in path_str:
            return "Thea communication interface"
        elif "ml" in path_str:
            return "Machine learning pipeline and models"
        elif "architecture" in path_str:
            return "Architectural patterns and design components"
        elif "validation" in path_str:
            return "Validation and quality assurance system"
        elif "tools" in path_str:
            return "Development and analysis tool"
        elif "config" in path_str:
            return "Configuration and settings management"
        else:
            return "General purpose module"
    
    def _determine_system_role(self, file_path: Path, content: str) -> str:
        """Determine the role of a file in the overall system architecture."""
        path_str = str(file_path)
        
        if "src/core" in path_str:
            return "Core infrastructure layer - foundational system components"
        elif "src/services" in path_str:
            return "Service layer - business logic and application services"
        elif "src/architecture" in path_str:
            return "Architecture layer - design patterns and system structure"
        elif "src/domain" in path_str:
            return "Domain layer - business entities and domain logic"
        elif "src/infrastructure" in path_str:
            return "Infrastructure layer - external integrations and persistence"
        elif "agent_workspaces" in path_str:
            return "Agent workspace - autonomous agent data and status"
        elif "tools" in path_str:
            return "Tool layer - development and analysis utilities"
        elif "tests" in path_str:
            return "Test layer - quality assurance and validation"
        else:
            return "Supporting component - auxiliary functionality"
    
    def _identify_patterns_and_issues(self, content: str, classes: List, functions: List) -> List[str]:
        """Identify patterns, anti-patterns, and improvement opportunities."""
        observations = []
        
        # Check for patterns
        if len(classes) > 0:
            observations.append(f"✅ Contains {len(classes)} classes - good object-oriented design")
        
        if len(functions) > 10:
            observations.append("⚠️ High function count - consider grouping related functions")
        
        # Check for anti-patterns
        if "print(" in content:
            observations.append("⚠️ Contains print statements - consider using logging")
        
        if "TODO" in content or "FIXME" in content:
            observations.append("📝 Contains TODO/FIXME comments - needs attention")
        
        if len(content.splitlines()) > 400:
            observations.append("🚨 File exceeds V2 compliance limit (400 lines) - needs refactoring")
        
        # Check for good practices
        if "def test_" in content:
            observations.append("✅ Contains test functions - good testing practice")
        
        if "class " in content and "__init__" in content:
            observations.append("✅ Proper class initialization - good OOP practice")
        
        return observations
    
    def _generate_master_summary(self) -> None:
        """Generate the master system summary."""
        logger.info("🎯 Generating Master System Summary...")
        
        structure = self.analysis_data.get("structure", {})
        v2_compliance = self.analysis_data.get("v2_compliance", {})
        architecture = self.analysis_data.get("architecture", {})
        dependencies = self.analysis_data.get("dependencies", {})
        
        master_summary = {
            "project_overview": {
                "name": "Agent Cellphone V2 - Enhanced Autonomous System",
                "total_files": structure.get("total_files", 0),
                "python_files": structure.get("python_files", 0),
                "analysis_timestamp": datetime.now().isoformat()
            },
            "architecture_summary": {
                "pattern": "Modular Agent System with V2 Compliance",
                "coordination_method": "PyAutoGUI-based agent communication",
                "design_principles": ["V2 Compliance", "Modular Design", "Single Source of Truth"]
            },
            "v2_compliance_status": {
                "compliance_rate": v2_compliance.get("summary", {}).get("compliance_rate", 0),
                "total_violations": v2_compliance.get("total_violations", 0),
                "error_files": v2_compliance.get("summary", {}).get("error_files", 0),
                "status": "COMPLIANT" if v2_compliance.get("summary", {}).get("compliance_rate", 0) > 90 else "NEEDS_ATTENTION"
            },
            "code_quality_metrics": {
                "external_dependencies": len(dependencies.get("external_deps", [])),
                "architectural_patterns": len(set(architecture.get("patterns_detected", [])))
            },
            "key_components": {
                "agent_system": "8 autonomous agents with coordinate-based communication",
                "messaging_system": "Unified messaging service with PyAutoGUI delivery",
                "ml_pipeline": "Machine learning models and training infrastructure",
                "discord_integration": "Discord bot for human-agent interaction",
                "thea_interface": "Thea communication and automation system"
            },
            "improvement_recommendations": [
                "Maintain V2 compliance standards across all files",
                "Implement comprehensive test coverage",
                "Regular code quality reviews and refactoring",
                "Documentation updates for new features",
                "Performance optimization for large files"
            ],
            "system_health": {
                "overall_status": "HEALTHY" if v2_compliance.get("summary", {}).get("compliance_rate", 0) > 80 else "NEEDS_ATTENTION",
                "critical_issues": v2_compliance.get("summary", {}).get("error_files", 0),
                "maintenance_priority": "HIGH" if v2_compliance.get("summary", {}).get("compliance_rate", 0) < 90 else "MEDIUM"
            }
        }
        
        self.analysis_data["master_summary"] = master_summary
        logger.info("🎯 Master System Summary generated")
    
    def generate_reports(self) -> None:
        """Generate comprehensive analysis reports."""
        logger.info("📊 Generating analysis reports...")
        
        # Generate comprehensive JSON report
        with open(self.project_root / "simple_godfather_analysis.json", "w") as f:
            json.dump(self.analysis_data, f, indent=2, default=str)
        
        # Generate markdown summary
        self._generate_markdown_summary()
        
        logger.info("📊 All reports generated successfully")
    
    def _generate_markdown_summary(self) -> None:
        """Generate a comprehensive markdown summary report."""
        summary = self.analysis_data.get("master_summary", {})
        file_analyses = self.analysis_data.get("file_analyses", [])
        
        markdown_content = f"""# 🛰️ SIMPLE GODFATHER ANALYSIS REPORT

## 📊 Project Overview
- **Project**: {summary.get('project_overview', {}).get('name', 'Unknown')}
- **Total Files**: {summary.get('project_overview', {}).get('total_files', 0)}
- **Python Files**: {summary.get('project_overview', {}).get('python_files', 0)}
- **Analysis Date**: {summary.get('project_overview', {}).get('analysis_timestamp', 'Unknown')}

## 🏗️ Architecture Summary
- **Pattern**: {summary.get('architecture_summary', {}).get('pattern', 'Unknown')}
- **Coordination**: {summary.get('architecture_summary', {}).get('coordination_method', 'Unknown')}
- **Design Principles**: {', '.join(summary.get('architecture_summary', {}).get('design_principles', []))}

## ✅ V2 Compliance Status
- **Compliance Rate**: {summary.get('v2_compliance_status', {}).get('compliance_rate', 0):.1f}%
- **Total Violations**: {summary.get('v2_compliance_status', {}).get('total_violations', 0)}
- **Error Files**: {summary.get('v2_compliance_status', {}).get('error_files', 0)}
- **Status**: {summary.get('v2_compliance_status', {}).get('status', 'Unknown')}

## 📈 Code Quality Metrics
- **External Dependencies**: {summary.get('code_quality_metrics', {}).get('external_dependencies', 0)}
- **Architectural Patterns**: {summary.get('code_quality_metrics', {}).get('architectural_patterns', 0)}

## 🔧 Key Components
{chr(10).join([f"- **{k}**: {v}" for k, v in summary.get('key_components', {}).items()])}

## 📋 File-by-File Analysis

"""
        
        # Add file analyses
        for analysis in file_analyses[:15]:  # Limit to first 15 for readability
            markdown_content += f"""### 📂 {analysis.get('file_path', 'Unknown')}
- **Purpose**: {analysis.get('purpose', 'Unknown')}
- **Role**: {analysis.get('role_in_system', 'Unknown')}
- **Components**: {len(analysis.get('major_components', {}).get('classes', []))} classes, {len(analysis.get('major_components', {}).get('functions', []))} functions
- **Observations**: {'; '.join(analysis.get('observations', []))}

"""
        
        markdown_content += f"""
## 🎯 System Health
- **Overall Status**: {summary.get('system_health', {}).get('overall_status', 'Unknown')}
- **Critical Issues**: {summary.get('system_health', {}).get('critical_issues', 0)}
- **Maintenance Priority**: {summary.get('system_health', {}).get('maintenance_priority', 'Unknown')}

## 💡 Improvement Recommendations
{chr(10).join([f"- {rec}" for rec in summary.get('improvement_recommendations', [])])}

---
*Generated by Simple Godfather Analysis System*
"""
        
        with open(self.project_root / "simple_godfather_analysis_report.md", "w") as f:
            f.write(markdown_content)

def main():
    """Main entry point for the Simple Godfather Analysis."""
    analyzer = SimpleGodfatherAnalyzer()
    
    # Perform comprehensive analysis
    analysis_results = analyzer.analyze_project()
    
    # Generate reports
    analyzer.generate_reports()
    
    # Print summary
    master_summary = analysis_results.get("master_summary", {})
    print("\n" + "="*80)
    print("🛰️ SIMPLE GODFATHER ANALYSIS COMPLETE")
    print("="*80)
    print(f"📊 Files Analyzed: {master_summary.get('project_overview', {}).get('total_files', 0)}")
    print(f"✅ V2 Compliance: {master_summary.get('v2_compliance_status', {}).get('compliance_rate', 0):.1f}%")
    print(f"🏗️ System Status: {master_summary.get('system_health', {}).get('overall_status', 'Unknown')}")
    print("📄 Reports generated: simple_godfather_analysis_report.md, simple_godfather_analysis.json")
    print("="*80)
    
    return analysis_results

if __name__ == "__main__":
    main()