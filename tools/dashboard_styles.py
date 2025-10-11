#!/usr/bin/env python3
"""
Dashboard Styles - CSS Generation
=================================

CSS styles for compliance dashboards.

V2 Compliance: Extracted from dashboard_html_generator.py (614 lines → modular)
Author: Agent-1 (refactored from Agent-6's work)
Original Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Date: 2025-10-11
License: MIT
"""


class DashboardStyles:
    """Generates CSS styles for compliance dashboards."""

    @staticmethod
    def get_css() -> str:
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
