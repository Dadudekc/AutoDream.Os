#!/usr/bin/env python3
"""
Service Manager for Agent Cellphone V2
=====================================

Central service manager that coordinates all system services including the new ChatMate integration.
Provides unified startup, shutdown, and service coordination for the multi-agent system.

V2 Compliance: ≤400 lines, comprehensive service orchestration
"""

import asyncio
import logging
import signal
import sys
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

# Import all services
from . import (
    ConsolidatedMessagingService,
    IntegratedDiscordBotService,
    get_social_media_service,
    initialize_social_media_integration,
    EnhancedDiscordAgentBot,
    AgentDevlogAutomation,
    AgentDevlogPoster
)

logger = logging.getLogger(__name__)


class ServiceManager:
    """
    Central service manager for the Agent Cellphone V2 system.

    Coordinates:
    - Messaging service
    - Discord bot integration
    - ChatMate social media integration
    - Devlog automation
    - Agent coordination

    Provides unified startup/shutdown and service health monitoring.
    """

    def __init__(self):
        """Initialize the service manager."""
        self.logger = logging.getLogger(f"{__name__}.ServiceManager")

        # Service instances
        self.messaging_service: Optional[ConsolidatedMessagingService] = None
        self.discord_bot: Optional[EnhancedDiscordAgentBot] = None
        self.social_media_service = None
        self.devlog_automation: Optional[AgentDevlogAutomation] = None
        self.devlog_posting: Optional[AgentDevlogPosting] = None

        # Service status
        self.services_status = {}
        self.is_running = False
        self.startup_complete = False

        # Configuration
        self.config = {
            'auto_start_discord': True,
            'auto_start_social_media': True,
            'health_check_interval': 30,  # seconds
            'max_retries': 3
        }

        self.logger.info("Service Manager initialized")

    async def start_all_services(self) -> bool:
        """
        Start all system services in the correct order.

        Returns:
            bool: True if all services started successfully, False otherwise
        """
        self.logger.info("🚀 Starting all services...")
        self.is_running = True

        try:
            # Step 1: Initialize core messaging service
            await self._start_messaging_service()

            # Step 2: Initialize ChatMate social media integration
            await self._start_social_media_service()

            # Step 3: Initialize Discord bot
            await self._start_discord_bot()

            # Step 4: Initialize devlog services
            await self._start_devlog_services()

            # Step 5: Start health monitoring
            asyncio.create_task(self._health_monitoring_loop())

            self.startup_complete = True
            self.logger.info("✅ All services started successfully")

            # Log service status
            self._log_service_status()

            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to start services: {e}")
            await self.stop_all_services()
            return False

    async def _start_messaging_service(self):
        """Start the consolidated messaging service."""
        try:
            self.logger.info("📨 Starting messaging service...")
            self.messaging_service = ConsolidatedMessagingService()
            self.services_status['messaging'] = 'active'
            self.logger.info("✅ Messaging service started")
        except Exception as e:
            self.logger.error(f"❌ Failed to start messaging service: {e}")
            self.services_status['messaging'] = 'failed'
            raise

    async def _start_social_media_service(self):
        """Start the ChatMate social media integration."""
        try:
            self.logger.info("🌐 Starting ChatMate social media integration...")
            success = await initialize_social_media_integration()
            if success:
                self.social_media_service = get_social_media_service()
                self.services_status['social_media'] = 'active'
                self.logger.info("✅ ChatMate social media integration started")
            else:
                self.services_status['social_media'] = 'inactive'
                self.logger.warning("⚠️ ChatMate social media integration not available")
        except Exception as e:
            self.logger.error(f"❌ Failed to start social media service: {e}")
            self.services_status['social_media'] = 'failed'
            raise

    async def _start_discord_bot(self):
        """Start the Discord bot with social media integration."""
        try:
            if not self.config['auto_start_discord']:
                self.logger.info("🤖 Discord bot startup disabled in config")
                self.services_status['discord_bot'] = 'disabled'
                return

            self.logger.info("🤖 Starting Discord bot with ChatMate integration...")

            # Create Discord bot instance
            self.discord_bot = EnhancedDiscordAgentBot(command_prefix="!")

            # Add service integrations
            self.discord_bot.messaging_service = self.messaging_service
            self.discord_bot.social_media_service = self.social_media_service

            # Note: Discord bot will only connect when run() is called with a valid token
            self.services_status['discord_bot'] = 'ready'
            self.logger.info("✅ Discord bot initialized with ChatMate integration")

        except Exception as e:
            self.logger.error(f"❌ Failed to start Discord bot: {e}")
            self.services_status['discord_bot'] = 'failed'
            raise

    async def _start_devlog_services(self):
        """Start devlog automation and posting services."""
        try:
            self.logger.info("📝 Starting devlog services...")

            # Initialize devlog automation
            self.devlog_automation = AgentDevlogAutomation()
            self.services_status['devlog_automation'] = 'active'

            # Initialize devlog posting
            self.devlog_posting = AgentDevlogPosting()
            self.services_status['devlog_posting'] = 'active'

            self.logger.info("✅ Devlog services started")

        except Exception as e:
            self.logger.error(f"❌ Failed to start devlog services: {e}")
            self.services_status['devlog_automation'] = 'failed'
            self.services_status['devlog_posting'] = 'failed'
            raise

    async def _health_monitoring_loop(self):
        """Health monitoring loop for all services."""
        self.logger.info("💓 Starting health monitoring...")

        while self.is_running:
            try:
                await self._perform_health_checks()
                await asyncio.sleep(self.config['health_check_interval'])
            except Exception as e:
                self.logger.error(f"❌ Health monitoring error: {e}")
                await asyncio.sleep(5)  # Brief pause on error

    async def _perform_health_checks(self):
        """Perform health checks on all services."""
        health_report = {
            'timestamp': datetime.utcnow().isoformat(),
            'services': {}
        }

        # Check messaging service
        if self.messaging_service:
            health_report['services']['messaging'] = 'healthy'

        # Check social media service
        if self.social_media_service and self.social_media_service.is_integrated:
            health_report['services']['social_media'] = 'healthy'
        elif self.social_media_service:
            health_report['services']['social_media'] = 'partial'

        # Check Discord bot
        if self.discord_bot and self.discord_bot.is_ready():
            health_report['services']['discord_bot'] = 'healthy'
        elif self.discord_bot:
            health_report['services']['discord_bot'] = 'ready'

        # Check devlog services
        if self.devlog_automation:
            health_report['services']['devlog_automation'] = 'healthy'
        if self.devlog_posting:
            health_report['services']['devlog_posting'] = 'healthy'

        # Log health status
        healthy_count = sum(1 for status in health_report['services'].values() if status == 'healthy')
        total_count = len(health_report['services'])

        self.logger.info(f"💓 Health check: {healthy_count}/{total_count} services healthy")

        # Store health report (could be used for monitoring/alerting)
        self._store_health_report(health_report)

    def _store_health_report(self, report: Dict[str, Any]):
        """Store health report for monitoring purposes."""
        # In a real system, this would be stored in a database or sent to monitoring
        pass

    def _log_service_status(self):
        """Log current status of all services."""
        self.logger.info("📊 Current Service Status:")
        for service, status in self.services_status.items():
            emoji = {
                'active': '✅',
                'ready': '🟡',
                'inactive': '⚫',
                'disabled': '🚫',
                'failed': '❌'
            }.get(status, '❓')

            self.logger.info(f"   {emoji} {service}: {status}")

    async def stop_all_services(self):
        """Stop all running services gracefully."""
        self.logger.info("🛑 Stopping all services...")
        self.is_running = False

        try:
            # Stop Discord bot
            if self.discord_bot:
                await self.discord_bot.close()
                self.logger.info("✅ Discord bot stopped")

            # Stop other services
            self.services_status = {k: 'stopped' for k in self.services_status.keys()}
            self.logger.info("✅ All services stopped")

        except Exception as e:
            self.logger.error(f"❌ Error stopping services: {e}")

    def get_service_status(self) -> Dict[str, Any]:
        """Get current status of all services."""
        return {
            'is_running': self.is_running,
            'startup_complete': self.startup_complete,
            'services': self.services_status.copy(),
            'health': 'healthy' if self.is_running else 'stopped'
        }

    async def run_discord_bot(self, token: str):
        """Run the Discord bot with the provided token."""
        if not self.discord_bot:
            await self._start_discord_bot()

        if self.discord_bot:
            self.logger.info("🚀 Starting Discord bot...")
            try:
                await self.discord_bot.start(token)
            except Exception as e:
                self.logger.error(f"❌ Failed to start Discord bot: {e}")
                raise
        else:
            raise RuntimeError("Discord bot not initialized")


