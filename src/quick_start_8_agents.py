#!/usr/bin/env python3
"""
Quick Start Script for 8-Agent PyAutoGUI Coordination System
TDD Integration of Agent_Cellphone_V2_Repository

This script provides a simple way to get started with the 8-agent coordination system.
"""

import os
import sys
import subprocess
import platform

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path


def print_banner():
    """Print the system banner."""
    print("=" * 80)
    print("🚀 8-AGENT PYTHON COORDINATION SYSTEM")
    print("   TDD Integration of Agent_Cellphone_V2_Repository")
    print("=" * 80)
    print()


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")

    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def check_platform():
    """Check if platform is supported."""
    print("💻 Checking platform...")

    system = platform.system()
    if system == "Windows":
        print("✅ Windows detected - Full support")
        return True
    elif system == "Linux":
        print("✅ Linux detected - Full support")
        return True
    elif system == "Darwin":
        print("✅ macOS detected - Full support")
        return True
    else:
        print(f"⚠️  Unknown platform: {system} - Limited support")
        return False


def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")

    requirements_file = "requirements_8_agents.txt"
    if not os.path.exists(requirements_file):
        print(f"❌ Requirements file not found: {requirements_file}")
        return False

    try:
        # Install core requirements first
        print("   Installing core PyAutoGUI...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyautogui", "pillow"],
            check=True,
            capture_output=True,
        )

        # Install all requirements
        print("   Installing all requirements...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file],
            check=True,
            capture_output=True,
        )

        print("✅ All packages installed successfully")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False


def create_directories():
    """Create necessary directories for the project."""
    print("📁 Creating project directories...")

    directories = [
        "ai_development",
        "multimedia",
        "integration",
        "deployment",
        "tests",
        "logs",
        "reports",
        "config",
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ Created: {directory}/")

    print("✅ All directories created")


def create_config_files():
    """Create basic configuration files."""
    print("⚙️  Creating configuration files...")

    # Create .env template
    env_content = """# Environment Configuration for 8-Agent System
# Copy this file to .env and fill in your values

# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///agent_coordination.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/coordination.log

# PyAutoGUI Configuration
PYAUTOGUI_FAILSAFE=true
PYAUTOGUI_PAUSE=0.5

# Agent Configuration
AGENT_TIMEOUT_SECONDS=1800
COORDINATION_INTERVAL_SECONDS=30
"""

    with open(".env.template", "w") as f:
        f.write(env_content)
    print("   ✅ Created: .env.template")

    # Create basic config
    config_content = """# 8-Agent Coordination Configuration
coordination:
  agents:
    - id: "Agent-1"
      name: "Foundation & Testing Specialist"
      screen_region: [0, 0, 800, 600]
    - id: "Agent-2"
      name: "AI & ML Integration Specialist"
      screen_region: [800, 0, 800, 600]
    - id: "Agent-3"
      name: "Multimedia & Content Specialist"
      screen_region: [0, 600, 800, 600]
    - id: "Agent-4"
      name: "Security & Infrastructure Specialist"
      screen_region: [800, 600, 800, 600]
    - id: "Agent-5"
      name: "Business Intelligence & Trading Specialist"
      screen_region: [1600, 0, 800, 600]
    - id: "Agent-6"
      name: "Gaming & Entertainment Development Specialist"
      screen_region: [1600, 600, 800, 600]
    - id: "Agent-7"
      name: "Web Development & UI Framework Specialist"
      screen_region: [2400, 0, 800, 600]
    - id: "Agent-8"
      name: "Integration & Performance Optimization Captain"
      screen_region: [2400, 600, 800, 600]

  settings:
    task_timeout_minutes: 30
    coordination_interval_seconds: 30
    progress_report_interval_seconds: 300
    max_retry_attempts: 3
"""

    with open("config/coordination_config.yaml", "w") as f:
        f.write(config_content)
    print("   ✅ Created: config/coordination_config.yaml")

    print("✅ Configuration files created")


def run_system_check():
    """Run a system compatibility check."""
    print("🔍 Running system compatibility check...")

    try:
        import pyautogui

        print("   ✅ PyAutoGUI imported successfully")

        # Test screen size
        screen_width, screen_height = pyautogui.size()
        print(f"   ✅ Screen resolution: {screen_width}x{screen_height}")

        if screen_width < 3200 or screen_height < 1200:
            print("   ⚠️  Screen resolution may be too small for 8-agent layout")
            print("   💡 Recommended: 3200x1200 or higher")

        # Test basic PyAutoGUI functionality
        pyautogui.FAILSAFE = True
        print("   ✅ PyAutoGUI safety features enabled")

        return True

    except ImportError:
        print("   ❌ PyAutoGUI not available")
        return False
    except Exception as e:
        print(f"   ❌ PyAutoGUI error: {e}")
        return False


def display_next_steps():
    """Display next steps for the user."""
    print("\n" + "=" * 80)
    print("🎯 NEXT STEPS TO GET STARTED:")
    print("=" * 80)
    print()
    print("1. 📝 Configure your environment:")
    print("   - Copy .env.template to .env")
    print("   - Add your API keys and configuration")
    print()
    print("2. 🖥️  Set up your screen layout:")
    print("   - Ensure you have enough screen space (3200x1200 recommended)")
    print("   - Position your terminals/IDEs in the configured regions")
    print()
    print("3. 🚀 Start the coordination system:")
    print("   python agent_coordination_automation.py")
    print()
    print("4. 📊 Monitor progress:")
    print("   - Check coordination_status_report.json")
    print("   - Watch the console output")
    print("   - Review logs/coordination.log")
    print()
    print("5. 🧪 Run tests:")
    print("   python -m pytest tests/ -v")
    print()
    print("📚 For detailed information, see:")
    print("   - TDD_INTEGRATION_BLUEPRINT_8_AGENTS.md")
    print("   - agent_coordination_automation.py")
    print("   - README.md")
    print()
    print("🎉 You're ready to transform Agent_Cellphone_V2_Repository!")
    print("=" * 80)


def main():
    """Main quick start function."""
    print_banner()

    # Check prerequisites
    if not check_python_version():
        sys.exit(1)

    if not check_platform():
        print("⚠️  Continuing with limited support...")

    # Install requirements
    if not install_requirements():
        print(
            "❌ Failed to install requirements. Please check your internet connection and try again."
        )
        sys.exit(1)

    # Create project structure
    create_directories()
    create_config_files()

    # Run system check
    if not run_system_check():
        print("❌ System compatibility check failed. Please review the errors above.")
        sys.exit(1)

    # Display next steps
    display_next_steps()


if __name__ == "__main__":
    main()
