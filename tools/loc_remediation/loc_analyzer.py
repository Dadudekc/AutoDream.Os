import logging
logger = logging.getLogger(__name__)
"""
LOC Analyzer - V2 Compliance Module
=================================

Main coordinator for LOC analysis and remediation.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: LOC Analysis
"""
import argparse
from pathlib import Path
from typing import Any
from .loc_remediator import LOCRemediator
from .loc_scanner import LOCScanner


class LOCAnalyzer:
    """Main coordinator for LOC analysis and remediation."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.scanner = LOCScanner()
        self.remediator = LOCRemediator(project_root)

    def analyze_project(self, target_dir: Path=None) ->dict[str, Any]:
        """Analyze project for LOC violations."""
        if target_dir is None:
            target_dir = self.project_root
        logger.info(f'🔍 Scanning {target_dir} for LOC violations...')
        violations = self.scanner.scan_directory(target_dir)
        plan = self.remediator.generate_remediation_plan(violations)
        return {'target_directory': str(target_dir), 'violations':
            violations, 'remediation_plan': plan, 'summary': self.
            _generate_summary(plan)}

    def _generate_summary(self, plan: dict[str, Any]) ->dict[str, Any]:
        """Generate summary of analysis results."""
        return {'total_violations': plan['total_violations'],
            'file_violations': len(plan['file_violations']),
            'class_violations': len(plan['class_violations']),
            'function_violations': len(plan['function_violations']),
            'high_priority': len([r for r in plan['recommendations'] if r.
            get('priority') == 'high']), 'medium_priority': len([r for r in
            plan['recommendations'] if r.get('priority') == 'medium']),
            'low_priority': len([r for r in plan['recommendations'] if r.
            get('priority') == 'low'])}

    def generate_reports(self, analysis_data: dict[str, Any]) ->dict[str, Path
        ]:
        """Generate all remediation reports."""
        plan = analysis_data['remediation_plan']
        plan_path = self.remediator.save_remediation_plan(plan)
        report_path = self.remediator.generate_human_readable_report(plan)
        return {'json_plan': plan_path, 'text_report': report_path}

    def print_summary(self, analysis_data: dict[str, Any]) ->None:
        """Print analysis summary to console."""
        summary = analysis_data['summary']
        logger.info('\n' + '=' * 60)
        logger.info('📊 LOC VIOLATION ANALYSIS SUMMARY')
        logger.info('=' * 60)
        logger.info(f"Target Directory: {analysis_data['target_directory']}")
        logger.info(f"Total Violations: {summary['total_violations']}")
        logger.info(f"File Violations: {summary['file_violations']}")
        logger.info(f"Class Violations: {summary['class_violations']}")
        logger.info(f"Function Violations: {summary['function_violations']}")
        logger.info(f"High Priority Issues: {summary['high_priority']}")
        logger.info(f"Medium Priority Issues: {summary['medium_priority']}")
        logger.info(f"Low Priority Issues: {summary['low_priority']}")
        logger.info('=' * 60)


def main():
    """Main entry point for LOC remediation tool."""
    parser = argparse.ArgumentParser(description=
        'Auto-Remediate LOC Violations')
    parser.add_argument('--target', type=str, help=
        'Target directory to analyze')
    parser.add_argument('--dry-run', action='store_true', help=
        'Show what would be done')
    parser.add_argument('--apply-fixes', action='store_true', help=
        'Apply auto-fixes')
    args = parser.parse_args()
    project_root = Path('.')
    target_dir = Path(args.target) if args.target else project_root
    analyzer = LOCAnalyzer(project_root)
    analysis_data = analyzer.analyze_project(target_dir)
    report_paths = analyzer.generate_reports(analysis_data)
    analyzer.print_summary(analysis_data)
    logger.info('\n📄 Reports generated:')
    logger.info(f"  JSON Plan: {report_paths['json_plan']}")
    logger.info(f"  Text Report: {report_paths['text_report']}")
    summary = analysis_data['summary']
    if summary['high_priority'] > 0:
        logger.info('\n⚠️  High priority LOC violations found!')
        exit(1)
    else:
        logger.info('\n✅ LOC analysis completed successfully!')
        exit(0)


if __name__ == '__main__':
    main()
