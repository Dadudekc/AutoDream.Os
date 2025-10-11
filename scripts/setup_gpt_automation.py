"""
Setup script for GPT Automation integration (Team Beta Repo 4/8).

Installs required dependencies and verifies installation.

Author: Agent-7 - Repository Cloning Specialist
"""

import subprocess
import sys


def main():
    """Install GPT Automation dependencies."""
    print("📦 Installing GPT Automation dependencies...")

    dependencies = [
        "openai>=1.0.0",
    ]

    for dep in dependencies:
        print(f"Installing {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            sys.exit(1)

    print("✅ GPT Automation dependencies installed!")
    print("\nVerifying imports...")

    try:
        from ai_automation import AutomationEngine

        print("✅ GPT Automation integration verified!")
        print("\n📋 Next steps:")
        print("1. Set OPENAI_API_KEY in your .env file")
        print("2. Import with: from ai_automation import AutomationEngine")
        print("3. Use: engine = AutomationEngine(); response = engine.run_prompt('Hello')")

    except ImportError as e:
        print(f"❌ Import verification failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
