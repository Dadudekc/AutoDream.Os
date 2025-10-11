#!/usr/bin/env python3
"""
Dashboard HTML Generator - V2 COMPLIANT REFACTORED VERSION
===========================================================

⚠️ REFACTORED: dashboard_html_generator.py was 614 lines.
Split into 3 V2-compliant modules:
  - dashboard_styles.py (69 lines) - CSS generation
  - dashboard_charts.py (180 lines) - JavaScript charts
  - dashboard_html_generator_refactored.py (245 lines) - Main HTML generation

HTML generation for compliance dashboards.

Original Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-10-11
License: MIT
"""

from typing import Any

from dashboard_charts import DashboardCharts
from dashboard_styles import DashboardStyles


class DashboardHTMLGenerator:
    """Generates HTML for compliance dashboards."""

    def __init__(self):
        """Initialize dashboard generator with styles and charts."""
        self.styles = DashboardStyles()
        self.charts = DashboardCharts()

    def generate_html(self, data: Any) -> str:
        """Generate complete HTML dashboard."""
        has_history = hasattr(data, "get") and "historical" in data
        has_comparison = hasattr(data, "get") and "week_comparison" in data

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>V2 Compliance Dashboard - {data.scan_date if hasattr(data, 'scan_date') else 'Report'}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        {self.styles.get_css()}
    </style>
</head>
<body>
    <div class="container">
        {self.generate_header(data)}
        {self.generate_score_card(data)}
        {self.generate_metrics_grid(data)}
        {self.generate_week_comparison(data) if has_comparison else ''}
        {self.generate_historical_trends(data) if has_history else ''}
        {self.generate_violations_section(data)}
        {self.generate_complexity_section(data)}
        {self.generate_top_violators(data)}
        {self.generate_suggestions(data)}
        {self.generate_footer()}
    </div>
    {self.charts.generate_chart_scripts(data) if has_history else ''}
