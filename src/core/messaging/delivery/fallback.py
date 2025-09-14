#!/usr/bin/env python3
"""
Fallback Delivery Service - V2 Compliant Backup Messaging
=========================================================

V2 compliant fallback delivery service for when primary delivery methods fail.
Provides reliable backup messaging with multiple fallback strategies.

V2 Compliance: <300 lines, single responsibility for fallback delivery
Enterprise Ready: High availability, reliability, monitoring, error handling

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

from __future__ import annotations

import logging
import time
from typing import Dict, List, Optional

from ..models import UnifiedMessage, DeliveryMethod, MessageStatus
from ..interfaces import BaseMessageDelivery, IMessageDelivery

logger = logging.getLogger(__name__)

class FallbackDeliveryService(BaseMessageDelivery):
    """V2 compliant fallback delivery service with multiple backup strategies."""

    def __init__(self, primary_delivery: Optional[IMessageDelivery] = None,
                 secondary_delivery: Optional[IMessageDelivery] = None):
        """Initialize fallback delivery service."""
        super().__init__(DeliveryMethod.FALLBACK)
        self.primary_delivery = primary_delivery
        self.secondary_delivery = secondary_delivery
        self.logger = logging.getLogger(__name__)
        
        # Fallback strategies
        self.fallback_strategies = [
            self._try_inbox_delivery,
            self._try_log_delivery,
            self._try_console_delivery
        ]

    def send_message(self, message: UnifiedMessage) -> bool:
        """Send message using fallback delivery strategies."""
        try:
            # Try primary delivery first
            if self.primary_delivery and self.primary_delivery.can_deliver(message):
                try:
                    success = self.primary_delivery.send_message(message)
                    if success:
                        message.status = MessageStatus.SENT
                        message.delivery_method = self.primary_delivery.get_delivery_method()
                        self._record_metrics(message, True)
                        self.logger.info(f"Message sent via primary delivery: {message.recipient}")
                        return True
                except Exception as e:
                    self.logger.warning(f"Primary delivery failed: {e}")

            # Try secondary delivery
            if self.secondary_delivery and self.secondary_delivery.can_deliver(message):
                try:
                    success = self.secondary_delivery.send_message(message)
                    if success:
                        message.status = MessageStatus.SENT
                        message.delivery_method = self.secondary_delivery.get_delivery_method()
                        self._record_metrics(message, True)
                        self.logger.info(f"Message sent via secondary delivery: {message.recipient}")
                        return True
                except Exception as e:
                    self.logger.warning(f"Secondary delivery failed: {e}")

            # Try fallback strategies
            for strategy in self.fallback_strategies:
                try:
                    success = strategy(message)
                    if success:
                        message.status = MessageStatus.SENT
                        message.delivery_method = DeliveryMethod.FALLBACK
                        self._record_metrics(message, True)
                        self.logger.info(f"Message sent via fallback strategy: {message.recipient}")
                        return True
                except Exception as e:
                    self.logger.warning(f"Fallback strategy failed: {e}")

            # All delivery methods failed
            message.status = MessageStatus.FAILED
            self._record_metrics(message, False)
            self.logger.error(f"All delivery methods failed for: {message.recipient}")
            return False

        except Exception as e:
            self.logger.error(f"Error in fallback delivery: {e}")
            message.status = MessageStatus.FAILED
            self._record_metrics(message, False)
            return False

    def can_deliver(self, message: UnifiedMessage) -> bool:
        """Check if fallback delivery can handle this message."""
        # Fallback can always attempt delivery
        return True

    def _try_inbox_delivery(self, message: UnifiedMessage) -> bool:
        """Try inbox delivery as fallback."""
        try:
            from .inbox import get_inbox_delivery_service
            inbox_service = get_inbox_delivery_service()
            return inbox_service.send_message(message)
        except Exception as e:
            self.logger.warning(f"Inbox fallback failed: {e}")
            return False

    def _try_log_delivery(self, message: UnifiedMessage) -> bool:
        """Try log delivery as fallback."""
        try:
            # Create log entry
            log_entry = self._format_log_entry(message)
            
            # Write to log file
            log_file = f"messaging_fallback_{time.strftime('%Y%m%d')}.log"
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
            
            self.logger.info(f"Message logged as fallback: {message.recipient}")
            return True
            
        except Exception as e:
            self.logger.warning(f"Log fallback failed: {e}")
            return False

    def _try_console_delivery(self, message: UnifiedMessage) -> bool:
        """Try console delivery as last resort."""
        try:
            # Format message for console
            console_message = self._format_console_message(message)
            
            # Print to console
            print(console_message)
            
            self.logger.info(f"Message sent to console as fallback: {message.recipient}")
            return True
            
        except Exception as e:
            self.logger.warning(f"Console fallback failed: {e}")
            return False

    def _format_log_entry(self, message: UnifiedMessage) -> str:
        """Format message for log entry."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"[{timestamp}] FALLBACK DELIVERY - {message.message_type.value.upper()}\n"
            f"From: {message.sender}\n"
            f"To: {message.recipient}\n"
            f"Priority: {message.priority.value}\n"
            f"Message ID: {message.message_id}\n"
            f"Content: {message.content}\n"
            f"{'='*50}"
        )

    def _format_console_message(self, message: UnifiedMessage) -> str:
        """Format message for console output."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"\n🚨 FALLBACK MESSAGE DELIVERY - {timestamp}\n"
            f"From: {message.sender}\n"
            f"To: {message.recipient}\n"
            f"Type: {message.message_type.value.upper()}\n"
            f"Priority: {message.priority.value.upper()}\n"
            f"Message ID: {message.message_id}\n"
            f"\nContent:\n{message.content}\n"
            f"\n{'='*60}\n"
        )

    def set_primary_delivery(self, delivery: IMessageDelivery) -> None:
        """Set primary delivery service."""
        self.primary_delivery = delivery
        self.logger.info("Primary delivery service set")

    def set_secondary_delivery(self, delivery: IMessageDelivery) -> None:
        """Set secondary delivery service."""
        self.secondary_delivery = delivery
        self.logger.info("Secondary delivery service set")

    def get_delivery_chain_status(self) -> Dict[str, any]:
        """Get status of delivery chain."""
        return {
            "primary_delivery_available": self.primary_delivery is not None,
            "secondary_delivery_available": self.secondary_delivery is not None,
            "fallback_strategies_count": len(self.fallback_strategies),
            "primary_delivery_method": (
                self.primary_delivery.get_delivery_method().value 
                if self.primary_delivery else None
            ),
            "secondary_delivery_method": (
                self.secondary_delivery.get_delivery_method().value 
                if self.secondary_delivery else None
            ),
            "fallback_delivery_method": self.delivery_method.value
        }

    def get_system_status(self) -> Dict[str, any]:
        """Get fallback delivery system status."""
        try:
            return {
                "delivery_method": self.delivery_method.value,
                "delivery_chain_status": self.get_delivery_chain_status(),
                "fallback_strategies": [
                    "inbox_delivery",
                    "log_delivery", 
                    "console_delivery"
                ],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            self.logger.error(f"Error getting fallback system status: {e}")
            return {
                "error": str(e),
                "delivery_method": self.delivery_method.value,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

# Global instance
fallback_delivery_service = FallbackDeliveryService()

# Public API functions
def get_fallback_delivery_service() -> FallbackDeliveryService:
    """Get the fallback delivery service instance."""
    return fallback_delivery_service

def send_message_via_fallback(message: UnifiedMessage) -> bool:
    """Send message via fallback delivery service."""
    return fallback_delivery_service.send_message(message)

def set_primary_delivery(delivery: IMessageDelivery) -> None:
    """Set primary delivery service for fallback."""
    fallback_delivery_service.set_primary_delivery(delivery)

def set_secondary_delivery(delivery: IMessageDelivery) -> None:
    """Set secondary delivery service for fallback."""
    fallback_delivery_service.set_secondary_delivery(delivery)

def get_delivery_chain_status() -> Dict[str, any]:
    """Get delivery chain status."""
    return fallback_delivery_service.get_delivery_chain_status()

# EXPORTS
__all__ = [
    # Main class
    "FallbackDeliveryService",
    
    # Global instance
    "fallback_delivery_service",
    
    # Public API functions
    "get_fallback_delivery_service",
    "send_message_via_fallback",
    "set_primary_delivery",
    "set_secondary_delivery",
    "get_delivery_chain_status",
]