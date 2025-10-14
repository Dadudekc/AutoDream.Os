"""
Hard Onboarding Handler - V2 Compliant Module
============================================

Handles hard onboarding commands for messaging CLI.
Integrates with hard_onboarding_service for 5-step protocol.

V2 Compliance: < 300 lines, single responsibility
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class HardOnboardingHandler:
    """Handles hard onboarding commands for messaging CLI."""

    def __init__(self):
        """Initialize hard onboarding handler."""
        self.exit_code = 0

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return hasattr(args, "hard_onboarding") and args.hard_onboarding

    def handle(self, args) -> bool:
        """Handle hard onboarding commands."""
        try:
            from ..hard_onboarding_service import HardOnboardingService

            # Validate required arguments
            if not args.agent:
                logger.error("❌ --agent required for hard onboarding")
                self.exit_code = 1
                return True

            if not args.message and not args.onboarding_file:
                logger.error("❌ --message or --onboarding-file required for hard onboarding")
                self.exit_code = 1
                return True

            # Load message from file if specified
            message = args.message
            if args.onboarding_file:
                try:
                    message_file = Path(args.onboarding_file)
                    if not message_file.exists():
                        logger.error(f"❌ Onboarding file not found: {args.onboarding_file}")
                        self.exit_code = 1
                        return True
                    message = message_file.read_text(encoding="utf-8")
                    logger.info(f"📄 Loaded onboarding message from {args.onboarding_file}")
                except Exception as e:
                    logger.error(f"❌ Failed to read onboarding file: {e}")
                    self.exit_code = 1
                    return True

            # AUTONOMY: No confirmation required - Captain's directive is authorization
            # If Captain orders hard onboarding, execute immediately for autonomous operation
            logger.info(f"🚨 HARD ONBOARDING AUTHORIZED for {args.agent}")
            logger.info("  Protocol: Clear chat → Execute → New window → Navigate → Send message")

            # Handle dry run
            if args.dry_run:
                logger.info("🧪 DRY RUN MODE - No actions will be executed")
                logger.info(f"Would hard onboard: {args.agent}")
                if message:
                    logger.info(f"Message: {message[:100]}...")
                if args.role:
                    logger.info(f"Role: {args.role}")
                self.exit_code = 0
                return True

            # Initialize service
            service = HardOnboardingService()

            # Execute hard onboarding protocol
            logger.info(f"🚨 Starting HARD ONBOARDING for {args.agent}")

            success = service.execute_hard_onboarding(
                agent_id=args.agent,
                onboarding_message=message,
                role=args.role,
            )

            if success:
                logger.info(f"🎉 Hard onboarding complete for {args.agent}!")
                self.exit_code = 0
            else:
                logger.error(f"❌ Hard onboarding failed for {args.agent}")
                self.exit_code = 1

            return True

        except ImportError as e:
            logger.error(f"❌ Hard onboarding service not available: {e}")
            self.exit_code = 1
            return True
        except Exception as e:
            logger.error(f"❌ Hard onboarding error: {e}")
            self.exit_code = 1
            return True
