"""
VSCode Customization Interface for Team Beta Mission
Agent-7 Web Development Expert - User-Friendly Interfaces

V2 Compliance: ≤400 lines, type hints, KISS principle
"""

import json
from dataclasses import dataclass
from enum import Enum


class ThemeType(Enum):
    """VSCode theme types for customization."""

    DARK = "dark"
    LIGHT = "light"
    AGENT_FRIENDLY = "agent_friendly"
    HIGH_CONTRAST = "high_contrast"


class LayoutType(Enum):
    """VSCode layout types for agent optimization."""

    STANDARD = "standard"
    AGENT_FOCUSED = "agent_focused"
    REPOSITORY_MANAGEMENT = "repository_management"
    DEVELOPMENT = "development"


@dataclass
class ThemeConfig:
    """Theme configuration for VSCode customization."""

    name: str
    type: ThemeType
    colors: dict[str, str]
    accessibility_contrast: float
    agent_optimized: bool


@dataclass
class ExtensionConfig:
    """Extension configuration for agent-specific tools."""

    id: str
    name: str
    category: str
    agent_specific: bool
    repository_management: bool
    enabled: bool


@dataclass
class LayoutConfig:
    """Layout configuration for workspace optimization."""

    type: LayoutType
    panel_arrangement: dict[str, str]
    workspace_organization: dict[str, bool]
    agent_workflow_optimized: bool


