"""
Soft Onboarding Handler - V2 Compliant Module
============================================

Handles soft onboarding commands for messaging CLI.
Integrates with soft_onboarding_service for 3-step protocol.

V2 Compliance: < 300 lines, single responsibility
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SoftOnboardingHandler:
    """Handles soft onboarding commands for messaging CLI."""

    def __init__(self):
        """Initialize soft onboarding handler."""
        self.exit_code = 0

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return (
            hasattr(args, "soft_onboarding")
            and args.soft_onboarding
            or hasattr(args, "onboarding_step")
            and args.onboarding_step
        )

    def _load_full_onboarding_template(
        self, agent_id: str, role: str, custom_message: str = ""
    ) -> str:
        """
        Load full onboarding template with operating cycle duties.

        Args:
            agent_id: Agent ID (e.g., "Agent-1")
            role: Agent role description
            custom_message: Optional custom mission message

        Returns:
            Complete onboarding message with template + custom content
        """
        try:
            # Load full template
            template_path = Path("prompts/agents/onboarding.md")
            if template_path.exists():
                template = template_path.read_text(encoding="utf-8")

                # Replace placeholders
                template = template.replace("{agent_id}", agent_id)
                template = template.replace("{role}", role)

                # If custom message provided, prepend it
                if custom_message:
                    full_message = f"## 🎯 YOUR MISSION:\n\n{custom_message}\n\n---\n\n{template}"
                else:
                    full_message = template

                logger.info(f"✅ Loaded full onboarding template for {agent_id}")
                return full_message
            else:
                logger.warning("⚠️ Template not found, using custom message only")
                return custom_message or ""

        except Exception as e:
            logger.error(f"❌ Failed to load template: {e}")
            return custom_message or ""

    def handle(self, args) -> bool:
        """Handle soft onboarding commands."""
        try:
            from ..soft_onboarding_service import SoftOnboardingService

            # Validate required arguments
            if not args.agent and not args.onboarding_step == 2:
                logger.error("❌ --agent required for soft onboarding (except step 2)")
                self.exit_code = 1
                return True

            if not args.message and not args.onboarding_file and not args.onboarding_step:
                logger.error("❌ --message or --onboarding-file required for soft onboarding")
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

            # CRITICAL FIX: Load FULL template with operating cycle duties
            if args.agent and not args.onboarding_step:
                role = args.role or "Agent"
                message = self._load_full_onboarding_template(args.agent, role, message)
                logger.info("✅ Using full onboarding template with operating cycle duties")

            # Handle dry run
            if args.dry_run:
                logger.info("🧪 DRY RUN MODE - No actions will be executed")
                logger.info(f"Would soft onboard: {args.agent}")
                if message:
                    logger.info(f"Message: {message[:100]}...")
                if args.role:
                    logger.info(f"Role: {args.role}")
                if args.onboarding_step:
                    logger.info(f"Step: {args.onboarding_step}")
                self.exit_code = 0
                return True

            # Initialize service
            service = SoftOnboardingService()

            # Handle single step execution
            if args.onboarding_step:
                self.exit_code = self._handle_single_step(service, args, message)
                return True

            # Handle full soft onboarding protocol
            logger.info(f"🚀 Starting soft onboarding for {args.agent}")

            success = service.execute_soft_onboarding(
                agent_id=args.agent,
                onboarding_message=message,
                role=args.role,
                custom_cleanup_message=args.cleanup_message,
            )

            if success:
                logger.info(f"🎉 Soft onboarding complete for {args.agent}!")
                self.exit_code = 0
            else:
                logger.error(f"❌ Soft onboarding failed for {args.agent}")
                self.exit_code = 1

            return True

        except ImportError as e:
            logger.error(f"❌ Soft onboarding service not available: {e}")
            self.exit_code = 1
            return True
        except Exception as e:
            logger.error(f"❌ Soft onboarding error: {e}")
            self.exit_code = 1
            return True

    def _handle_single_step(self, service, args, message) -> int:
        """Handle single step execution."""
        try:
            if args.onboarding_step == 1:
                # Step 1: Click chat input
                if not args.agent:
                    logger.error("❌ --agent required for step 1")
                    return 1

                logger.info(f"👆 Step 1: Clicking chat input for {args.agent}")
                success = service.step_1_click_chat_input(args.agent)

                if success:
                    logger.info("✅ Chat input clicked!")
                    return 0
                else:
                    logger.error("❌ Failed to click chat input")
                    return 1

            elif args.onboarding_step == 2:
                # Step 2: Save session (no agent required)
                logger.info("💾 Step 2: Saving session (Ctrl+Enter)")
                success = service.step_2_save_session()

                if success:
                    logger.info("✅ Session saved!")
                    return 0
                else:
                    logger.error("❌ Failed to save session")
                    return 1

            elif args.onboarding_step == 3:
                # Step 3: Send cleanup prompt
                if not args.agent:
                    logger.error("❌ --agent required for step 3")
                    return 1

                logger.info(f"📝 Step 3: Sending cleanup prompt to {args.agent}")
                success = service.step_3_send_cleanup_prompt(args.agent, args.cleanup_message)

                if success:
                    logger.info("✅ Cleanup prompt sent!")
                    logger.info(
                        "⏳ Agent should complete: passdown.json, devlog, "
                        "Discord post, swarm brain update, tool creation"
                    )
                    return 0
                else:
                    logger.error("❌ Failed to send cleanup prompt")
                    return 1

            elif args.onboarding_step == 4:
                # Step 4: Open new tab (no agent required)
                logger.info("🆕 Step 4: Opening new tab (Ctrl+T)")
                success = service.step_4_open_new_tab()

                if success:
                    logger.info("✅ New tab opened!")
                    return 0
                else:
                    logger.error("❌ Failed to open new tab")
                    return 1

            elif args.onboarding_step == 5:
                # Step 5: Navigate to onboarding
                if not args.agent:
                    logger.error("❌ --agent required for step 5")
                    return 1

                logger.info(f"🎯 Step 5: Navigating to onboarding coords for {args.agent}")
                success = service.step_5_navigate_to_onboarding(args.agent)

                if success:
                    logger.info("✅ Navigated to onboarding input!")
                    return 0
                else:
                    logger.error("❌ Failed to navigate to onboarding")
                    return 1

            elif args.onboarding_step == 6:
                # Step 6: Paste onboarding message
                if not args.agent:
                    logger.error("❌ --agent required for step 6")
                    return 1

                if not message:
                    logger.error("❌ --message or --onboarding-file required for step 6")
                    return 1

                logger.info(f"📝 Step 6: Pasting onboarding message for {args.agent}")
                success = service.step_6_paste_onboarding_message(args.agent, message)

                if success:
                    logger.info("✅ Onboarding message sent!")
                    return 0
                else:
                    logger.error("❌ Failed to paste onboarding message")
                    return 1

        except Exception as e:
            logger.error(f"❌ Step execution error: {e}")
            return 1

        return 1
