"""Notification channels for the performance alerting system."""

import logging
import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from typing import List, Optional

import aiohttp

from .performance_monitor import PerformanceAlert

logger = logging.getLogger(__name__)


class AlertChannel(ABC):
    """Base class for all alert notification channels."""

    def __init__(self, name: str, enabled: bool = True):
        self.name = name
        self.enabled = enabled

    def should_send_alert(self, alert: PerformanceAlert) -> bool:  # noqa: D401
        """Return ``True`` if the alert should be delivered."""
        return self.enabled

    @abstractmethod
    async def send_alert(self, alert: PerformanceAlert) -> bool:
        """Send the given alert.

        Implementations should return ``True`` if the alert was sent
        successfully.  The default implementations below swallow any
        exceptions and simply log failures to keep the tests lightweight.
        """
        raise NotImplementedError("send_alert must be implemented by subclasses")


class EmailAlertChannel(AlertChannel):
    """Send alerts via SMTP e-mail."""

    def __init__(
        self,
        name: str,
        recipients: List[str],
        smtp_server: str,
        smtp_port: int = 25,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = False,
        sender_email: Optional[str] = None,
    ) -> None:
        super().__init__(name)
        self.recipients = recipients
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.sender_email = sender_email or username or "noreply@example.com"

    async def send_alert(self, alert: PerformanceAlert) -> bool:
        if not self.should_send_alert(alert):
            return False
        body = f"[{alert.severity.value.upper()}] {alert.rule_name}: {alert.message}"
        msg = MIMEText(body)
        msg["From"] = self.sender_email
        msg["To"] = ", ".join(self.recipients)
        msg["Subject"] = f"Performance Alert: {alert.rule_name}"
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                if self.use_tls:
                    server.starttls()
                if self.username and self.password:
                    server.login(self.username, self.password)
                server.sendmail(self.sender_email, self.recipients, msg.as_string())
            return True
        except Exception:  # pragma: no cover - network interactions
            logger.exception("email alert failed")
            return False


class SlackAlertChannel(AlertChannel):
    """Send alerts to a Slack webhook."""

    def __init__(self, name: str, webhook_url: str, channel: str = "#alerts") -> None:
        super().__init__(name)
        self.webhook_url = webhook_url
        self.channel = channel

    async def send_alert(self, alert: PerformanceAlert) -> bool:
        if not self.should_send_alert(alert):
            return False
        payload = {
            "channel": self.channel,
            "text": f"[{alert.severity.value.upper()}] {alert.rule_name}: {alert.message}",
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as resp:
                    return resp.status < 400
        except Exception:  # pragma: no cover - network interactions
            logger.exception("slack alert failed")
            return False


class WebhookAlertChannel(AlertChannel):
    """Send alerts to a generic HTTP webhook."""

    def __init__(self, name: str, webhook_url: str, method: str = "POST") -> None:
        super().__init__(name)
        self.webhook_url = webhook_url
        self.method = method.upper()

    async def send_alert(self, alert: PerformanceAlert) -> bool:
        if not self.should_send_alert(alert):
            return False
        payload = {
            "rule": alert.rule_name,
            "severity": alert.severity.value,
            "message": alert.message,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    self.method, self.webhook_url, json=payload
                ) as resp:
                    return resp.status < 400
        except Exception:  # pragma: no cover - network interactions
            logger.exception("webhook alert failed")
            return False
