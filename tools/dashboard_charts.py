#!/usr/bin/env python3
"""
Dashboard Charts - JavaScript Chart Generation
==============================================

JavaScript generation for interactive Chart.js dashboards.

V2 Compliance: Extracted from dashboard_html_generator.py (614 lines → modular)
Author: Agent-1 (refactored from Agent-6's work)
Original Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Date: 2025-10-11
License: MIT
"""

from typing import Any


class DashboardCharts:
    """Generates JavaScript for interactive Chart.js visualizations."""

    @staticmethod
    def generate_chart_scripts(data: Any) -> str:
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
