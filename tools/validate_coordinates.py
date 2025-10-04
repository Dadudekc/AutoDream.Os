#!/usr/bin/env python3
"""
Coordinates Schema Validator
============================

Pre-flight validation of agent coordinates configuration for hard onboarding.
Validates schema structure and coordinate format before PyAutoGUI execution.

V2 Compliance: ≤400 lines, focused validation tool
Author: Agent-4 (Captain) - Strategic Oversight & Emergency Intervention
"""

import json
from pathlib import Path
from typing import Any


def validate_coordinates_file(path: str) -> tuple[bool, list[str]]:
    """
    Validate coordinates configuration file.

    Args:
        path: Path to coordinates.json file

    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    file_path = Path(path)

    # Check file exists
    if not file_path.exists():
        errors.append(f"❌ Missing file: {file_path}")
        return False, errors

    # Check file is readable
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(f"❌ Cannot read file: {e}")
        return False, errors

    # Check JSON validity
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        errors.append(f"❌ Invalid JSON: {e}")
        return False, errors

    # Check root structure
    if not isinstance(data, dict):
        errors.append("❌ Root must be a JSON object")
        return False, errors

    # Check agents section
    agents = data.get("agents")
    if not isinstance(agents, dict):
        errors.append("❌ Missing or invalid 'agents' section")
        return False, errors

    if not agents:
        errors.append("❌ 'agents' section is empty")
        return False, errors

    # Validate each agent
    required_agents = [
        "Agent-1",
        "Agent-2",
        "Agent-3",
        "Agent-4",
        "Agent-5",
        "Agent-6",
        "Agent-7",
        "Agent-8",
    ]

    for agent_id in required_agents:
        if agent_id not in agents:
            errors.append(f"❌ Missing agent: {agent_id}")
            continue

        agent_config = agents[agent_id]
        if not isinstance(agent_config, dict):
            errors.append(f"❌ {agent_id}: Configuration must be an object")
            continue

        # Validate chat_input_coordinates
        chat_coords = agent_config.get("chat_input_coordinates")
        if not _validate_coordinate_pair(chat_coords, f"{agent_id}.chat_input_coordinates"):
            errors.extend(_get_coordinate_errors(chat_coords, f"{agent_id}.chat_input_coordinates"))

        # Validate onboarding_coordinates (optional)
        onboard_coords = agent_config.get("onboarding_coordinates")
        if onboard_coords is not None:
            if not _validate_coordinate_pair(onboard_coords, f"{agent_id}.onboarding_coordinates"):
                errors.extend(
                    _get_coordinate_errors(onboard_coords, f"{agent_id}.onboarding_coordinates")
                )

    # Check for extra agents (warn but don't fail)
    extra_agents = set(agents.keys()) - set(required_agents)
    if extra_agents:
        print(f"⚠️  Extra agents found: {sorted(extra_agents)}")

    return len(errors) == 0, errors


def _validate_coordinate_pair(coords: Any, field_name: str) -> bool:
    """Validate a coordinate pair [x, y]."""
    if not isinstance(coords, list):
        return False

    if len(coords) != 2:
        return False

    if not all(isinstance(v, int) for v in coords):
        return False

    # Check reasonable screen coordinates (basic sanity check)
    # Note: Negative X values are valid for multi-monitor setups
    x, y = coords
    if y < 0:  # Only Y must be non-negative
        return False

    if x > 10000 or y > 10000:  # Reasonable upper bound
        return False

    return True


def _get_coordinate_errors(coords: Any, field_name: str) -> list[str]:
    """Get detailed error messages for coordinate validation."""
    errors = []

    if coords is None:
        errors.append(f"❌ {field_name}: Missing required field")
    elif not isinstance(coords, list):
        errors.append(f"❌ {field_name}: Must be a list [x, y]")
    elif len(coords) != 2:
        errors.append(f"❌ {field_name}: Must have exactly 2 elements [x, y]")
    elif not all(isinstance(v, int) for v in coords):
        errors.append(f"❌ {field_name}: Both elements must be integers")
    else:
        x, y = coords
        if y < 0:
            errors.append(f"❌ {field_name}: Y coordinate must be non-negative")
        if x > 10000 or y > 10000:
            errors.append(f"❌ {field_name}: Coordinates seem unreasonably large")

    return errors


def print_validation_summary(is_valid: bool, errors: list[str], file_path: str) -> None:
    """Print validation results summary."""
    print(f"\n{'='*60}")
    print(f"COORDINATES VALIDATION: {file_path}")
    print(f"{'='*60}")

    if is_valid:
        print("✅ Coordinates schema is valid")
        print("✅ All required agents have valid coordinates")
        print("✅ Ready for hard onboarding execution")
    else:
        print("❌ Coordinates schema validation failed")
        print("\nErrors found:")
        for error in errors:
            print(f"  {error}")
        print("\n❌ Fix errors before running hard onboarding")

    print(f"{'='*60}")


def main() -> int:
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate agent coordinates configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate default coordinates file
  python tools/validate_coordinates.py

  # Validate specific file
  python tools/validate_coordinates.py config/custom_coordinates.json

  # Silent mode (exit codes only)
  python tools/validate_coordinates.py --quiet
        """,
    )

    parser.add_argument(
        "path",
        nargs="?",
        default="config/coordinates.json",
        help="Path to coordinates.json file (default: config/coordinates.json)",
    )

    parser.add_argument(
        "--quiet", action="store_true", help="Quiet mode - only exit codes, no output"
    )

    parser.add_argument(
        "--verbose", action="store_true", help="Verbose mode - show detailed validation info"
    )

    args = parser.parse_args()

    # Validate coordinates
    is_valid, errors = validate_coordinates_file(args.path)

    if not args.quiet:
        print_validation_summary(is_valid, errors, args.path)

        if args.verbose and is_valid:
            # Show coordinate summary
            try:
                with open(args.path) as f:
                    data = json.load(f)

                print("\nAgent Coordinates Summary:")
                for agent_id, config in data["agents"].items():
                    chat = config["chat_input_coordinates"]
                    onboard = config.get("onboarding_coordinates", "same as chat")
                    print(f"  {agent_id}: chat={chat}, onboard={onboard}")

            except Exception as e:
                print(f"⚠️  Could not show coordinate summary: {e}")

    # Return appropriate exit code
    return 0 if is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