</body>
</html>"""

    def generate_header(self, data: Any) -> str:
        """Generate header HTML."""
        return f"""
        <header>
            <h1>🐝 V2 Compliance Dashboard</h1>
            <p class="subtitle">Agent_Cellphone_V2 Quality Gates Report</p>
            <p class="scan-date">Scan Date: {data.scan_date}</p>
        </header>"""

    def generate_score_card(self, data: Any) -> str:
        """Generate score card HTML."""
        score_class = self.get_score_class(data.overall_score)
        return f"""
        <div class="score-card">
            <div class="score-circle {score_class}">
                <div class="score-value">{data.overall_score}</div>
                <div class="score-label">Overall Quality Score</div>
            </div>
        </div>"""

    def generate_metrics_grid(self, data: Any) -> str:
        """Generate metrics grid HTML."""
        return f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>📁 Files Scanned</h3>
                <div class="metric-value">{data.total_files}</div>
            </div>
            <div class="metric-card">
                <h3>✅ V2 Compliance</h3>
                <div class="metric-value">{data.v2_compliance_rate:.1f}%</div>
            </div>
            <div class="metric-card">
                <h3>🧠 Complexity</h3>
                <div class="metric-value">{data.complexity_compliance_rate:.1f}%</div>
            </div>
        </div>"""

    def generate_violations_section(self, data: Any) -> str:
        """Generate V2 violations section."""
        return f"""
        <div class="violations-section">
            <h2>🚨 V2 Violations Summary</h2>
            <div class="violations-grid">
                <div class="violation-card critical">
                    <h4>🔴 CRITICAL</h4>
                    <div class="violation-count">{data.critical_violations}</div>
                    <p>Files >600 lines</p>
                </div>
                <div class="violation-card major">
                    <h4>🟡 MAJOR</h4>
                    <div class="violation-count">{data.major_violations}</div>
                    <p>V2 rule violations</p>
                </div>
                <div class="violation-card minor">
                    <h4>🟢 MINOR</h4>
                    <div class="violation-count">{data.minor_violations}</div>
                    <p>Guideline violations</p>
                </div>
            </div>
        </div>"""

    def generate_complexity_section(self, data: Any) -> str:
        """Generate complexity section."""
        return f"""
        <div class="complexity-section">
            <h2>📊 Complexity Violations</h2>
            <div class="violations-grid">
                <div class="violation-card high">
                    <h4>🔴 HIGH</h4>
                    <div class="violation-count">{data.high_complexity}</div>
                    <p>≥2x threshold</p>
                </div>
                <div class="violation-card medium">
                    <h4>🟡 MEDIUM</h4>
                    <div class="violation-count">{data.medium_complexity}</div>
                    <p>1.5-2x threshold</p>
                </div>
                <div class="violation-card low">
                    <h4>🟢 LOW</h4>
                    <div class="violation-count">{data.low_complexity}</div>
                    <p>1-1.5x threshold</p>
                </div>
            </div>
        </div>"""

    def generate_top_violators(self, data: Any) -> str:
        """Generate top violators table."""
        rows = self.generate_violators_rows(data.top_violators)
        return f"""
        <div class="top-violators-section">
            <h2>🎯 Top Violators</h2>
            <table class="violators-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>File</th>
                        <th>V2 Issues</th>
                        <th>Complexity</th>
                        <th>Suggestion</th>
                        <th>Priority</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>"""

    def generate_suggestions(self, data: Any) -> str:
        """Generate suggestions table."""
        rows = self.generate_suggestions_rows(data.suggestions_summary)
        return f"""
        <div class="suggestions-section">
            <h2>💡 Refactoring Suggestions</h2>
            <table class="suggestions-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>File</th>
                        <th>Current Lines</th>
                        <th>Estimated Result</th>
                        <th>Modules</th>
                        <th>Confidence</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>"""

    def generate_footer(self) -> str:
        """Generate footer HTML."""
        return """
        <footer>
            <p>Generated by Agent-6 Quality Gates Suite</p>
            <p>🐝 WE ARE SWARM - Intelligent Quality Automation</p>
        </footer>"""

    def generate_violators_rows(self, violators: list[dict[str, Any]]) -> str:
        """Generate HTML rows for violators table."""
        rows = []
        for i, v in enumerate(violators, 1):
            priority = self.get_priority_badge(v["total_score"])
            suggestion = (
                '<span class="badge yes">Yes</span>'
                if v["has_suggestion"]
                else '<span class="badge no">No</span>'
            )

            rows.append(
                f"""
                <tr>
                    <td>{i}</td>
                    <td><strong>{v["file"]}</strong></td>
                    <td>{v["v2_violations"]}</td>
                    <td>{v["complexity_violations"]}</td>
                    <td>{suggestion}</td>
                    <td>{priority}</td>
                </tr>
            """
            )

        return "\n".join(rows)

    def generate_suggestions_rows(self, suggestions: list[dict[str, Any]]) -> str:
        """Generate HTML rows for suggestions table."""
        rows = []
        for i, s in enumerate(suggestions, 1):
            reduction = s["current_lines"] - s["estimated_lines"]
            reduction_pct = (reduction / s["current_lines"] * 100) if s["current_lines"] > 0 else 0
            confidence_pct = s["confidence"] * 100

            rows.append(
                f"""
                <tr>
                    <td>{i}</td>
                    <td><strong>{s["file"]}</strong></td>
                    <td>{s["current_lines"]}</td>
                    <td>{s["estimated_lines"]} <span style="color: #28a745;">(-{reduction_pct:.0f}%)</span></td>
                    <td>{s["modules"]}</td>
                    <td>
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: {confidence_pct}%"></div>
                        </div>
                        {confidence_pct:.0f}%
                    </td>
                </tr>
            """
            )

        return "\n".join(rows)

    def get_score_class(self, score: float) -> str:
        """Get CSS class for quality score."""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        else:
            return "poor"

    def get_priority_badge(self, score: int) -> str:
        """Get HTML for priority badge."""
        if score >= 10:
            return '<span class="badge high">HIGH</span>'
        elif score >= 5:
            return '<span class="badge medium">MEDIUM</span>'
        else:
            return '<span class="badge low">LOW</span>'

    def generate_week_comparison(self, data: Any) -> str:
        """Generate week-over-week comparison section."""
        if not hasattr(data, "get") or "week_comparison" not in data:
            return ""

        comparison = data["week_comparison"]
        if not comparison:
            return ""

        current = comparison["current"]
        previous = comparison["previous"]
        changes = comparison["changes"]
        days = comparison["days_apart"]

        # Generate change indicators
        def get_change_indicator(value, reverse=False):
            if value > 0:
                return (
                    f"<span style='color: {'#dc3545' if reverse else '#28a745'}'>↑ +{value}</span>"
                )
            elif value < 0:
                return (
                    f"<span style='color: {'#28a745' if reverse else '#dc3545'}'>↓ {value}</span>"
                )
            else:
                return "<span style='color: #6c757d'>→ 0</span>"

        return f"""
        <div class="week-comparison-section">
            <h2>📊 Week-over-Week Comparison</h2>
            <p class="subtitle">Comparing last {days} days of progress</p>
            <div class="comparison-grid">
                <div class="comparison-card">
                    <h4>V2 Compliance</h4>
                    <div class="comparison-values">
                        <div class="current-value">{current['v2_rate']:.1f}%</div>
                        <div class="previous-value">was {previous['v2_rate']:.1f}%</div>
                    </div>
                    <div class="change-indicator">{get_change_indicator(changes['v2_rate'])}</div>
                </div>
                <div class="comparison-card">
                    <h4>Complexity</h4>
                    <div class="comparison-values">
                        <div class="current-value">{current['complexity_rate']:.1f}%</div>
                        <div class="previous-value">was {previous['complexity_rate']:.1f}%</div>
                    </div>
                    <div class="change-indicator">{get_change_indicator(changes['complexity_rate'])}</div>
                </div>
                <div class="comparison-card">
                    <h4>Overall Score</h4>
                    <div class="comparison-values">
                        <div class="current-value">{current['score']:.1f}</div>
                        <div class="previous-value">was {previous['score']:.1f}</div>
                    </div>
                    <div class="change-indicator">{get_change_indicator(changes['score'])}</div>
                </div>
                <div class="comparison-card">
                    <h4>Critical Violations</h4>
                    <div class="comparison-values">
                        <div class="current-value">{current['critical']}</div>
                        <div class="previous-value">was {previous['critical']}</div>
                    </div>
                    <div class="change-indicator">{get_change_indicator(changes['critical'], reverse=True)}</div>
                </div>
            </div>
        </div>"""

    def generate_historical_trends(self, data: Any) -> str:
        """Generate historical trends section with charts."""
        if not hasattr(data, "get") or "historical" not in data:
            return ""

        historical = data["historical"]
        if not historical or not historical.get("dates"):
            return ""

        snapshot_count = len(historical["dates"])
        date_range = (
            f"{historical['dates'][0]} to {historical['dates'][-1]}"
            if snapshot_count > 1
            else historical["dates"][0]
        )

        return f"""
        <div class="historical-trends-section">
            <h2>📈 Historical Trends</h2>
            <p class="subtitle">{snapshot_count} snapshots from {date_range}</p>
            
            <div class="charts-grid">
                <div class="chart-container">
                    <h3>V2 Compliance & Complexity Over Time</h3>
                    <canvas id="complianceChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3>Overall Quality Score Trend</h3>
                    <canvas id="scoreChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3>Violations Trend</h3>
                    <canvas id="violationsChart"></canvas>
                </div>
            </div>
        </div>"""
