"""
launch_cross_system_communication_part_3.py
Module: launch_cross_system_communication_part_3.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:58
"""

# Part 3 of launch_cross_system_communication.py
# Original file: .\scripts\launchers\launch_cross_system_communication.py

        "--message-type",
        "-mt",
        default="request",
        choices=[
            "request",
            "response",
            "event",
            "command",
            "query",
            "notification",
            "heartbeat",
        ],
        help="Message type for send-message action",
    )

    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        default=300,
        help="Timeout in seconds for test execution",
    )

    args = parser.parse_args()

    # Create launcher
    launcher = CrossSystemCommunicationLauncher(args.config)

    try:
        if args.action == "start":
            success = await launcher.start()
            if success:
                logger.info("System started successfully")
                # Keep running until interrupted
                while launcher.running:
                    await asyncio.sleep(1)
            else:
                logger.error("Failed to start system")
                sys.exit(1)

        elif args.action == "stop":
            success = await launcher.stop()
            if success:
                logger.info("System stopped successfully")
            else:
                logger.error("Failed to stop system")
                sys.exit(1)

        elif args.action == "restart":
            await launcher.stop()
            await asyncio.sleep(2)
            success = await launcher.start()
            if success:
                logger.info("System restarted successfully")
            else:
                logger.error("Failed to restart system")
                sys.exit(1)

        elif args.action == "status":
            status = await launcher.get_status()
            print(json.dumps(status, indent=2, default=str))

        elif args.action == "test":
            if args.suite:
                results = await launcher.run_tests(args.suite)
            else:
                results = await launcher.run_tests()
            print(json.dumps(results, indent=2, default=str))

        elif args.action == "connect":
            if not args.system:
                logger.error("System ID required for connect action")
                sys.exit(1)
            success = await launcher.connect_system(args.system)
            if success:
                logger.info(f"Connected to system: {args.system}")
            else:
                logger.error(f"Failed to connect to system: {args.system}")
                sys.exit(1)

        elif args.action == "disconnect":
            if not args.system:
                logger.error("System ID required for disconnect action")
                sys.exit(1)
            success = await launcher.disconnect_system(args.system)
            if success:
                logger.info(f"Disconnected from system: {args.system}")
            else:
                logger.error(f"Failed to disconnect from system: {args.system}")
                sys.exit(1)

        elif args.action == "send-message":
            if not args.system:
                logger.error("System ID required for send-message action")
                sys.exit(1)
            success = await launcher.send_test_message(args.system, args.message_type)
            if success:
                logger.info(f"Test message sent to system: {args.system}")
            else:
                logger.error(f"Failed to send test message to system: {args.system}")
                sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
        await launcher.stop()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await launcher.stop()
        sys.exit(1)


if __name__ == "__main__":
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    # Run the launcher
    asyncio.run(main())


