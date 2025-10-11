"""
GUI Themes - V2 Compliant
========================

Theme definitions for GUI applications.
Provides consistent styling across all GUI components.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive type hints.

Author: Agent-1 - GUI Specialist
License: MIT
"""

from typing import Any


class Theme:
    """Base theme class."""

    def __init__(self, name: str):
        self.name = name
        self.colors: dict[str, str] = {}
        self.styles: dict[str, str] = {}

    def get_color(self, key: str, default: str = "#000000") -> str:
        """Get color by key."""
        return self.colors.get(key, default)

    def get_style(self, component: str) -> str:
        """Get style for component."""
        return self.styles.get(component, "")

    def to_dict(self) -> dict[str, Any]:
        """Convert theme to dictionary."""
        return {"name": self.name, "colors": self.colors, "styles": self.styles}


class DarkTheme(Theme):
    """Dark theme for GUI applications."""

    def __init__(self):
        super().__init__("dark")

        # Color palette
        self.colors = {
            "background": "#1A1A1A",
            "surface": "#2C3E50",
            "foreground": "#ECF0F1",
            "primary": "#3498DB",
            "secondary": "#34495E",
            "success": "#27AE60",
            "warning": "#F39C12",
            "error": "#E74C3C",
            "info": "#3498DB",
            "text_primary": "#ECF0F1",
            "text_secondary": "#BDC3C7",
            "text_disabled": "#7F8C8D",
            "border": "#34495E",
            "hover": "#2980B9",
            "active": "#2C3E50",
        }

        # Component styles
        self.styles = {
            "main_window": f"""
                QMainWindow {{
                    background-color: {self.colors['background']};
                }}
            """,
            "frame": f"""
                QFrame {{
                    background-color: {self.colors['surface']};
                    border: 2px solid {self.colors['border']};
                    border-radius: 8px;
                    padding: 10px;
                }}
                QFrame:hover {{
                    border-color: {self.colors['primary']};
                }}
            """,
            "button": f"""
                QPushButton {{
                    background-color: {self.colors['primary']};
                    color: white;
                    border-radius: 5px;
                    padding: 10px 20px;
                    font-weight: bold;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['hover']};
                }}
                QPushButton:pressed {{
                    background-color: {self.colors['active']};
                }}
            """,
            "button_success": f"""
                QPushButton {{
                    background-color: {self.colors['success']};
                    color: white;
                    border-radius: 5px;
                    padding: 8px 15px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #229954;
                }}
            """,
            "button_error": f"""
                QPushButton {{
                    background-color: {self.colors['error']};
                    color: white;
                    border-radius: 5px;
                    padding: 8px 15px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #C0392B;
                }}
            """,
            "label": f"""
                QLabel {{
                    color: {self.colors['text_primary']};
                    font-size: 12px;
                }}
            """,
            "text_edit": f"""
                QTextEdit {{
                    background-color: {self.colors['surface']};
                    color: {self.colors['foreground']};
                    border: 1px solid {self.colors['border']};
                    border-radius: 5px;
                    font-family: Consolas, Monaco, monospace;
                    padding: 5px;
                }}
            """,
            "group_box": f"""
                QGroupBox {{
                    font-weight: bold;
                    color: white;
                    border: 2px solid {self.colors['border']};
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """,
        }


class LightTheme(Theme):
    """Light theme for GUI applications."""

    def __init__(self):
        super().__init__("light")

        # Color palette
        self.colors = {
            "background": "#FFFFFF",
            "surface": "#F8F9FA",
            "foreground": "#2C3E50",
            "primary": "#3498DB",
            "secondary": "#BDC3C7",
            "success": "#27AE60",
            "warning": "#F39C12",
            "error": "#E74C3C",
            "info": "#3498DB",
            "text_primary": "#2C3E50",
            "text_secondary": "#7F8C8D",
            "text_disabled": "#BDC3C7",
            "border": "#BDC3C7",
            "hover": "#2980B9",
            "active": "#D6EAF8",
        }

        # Component styles
        self.styles = {
            "main_window": f"""
                QMainWindow {{
                    background-color: {self.colors['background']};
                }}
            """,
            "frame": f"""
                QFrame {{
                    background-color: {self.colors['surface']};
                    border: 2px solid {self.colors['border']};
                    border-radius: 8px;
                    padding: 10px;
                }}
                QFrame:hover {{
                    border-color: {self.colors['primary']};
                }}
            """,
            "button": f"""
                QPushButton {{
                    background-color: {self.colors['primary']};
                    color: white;
                    border-radius: 5px;
                    padding: 10px 20px;
                    font-weight: bold;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['hover']};
                }}
                QPushButton:pressed {{
                    background-color: {self.colors['active']};
                }}
            """,
            "label": f"""
                QLabel {{
                    color: {self.colors['text_primary']};
                    font-size: 12px;
                }}
            """,
            "text_edit": f"""
                QTextEdit {{
                    background-color: {self.colors['surface']};
                    color: {self.colors['foreground']};
                    border: 1px solid {self.colors['border']};
                    border-radius: 5px;
                    font-family: Consolas, Monaco, monospace;
                    padding: 5px;
                }}
            """,
        }


class ThemeManager:
    """Manager for GUI themes."""

    def __init__(self):
        self.themes: dict[str, Theme] = {"dark": DarkTheme(), "light": LightTheme()}
        self.current_theme: Theme = self.themes["dark"]

    def set_theme(self, theme_name: str) -> bool:
        """Set active theme."""
        if theme_name in self.themes:
            self.current_theme = self.themes[theme_name]
            return True
        return False

    def get_theme(self) -> Theme:
        """Get current theme."""
        return self.current_theme

    def add_theme(self, theme: Theme) -> None:
        """Add custom theme."""
        self.themes[theme.name] = theme

    def get_available_themes(self) -> list[str]:
        """Get list of available theme names."""
        return list(self.themes.keys())

    class ThemeManager:
        pass
