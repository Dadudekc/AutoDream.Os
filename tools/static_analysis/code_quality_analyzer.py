#!/usr/bin/env python3
"""
Code Quality Analyzer - Comprehensive Code Quality Assessment
===========================================================

Advanced code quality analysis tool that combines multiple static analysis tools
to provide comprehensive code quality assessment and recommendations.

Author: Agent-2 (Security & Quality Specialist)
License: MIT
"""

import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import argparse

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


class CodeQualityAnalyzer:
    """Comprehensive code quality analyzer for Python projects."""
    
    def __init__(self, project_root: str = "."):
        """Initialize code quality analyzer."""
        self.project_root = Path(project_root).resolve()
        self.results: Dict[str, Any] = {}
        self.quality_metrics = {
            'complexity': 0,
            'maintainability': 0,
            'readability': 0,
            'testability': 0,
            'performance': 0
        }
    
    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive code quality analysis."""
        logger.info("🔍 Starting comprehensive code quality analysis...")
        
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'tools': {},
            'metrics': {},
            'violations': {}
        }
        
        # Run individual quality tools
        analysis_results['tools']['ruff'] = self._run_ruff_analysis()
        analysis_results['tools']['pylint'] = self._run_pylint_analysis()
        analysis_results['tools']['mypy'] = self._run_mypy_analysis()
        analysis_results['tools']['flake8'] = self._run_flake8_analysis()
        analysis_results['tools']['complexity'] = self._run_complexity_analysis()
        
        # Calculate quality metrics
        analysis_results['metrics'] = self._calculate_quality_metrics(analysis_results['tools'])
        
        # Generate violation summary
        analysis_results['violations'] = self._generate_violation_summary(analysis_results['tools'])
        
        # Generate recommendations
        analysis_results['recommendations'] = self._generate_recommendations(analysis_results)
        
        self.results = analysis_results
        return analysis_results
    
    def _run_ruff_analysis(self) -> Dict[str, Any]:
        """Run Ruff linter analysis."""
        logger.info("🔍 Running Ruff analysis...")
        
        try:
            cmd = ['ruff', 'check', '--output-format=json', str(self.project_root / 'src')]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            ruff_data = []
            if result.stdout:
                try:
                    ruff_data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    ruff_data = [{'raw_output': result.stdout}]
            
            return {
                'status': 'success',
                'data': ruff_data,
                'command': ' '.join(cmd)
            }
            
        except Exception as e:
            logger.error(f"Ruff analysis failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'data': []
            }
    
    def _run_pylint_analysis(self) -> Dict[str, Any]:
        """Run Pylint analysis."""
        logger.info("🔍 Running Pylint analysis...")
        
        try:
            cmd = [
                'pylint', '--output-format=json',
                '--disable=C0114,C0115,C0116',  # Disable docstring warnings
                str(self.project_root / 'src')
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            pylint_data = []
            if result.stdout:
                try:
                    pylint_data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    pylint_data = [{'raw_output': result.stdout}]
            
            return {
                'status': 'success',
                'data': pylint_data,
                'command': ' '.join(cmd)
            }
            
        except Exception as e:
            logger.error(f"Pylint analysis failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'data': []
            }
    
    def _run_mypy_analysis(self) -> Dict[str, Any]:
        """Run MyPy type checking analysis."""
        logger.info("🔍 Running MyPy analysis...")
        
        try:
            cmd = [
                'mypy', '--json-report', '/tmp/mypy-report.json',
                str(self.project_root / 'src')
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            mypy_data = []
            try:
                with open('/tmp/mypy-report.json', 'r') as f:
                    mypy_data = json.load(f)
            except FileNotFoundError:
                mypy_data = [{'raw_output': result.stdout}]
            
            return {
                'status': 'success',
                'data': mypy_data,
                'command': ' '.join(cmd)
            }
            
        except Exception as e:
            logger.error(f"MyPy analysis failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'data': []
            }
    
    def _run_flake8_analysis(self) -> Dict[str, Any]:
        """Run Flake8 analysis."""
        logger.info("🔍 Running Flake8 analysis...")
        
        try:
            cmd = [
                'flake8', '--format=%(path)s:%(row)d:%(col)d: %(code)s %(text)s',
                str(self.project_root / 'src')
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            flake8_data = []
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split(':', 3)
                        if len(parts) >= 4:
                            flake8_data.append({
                                'file': parts[0],
                                'line': int(parts[1]),
                                'column': int(parts[2]),
                                'code': parts[3].split()[0],
                                'message': ' '.join(parts[3].split()[1:])
                            })
            
            return {
                'status': 'success',
                'data': flake8_data,
                'command': ' '.join(cmd)
            }
            
        except Exception as e:
            logger.error(f"Flake8 analysis failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'data': []
            }
    
    def _run_complexity_analysis(self) -> Dict[str, Any]:
        """Run complexity analysis using radon."""
        logger.info("🔍 Running complexity analysis...")
        
        try:
            # Check if radon is available
            subprocess.run(['radon', '--version'], capture_output=True, check=True)
            
            cmd = [
                'radon', 'cc', '--json', '--min', 'B',
                str(self.project_root / 'src')
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            complexity_data = []
            if result.stdout:
                try:
                    complexity_data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    complexity_data = [{'raw_output': result.stdout}]
            
            return {
                'status': 'success',
                'data': complexity_data,
                'command': ' '.join(cmd)
            }
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Radon not available, skipping complexity analysis...")
            return {
                'status': 'skipped',
                'reason': 'Radon not installed',
                'data': []
            }
        except Exception as e:
            logger.error(f"Complexity analysis failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'data': []
            }
    
    def _calculate_quality_metrics(self, tools_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall quality metrics."""
        metrics = {
            'overall_score': 0,
            'code_style': 0,
            'type_safety': 0,
            'complexity': 0,
            'maintainability': 0,
            'total_violations': 0,
            'critical_violations': 0,
            'warning_violations': 0,
            'info_violations': 0
        }
        
        # Analyze Ruff results
        if tools_results['ruff']['status'] == 'success':
            ruff_data = tools_results['ruff']['data']
            for issue in ruff_data:
                metrics['total_violations'] += 1
                severity = issue.get('code', '')
                if severity.startswith('E') or severity.startswith('F'):
                    metrics['critical_violations'] += 1
                elif severity.startswith('W'):
                    metrics['warning_violations'] += 1
                else:
                    metrics['info_violations'] += 1
        
        # Analyze Pylint results
        if tools_results['pylint']['status'] == 'success':
            pylint_data = tools_results['pylint']['data']
            for issue in pylint_data:
                metrics['total_violations'] += 1
                severity = issue.get('type', '')
                if severity == 'error':
                    metrics['critical_violations'] += 1
                elif severity == 'warning':
                    metrics['warning_violations'] += 1
                else:
                    metrics['info_violations'] += 1
        
        # Analyze MyPy results
        if tools_results['mypy']['status'] == 'success':
            mypy_data = tools_results['mypy']['data']
            if 'files' in mypy_data:
                for file_data in mypy_data['files'].values():
                    if 'messages' in file_data:
                        for message in file_data['messages']:
                            metrics['total_violations'] += 1
                            severity = message.get('severity', '')
                            if severity == 'error':
                                metrics['critical_violations'] += 1
                            elif severity == 'warning':
                                metrics['warning_violations'] += 1
                            else:
                                metrics['info_violations'] += 1
        
        # Calculate overall score (0-100)
        if metrics['total_violations'] == 0:
            metrics['overall_score'] = 100
        else:
            # Penalize based on violation count and severity
            critical_penalty = metrics['critical_violations'] * 10
            warning_penalty = metrics['warning_violations'] * 5
            info_penalty = metrics['info_violations'] * 1
            
            total_penalty = critical_penalty + warning_penalty + info_penalty
            metrics['overall_score'] = max(0, 100 - total_penalty)
        
        # Calculate individual metric scores
        metrics['code_style'] = max(0, 100 - (metrics['warning_violations'] * 2))
        metrics['type_safety'] = max(0, 100 - (metrics['critical_violations'] * 5))
        metrics['complexity'] = 85  # Default, would be calculated from radon
        metrics['maintainability'] = (metrics['code_style'] + metrics['type_safety']) / 2
        
        return metrics
    
    def _generate_violation_summary(self, tools_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate violation summary."""
        summary = {
            'by_tool': {},
            'by_severity': {
                'critical': 0,
                'warning': 0,
                'info': 0
            },
            'by_category': {
                'style': 0,
                'type': 0,
                'complexity': 0,
                'security': 0
            }
        }
        
        # Count violations by tool
        for tool_name, tool_result in tools_results.items():
            if tool_result['status'] == 'success':
                summary['by_tool'][tool_name] = len(tool_result['data'])
        
        return summary
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate quality improvement recommendations."""
        recommendations = []
        metrics = analysis_results['metrics']
        
        if metrics['overall_score'] < 70:
            recommendations.append("🚨 CRITICAL: Overall code quality score is below 70%")
        
        if metrics['critical_violations'] > 10:
            recommendations.append("⚠️  WARNING: High number of critical violations detected")
        
        if metrics['warning_violations'] > 50:
            recommendations.append("⚠️  WARNING: High number of warning violations detected")
        
        if metrics['code_style'] < 80:
            recommendations.append("📝 RECOMMENDATION: Improve code style consistency")
        
        if metrics['type_safety'] < 80:
            recommendations.append("🔒 RECOMMENDATION: Improve type annotations and type safety")
        
        if metrics['overall_score'] >= 90:
            recommendations.append("✅ EXCELLENT: Code quality is very high")
        elif metrics['overall_score'] >= 80:
            recommendations.append("✅ GOOD: Code quality is good")
        elif metrics['overall_score'] >= 70:
            recommendations.append("⚠️  FAIR: Code quality needs improvement")
        else:
            recommendations.append("🚨 POOR: Code quality requires immediate attention")
        
        return recommendations
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate code quality report."""
        if not self.results:
            self.run_comprehensive_analysis()
        
        report_file = output_file or self.project_root / 'code_quality_report.json'
        
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"📄 Code quality report generated: {report_file}")
        return str(report_file)


def main():
    """Main entry point for code quality analyzer."""
    parser = argparse.ArgumentParser(description='Comprehensive Code Quality Analyzer')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--output', help='Output file for quality report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    analyzer = CodeQualityAnalyzer(args.project_root)
    results = analyzer.run_comprehensive_analysis()
    
    # Print summary
    metrics = results['metrics']
    print(f"\n🔍 Code Quality Analysis Summary:")
    print(f"Overall Score: {metrics['overall_score']:.1f}/100")
    print(f"Total Violations: {metrics['total_violations']}")
    print(f"Critical: {metrics['critical_violations']}")
    print(f"Warnings: {metrics['warning_violations']}")
    print(f"Info: {metrics['info_violations']}")
    
    if results['recommendations']:
        print(f"\n📋 Recommendations:")
        for rec in results['recommendations']:
            print(f"  {rec}")
    
    # Generate report
    report_file = analyzer.generate_report(args.output)
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    return 0 if metrics['overall_score'] >= 70 else 1


if __name__ == '__main__':
    sys.exit(main())



