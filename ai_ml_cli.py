#!/usr/bin/env python3
"""
AI/ML CLI Launcher - Root Level Access
Quick access to AI/ML functionality for agents from anywhere in the repository

Usage:
    python ai_ml_cli.py --help
    python ai_ml_cli.py contracts
    python ai_ml_cli.py ai-status
    python ai_ml_cli.py system-status
"""

import sys
import os
from pathlib import Path

def main():
    """Main launcher that routes to appropriate CLI"""
    if len(sys.argv) < 2:
        print("🚀 AI/ML CLI Launcher")
        print("=" * 50)
        print("Quick Commands:")
        print("  python ai_ml_cli.py contracts          - Show available contracts")
        print("  python ai_ml_cli.py ai-status         - Show AI system status")
        print("  python ai_ml_cli.py ml-status         - Show ML system status")
        print("  python ai_ml_cli.py system-status     - Show overall system status")
        print("  python ai_ml_cli.py health-check      - Run system health check")
        print("  python ai_ml_cli.py quick-start       - Show quick start guide")
        print("\nAdvanced Usage:")
        print("  python ai_ml_cli.py --full --help     - Full CLI options")
        print("  python ai_ml_cli.py --full contracts --list --category emergency_system_restoration")
        print("\nDirect Module Access:")
        print("  python -m src.ai_ml.agent_cli --help  - Agent CLI help")
        print("  python -m src.ai_ml.cli --help        - Full CLI help")
        return
    
    # Check if user wants full CLI
    if sys.argv[1] == "--full":
        # Remove --full and pass remaining args to full CLI
        sys.argv = sys.argv[2:]
        try:
            # Add src to Python path
            src_path = Path(__file__).parent / "src"
            sys.path.insert(0, str(src_path))
            
            from ai_ml.cli import main as full_main
            full_main()
        except ImportError as e:
            print(f"❌ Error importing full CLI: {e}")
            print("💡 Try: python -m src.ai_ml.cli --help")
            sys.exit(1)
    else:
        # Use simplified agent CLI
        try:
            # Add src to Python path
            src_path = Path(__file__).parent / "src"
            sys.path.insert(0, str(src_path))
            
            from ai_ml.agent_cli import main as agent_main
            agent_main()
        except ImportError as e:
            print(f"❌ Error importing agent CLI: {e}")
            print("💡 Try: python -m src.ai_ml.agent_cli --help")
            print("💡 Or use direct module access:")
            print("   python -m src.ai_ml.agent_cli contracts")
            sys.exit(1)

if __name__ == "__main__":
    main()
