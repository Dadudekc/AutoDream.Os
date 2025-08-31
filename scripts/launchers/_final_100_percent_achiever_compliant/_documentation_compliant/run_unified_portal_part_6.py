"""
run_unified_portal_part_6.py
Module: run_unified_portal_part_6.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:00
"""

# Part 6 of run_unified_portal.py
# Original file: .\scripts\launchers\run_unified_portal.py


def main():
    """Main command-line interface"""
    parser = argparse.ArgumentParser(
        description="Unified Portal Launcher for Agent_Cellphone_V2_Repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch Flask portal with default settings
  python run_unified_portal.py launch flask

  # Launch FastAPI portal on custom host/port
  python run_unified_portal.py launch fastapi --host 127.0.0.1 --port 8000

  # Show portal status
  python run_unified_portal.py status

  # Test portal integration
  python run_unified_portal.py test

  # Launch with custom config
  python run_unified_portal.py launch flask --config config/custom_portal.yaml
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Launch command
    launch_parser = subparsers.add_parser("launch", help="Launch the portal")
    launch_parser.add_argument(
        "backend", choices=["flask", "fastapi"], help="Backend type"
    )
    launch_parser.add_argument("--host", help="Host to bind to")
    launch_parser.add_argument("--port", type=int, help="Port to bind to")
    launch_parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload"
    )
    launch_parser.add_argument(
        "--no-reload", action="store_true", help="Disable auto-reload"
    )
    launch_parser.add_argument("--config", help="Configuration file path")

    # Status command
    subparsers.add_parser("status", help="Show portal status")

    # Test command
    subparsers.add_parser("test", help="Test portal integration")

    # Parse arguments
    args = parser.parse_args()

