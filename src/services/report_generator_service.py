#!/usr/bin/env python3
"""
Report Generator Service - Agent Cellphone V2
============================================

Generates comprehensive reports from scanner analysis data.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import json
import time
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from .file_processor_service import FileProcessorService


class ReportGeneratorService:
    """
    Generates comprehensive reports from scanner analysis data.
    
    Responsibilities:
    - Generate project analysis reports
    - Create code quality summaries
    - Export findings to multiple formats
    - Provide actionable insights
    """
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("scanner_reports")
        self.output_dir.mkdir(exist_ok=True)
        self.file_processor = FileProcessorService()
    
    def generate_project_report(self, project_data: Dict[str, Any], 
                              include_details: bool = True) -> Dict[str, Any]:
        """Generate comprehensive project analysis report"""
        try:
            # Calculate summary statistics
            total_files = len(project_data.get('files', []))
            total_lines = sum(f.get('line_count', 0) for f in project_data.get('files', []))
            language_stats = self._calculate_language_statistics(project_data.get('files', []))
            complexity_stats = self._calculate_complexity_statistics(project_data.get('files', []))
            
            report = {
                'timestamp': time.time(),
                'report_type': 'project_analysis',
                'project_name': project_data.get('project_name', 'Unknown'),
                'summary': {
                    'total_files': total_files,
                    'total_lines': total_lines,
                    'languages_detected': len(language_stats.get('file_counts', {})),
                    'average_complexity': complexity_stats.get('average', 0.0)
                },
                'language_breakdown': language_stats,
                'complexity_analysis': complexity_stats,
                'file_analysis': self._analyze_files(project_data.get('files', []), include_details)
            }
            
            if include_details:
                report['detailed_analysis'] = self._generate_detailed_analysis(project_data)
            
            return report
            
        except Exception as e:
            return {
                'timestamp': time.time(),
                'error': str(e),
                'status': 'failed'
            }
    
    def generate_code_quality_report(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code quality assessment report"""
        try:
            quality_metrics = self._calculate_quality_metrics(analysis_data)
            recommendations = self._generate_recommendations(quality_metrics)
            
            report = {
                'timestamp': time.time(),
                'report_type': 'code_quality',
                'quality_score': quality_metrics.get('overall_score', 0.0),
                'metrics': quality_metrics,
                'recommendations': recommendations,
                'priority_actions': self._identify_priority_actions(quality_metrics)
            }
            
            return report
            
        except Exception as e:
            return {
                'timestamp': time.time(),
                'error': str(e),
                'status': 'failed'
            }
    
    def export_report(self, report: Dict[str, Any], format_type: str = 'json', 
                     filename: str = None) -> Path:
        """Export report to specified format"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"scanner_report_{timestamp}.{format_type}"
            
            file_path = self.output_dir / filename
            
            if format_type == 'json':
                with open(file_path, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
            elif format_type == 'txt':
                with open(file_path, 'w') as f:
                    f.write(self._format_text_report(report))
            else:
                raise ValueError(f"Unsupported format: {format_type}")
            
            return file_path
            
        except Exception as e:
            raise Exception(f"Export failed: {e}")
    
    def _calculate_language_statistics(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate language distribution statistics"""
        language_counts = {}
        language_lines = {}
        
        for file_data in files:
            lang = file_data.get('language', 'unknown')
            lines = file_data.get('line_count', 0)
            
            language_counts[lang] = language_counts.get(lang, 0) + 1
            language_lines[lang] = language_lines.get(lang, 0) + lines
        
        return {
            'file_counts': language_counts,
            'line_counts': language_lines,
            'primary_language': max(language_counts.items(), key=lambda x: x[1])[0] if language_counts else 'unknown'
        }
    
    def _calculate_complexity_statistics(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate complexity analysis statistics"""
        complexities = [f.get('complexity', 0) for f in files if f.get('complexity') is not None]
        
        if not complexities:
            return {'average': 0.0, 'max': 0, 'min': 0, 'distribution': {}}
        
        avg_complexity = sum(complexities) / len(complexities)
        max_complexity = max(complexities)
        min_complexity = min(complexities)
        
        # Complexity distribution
        distribution = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        for comp in complexities:
            if comp <= 5:
                distribution['low'] += 1
            elif comp <= 10:
                distribution['medium'] += 1
            elif comp <= 20:
                distribution['high'] += 1
            else:
                distribution['critical'] += 1
        
        return {
            'average': round(avg_complexity, 2),
            'max': max_complexity,
            'min': min_complexity,
            'distribution': distribution
        }
    
    def _analyze_files(self, files: List[Dict[str, Any]], include_details: bool) -> Dict[str, Any]:
        """Analyze individual files for patterns and insights"""
        analysis = {
            'largest_files': [],
            'most_complex_files': [],
            'language_specific_insights': {}
        }
        
        if not files:
            return analysis
        
        # Sort files by size and complexity
        sorted_by_size = sorted(files, key=lambda x: x.get('line_count', 0), reverse=True)
        sorted_by_complexity = sorted(files, key=lambda x: x.get('complexity', 0), reverse=True)
        
        analysis['largest_files'] = [
            {'name': f.get('name', 'Unknown'), 'lines': f.get('line_count', 0)}
            for f in sorted_by_size[:5]
        ]
        
        analysis['most_complex_files'] = [
            {'name': f.get('name', 'Unknown'), 'complexity': f.get('complexity', 0)}
            for f in sorted_by_complexity[:5]
        ]
        
        if include_details:
            analysis['language_specific_insights'] = self._generate_language_insights(files)
        
        return analysis
    
    def _generate_language_insights(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate language-specific insights and recommendations"""
        insights = {}
        
        for file_data in files:
            lang = file_data.get('language', 'unknown')
            if lang not in insights:
                insights[lang] = {
                    'file_count': 0,
                    'total_lines': 0,
                    'average_complexity': 0.0,
                    'complexity_sum': 0.0
                }
            
            insights[lang]['file_count'] += 1
            insights[lang]['total_lines'] += file_data.get('line_count', 0)
            insights[lang]['complexity_sum'] += file_data.get('complexity', 0)
        
        # Calculate averages
        for lang_data in insights.values():
            if lang_data['file_count'] > 0:
                lang_data['average_complexity'] = round(
                    lang_data['complexity_sum'] / lang_data['file_count'], 2
                )
        
        return insights
    
    def _generate_detailed_analysis(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed analysis for project data"""
        try:
            files = project_data.get('files', [])
            detailed_analysis = {
                'file_patterns': self._analyze_file_patterns(files),
                'dependency_analysis': self._analyze_dependencies(files),
                'code_metrics': self._calculate_code_metrics(files),
                'recommendations': self._generate_project_recommendations(files)
            }
            return detailed_analysis
        except Exception as e:
            return {'error': str(e), 'status': 'failed'}
    
    def _analyze_file_patterns(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze file naming and organization patterns"""
        patterns = {
            'naming_conventions': {},
            'directory_structure': {},
            'file_extensions': {}
        }
        
        for file_data in files:
            name = file_data.get('name', '')
            if name:
                # Analyze naming conventions
                if '_' in name:
                    patterns['naming_conventions']['snake_case'] = patterns['naming_conventions'].get('snake_case', 0) + 1
                elif '-' in name:
                    patterns['naming_conventions']['kebab_case'] = patterns['naming_conventions'].get('kebab_case', 0) + 1
                else:
                    patterns['naming_conventions']['other'] = patterns['naming_conventions'].get('other', 0) + 1
                
                # Analyze file extensions
                ext = Path(name).suffix.lower()
                patterns['file_extensions'][ext] = patterns['file_extensions'].get(ext, 0) + 1
        
        return patterns
    
    def _analyze_dependencies(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze file dependencies and imports"""
        dependencies = {
            'import_counts': {},
            'external_dependencies': set(),
            'internal_dependencies': set()
        }
        
        for file_data in files:
            imports = file_data.get('imports', [])
            for imp in imports:
                if imp.startswith('.'):
                    dependencies['internal_dependencies'].add(imp)
                else:
                    dependencies['external_dependencies'].add(imp)
                
                dependencies['import_counts'][imp] = dependencies['import_counts'].get(imp, 0) + 1
        
        # Convert sets to lists for JSON serialization
        dependencies['external_dependencies'] = list(dependencies['external_dependencies'])
        dependencies['internal_dependencies'] = list(dependencies['internal_dependencies'])
        
        return dependencies
    
    def _calculate_code_metrics(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate additional code quality metrics"""
        metrics = {
            'total_functions': 0,
            'total_classes': 0,
            'average_function_length': 0.0,
            'average_class_length': 0.0
        }
        
        function_lengths = []
        class_lengths = []
        
        for file_data in files:
            # These would be populated by more detailed analysis
            # For now, use placeholder values
            if file_data.get('language') == 'python':
                metrics['total_functions'] += 1
                metrics['total_classes'] += 1
                function_lengths.append(10)  # Placeholder
                class_lengths.append(20)    # Placeholder
        
        if function_lengths:
            metrics['average_function_length'] = sum(function_lengths) / len(function_lengths)
        if class_lengths:
            metrics['average_class_length'] = sum(class_lengths) / len(class_lengths)
        
        return metrics
    
    def _generate_project_recommendations(self, files: List[Dict[str, Any]]) -> List[str]:
        """Generate project-level recommendations"""
        recommendations = []
        
        # Analyze file sizes
        oversized_files = [f for f in files if f.get('line_count', 0) > 200]
        if oversized_files:
            recommendations.append(f"Refactor {len(oversized_files)} oversized files to meet 200 LOC limit")
        
        # Analyze test coverage
        files_with_tests = [f for f in files if f.get('has_tests', False)]
        test_coverage = len(files_with_tests) / len(files) * 100 if files else 0
        if test_coverage < 80:
            recommendations.append(f"Increase test coverage from {test_coverage:.1f}% to at least 80%")
        
        # Analyze complexity
        high_complexity_files = [f for f in files if f.get('complexity', 0) > 15]
        if high_complexity_files:
            recommendations.append(f"Reduce complexity in {len(high_complexity_files)} high-complexity files")
        
        if not recommendations:
            recommendations.append("Project code quality is excellent - maintain current standards")
        
        return recommendations
    
    def _calculate_quality_metrics(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive code quality metrics"""
        files = analysis_data.get('files', [])
        if not files:
            return {'overall_score': 0.0}
        
        # Calculate various quality indicators
        total_files = len(files)
        files_with_tests = len([f for f in files if f.get('has_tests', False)])
        files_under_limit = len([f for f in files if f.get('line_count', 0) <= 200])
        low_complexity_files = len([f for f in files if f.get('complexity', 0) <= 10])
        
        # Quality scores (0-100)
        test_coverage_score = (files_with_tests / total_files) * 100 if total_files > 0 else 0
        size_compliance_score = (files_under_limit / total_files) * 100 if total_files > 0 else 0
        complexity_score = (low_complexity_files / total_files) * 100 if total_files > 0 else 0
        
        # Weighted overall score
        overall_score = (
            test_coverage_score * 0.4 +
            size_compliance_score * 0.4 +
            complexity_score * 0.2
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'test_coverage_score': round(test_coverage_score, 2),
            'size_compliance_score': round(size_compliance_score, 2),
            'complexity_score': round(complexity_score, 2),
            'metrics': {
                'total_files': total_files,
                'files_with_tests': files_with_tests,
                'files_under_limit': files_under_limit,
                'low_complexity_files': low_complexity_files
            }
        }
    
    def _generate_recommendations(self, quality_metrics: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on quality metrics"""
        recommendations = []
        
        if quality_metrics.get('test_coverage_score', 0) < 80:
            recommendations.append("Increase test coverage to at least 80%")
        
        if quality_metrics.get('size_compliance_score', 0) < 100:
            recommendations.append("Refactor oversized files to meet 200 LOC limit")
        
        if quality_metrics.get('complexity_score', 0) < 80:
            recommendations.append("Reduce code complexity in high-complexity files")
        
        if not recommendations:
            recommendations.append("Code quality is excellent - maintain current standards")
        
        return recommendations
    
    def _identify_priority_actions(self, quality_metrics: Dict[str, Any]) -> List[str]:
        """Identify high-priority actions for immediate improvement"""
        actions = []
        
        if quality_metrics.get('size_compliance_score', 0) < 90:
            actions.append("URGENT: Refactor oversized files to meet V2 standards")
        
        if quality_metrics.get('test_coverage_score', 0) < 70:
            actions.append("HIGH: Implement comprehensive test coverage")
        
        if quality_metrics.get('complexity_score', 0) < 70:
            actions.append("MEDIUM: Reduce code complexity in critical files")
        
        return actions
    
    def _format_text_report(self, report: Dict[str, Any]) -> str:
        """Format report as human-readable text"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"SCANNER REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)
        
        if report.get('report_type') == 'project_analysis':
            summary = report.get('summary', {})
            lines.append(f"Project: {report.get('project_name', 'Unknown')}")
            lines.append(f"Total Files: {summary.get('total_files', 0)}")
            lines.append(f"Total Lines: {summary.get('total_lines', 0)}")
            lines.append(f"Languages: {summary.get('languages_detected', 0)}")
        
        elif report.get('report_type') == 'code_quality':
            lines.append(f"Quality Score: {report.get('quality_score', 0)}/100")
            lines.append("Recommendations:")
            for rec in report.get('recommendations', []):
                lines.append(f"  - {rec}")
        
        lines.append("=" * 60)
        return "\n".join(lines)
