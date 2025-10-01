#!/usr/bin/env python3
"""
Memory Leak Report Generator - Phase 4
======================================

Advanced report generation for memory leak analysis.
Supports multiple output formats and comprehensive visualization.

Author: Agent-7 (Web Development Expert)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions, KISS principle
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.observability.memory.cli import MemoryMonitorCLI

logger = logging.getLogger(__name__)


# ============================================================
# REPORT FORMATTERS
# ============================================================

class JSONReportFormatter:
    """Format reports as JSON"""
    
    def format(self, data: Dict[str, Any]) -> str:
        """Format data as JSON"""
        return json.dumps(data, indent=2, default=str)


class TextReportFormatter:
    """Format reports as human-readable text"""
    
    def format(self, data: Dict[str, Any]) -> str:
        """Format data as text"""
        lines = []
        lines.append("=" * 80)
        lines.append("MEMORY LEAK ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {data.get('timestamp', 'N/A')}")
        lines.append("")
        
        # Summary section
        summary = data.get('summary', {})
        lines.append("SUMMARY")
        lines.append("-" * 80)
        for key, value in summary.items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        
        # Analysis section
        analysis = data.get('analysis', {})
        if analysis:
            lines.append("ANALYSIS")
            lines.append("-" * 80)
            for key, value in analysis.items():
                if isinstance(value, (list, dict)):
                    lines.append(f"  {key}:")
                    lines.append(f"    {json.dumps(value, indent=4)}")
                else:
                    lines.append(f"  {key}: {value}")
            lines.append("")
        
        # Recommendations
        recommendations = data.get('recommendations', [])
        if recommendations:
            lines.append("RECOMMENDATIONS")
            lines.append("-" * 80)
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"  {i}. {rec}")
            lines.append("")
        
        lines.append("=" * 80)
        return "\n".join(lines)


class HTMLReportFormatter:
    """Format reports as HTML"""
    
    def format(self, data: Dict[str, Any]) -> str:
        """Format data as HTML"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Memory Leak Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; border-bottom: 2px solid #ddd; padding-bottom: 5px; }}
        .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
        .analysis {{ margin: 20px 0; }}
        .recommendations {{ background: #e8f4f8; padding: 15px; border-radius: 5px; }}
        .timestamp {{ color: #999; font-size: 0.9em; }}
        pre {{ background: #f5f5f5; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>Memory Leak Analysis Report</h1>
    <p class="timestamp">Generated: {data.get('timestamp', 'N/A')}</p>
    
    <h2>Summary</h2>
    <div class="summary">
        <pre>{json.dumps(data.get('summary', {}), indent=2)}</pre>
    </div>
    
    <h2>Analysis</h2>
    <div class="analysis">
        <pre>{json.dumps(data.get('analysis', {}), indent=2)}</pre>
    </div>
    
    <h2>Recommendations</h2>
    <div class="recommendations">
        <ul>
"""
        # Add recommendations
        for rec in data.get('recommendations', []):
            html += f"            <li>{rec}</li>\n"
        
        html += """        </ul>
    </div>
</body>
</html>"""
        return html


# ============================================================
# REPORT GENERATOR
# ============================================================

class MemoryLeakReportGenerator:
    """Generate comprehensive memory leak reports"""
    
    def __init__(self):
        """Initialize report generator"""
        self.cli = MemoryMonitorCLI()
        self.formatters = {
            'json': JSONReportFormatter(),
            'text': TextReportFormatter(),
            'html': HTMLReportFormatter(),
        }
    
    def generate_report(self, output_format: str = 'json', output_file: str = None) -> int:
        """Generate memory leak report"""
        try:
            # Get report data from CLI
            report_data = self._collect_report_data()
            
            # Format report
            formatter = self.formatters.get(output_format, self.formatters['json'])
            formatted_report = formatter.format(report_data)
            
            # Output report
            if output_file:
                Path(output_file).write_text(formatted_report)
                print(f"✅ Report saved to: {output_file}")
            else:
                print(formatted_report)
            
            return 0
        
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            print(f"❌ Error: {e}")
            return 1
    
    def _collect_report_data(self) -> Dict[str, Any]:
        """Collect data for report"""
        # Get current analysis
        analysis = self.cli.analyzer.analyze_system()
        
        # Build comprehensive report
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_memory_mb': analysis.get('system_stats', {}).get('memory_usage', 0) / (1024*1024),
                'total_objects': analysis.get('system_stats', {}).get('object_count', 0),
                'leaks_detected': len(analysis.get('leaks', [])),
                'recommendations_count': len(analysis.get('recommendations', [])),
            },
            'analysis': analysis,
            'recommendations': analysis.get('recommendations', []),
        }
        
        return report_data


# ============================================================
# CLI INTERFACE
# ============================================================

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Memory Leak Report Generator - Phase 4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Generate JSON report to stdout
  %(prog)s -o report.json           # Save JSON report to file
  %(prog)s -f text                  # Generate text report
  %(prog)s -f html -o report.html   # Generate HTML report
        """
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['json', 'text', 'html'],
        default='json',
        help='Output format (default: json)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s'
    )
    
    # Generate report
    generator = MemoryLeakReportGenerator()
    return generator.generate_report(args.format, args.output)


if __name__ == '__main__':
    sys.exit(main())

