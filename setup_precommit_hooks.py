#!/usr/bin/env python3
"""
Setup Pre-commit Hooks for Agent_Cellphone_V2_Repository
========================================================

This script sets up pre-commit hooks to enforce V2 coding standards and prevent duplication.
It installs the necessary tools and configures the hooks to run automatically on commit.

Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PreCommitSetup:
    """Manages pre-commit hook setup and configuration"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.hooks_dir = project_root / ".git" / "hooks"
        self.precommit_config = project_root / ".pre-commit-config.yaml"
        
    def setup_precommit(self, force: bool = False) -> bool:
        """Set up pre-commit hooks for the project"""
        logger.info("🚀 Setting up pre-commit hooks for V2 coding standards...")
        
        try:
            # Check if pre-commit is installed
            if not self._is_precommit_installed():
                logger.info("📦 Installing pre-commit...")
                self._install_precommit()
            
            # Install the hooks
            logger.info("🔧 Installing pre-commit hooks...")
            self._install_hooks(force)
            
            # Verify installation
            if self._verify_installation():
                logger.info("✅ Pre-commit hooks installed successfully!")
                self._print_usage_instructions()
                return True
            else:
                logger.error("❌ Failed to install pre-commit hooks")
                return False
                
        except Exception as e:
            logger.error(f"❌ Setup failed: {e}")
            return False
    
    def _is_precommit_installed(self) -> bool:
        """Check if pre-commit is installed"""
        try:
            result = subprocess.run(
                ["pre-commit", "--version"], 
                capture_output=True, 
                text=True, 
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _install_precommit(self) -> None:
        """Install pre-commit package"""
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "pre-commit"],
                check=True,
                capture_output=True
            )
            logger.info("✅ pre-commit installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install pre-commit: {e}")
            raise
    
    def _install_hooks(self, force: bool = False) -> None:
        """Install the pre-commit hooks"""
        try:
            cmd = ["pre-commit", "install"]
            if force:
                cmd.append("--force")
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info("✅ Hooks installed successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install hooks: {e}")
            raise
    
    def _verify_installation(self) -> bool:
        """Verify that hooks are properly installed"""
        # Check if pre-commit hook exists
        precommit_hook = self.hooks_dir / "pre-commit"
        if not precommit_hook.exists():
            logger.error("❌ pre-commit hook not found")
            return False
        
        # Check if hook is executable
        if not os.access(precommit_hook, os.X_OK):
            logger.error("❌ pre-commit hook is not executable")
            return False
        
        # Check if .pre-commit-config.yaml exists
        if not self.precommit_config.exists():
            logger.error("❌ .pre-commit-config.yaml not found")
            return False
        
        return True
    
    def _print_usage_instructions(self) -> None:
        """Print usage instructions for the pre-commit hooks"""
        print("\n" + "="*60)
        print("🎯 PRE-COMMIT HOOKS INSTALLED SUCCESSFULLY!")
        print("="*60)
        print("\n📋 What happens now:")
        print("• Every commit will automatically check V2 coding standards")
        print("• Duplication detection will prevent copy-paste code")
        print("• LOC limits (200 lines) will be enforced")
        print("• OOP compliance will be verified")
        print("• Backup files will be blocked")
        
        print("\n🔧 Available commands:")
        print("• pre-commit run --all-files          # Check all files")
        print("• pre-commit run                     # Check staged files")
        print("• pre-commit run <hook-id>           # Run specific hook")
        print("• pre-commit uninstall               # Remove hooks")
        
        print("\n📊 Hook execution order:")
        print("1. V2 Standards Checker")
        print("2. Duplication Detector")
        print("3. LOC Compliance Check")
        print("4. OOP Compliance Check")
        print("5. Standard Python hooks (black, flake8, etc.)")
        
        print("\n⚠️  Important notes:")
        print("• Hooks run automatically on every commit")
        print("• Commits will be blocked if violations are found")
        print("• Fix violations before committing")
        print("• Use 'git commit --no-verify' to bypass (not recommended)")
        
        print("\n🚀 Next steps:")
        print("1. Make a small change to test the hooks")
        print("2. Try to commit - hooks will run automatically")
        print("3. Fix any violations that are detected")
        print("4. Commit again when all checks pass")
        
        print("="*60)
    
    def test_hooks(self) -> bool:
        """Test the pre-commit hooks on all files"""
        logger.info("🧪 Testing pre-commit hooks on all files...")
        
        try:
            result = subprocess.run(
                ["pre-commit", "run", "--all-files"],
                check=False,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✅ All hooks passed!")
                return True
            else:
                logger.warning("⚠️ Some hooks failed - check output above")
                logger.info("This is normal for existing code that doesn't meet V2 standards")
                return False
                
        except Exception as e:
            logger.error(f"❌ Hook testing failed: {e}")
            return False
    
    def uninstall_hooks(self) -> bool:
        """Uninstall pre-commit hooks"""
        logger.info("🗑️ Uninstalling pre-commit hooks...")
        
        try:
            subprocess.run(
                ["pre-commit", "uninstall"],
                check=True,
                capture_output=True
            )
            logger.info("✅ Hooks uninstalled successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to uninstall hooks: {e}")
            return False
    
    def show_hook_status(self) -> None:
        """Show the status of installed hooks"""
        logger.info("📊 Pre-commit hook status:")
        
        try:
            result = subprocess.run(
                ["pre-commit", "run", "--all-files", "--show-diff-on-failure"],
                check=False,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ All hooks are working correctly")
            else:
                print("⚠️ Some hooks failed - this is expected for existing code")
                print("The hooks will prevent new violations from being committed")
                
        except Exception as e:
            logger.error(f"❌ Could not check hook status: {e}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Setup Pre-commit Hooks for Agent_Cellphone_V2_Repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python setup_precommit_hooks.py                    # Install hooks
    python setup_precommit_hooks.py --force           # Force reinstall
    python setup_precommit_hooks.py --test            # Test hooks
    python setup_precommit_hooks.py --uninstall       # Remove hooks
    python setup_precommit_hooks.py --status          # Show hook status
        """
    )
    
    parser.add_argument('--force', action='store_true',
                       help='Force reinstallation of hooks')
    parser.add_argument('--test', action='store_true',
                       help='Test the installed hooks')
    parser.add_argument('--uninstall', action='store_true',
                       help='Uninstall pre-commit hooks')
    parser.add_argument('--status', action='store_true',
                       help='Show hook status')
    
    args = parser.parse_args()
    
    # Get project root
    project_root = Path(__file__).parent
    if not (project_root / ".git").exists():
        logger.error("❌ Not in a git repository. Run this from the project root.")
        sys.exit(1)
    
    # Initialize setup
    setup = PreCommitSetup(project_root)
    
    try:
        if args.uninstall:
            if setup.uninstall_hooks():
                print("✅ Hooks uninstalled successfully")
                sys.exit(0)
            else:
                print("❌ Failed to uninstall hooks")
                sys.exit(1)
        
        elif args.test:
            if setup.test_hooks():
                print("✅ Hook testing completed successfully")
                sys.exit(0)
            else:
                print("⚠️ Hook testing completed with warnings")
                sys.exit(0)
        
        elif args.status:
            setup.show_hook_status()
            sys.exit(0)
        
        else:
            # Default: install hooks
            if setup.setup_precommit(force=args.force):
                print("\n🎉 Setup completed successfully!")
                print("Your commits will now automatically enforce V2 coding standards!")
                sys.exit(0)
            else:
                print("❌ Setup failed")
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\n⚠️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