class VSCodeCustomizationInterface:
    """
    VSCode customization interface for Team Beta mission.

    Provides user-friendly and agent-friendly VSCode customization tools
    for repository management and development workflows.
    """

    def __init__(self):
        """Initialize VSCode customization interface."""
        self.themes = self._initialize_themes()
        self.extensions = self._initialize_extensions()
        self.layouts = self._initialize_layouts()

    def _initialize_themes(self) -> list[ThemeConfig]:
        """Initialize available themes for customization."""
        return [
            ThemeConfig(
                name="Agent Dark Pro",
                type=ThemeType.AGENT_FRIENDLY,
                colors={
                    "background": "#1e1e1e",
                    "foreground": "#d4d4d4",
                    "accent": "#007acc",
                    "error": "#f48771",
                    "warning": "#dcdcaa",
                    "success": "#4ec9b0",
                },
                accessibility_contrast=4.5,
                agent_optimized=True,
            ),
            ThemeConfig(
                name="Repository Light",
                type=ThemeType.LIGHT,
                colors={
                    "background": "#ffffff",
                    "foreground": "#333333",
                    "accent": "#007acc",
                    "error": "#e51400",
                    "warning": "#ff8c00",
                    "success": "#008000",
                },
                accessibility_contrast=7.0,
                agent_optimized=False,
            ),
            ThemeConfig(
                name="High Contrast Agent",
                type=ThemeType.HIGH_CONTRAST,
                colors={
                    "background": "#000000",
                    "foreground": "#ffffff",
                    "accent": "#00ffff",
                    "error": "#ff0000",
                    "warning": "#ffff00",
                    "success": "#00ff00",
                },
                accessibility_contrast=21.0,
                agent_optimized=True,
            ),
        ]

    def _initialize_extensions(self) -> list[ExtensionConfig]:
        """Initialize agent-specific extensions."""
        return [
            ExtensionConfig(
                id="agent.repository-manager",
                name="Agent Repository Manager",
                category="Repository Management",
                agent_specific=True,
                repository_management=True,
                enabled=True,
            ),
            ExtensionConfig(
                id="agent.vscode-forker",
                name="VSCode Forker",
                category="Development Tools",
                agent_specific=True,
                repository_management=True,
                enabled=True,
            ),
            ExtensionConfig(
                id="agent.interface-optimizer",
                name="Agent Interface Optimizer",
                category="UI/UX",
                agent_specific=True,
                repository_management=False,
                enabled=True,
            ),
            ExtensionConfig(
                id="gitlens",
                name="GitLens",
                category="Git Integration",
                agent_specific=False,
                repository_management=True,
                enabled=True,
            ),
            ExtensionConfig(
                id="prettier",
                name="Prettier",
                category="Code Formatting",
                agent_specific=False,
                repository_management=False,
                enabled=True,
            ),
        ]

    def _initialize_layouts(self) -> list[LayoutConfig]:
        """Initialize workspace layouts for optimization."""
        return [
            LayoutConfig(
                type=LayoutType.AGENT_FOCUSED,
                panel_arrangement={
                    "explorer": "left",
                    "repository_manager": "left",
                    "terminal": "bottom",
                    "output": "bottom",
                },
                workspace_organization={
                    "multi_root": True,
                    "auto_save": True,
                    "file_watcher": True,
                },
                agent_workflow_optimized=True,
            ),
            LayoutConfig(
                type=LayoutType.REPOSITORY_MANAGEMENT,
                panel_arrangement={
                    "source_control": "left",
                    "repository_viewer": "left",
                    "terminal": "bottom",
                    "problems": "bottom",
                },
                workspace_organization={
                    "multi_root": True,
                    "auto_save": True,
                    "file_watcher": True,
                },
                agent_workflow_optimized=True,
            ),
        ]

    def get_available_themes(self) -> list[ThemeConfig]:
        """Get list of available themes for customization."""
        return self.themes

    def get_agent_optimized_themes(self) -> list[ThemeConfig]:
        """Get themes optimized for agent workflows."""
        return [theme for theme in self.themes if theme.agent_optimized]

    def get_extension_by_category(self, category: str) -> list[ExtensionConfig]:
        """Get extensions by category."""
        return [ext for ext in self.extensions if ext.category == category]

    def get_agent_specific_extensions(self) -> list[ExtensionConfig]:
        """Get extensions specifically designed for agents."""
        return [ext for ext in self.extensions if ext.agent_specific]

    def get_repository_management_extensions(self) -> list[ExtensionConfig]:
        """Get extensions for repository management."""
        return [ext for ext in self.extensions if ext.repository_management]

    def get_layout_by_type(self, layout_type: LayoutType) -> LayoutConfig | None:
        """Get layout configuration by type."""
        for layout in self.layouts:
            if layout.type == layout_type:
                return layout
        return None

    def create_customization_config(
        self, theme: ThemeConfig, extensions: list[ExtensionConfig], layout: LayoutConfig
    ) -> dict:
        """Create complete customization configuration."""
        return {
            "theme": {
                "name": theme.name,
                "type": theme.type.value,
                "colors": theme.colors,
                "accessibility_contrast": theme.accessibility_contrast,
                "agent_optimized": theme.agent_optimized,
            },
            "extensions": [
                {
                    "id": ext.id,
                    "name": ext.name,
                    "category": ext.category,
                    "agent_specific": ext.agent_specific,
                    "repository_management": ext.repository_management,
                    "enabled": ext.enabled,
                }
                for ext in extensions
            ],
            "layout": {
                "type": layout.type.value,
                "panel_arrangement": layout.panel_arrangement,
                "workspace_organization": layout.workspace_organization,
                "agent_workflow_optimized": layout.agent_workflow_optimized,
            },
            "metadata": {
                "created_by": "Agent-7",
                "team_beta_mission": True,
                "v2_compliant": True,
                "user_friendly": True,
                "agent_friendly": True,
            },
        }

    def export_configuration(self, config: dict, filepath: str) -> bool:
        """Export customization configuration to file."""
        try:
            with open(filepath, "w") as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting configuration: {e}")
            return False

    def validate_configuration(self, config: dict) -> tuple[bool, list[str]]:
        """Validate customization configuration."""
        errors = []

        # Validate theme
        if "theme" not in config:
            errors.append("Missing theme configuration")
        elif "colors" not in config["theme"]:
            errors.append("Missing theme colors")

        # Validate extensions
        if "extensions" not in config:
            errors.append("Missing extensions configuration")

        # Validate layout
        if "layout" not in config:
            errors.append("Missing layout configuration")

        return len(errors) == 0, errors


def create_agent_optimized_config() -> dict:
    """Create agent-optimized VSCode configuration."""
    interface = VSCodeCustomizationInterface()

    # Get agent-optimized theme
    agent_themes = interface.get_agent_optimized_themes()
    theme = agent_themes[0] if agent_themes else interface.themes[0]

    # Get agent-specific extensions
    extensions = interface.get_agent_specific_extensions()

    # Get agent-focused layout
    layout = interface.get_layout_by_type(LayoutType.AGENT_FOCUSED)
    if not layout:
        layout = interface.layouts[0]

    return interface.create_customization_config(theme, extensions, layout)


if __name__ == "__main__":
    # Example usage
    interface = VSCodeCustomizationInterface()

    # Create agent-optimized configuration
    config = create_agent_optimized_config()

    # Export configuration
    success = interface.export_configuration(config, "vscode_agent_config.json")
    if success:
        print("✅ Agent-optimized VSCode configuration exported successfully")
    else:
        print("❌ Failed to export configuration")

    # Validate configuration
    is_valid, errors = interface.validate_configuration(config)
    if is_valid:
        print("✅ Configuration validation passed")
    else:
        print(f"❌ Configuration validation failed: {errors}")
