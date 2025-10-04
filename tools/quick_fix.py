#!/usr/bin/env python3
"""
Quick Fix Tool - Simple workflow automation for common agent tasks
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def fix_imports(module_path: str):
    """Fix missing imports by creating __init__.py files."""
    print(f"🔧 Fixing imports for: {module_path}")

    # Convert to Path object relative to project root
    module_path = project_root / module_path
    if not module_path.exists():
        print(f"❌ Path {module_path} does not exist")
        return False

    # Create __init__.py files for all directories in the path
    current_path = project_root
    for part in module_path.relative_to(project_root).parts:
        current_path = current_path / part
        if current_path.is_dir() and not (current_path / "__init__.py").exists():
            create_init_file(current_path)
            print(f"✅ Created __init__.py in {current_path}")

    return True


def create_init_file(directory: Path):
    """Create an __init__.py file for a directory."""
    init_file = directory / "__init__.py"

    # Get all Python files in the directory
    python_files = [
        f.stem
        for f in directory.iterdir()
        if f.is_file() and f.suffix == ".py" and f.name != "__init__.py"
    ]

    # Create __init__.py content
    content = """# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""

    # Add imports for each Python file
    for py_file in python_files:
        content += f"from . import {py_file}\n"

    content += f"""
__all__ = {python_files}
"""

    init_file.write_text(content)


def test_imports(module_path: str):
    """Test if a module can be imported."""
    try:
        # Convert path to import string
        import_path = (
            str(module_path).replace(str(project_root), "").replace("/", ".").replace("\\", ".")
        )
        if import_path.startswith("."):
            import_path = import_path[1:]

        # Test import
        exec(f"import {import_path}")
        print(f"✅ Import test successful: {import_path}")
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


def send_status_update(agent_id: str, message: str):
    """Send status update via messaging service."""
    try:
        from src.services.messaging_service import ConsolidatedMessagingService

        service = ConsolidatedMessagingService()
        success = service.send_message(agent_id, message, "Agent-2", "NORMAL")
        if success:
            print(f"📤 Status update sent to {agent_id}")
        else:
            print(f"❌ Failed to send status update to {agent_id}")
        return success
    except Exception as e:
        print(f"❌ Error sending status update: {e}")
        return False


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Quick Fix Tool - Simple workflow automation")
        print("===========================================")
        print()
        print("Usage:")
        print("  python tools/quick_fix.py fix-imports <module_path>")
        print("  python tools/quick_fix.py test-imports <module_path>")
        print("  python tools/quick_fix.py fix-and-test <module_path>")
        print()
        print("Examples:")
        print("  python tools/quick_fix.py fix-imports src.core")
        print("  python tools/quick_fix.py fix-and-test src.services")
        return

    command = sys.argv[1]

    if command == "fix-imports":
        if len(sys.argv) < 3:
            print("Error: Module path required")
            return
        fix_imports(sys.argv[2])

    elif command == "test-imports":
        if len(sys.argv) < 3:
            print("Error: Module path required")
            return
        test_imports(sys.argv[2])

    elif command == "fix-and-test":
        if len(sys.argv) < 3:
            print("Error: Module path required")
            return

        module_path = sys.argv[2]
        print(f"🚀 Starting fix-and-test workflow for: {module_path}")

        # Fix imports
        fix_success = fix_imports(module_path)

        if fix_success:
            # Test imports
            test_success = test_imports(module_path)

            if test_success:
                # Send status update
                message = f"Agent-2 Quick Fix: {module_path} imports fixed and tested successfully"
                send_status_update("Agent-4", message)
                print("✅ Fix-and-test workflow completed successfully")
            else:
                print("❌ Import test failed after fix")
        else:
            print("❌ Import fix failed")

    else:
        print(f"Unknown command: {command}")
        print("Use 'python tools/quick_fix.py' for help")


if __name__ == "__main__":
    main()
