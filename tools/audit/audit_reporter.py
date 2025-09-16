import logging
logger = logging.getLogger(__name__)
"""
Audit Reporter - V2 Compliance Module
==================================

Focused module for generating audit reports.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: Audit Reporting
"""
import json
from pathlib import Path
from typing import Any


class AuditReporter:
    """Generates reports for audit results."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.reports_dir = project_root / 'runtime' / 'reports'
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_audit_report(self, scan_results: dict[str, Any], analysis:
        dict[str, Any]) ->dict[str, Any]:
        """Generate comprehensive audit report."""
        report = {'report_type': 'audit_cleanup', 'timestamp': scan_results
            .get('timestamp', ''), 'scan_summary': self.
            _generate_scan_summary(scan_results), 'analysis_summary': self.
            _generate_analysis_summary(analysis), 'cleanup_opportunities':
            analysis.get('cleanup_opportunities', []), 'risk_assessment':
            analysis.get('risk_assessment', {}), 'recommendations':
            analysis.get('recommendations', []), 'raw_data': {
            'scan_results': scan_results, 'analysis': analysis}}
        return report

    def _generate_scan_summary(self, scan_results: dict[str, Any]) ->dict[
        str, Any]:
        """Generate scan summary."""
        return {'total_files': scan_results.get('total_files', 0),
            'total_size': scan_results.get('total_size', 0), 'file_types':
            len(scan_results.get('file_counts', {})), 'duplicate_groups':
            len([g for g in scan_results.get('duplicate_groups', {}).values
            () if len(g) > 1]), 'temp_files': len(scan_results.get(
            'temp_files', [])), 'versioned_files': len(scan_results.get(
            'versioned_files', []))}

    def _generate_analysis_summary(self, analysis: dict[str, Any]) ->dict[
        str, Any]:
        """Generate analysis summary."""
        return {'cleanup_opportunities': len(analysis.get(
            'cleanup_opportunities', [])), 'high_priority_opportunities':
            len([o for o in analysis.get('cleanup_opportunities', []) if o.
            get('priority') == 'high']), 'overall_risk': analysis.get(
            'risk_assessment', {}).get('overall_risk', 'unknown'),
            'py_file_count': analysis.get('risk_assessment', {}).get(
            'py_file_count', 0), 'potential_savings': sum(o.get(
            'potential_savings', 0) for o in analysis.get(
            'cleanup_opportunities', []))}

    def save_json_report(self, report: dict[str, Any], filename: str=None
        ) ->Path:
        """Save JSON audit report."""
        if filename is None:
            timestamp = report.get('timestamp', '').replace(':', '-').replace(
                ' ', '_')
            filename = f'audit_report_{timestamp}.json'
        report_path = self.reports_dir / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        return report_path

    def save_markdown_report(self, report: dict[str, Any], filename: str=None
        ) ->Path:
        """Save Markdown audit report."""
        if filename is None:
            timestamp = report.get('timestamp', '').replace(':', '-').replace(
                ' ', '_')
            filename = f'audit_report_{timestamp}.md'
        report_path = self.reports_dir / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_markdown_content(report))
        return report_path

    def _generate_markdown_content(self, report: dict[str, Any]) ->str:
        """Generate Markdown report content."""
        content = []
        content.append('# Audit Cleanup Report')
        content.append(f"**Generated:** {report.get('timestamp', 'N/A')}")
        content.append('')
        scan_summary = report.get('scan_summary', {})
        content.append('## Scan Summary')
        content.append(
            f"- **Total Files:** {scan_summary.get('total_files', 0):,}")
        content.append(
            f"- **Total Size:** {self._format_size(scan_summary.get('total_size', 0))}"
            )
        content.append(f"- **File Types:** {scan_summary.get('file_types', 0)}"
            )
        content.append(
            f"- **Duplicate Groups:** {scan_summary.get('duplicate_groups', 0)}"
            )
        content.append(f"- **Temp Files:** {scan_summary.get('temp_files', 0)}"
            )
        content.append(
            f"- **Versioned Files:** {scan_summary.get('versioned_files', 0)}")
        content.append('')
        analysis_summary = report.get('analysis_summary', {})
        content.append('## Analysis Summary')
        content.append(
            f"- **Cleanup Opportunities:** {analysis_summary.get('cleanup_opportunities', 0)}"
            )
        content.append(
            f"- **High Priority:** {analysis_summary.get('high_priority_opportunities', 0)}"
            )
        content.append(
            f"- **Overall Risk:** {analysis_summary.get('overall_risk', 'unknown').upper()}"
            )
        content.append(
            f"- **Python Files:** {analysis_summary.get('py_file_count', 0)}")
        content.append(
            f"- **Potential Savings:** {self._format_size(analysis_summary.get('potential_savings', 0))}"
            )
        content.append('')
        opportunities = report.get('cleanup_opportunities', [])
        if opportunities:
            content.append('## Cleanup Opportunities')
            for i, opp in enumerate(opportunities, 1):
                priority = opp.get('priority', 'medium')
                description = opp.get('description', 'No description')
                savings = self._format_size(opp.get('potential_savings', 0))
                risk = opp.get('risk', 'unknown')
                content.append(f'### {i}. {description}')
                content.append(f'- **Priority:** {priority.upper()}')
                content.append(f'- **Potential Savings:** {savings}')
                content.append(f'- **Risk:** {risk.upper()}')
                content.append('')
        risk_assessment = report.get('risk_assessment', {})
        if risk_assessment:
            content.append('## Risk Assessment')
            content.append(
                f"- **Overall Risk:** {risk_assessment.get('overall_risk', 'unknown').upper()}"
                )
            content.append(
                f"- **Python File Risk:** {risk_assessment.get('py_file_risk', 'unknown').upper()}"
                )
            cleanup_risks = risk_assessment.get('cleanup_risks', [])
            if cleanup_risks:
                content.append('- **Specific Risks:**')
                for risk in cleanup_risks:
                    content.append(f'  - {risk}')
            content.append('')
        recommendations = report.get('recommendations', [])
        if recommendations:
            content.append('## Recommendations')
            for i, rec in enumerate(recommendations, 1):
                content.append(f'{i}. {rec}')
            content.append('')
        return '\n'.join(content)

    def _format_size(self, size_bytes: int) ->str:
        """Format size in bytes to human readable format."""
        if size_bytes == 0:
            return '0 B'
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = float(size_bytes)
        unit_index = 0
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        return f'{size:.1f} {units[unit_index]}'

    def print_audit_summary(self, report: dict[str, Any]) ->None:
        """Print audit summary to console."""
        logger.info('\n' + '=' * 70)
        logger.info('📋 AUDIT CLEANUP REPORT')
        logger.info('=' * 70)
        scan_summary = report.get('scan_summary', {})
        logger.info(f"Total Files: {scan_summary.get('total_files', 0):,}")
        logger.info(
            f"Total Size: {self._format_size(scan_summary.get('total_size', 0))}"
            )
        logger.info(f"File Types: {scan_summary.get('file_types', 0)}")
        logger.info(
            f"Duplicate Groups: {scan_summary.get('duplicate_groups', 0)}")
        logger.info(f"Temp Files: {scan_summary.get('temp_files', 0)}")
        analysis_summary = report.get('analysis_summary', {})
        logger.info(
            f"\nCleanup Opportunities: {analysis_summary.get('cleanup_opportunities', 0)}"
            )
        logger.info(
            f"High Priority: {analysis_summary.get('high_priority_opportunities', 0)}"
            )
        logger.info(
            f"Overall Risk: {analysis_summary.get('overall_risk', 'unknown').upper()}"
            )
        logger.info(
            f"Potential Savings: {self._format_size(analysis_summary.get('potential_savings', 0))}"
            )
        recommendations = report.get('recommendations', [])
        if recommendations:
            logger.info('\n💡 RECOMMENDATIONS:')
            for i, rec in enumerate(recommendations, 1):
                logger.info(f'  {i}. {rec}')
        logger.info('=' * 70)
