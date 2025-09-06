#!/usr/bin/env python3
"""
Messaging Status Reporting Module - V2 Compliant
===============================================

Modular component for messaging system status reporting and monitoring.
Provides comprehensive status information and metrics.

Author: Agent-7 - Web Development Specialist
License: MIT
"""


try:

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


# Fallback logger
class FallbackLogger:
    """Simple fallback logger."""

    def info(self, msg):
        get_logger(__name__).info(f"INFO: {msg}")

    def error(self, msg):
        get_logger(__name__).info(f"ERROR: {msg}")

    def warning(self, msg):
        get_logger(__name__).info(f"WARNING: {msg}")


class MessagingStatusReporting:
    """Handles messaging system status reporting and monitoring."""

    def __init__(self, logger=None):
        """Initialize status reporting handler."""
        self.logger = logger or FallbackLogger()

    async def show_coordinates(self) -> Dict[str, Any]:
        """Display current agent coordinates configuration. Uses Discord Commander
        coordinates as primary source.

        Returns:
            Dict containing coordinate information
        """
        try:
            # Use coordinate delivery system to load Discord Commander coordinates

            coordinate_delivery = CoordinateMessagingDelivery(self.logger)
            coordinates = coordinate_delivery.load_coordinates()

            if coordinates:
                if self.logger:
                    self.get_logger(__name__).info(
                        "📍 Current Agent Coordinates (Discord Commander):"
                    )
                else:
                    get_logger(__name__).info(
                        "📍 Current Agent Coordinates (Discord Commander):"
                    )

                for agent, coords in coordinates.items():
                    coord_info = f"{agent}: [{coords[0]}, {coords[1]}]"
                    if self.logger:
                        self.get_logger(__name__).info(f"  {coord_info}")
                    else:
                        get_logger(__name__).info(f"  {coord_info}")

                success_msg = f"✅ Total configured agents: {len(coordinates)}"
                if self.logger:
                    self.get_logger(__name__).info(success_msg)
                else:
                    get_logger(__name__).info(success_msg)

                return {
                    "success": True,
                    "coordinates": coordinates,
                    "agent_count": len(coordinates),
                    "configured_agents": list(coordinates.keys()),
                }
            else:
                no_coords_msg = "❌ No coordinates configured!"
                if self.logger:
                    self.get_logger(__name__).warning(no_coords_msg)
                else:
                    get_logger(__name__).info(no_coords_msg)

                config_hint = "💡 Check src/discord_commander_coordinates.json"
                if self.logger:
                    self.get_logger(__name__).info(config_hint)
                else:
                    get_logger(__name__).info(config_hint)

                return {
                    "success": False,
                    "message": "No coordinates configured",
                    "coordinates": {},
                    "agent_count": 0,
                    "configured_agents": [],
                }

        except Exception as e:
            error_msg = f"❌ Error loading coordinates: {e}"
            if self.logger:
                self.get_logger(__name__).error(error_msg)
            else:
                get_logger(__name__).info(error_msg)

            return {
                "success": False,
                "message": f"Failed to load coordinates: {str(e)}",
                "coordinates": {},
                "agent_count": 0,
                "configured_agents": [],
            }

    def get_system_status(
        self, inbox_paths: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Get comprehensive messaging system status.

        Args:
            inbox_paths: Optional inbox paths for status checking

        Returns:
            Dict containing system status information
        """
        status = {
            "system_health": "operational",
            "components": {},
            "metrics": {},
            "issues": [],
        }

        # Check configuration files
        config_files = {
            "messaging_config": "config/messaging.yml",
            "devlog_config": "config/devlog_config.json",
        }

        for name, path in config_files.items():
            if get_unified_utility().path.exists(path):
                status["components"][f"{name}_file"] = "present"
            else:
                status["components"][f"{name}_file"] = "missing"
                status["issues"].append(f"Missing {name} file: {path}")

        # Check inbox directories
        if inbox_paths:
            for agent, path in inbox_paths.items():
                if get_unified_utility().path.exists(path):
                    status["components"][f"{agent}_inbox"] = "present"
                    # Count messages in inbox
                    try:
                        inbox_dir = get_unified_utility().Path(path)
                        if inbox_dir.exists():
                            message_count = len(list(inbox_dir.glob("*.md")))
                            status["metrics"][f"{agent}_messages"] = message_count
                    except Exception as e:
                        status["issues"].append(f"Error counting {agent} messages: {e}")
                else:
                    status["components"][f"{agent}_inbox"] = "missing"
                    status["issues"].append(f"Missing {agent} inbox: {path}")

        # Check PyAutoGUI availability
        try:

            status["components"]["pyautogui"] = "available"
        except ImportError:
            status["components"]["pyautogui"] = "unavailable"
            status["issues"].append(
                "PyAutoGUI not available - coordinate delivery disabled"
            )

        # Determine overall system health
        if status["issues"]:
            if len(status["issues"]) > 3:
                status["system_health"] = "critical"
            else:
                status["system_health"] = "degraded"
        else:
            status["system_health"] = "operational"

        return status

    def generate_status_report(
        self, inbox_paths: Optional[Dict[str, str]] = None
    ) -> str:
        """Generate a formatted status report.

        Args:
            inbox_paths: Optional inbox paths for status checking

        Returns:
            Formatted status report string
        """
        status = self.get_system_status(inbox_paths)

        report_lines = [
            "📊 MESSAGING SYSTEM STATUS REPORT",
            "=" * 50,
            f"System Health: {status['system_health'].upper()}",
            "",
            "📁 COMPONENTS:",
        ]

        for component, state in status["components"].items():
            icon = "✅" if state in ["present", "available"] else "❌"
            report_lines.append(f"  {icon} {component}: {state}")

        if status["metrics"]:
            report_lines.append("")
            report_lines.append("📈 METRICS:")
            for metric, value in status["metrics"].items():
                report_lines.append(f"  📊 {metric}: {value}")

        if status["issues"]:
            report_lines.append("")
            report_lines.append("⚠️ ISSUES:")
            for issue in status["issues"]:
                report_lines.append(f"  ❌ {issue}")

        return "\n".join(report_lines)
