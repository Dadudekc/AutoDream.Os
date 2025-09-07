"""
setup_precommit_hooks_part_4.py
Module: setup_precommit_hooks_part_4.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:47
"""

# Part 4 of setup_precommit_hooks.py
# Original file: .\scripts\utilities\setup_precommit_hooks.py

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