# Global service manager instance
_service_manager = None

def get_service_manager() -> ServiceManager:
    """Get or create the global service manager instance."""
    global _service_manager
    if _service_manager is None:
        _service_manager = ServiceManager()
    return _service_manager

async def start_all_services() -> bool:
    """Start all services using the global service manager."""
    manager = get_service_manager()
    return await manager.start_all_services()

async def stop_all_services():
    """Stop all services using the global service manager."""
    manager = get_service_manager()
    await manager.stop_all_services()

def get_service_status() -> Dict[str, Any]:
    """Get service status from the global service manager."""
    manager = get_service_manager()
    return manager.get_service_status()


# Signal handlers for graceful shutdown
def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}, shutting down...")
    asyncio.create_task(stop_all_services())

async def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown."""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


async def main():
    """Main entry point for the service manager."""
    print("🐝 Agent Cellphone V2 Service Manager")
    print("=====================================")

    # Setup signal handlers
    await setup_signal_handlers()

    try:
        # Start all services
        success = await start_all_services()

        if success:
            manager = get_service_manager()
            print("✅ All services started successfully!")

            # Get service status
            status = manager.get_service_status()
            print(f"📊 Services: {len(status['services'])} total")
            print(f"💓 Health: {status['health']}")
            print(f"🔗 ChatMate Integration: {'✅ Active' if status['services'].get('social_media') == 'active' else '⚠️ Limited'}")

            # Keep the main task running
            while manager.is_running:
                await asyncio.sleep(1)

        else:
            print("❌ Failed to start services")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n🛑 Received keyboard interrupt, shutting down...")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
    finally:
        await stop_all_services()
        print("✅ Shutdown complete")


if __name__ == "__main__":
    # Run the service manager
    asyncio.run(main())
