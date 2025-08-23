#!/usr/bin/env python3
"""
Dashboard CSS Generator - Agent Cellphone V2
===========================================

CSS generation functionality for the dashboard system.
Follows V2 coding standards: ≤300 LOC, OOP design, SRP
"""

import logging
from typing import Dict, Any

from .dashboard_core import DashboardLayout

logger = logging.getLogger(__name__)


class DashboardCSSGenerator:
    """Generates CSS styles for dashboard components."""

    def __init__(self, layout: DashboardLayout):
        self.layout = layout
        self._theme_colors = self._get_theme_colors()
        logger.info("Dashboard CSS generator initialized")

    def _get_theme_colors(self) -> Dict[str, Dict[str, str]]:
        """Get color schemes for different themes."""
        return {
            "dark": {
                "bg": "#1a1a1a",
                "surface": "#2d2d2d",
                "primary": "#4a9eff",
                "text": "#ffffff",
                "text_secondary": "#b0b0b0",
                "border": "#404040",
                "success": "#00c851",
                "warning": "#ffbb33",
                "danger": "#ff4444",
            },
            "light": {
                "bg": "#f5f5f5",
                "surface": "#ffffff",
                "primary": "#2196f3",
                "text": "#333333",
                "text_secondary": "#666666",
                "border": "#e0e0e0",
                "success": "#4caf50",
                "warning": "#ff9800",
                "danger": "#f44336",
            },
        }

    def generate_main_css(self) -> str:
        """Generate the main CSS for the dashboard."""
        colors = self._theme_colors[self.layout.theme]

        css = f"""
        /* Dashboard Main Styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: {colors['bg']};
            color: {colors['text']};
            line-height: 1.6;
        }}

        {self._generate_header_css(colors)}
        {self._generate_container_css(colors)}
        {self._generate_widget_css(colors)}
        {self._generate_footer_css(colors)}
        {self._generate_settings_css(colors)}
        {self._generate_utilities_css(colors)}
        """

        return css

    def _generate_header_css(self, colors: Dict[str, str]) -> str:
        """Generate CSS for the dashboard header."""
        return f"""
        .dashboard-header {{
            background-color: {colors['surface']};
            border-bottom: 1px solid {colors['border']};
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .dashboard-header h1 {{
            color: {colors['primary']};
            font-size: 1.5rem;
            font-weight: 600;
        }}

        .dashboard-controls {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .connection-status {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .status-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: {colors['warning']};
        }}

        .status-dot.connected {{
            background-color: {colors['success']};
        }}

        .status-dot.disconnected {{
            background-color: {colors['danger']};
        }}

        button {{
            background-color: {colors['primary']};
            color: {colors['text']};
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
        }}

        button:hover {{
            background-color: {colors['primary']}dd;
        }}"""

    def _generate_container_css(self, colors: Dict[str, str]) -> str:
        """Generate CSS for the dashboard container."""
        return f"""
        .dashboard-container {{
            display: grid;
            grid-template-columns: repeat({self.layout.columns}, 1fr);
            gap: {self.layout.widget_spacing}px;
            padding: 2rem;
            min-height: calc(100vh - 140px);
        }}

        @media (max-width: 768px) {{
            .dashboard-container {{
                grid-template-columns: 1fr;
                padding: 1rem;
            }}
        }}"""

    def _generate_widget_css(self, colors: Dict[str, str]) -> str:
        """Generate CSS for dashboard widgets."""
        return f"""
        .widget {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .widget-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid {colors['border']};
        }}

        .widget-title {{
            color: {colors['text']};
            font-size: 1.1rem;
            font-weight: 600;
        }}

        .widget-controls {{
            display: flex;
            gap: 0.5rem;
        }}

        .widget-controls button {{
            background: none;
            border: 1px solid {colors['border']};
            padding: 0.25rem 0.5rem;
            font-size: 0.8rem;
        }}

        .widget-content {{
            min-height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .chart-canvas {{
            width: 100% !important;
            height: 100% !important;
        }}

        .gauge-container {{
            position: relative;
            text-align: center;
        }}

        .gauge-value {{
            font-size: 2rem;
            font-weight: bold;
            color: {colors['primary']};
        }}

        .gauge-unit {{
            font-size: 1rem;
            color: {colors['text_secondary']};
        }}

        .table-container {{
            overflow-x: auto;
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .data-table th,
        .data-table td {{
            padding: 0.5rem;
            text-align: left;
            border-bottom: 1px solid {colors['border']};
        }}

        .data-table th {{
            background-color: {colors['bg']};
            font-weight: 600;
        }}

        .widget-footer {{
            margin-top: 1rem;
            padding-top: 0.5rem;
            border-top: 1px solid {colors['border']};
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: {colors['text_secondary']};
        }}"""

    def _generate_footer_css(self, colors: Dict[str, str]) -> str:
        """Generate CSS for the dashboard footer."""
        return f"""
        .dashboard-footer {{
            background-color: {colors['surface']};
            border-top: 1px solid {colors['border']};
            padding: 1rem 2rem;
            margin-top: auto;
        }}

        .footer-info {{
            display: flex;
            justify-content: space-between;
            color: {colors['text_secondary']};
            font-size: 0.9rem;
        }}"""

    def _generate_settings_css(self, colors: Dict[str, str]) -> str:
        """Generate CSS for the settings panel."""
        return f"""
        .settings-panel {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }}

        .settings-panel.hidden {{
            display: none;
        }}

        .settings-content {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
        }}

        .setting-group {{
            margin-bottom: 1rem;
        }}

        .setting-group label {{
            display: block;
            margin-bottom: 0.5rem;
            color: {colors['text']};
        }}

        .setting-group input,
        .setting-group select {{
            width: 100%;
            padding: 0.5rem;
            border: 1px solid {colors['border']};
            border-radius: 4px;
            background-color: {colors['bg']};
            color: {colors['text']};
        }}

        .config-modal {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1001;
        }}

        .config-modal.hidden {{
            display: none;
        }}

        .config-content {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 2rem;
            max-width: 400px;
            width: 90%;
        }}

        .config-group {{
            margin-bottom: 1rem;
        }}

        .config-buttons {{
            display: flex;
            gap: 1rem;
            justify-content: flex-end;
            margin-top: 1.5rem;
        }}"""

    def _generate_utilities_css(self, colors: Dict[str, str]) -> str:
        """Generate utility CSS classes."""
        return f"""
        .hidden {{
            display: none !important;
        }}

        .widget-placeholder {{
            color: {colors['text_secondary']};
            font-style: italic;
            text-align: center;
        }}

        .heatmap-container {{
            width: 100%;
            height: 100%;
            min-height: 200px;
        }}

        .pie-chart {{
            max-width: 300px;
            max-height: 300px;
        }}"""

    def generate_theme_css(self, theme: str) -> str:
        """Generate CSS for a specific theme."""
        if theme not in self._theme_colors:
            logger.warning(f"Unknown theme: {theme}, using dark theme")
            theme = "dark"

        colors = self._theme_colors[theme]
        return self._generate_main_css_with_colors(colors)

    def _generate_main_css_with_colors(self, colors: Dict[str, str]) -> str:
        """Generate main CSS with specific colors."""
        # This would be similar to generate_main_css but with passed colors
        # Implementation would be similar to the main method
        return self.generate_main_css()

    def export_css_file(self, filepath: str) -> bool:
        """Export CSS to a file."""
        try:
            css_content = self.generate_main_css()
            with open(filepath, "w") as f:
                f.write(css_content)
            logger.info(f"CSS exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export CSS: {e}")
            return False
