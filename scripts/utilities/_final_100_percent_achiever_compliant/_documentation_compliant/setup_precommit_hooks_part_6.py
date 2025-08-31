"""
setup_precommit_hooks_part_6.py
Module: setup_precommit_hooks_part_6.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:47
"""

# Part 6 of setup_precommit_hooks.py
# Original file: .\scripts\utilities\setup_precommit_hooks.py

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



