"""
Dashboard HTML Generator - DEPRECATED (V2 VIOLATION FIXED)
===========================================================

⚠️ DEPRECATED: This file was 614 lines (V2 violation).
Refactored into 3 V2-compliant modules:
  - dashboard_styles.py (81 lines)
  - dashboard_charts.py (187 lines)
  - dashboard_html_generator_refactored.py (381 lines)

Use dashboard_html_generator_refactored.py instead.

Original Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-10-11
License: MIT
"""

from typing import Any


class DashboardHTMLGenerator:
    """Generates HTML for compliance dashboards."""

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
        {self.get_css()}
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
    {self.generate_chart_scripts(data) if has_history else ''}
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

    def get_css(self) -> str:
        """Get CSS styles."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: #333; }
        .container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); padding: 40px; }
        header { text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 3px solid #667eea; }
        h1 { font-size: 2.5em; color: #667eea; margin-bottom: 10px; }
        .subtitle { font-size: 1.2em; color: #666; margin-bottom: 10px; }
        .scan-date { color: #999; font-size: 0.9em; }
        .score-card { text-align: center; margin: 40px 0; }
        .score-circle { width: 200px; height: 200px; border-radius: 50%; margin: 0 auto; display: flex; flex-direction: column; justify-content: center; align-items: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .score-circle.excellent { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
        .score-circle.good { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .score-circle.poor { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
        .score-value { font-size: 4em; font-weight: bold; color: white; }
        .score-label { color: rgba(255,255,255,0.9); font-size: 0.9em; margin-top: 5px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 40px 0; }
        .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        .metric-card h3 { font-size: 1.1em; margin-bottom: 15px; opacity: 0.9; }
        .metric-value { font-size: 3em; font-weight: bold; }
        .violations-section, .complexity-section, .top-violators-section, .suggestions-section { margin: 40px 0; }
        h2 { color: #667eea; margin-bottom: 20px; font-size: 1.8em; }
        .violations-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .violation-card { padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .violation-card.critical { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); color: white; }
        .violation-card.major { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); color: #333; }
        .violation-card.minor { background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%); color: white; }
        .violation-card.high { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); color: white; }
        .violation-card.medium { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); color: #333; }
        .violation-card.low { background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%); color: white; }
        .violation-card h4 { margin-bottom: 10px; font-size: 1.2em; }
        .violation-count { font-size: 2.5em; font-weight: bold; margin: 10px 0; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        thead { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        th, td { padding: 15px; text-align: left; }
        tbody tr:nth-child(even) { background: #f8f9fa; }
        tbody tr:hover { background: #e9ecef; }
        .badge { padding: 5px 10px; border-radius: 5px; font-size: 0.85em; font-weight: bold; }
        .badge.high { background: #dc3545; color: white; }
        .badge.medium { background: #ffc107; color: #333; }
        .badge.low { background: #28a745; color: white; }
        .badge.yes { background: #17a2b8; color: white; }
        .badge.no { background: #6c757d; color: white; }
        .confidence-bar { width: 100px; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; display: inline-block; }
        .confidence-fill { height: 100%; background: linear-gradient(90deg, #56ab2f 0%, #a8e063 100%); }
        footer { text-align: center; margin-top: 60px; padding-top: 30px; border-top: 2px solid #e9ecef; color: #999; }
        footer p { margin: 5px 0; }
        .week-comparison-section, .historical-trends-section { background: white; padding: 40px; margin: 30px 0; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .week-comparison-section h2, .historical-trends-section h2 { color: #333; margin-bottom: 10px; }
        .comparison-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-top: 20px; }
        .comparison-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.15); }
        .comparison-card h4 { margin: 0 0 15px 0; font-size: 1.1em; opacity: 0.9; }
        .comparison-values { margin: 15px 0; }
        .current-value { font-size: 2.5em; font-weight: bold; line-height: 1; }
        .previous-value { font-size: 0.9em; opacity: 0.8; margin-top: 5px; }
        .change-indicator { font-size: 1.3em; font-weight: bold; margin-top: 10px; }
        .charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 30px; margin-top: 30px; }
        .chart-container { background: #f8f9fa; padding: 25px; border-radius: 12px; box-shadow: 0 3px 10px rgba(0,0,0,0.08); }
        .chart-container h3 { color: #333; margin: 0 0 20px 0; font-size: 1.1em; text-align: center; }
        """

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

    def generate_chart_scripts(self, data: Any) -> str:
        """Generate JavaScript for interactive charts."""
        if not hasattr(data, "get") or "historical" not in data:
            return ""

        historical = data["historical"]
        if not historical or not historical.get("dates"):
            return ""

        # Convert Python data to JavaScript arrays
        import json

        dates_json = json.dumps(historical["dates"])
        v2_rates_json = json.dumps(historical["v2_rates"])
        complexity_rates_json = json.dumps(historical["complexity_rates"])
        scores_json = json.dumps(historical["overall_scores"])
        critical_json = json.dumps(historical["critical_violations"])
        major_json = json.dumps(historical["major_violations"])

        return f"""
    <script>
        // Compliance & Complexity Chart
        new Chart(document.getElementById('complianceChart'), {{
            type: 'line',
            data: {{
                labels: {dates_json},
                datasets: [
                    {{
                        label: 'V2 Compliance %',
                        data: {v2_rates_json},
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    }},
                    {{
                        label: 'Complexity Compliance %',
                        data: {complexity_rates_json},
                        borderColor: '#764ba2',
                        backgroundColor: 'rgba(118, 75, 162, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    }}
                ]
            }},
            options: {{
                responsive: true,
                interaction: {{
                    mode: 'index',
                    intersect: false
                }},
                plugins: {{
                    legend: {{
                        position: 'top'
                    }},
                    tooltip: {{
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {{ size: 14 }},
                        bodyFont: {{ size: 13 }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{
                            display: true,
                            text: 'Compliance Rate (%)'
                        }}
                    }}
                }}
            }}
        }});

        // Overall Score Chart
        new Chart(document.getElementById('scoreChart'), {{
            type: 'line',
            data: {{
                labels: {dates_json},
                datasets: [{{
                    label: 'Overall Quality Score',
                    data: {scores_json},
                    borderColor: '#f093fb',
                    backgroundColor: 'rgba(240, 147, 251, 0.2)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'top'
                    }},
                    tooltip: {{
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{
                            display: true,
                            text: 'Score'
                        }}
                    }}
                }}
            }}
        }});

        // Violations Chart
        new Chart(document.getElementById('violationsChart'), {{
            type: 'bar',
            data: {{
                labels: {dates_json},
                datasets: [
                    {{
                        label: 'Critical Violations',
                        data: {critical_json},
                        backgroundColor: 'rgba(220, 53, 69, 0.7)',
                        borderColor: '#dc3545',
                        borderWidth: 2
                    }},
                    {{
                        label: 'Major Violations',
                        data: {major_json},
                        backgroundColor: 'rgba(255, 193, 7, 0.7)',
                        borderColor: '#ffc107',
                        borderWidth: 2
                    }}
                ]
            }},
            options: {{
                responsive: true,
                interaction: {{
                    mode: 'index',
                    intersect: false
                }},
                plugins: {{
                    legend: {{
                        position: 'top'
                    }},
                    tooltip: {{
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Number of Violations'
                        }}
                    }}
                }}
            }}
        }});
    </script>"""

    def get_css_full(self) -> str:
        """Get full CSS styles for dashboard."""
        return self.get_css()

    def get_score_class(self, score: float) -> str:
        """Get CSS class for score."""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        else:
            return "poor"

    def get_priority_badge(self, score: int) -> str:
        """Get priority badge HTML."""
        if score >= 10:
            return '<span class="badge high">HIGH</span>'
        elif score >= 5:
            return '<span class="badge medium">MEDIUM</span>'
        else:
            return '<span class="badge low">LOW</span>'
