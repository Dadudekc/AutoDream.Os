#!/usr/bin/env python3
"""
File Generator - V2 Dashboard System

This module handles dashboard file generation and output operations.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List
from .dashboard_types import DashboardWidget, DashboardLayout
from .html_generator import HTMLGenerator
from .javascript_generator import JavaScriptGenerator


class FileGenerator:
    """Handles dashboard file generation and output operations."""
    
    def __init__(self, html_generator: HTMLGenerator, js_generator: JavaScriptGenerator):
        self.html_generator = html_generator
        self.js_generator = js_generator
        self.logger = logging.getLogger(f"{__name__}.FileGenerator")
    
    def generate_dashboard_files(self, widgets: List[DashboardWidget], layout: DashboardLayout, 
                                output_dir: str = "dashboard_output") -> Dict[str, str]:
        """Generate all dashboard files and save to directory."""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            # Generate HTML
            html_content = self.html_generator.generate_html(widgets, layout)
            html_path = output_path / "index.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Generate JavaScript
            js_content = self.js_generator.generate_javascript(widgets, layout)
            js_path = output_path / "dashboard.js"
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(js_content)
            
            # Generate CSS using CSS generator
            from .css_generator import CSSGenerator
            css_generator = CSSGenerator()
            css_content = css_generator.generate_css(layout)
            css_path = output_path / "dashboard.css"
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
            
            # Generate configuration file
            config_content = self._generate_config_file(widgets, layout)
            config_path = output_path / "dashboard_config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(config_content)
            
            self.logger.info(f"Dashboard files generated in: {output_path}")
            
            return {
                "html": str(html_path),
                "javascript": str(js_path),
                "css": str(css_path),
                "config": str(config_path)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to generate dashboard files: {e}")
            raise
    
    def _generate_config_file(self, widgets: List[DashboardWidget], layout: DashboardLayout) -> str:
        """Generate configuration file content."""
        import json
        
        config_data = {
            "layout": {
                "columns": layout.columns,
                "rows": layout.rows,
                "theme": layout.theme,
                "auto_refresh": layout.auto_refresh,
                "refresh_interval": layout.refresh_interval
            },
            "widgets": [
                {
                    "id": w.widget_id,
                    "title": w.title,
                    "chart_type": w.chart_type.value,
                    "metric": w.metric_name,
                    "refresh_interval": w.refresh_interval,
                    "width": w.width,
                    "height": w.height,
                    "position_x": w.position_x,
                    "position_y": w.position_y
                }
                for w in widgets
            ]
        }
        
        return json.dumps(config_data, indent=2)
    
    def generate_minimal_dashboard(self, widgets: List[DashboardWidget], layout: DashboardLayout, 
                                  output_dir: str = "minimal_dashboard") -> Dict[str, str]:
        """Generate minimal dashboard with just HTML and inline CSS/JS."""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            # Generate minimal HTML with inline CSS and JS
            minimal_html = self._generate_minimal_html(widgets, layout)
            html_path = output_path / "index.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(minimal_html)
            
            self.logger.info(f"Minimal dashboard generated in: {output_path}")
            
            return {"html": str(html_path)}
            
        except Exception as e:
            self.logger.error(f"Failed to generate minimal dashboard: {e}")
            raise
    
    def _generate_minimal_html(self, widgets: List[DashboardWidget], layout: DashboardLayout) -> str:
        """Generate minimal HTML with inline CSS and JS."""
        # This would generate a single HTML file with everything inline
        # For now, return a placeholder
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Minimal Dashboard</title>
</head>
<body>
    <h1>Minimal Dashboard</h1>
    <p>Widgets: {len(widgets)}</p>
    <p>Layout: {layout.columns}x{layout.rows}</p>
</body>
</html>"""
    
    def cleanup_output_directory(self, output_dir: str):
        """Clean up output directory."""
        try:
            output_path = Path(output_dir)
            if output_path.exists():
                import shutil
                shutil.rmtree(output_path)
                self.logger.info(f"Cleaned up output directory: {output_dir}")
        except Exception as e:
            self.logger.error(f"Failed to cleanup output directory: {e}")
    
    def get_file_sizes(self, output_dir: str) -> Dict[str, int]:
        """Get sizes of generated files."""
        try:
            output_path = Path(output_dir)
            if not output_path.exists():
                return {}
            
            file_sizes = {}
            for file_path in output_path.glob("*"):
                if file_path.is_file():
                    file_sizes[file_path.name] = file_path.stat().st_size
            
            return file_sizes
            
        except Exception as e:
            self.logger.error(f"Failed to get file sizes: {e}")
            return {}
