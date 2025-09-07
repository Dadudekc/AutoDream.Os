"""
run_unified_portal_part_7.py
Module: run_unified_portal_part_7.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:00
"""

# Part 7 of run_unified_portal.py
# Original file: .\scripts\launchers\run_unified_portal.py


    if not args.command:
        parser.print_help()
        return

    try:
        # Create launcher
        config_path = args.config if hasattr(args, "config") and args.config else None
        launcher = PortalLauncher(config_path)

        if args.command == "launch":
            # Determine reload setting
            reload = None
            if args.reload:
                reload = True
            elif args.no_reload:
                reload = False

            launcher.launch_portal(
                backend_type=args.backend, host=args.host, port=args.port, reload=reload
            )

        elif args.command == "status":
            launcher.show_status()

        elif args.command == "test":
            launcher.test_integration()

    except KeyboardInterrupt:
        logger.info("Portal launch interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


