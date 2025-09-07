"""
setup_precommit_hooks_part_2.py
Module: setup_precommit_hooks_part_2.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:47
"""

# Part 2 of setup_precommit_hooks.py
# Original file: .\scripts\utilities\setup_precommit_hooks.py

                capture_output=True
            )
            logger.info("✅ pre-commit installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install pre-commit: {e}")
            raise
    
    def _install_hooks(self, force: bool = False) -> None:
        """
        _install_hooks
        
        Purpose: Automated function documentation
        """
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

