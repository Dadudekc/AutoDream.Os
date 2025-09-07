"""
setup_precommit_hooks_part_5.py
Module: setup_precommit_hooks_part_5.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:47
"""

# Part 5 of setup_precommit_hooks.py
# Original file: .\scripts\utilities\setup_precommit_hooks.py

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

