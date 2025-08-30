#!/usr/bin/env python3
"""
CSS Generator - V2 Dashboard System

This module handles CSS generation for dashboard styling.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from .dashboard_types import DashboardLayout


class CSSGenerator:
    """Handles CSS generation for dashboard styling"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.CSSGenerator")
    
    def generate_css(self, layout: DashboardLayout) -> str:
        """Generate CSS styles for the dashboard."""
        return f"""
        /* Dashboard Styles */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--bg-color); color: var(--text-color); transition: all 0.3s ease; }}
        .dashboard-container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .dashboard-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding: 20px; background: var(--header-bg); border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .dashboard-grid {{ display: grid; gap: {layout.widget_spacing}px; margin-bottom: 30px; }}
        .widget {{ background: var(--widget-bg); border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease; }}
        .widget:hover {{ transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); }}
        .widget-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid var(--border-color); }}
        .widget-content {{ min-height: 200px; display: flex; align-items: center; justify-content: center; }}
        .chart-placeholder {{ text-align: center; color: var(--muted-color); }}
        .chart-type {{ display: block; font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
        .metric-name {{ display: block; font-size: 14px; opacity: 0.7; }}
        .btn {{ padding: 8px 16px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; transition: all 0.2s ease; }}
        .btn-secondary {{ background: var(--btn-secondary-bg); color: var(--btn-secondary-text); }}
        .btn-small {{ padding: 4px 8px; font-size: 12px; }}
        
        /* Theme Variables */
        :root {{ --bg-color: #1a1a1a; --text-color: #ffffff; --header-bg: #2d2d2d; --widget-bg: #333333; --border-color: #444444; --muted-color: #888888; --btn-secondary-bg: #555555; --btn-secondary-text: #ffffff; }}
        .theme-light {{ --bg-color: #f5f5f5; --text-color: #333333; --header-bg: #ffffff; --widget-bg: #ffffff; --border-color: #e0e0e0; --muted-color: #666666; --btn-secondary-bg: #e0e0e0; --btn-secondary-text: #333333; }}
        """
    
    def generate_responsive_css(self, layout: DashboardLayout) -> str:
        """Generate responsive CSS for mobile devices."""
        if not layout.responsive:
            return ""
        
        return """
        /* Responsive Design */
        @media (max-width: 768px) { .dashboard-container { padding: 10px; } .dashboard-header { flex-direction: column; gap: 15px; text-align: center; } .dashboard-grid { grid-template-columns: 1fr; gap: 15px; } .widget { padding: 15px; } }
        @media (max-width: 480px) { .widget-header { flex-direction: column; gap: 10px; text-align: center; } .btn { padding: 6px 12px; font-size: 12px; } }
        """
    
    def generate_animation_css(self) -> str:
        """Generate CSS animations for dashboard elements."""
        return """
        /* Animations */
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideIn { from { transform: translateX(-100%); } to { transform: translateX(0); } }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
        .widget { animation: fadeIn 0.5s ease-out; }
        .dashboard-header { animation: slideIn 0.3s ease-out; }
        .refreshing { animation: pulse 1s infinite; }
        """
