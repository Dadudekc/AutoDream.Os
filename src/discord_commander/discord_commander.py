import logging
logger = logging.getLogger(__name__)
"""
Discord Commander - V2 Compliance Module
========================================

Main Discord integration for V2_SWARM DevLog monitoring and agent communication.

Author: Agent-3 (Infrastructure & DevOps) - V2 Restoration
License: MIT
"""
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any
try:
    from .agent_communication_engine_refactored import AgentCommunicationEngine
    from .discord_webhook_integration import DiscordWebhookIntegration
    from .onboarding_integration import DiscordOnboardingIntegration, integrate_onboarding_with_discord_commander
except ImportError:
    from agent_communication_engine_refactored import AgentCommunicationEngine
    from discord_webhook_integration import DiscordWebhookIntegration
    from onboarding_integration import DiscordOnboardingIntegration, integrate_onboarding_with_discord_commander


class DiscordCommander:
    """Main Discord commander for V2_SWARM DevLog integration."""

    def __init__(self, webhook_url: (str | None)=None):
        """Initialize Discord commander."""
        self.agent_engine = AgentCommunicationEngine()
        self.webhook_integration = DiscordWebhookIntegration(webhook_url)
        self.devlogs_path = Path('devlogs')
        self.last_check_time = datetime.utcnow()
        self.is_running = False
        self.onboarding_integration = None
        self.command_handlers = {}

    async def start_devlog_monitoring(self, check_interval: int=60):
        """Start monitoring devlogs and sending Discord notifications."""
        logger.info('🚀 Starting Discord DevLog monitoring...')
        logger.info(f'📁 Monitoring directory: {self.devlogs_path}')
        logger.info(f'⏱️  Check interval: {check_interval} seconds')
        logger.info('')
        if not self.devlogs_path.exists():
            logger.info(f'❌ DevLogs directory not found: {self.devlogs_path}')
            return
        if not self.webhook_integration.test_webhook_connection():
            logger.info('⚠️  Continuing without Discord notifications...')
            logger.info('')
        self.is_running = True
        try:
            while self.is_running:
                await self._check_for_new_devlogs()
                await asyncio.sleep(check_interval)
        except KeyboardInterrupt:
            logger.info('\n🛑 DevLog monitoring stopped by user')
        except Exception as e:
            logger.info(f'\n❌ DevLog monitoring error: {e}')
        finally:
            self.is_running = False

    async def _check_for_new_devlogs(self):
        """Check for new devlog files and process them."""
        try:
            new_devlogs = self._find_new_devlogs()
            for devlog_path in new_devlogs:
                await self._process_devlog(devlog_path)
        except Exception as e:
            logger.info(f'❌ Error checking devlogs: {e}')

    def _find_new_devlogs(self) ->list[Path]:
        """Find devlog files newer than last check."""
        new_files = []
        if not self.devlogs_path.exists():
            return new_files
        for file_path in self.devlogs_path.rglob('*.md'):
            if file_path.stat().st_mtime > self.last_check_time.timestamp():
                new_files.append(file_path)
        return sorted(new_files, key=lambda x: x.stat().st_mtime)

    async def _process_devlog(self, devlog_path: Path):
        """Process a single devlog file."""
        try:
            with open(devlog_path, encoding='utf-8') as f:
                content = f.read()
            filename = devlog_path.name
            metadata = self._parse_devlog_filename(filename)
            devlog_data = {'title': metadata.get('title', filename),
                'description': self._extract_devlog_summary(content),
                'category': metadata.get('category', 'general'), 'agent':
                metadata.get('agent', 'Unknown'), 'filepath': str(
                devlog_path), 'timestamp': datetime.utcnow().isoformat()}
            logger.info(f"📝 Processing devlog: {devlog_data['title']}")
            if self.webhook_integration.send_devlog_notification(devlog_data):
                logger.info('✅ Discord notification sent')
                await self._notify_agents_of_devlog(devlog_data)
            else:
                logger.info('❌ Failed to send Discord notification')
        except Exception as e:
            logger.info(f'❌ Error processing devlog {devlog_path}: {e}')

    def _parse_devlog_filename(self, filename: str) ->dict[str, str]:
        """Parse metadata from devlog filename."""
        parts = filename.replace('.md', '').split('_')
        metadata = {'timestamp': 'unknown', 'category': 'general', 'agent':
            'Unknown', 'title': filename}
        if len(parts) >= 4:
            metadata['timestamp'] = f'{parts[0]}_{parts[1]}'
            metadata['category'] = parts[2]
            metadata['agent'] = parts[3]
            metadata['title'] = '_'.join(parts[4:]) if len(parts
                ) > 4 else 'DevLog Update'
        return metadata

    def _extract_devlog_summary(self, content: str, max_length: int=500) ->str:
        """Extract summary from devlog content."""
        lines = content.split('\n')
        summary = ''
        for line in lines[:20]:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 20:
                summary += line + ' '
                if len(summary) > max_length:
                    break
        if not summary:
            summary = 'DevLog update processed by V2_SWARM monitoring system.'
        return summary[:max_length].strip()

    async def _notify_agents_of_devlog(self, devlog_data: dict[str, Any]):
        """Notify relevant agents about the devlog."""
        try:
            agent = devlog_data.get('agent', 'Unknown')
            category = devlog_data.get('category', 'general')
            message = f"""🚨 DEVCORD DEVLOG ALERT

**New DevLog Activity Detected:**
• **Title:** {devlog_data['title']}
• **Category:** {category.title()}
• **Agent:** {agent}
• **Summary:** {devlog_data['description'][:200]}...

**DevLog monitoring is active and Discord notifications are enabled.**
**WE ARE SWARM - Stay coordinated!**

---
*Automated DevLog Monitor*
"""
            result = await self.agent_engine.broadcast_to_all_agents(message,
                sender='Discord_DevLog_Monitor')
            if result.success:
                logger.info(
                    f"✅ Notified {result.data.get('successful_deliveries', 0)} agents"
                    )
            else:
                logger.info('❌ Failed to notify agents about devlog')
        except Exception as e:
            logger.info(f'❌ Error notifying agents: {e}')

    async def send_agent_status_update(self, agent_id: str, status: str,
        details: str=''):
        """Send agent status update via Discord."""
        status_data = {'agent_id': agent_id, 'status': status,
            'last_activity': details or
            f'Status update at {datetime.utcnow().isoformat()}',
            'timestamp': datetime.utcnow().isoformat()}
        if self.webhook_integration.send_agent_status_notification(status_data
            ):
            logger.info(f'✅ Agent {agent_id} status sent to Discord')
        else:
            logger.info(f'❌ Failed to send agent {agent_id} status to Discord')

    async def send_coordination_notification(self, topic: str, description:
        str, priority: str='NORMAL'):
        """Send swarm coordination notification via Discord."""
        coordination_data = {'topic': topic, 'description': description,
            'priority': priority, 'participants': ['All Agents'],
            'timestamp': datetime.utcnow().isoformat()}
        if self.webhook_integration.send_swarm_coordination_notification(
            coordination_data):
            logger.info(f'✅ Coordination notification sent: {topic}')
        else:
            logger.info('❌ Failed to send coordination notification')

    def stop_monitoring(self):
        """Stop devlog monitoring."""
        self.is_running = False
        logger.info('🛑 DevLog monitoring stopping...')

    async def test_integration(self):
        """Test all Discord integration components."""
        logger.info('🧪 Testing Discord Commander Integration')
        logger.info('=' * 50)
        webhook_test = self.webhook_integration.test_webhook_connection()
        logger.info(
            f"Webhook Connection: {'✅ PASS' if webhook_test else '❌ FAIL'}")
        test_message = """🧪 **Discord Commander Integration Test**

Testing agent communication system..."""
        broadcast_result = await self.agent_engine.broadcast_to_all_agents(
            test_message, sender='Discord_Commander_Test')
        agent_test = broadcast_result.success
        logger.info(
            f"Agent Communication: {'✅ PASS' if agent_test else '❌ FAIL'}")
        devlog_test_data = {'title': 'Integration Test DevLog',
            'description':
            'Testing Discord DevLog integration functionality', 'category':
            'testing', 'agent': 'Discord_Commander', 'filepath':
            'test/integration_test.md', 'timestamp': datetime.utcnow().
            isoformat()}
        devlog_test = self.webhook_integration.send_devlog_notification(
            devlog_test_data)
        logger.info(
            f"DevLog Processing: {'✅ PASS' if devlog_test else '❌ FAIL'}")
        all_tests_pass = webhook_test and agent_test and devlog_test
        logger.info(
            f"""
📊 Integration Test Result: {'✅ ALL TESTS PASSED' if all_tests_pass else '❌ SOME TESTS FAILED'}"""
            )
        return all_tests_pass
    
    def setup_onboarding_integration(self, onboarding_service):
        """Setup onboarding integration with Discord Commander."""
        try:
            self.onboarding_integration = DiscordOnboardingIntegration(self, onboarding_service)
            logger.info("✅ Onboarding integration setup completed")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to setup onboarding integration: {e}")
            return False
    
    def add_command_handler(self, command: str, handler):
        """Add a command handler for Discord commands."""
        self.command_handlers[command] = handler
        logger.info(f"📝 Added command handler: {command}")
    
    async def handle_discord_command(self, command: str, args: Dict[str, Any] = None) -> str:
        """Handle Discord commands."""
        try:
            if not args:
                args = {}
            
            command_parts = command.lower().split()
            base_command = command_parts[0] if command_parts else ""
            
            # Handle onboarding commands
            if base_command in ["onboard", "onboarding", "onboard_all", "agent_state", "contracts", "reset_agent"]:
                if self.onboarding_integration:
                    return await self.onboarding_integration.handle_discord_command(command, args)
                else:
                    return "❌ Onboarding integration not available"
            
            # Handle other command handlers
            if base_command in self.command_handlers:
                return await self.command_handlers[base_command](args)
            
            return f"❌ Unknown command: {base_command}. Use 'help' for available commands."
            
        except Exception as e:
            logger.error(f"Discord command failed: {e}")
            return f"❌ Command failed: {e}"
    
    async def send_notification(self, notification: Dict[str, Any]):
        """Send notification via Discord webhook."""
        try:
            if self.webhook_integration:
                # Format notification for Discord
                if notification.get("type") == "onboarding_notification":
                    message = f"🤖 **Onboarding Update**\n"
                    message += f"**Agent**: {notification.get('agent_id', 'Unknown')}\n"
                    message += f"**Event**: {notification.get('event_type', 'Unknown')}\n"
                    if notification.get('details'):
                        message += f"**Details**: {notification['details']}\n"
                    message += f"**Time**: {notification.get('timestamp', 'Unknown')}"
                    
                    # Send as devlog notification
                    devlog_data = {
                        'title': f"Onboarding: {notification.get('agent_id', 'Unknown')}",
                        'description': message,
                        'category': 'onboarding',
                        'agent': notification.get('agent_id', 'System'),
                        'filepath': 'onboarding/notification.md',
                        'timestamp': notification.get('timestamp', datetime.utcnow().isoformat())
                    }
                    
                    return self.webhook_integration.send_devlog_notification(devlog_data)
            
            return False
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False


_discord_commander_instance = None


def get_discord_commander(webhook_url: (str | None)=None) ->DiscordCommander:
    """Get Discord commander instance (singleton pattern)."""
    global _discord_commander_instance
    if _discord_commander_instance is None:
        _discord_commander_instance = DiscordCommander(webhook_url)
    return _discord_commander_instance


async def start_discord_devlog_monitoring(webhook_url: (str | None)=None,
    check_interval: int=60):
    """Start Discord DevLog monitoring (convenience function)."""
    commander = get_discord_commander(webhook_url)
    await commander.start_devlog_monitoring(check_interval)


if __name__ == '__main__':

    async def main():
        commander = DiscordCommander()
        await commander.test_integration()
    asyncio.run(main())
