#!/usr/bin/env python3
"""
V2 Refactoring Assistant - Automated Refactoring Tool
====================================================

Automated tool to assist with V2 compliance refactoring by analyzing
files and suggesting refactoring strategies.

Author: Agent-8 (System Architecture & Refactoring Specialist)
License: MIT
"""

import ast
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import argparse

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


class V2RefactoringAssistant:
    """Assistant for V2 compliance refactoring."""
    
    def __init__(self, project_root: str = "."):
        """Initialize refactoring assistant."""
        self.project_root = Path(project_root).resolve()
        self.violations: List[Dict[str, Any]] = []
        self.refactoring_suggestions: Dict[str, List[str]] = {}
    
    def analyze_violations(self) -> List[Dict[str, Any]]:
        """Analyze V2 compliance violations."""
        logger.info("🔍 Analyzing V2 compliance violations...")
        
        violations = []
        
        for py_file in self.project_root.rglob('*.py'):
            # Skip test files and cache directories
            if any(x in str(py_file) for x in ['test', '__pycache__', '.git', '.venv']):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                line_count = len(lines)
                
                if line_count > 400:
                    # Analyze AST for detailed metrics
                    try:
                        tree = ast.parse(content)
                        metrics = self._analyze_ast_metrics(tree)
                        
                        violation = {
                            'file': str(py_file),
                            'lines': line_count,
                            'excess': line_count - 400,
                            'severity': self._calculate_severity(line_count),
                            'metrics': metrics,
                            'suggestions': self._generate_suggestions(line_count, metrics)
                        }
                        
                        violations.append(violation)
                        
                    except SyntaxError as e:
                        logger.warning(f"Syntax error in {py_file}: {e}")
                        violations.append({
                            'file': str(py_file),
                            'lines': line_count,
                            'excess': line_count - 400,
                            'severity': 'CRITICAL',
                            'metrics': {'error': str(e)},
                            'suggestions': ['Fix syntax errors first']
                        })
                        
            except Exception as e:
                logger.error(f"Error analyzing {py_file}: {e}")
                continue
        
        # Sort by severity and line count
        violations.sort(key=lambda x: (x['severity'] == 'CRITICAL', x['excess']), reverse=True)
        
        self.violations = violations
        return violations
    
    def _analyze_ast_metrics(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze AST for detailed metrics."""
        metrics = {
            'classes': 0,
            'functions': 0,
            'methods': 0,
            'enums': 0,
            'imports': 0,
            'complex_functions': [],
            'large_classes': [],
            'deep_inheritance': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                metrics['classes'] += 1
                
                # Check for enums
                if self._is_enum_class(node):
                    metrics['enums'] += 1
                
                # Count methods
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                metrics['methods'] += len(methods)
                
                # Check for large classes
                if len(methods) > 10:
                    metrics['large_classes'].append({
                        'name': node.name,
                        'methods': len(methods),
                        'line': node.lineno
                    })
                
                # Check inheritance depth
                if len(node.bases) > 2:
                    metrics['deep_inheritance'].append({
                        'name': node.name,
                        'bases': len(node.bases),
                        'line': node.lineno
                    })
            
            elif isinstance(node, ast.FunctionDef):
                metrics['functions'] += 1
                
                # Check complexity
                complexity = self._calculate_complexity(node)
                if complexity > 10:
                    metrics['complex_functions'].append({
                        'name': node.name,
                        'complexity': complexity,
                        'line': node.lineno,
                        'parameters': len(node.args.args)
                    })
            
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                metrics['imports'] += 1
        
        return metrics
    
    def _is_enum_class(self, node: ast.ClassDef) -> bool:
        """Check if class is an enum."""
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == 'Enum':
                return True
        return False
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity
    
    def _calculate_severity(self, line_count: int) -> str:
        """Calculate violation severity."""
        if line_count > 600:
            return 'CRITICAL'
        elif line_count > 500:
            return 'HIGH'
        elif line_count > 450:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _generate_suggestions(self, line_count: int, metrics: Dict[str, Any]) -> List[str]:
        """Generate refactoring suggestions."""
        suggestions = []
        
        # File size suggestions
        if line_count > 600:
            suggestions.append("🚨 CRITICAL: Split into 3+ modules")
        elif line_count > 500:
            suggestions.append("⚠️ HIGH: Split into 2 modules")
        elif line_count > 450:
            suggestions.append("📝 MEDIUM: Extract 1-2 classes/methods")
        else:
            suggestions.append("✅ LOW: Minor refactoring needed")
        
        # Class suggestions
        if metrics.get('classes', 0) > 5:
            suggestions.append("📦 Too many classes: Extract some to separate modules")
        
        if metrics.get('large_classes'):
            for cls in metrics['large_classes']:
                suggestions.append(f"🏗️ Large class '{cls['name']}': Split into smaller classes")
        
        # Function suggestions
        if metrics.get('functions', 0) > 10:
            suggestions.append("🔧 Too many functions: Extract some to separate modules")
        
        if metrics.get('complex_functions'):
            for func in metrics['complex_functions']:
                suggestions.append(f"🧩 Complex function '{func['name']}': Break into smaller functions")
        
        # Enum suggestions
        if metrics.get('enums', 0) > 3:
            suggestions.append("📋 Too many enums: Move some to separate files")
        
        # Inheritance suggestions
        if metrics.get('deep_inheritance'):
            for cls in metrics['deep_inheritance']:
                suggestions.append(f"🌳 Deep inheritance '{cls['name']}': Simplify inheritance chain")
        
        return suggestions
    
    def generate_refactoring_plan(self) -> Dict[str, Any]:
        """Generate comprehensive refactoring plan."""
        if not self.violations:
            self.analyze_violations()
        
        plan = {
            'timestamp': datetime.now().isoformat(),
            'total_violations': len(self.violations),
            'severity_breakdown': self._calculate_severity_breakdown(),
            'refactoring_phases': self._create_refactoring_phases(),
            'agent_assignments': self._create_agent_assignments(),
            'timeline': self._create_timeline()
        }
        
        return plan
    
    def _calculate_severity_breakdown(self) -> Dict[str, int]:
        """Calculate severity breakdown."""
        breakdown = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for violation in self.violations:
            severity = violation['severity']
            breakdown[severity] += 1
        
        return breakdown
    
    def _create_refactoring_phases(self) -> List[Dict[str, Any]]:
        """Create refactoring phases."""
        phases = []
        
        # Phase 1: Critical files
        critical_files = [v for v in self.violations if v['severity'] == 'CRITICAL']
        if critical_files:
            phases.append({
                'phase': 1,
                'name': 'Critical Files Refactoring',
                'files': critical_files,
                'timeline': '6 cycles',
                'agents': ['Agent-2', 'Agent-7', 'Agent-8']
            })
        
        # Phase 2: High priority files
        high_files = [v for v in self.violations if v['severity'] == 'HIGH']
        if high_files:
            phases.append({
                'phase': 2,
                'name': 'High Priority Files Refactoring',
                'files': high_files,
                'timeline': '12 cycles',
                'agents': ['Agent-1', 'Agent-3', 'Agent-4', 'Agent-5']
            })
        
        # Phase 3: Medium priority files
        medium_files = [v for v in self.violations if v['severity'] == 'MEDIUM']
        if medium_files:
            phases.append({
                'phase': 3,
                'name': 'Medium Priority Files Refactoring',
                'files': medium_files,
                'timeline': '36 cycles',
                'agents': ['Agent-6', 'Agent-7', 'Agent-8']
            })
        
        # Phase 4: Low priority files
        low_files = [v for v in self.violations if v['severity'] == 'LOW']
        if low_files:
            phases.append({
                'phase': 4,
                'name': 'Low Priority Files Refactoring',
                'files': low_files,
                'timeline': '72 cycles',
                'agents': ['All Agents']
            })
        
        return phases
    
    def _create_agent_assignments(self) -> Dict[str, List[str]]:
        """Create agent assignments."""
        assignments = {
            'Agent-2': [],  # Security & Quality
            'Agent-7': [],  # Refactoring Specialist
            'Agent-8': [],  # Architecture
            'Agent-1': [],  # Team Coordination
            'Agent-3': [],  # Data Management
            'Agent-4': [],  # Operations
            'Agent-5': [],  # Quality Assurance
            'Agent-6': []   # Code Quality
        }
        
        # Assign files based on agent expertise
        for violation in self.violations:
            file_path = violation['file']
            
            if 'security' in file_path.lower() or 'auth' in file_path.lower():
                assignments['Agent-2'].append(file_path)
            elif 'core' in file_path.lower() or 'main' in file_path.lower():
                assignments['Agent-7'].append(file_path)
            elif 'architecture' in file_path.lower() or 'infrastructure' in file_path.lower():
                assignments['Agent-8'].append(file_path)
            elif 'ml' in file_path.lower() or 'data' in file_path.lower():
                assignments['Agent-3'].append(file_path)
            elif 'service' in file_path.lower() or 'api' in file_path.lower():
                assignments['Agent-4'].append(file_path)
            elif 'validation' in file_path.lower() or 'test' in file_path.lower():
                assignments['Agent-5'].append(file_path)
            elif 'tool' in file_path.lower() or 'utility' in file_path.lower():
                assignments['Agent-6'].append(file_path)
            else:
                # Default assignment
                assignments['Agent-1'].append(file_path)
        
        return assignments
    
    def _create_timeline(self) -> Dict[str, str]:
        """Create refactoring timeline."""
        return {
            'Phase 1 (Critical)': '6 cycles',
            'Phase 2 (High)': '12 cycles',
            'Phase 3 (Medium)': '36 cycles',
            'Phase 4 (Low)': '72 cycles',
            'Total Completion': '72 cycles'
        }
    
    def generate_refactoring_report(self, output_file: Optional[str] = None) -> str:
        """Generate refactoring report."""
        if not self.violations:
            self.analyze_violations()
        
        plan = self.generate_refactoring_plan()
        
        report_file = output_file or self.project_root / 'v2_refactoring_report.json'
        
        with open(report_file, 'w') as f:
            json.dump(plan, f, indent=2)
        
        logger.info(f"📄 Refactoring report generated: {report_file}")
        return str(report_file)
    
    def print_summary(self) -> None:
        """Print refactoring summary."""
        if not self.violations:
            self.analyze_violations()
        
        plan = self.generate_refactoring_plan()
        
        print(f"\n🚨 V2 Compliance Refactoring Summary")
        print(f"=" * 50)
        print(f"Total Violations: {plan['total_violations']}")
        
        print(f"\n📊 Severity Breakdown:")
        for severity, count in plan['severity_breakdown'].items():
            print(f"  {severity}: {count} files")
        
        print(f"\n🎯 Refactoring Phases:")
        for phase in plan['refactoring_phases']:
            print(f"  Phase {phase['phase']}: {phase['name']}")
            print(f"    Files: {len(phase['files'])}")
            print(f"    Timeline: {phase['timeline']}")
            print(f"    Agents: {', '.join(phase['agents'])}")
        
        print(f"\n🤖 Agent Assignments:")
        for agent, files in plan['agent_assignments'].items():
            if files:
                print(f"  {agent}: {len(files)} files")
        
        print(f"\n⏰ Timeline:")
        for phase, timeline in plan['timeline'].items():
            print(f"  {phase}: {timeline}")


def main():
    """Main entry point for V2 refactoring assistant."""
    parser = argparse.ArgumentParser(description='V2 Refactoring Assistant')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--analyze', action='store_true', help='Analyze violations')
    parser.add_argument('--plan', action='store_true', help='Generate refactoring plan')
    parser.add_argument('--report', action='store_true', help='Generate refactoring report')
    parser.add_argument('--output', help='Output file for report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    assistant = V2RefactoringAssistant(args.project_root)
    
    if args.analyze or args.plan or args.report:
        assistant.print_summary()
        
        if args.report:
            report_file = assistant.generate_refactoring_report(args.output)
            print(f"\n📄 Detailed report saved to: {report_file}")
    else:
        assistant.print_summary()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
