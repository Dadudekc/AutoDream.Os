from __future__ import annotations
from src.services.messaging.delivery.fallback import send_with_fallback
from src.services.messaging.models import UnifiedMessage, UnifiedMessageType

def test_fallback_inbox(monkeypatch):
    # Force coords None
    monkeypatch.setattr("src.services.messaging.delivery.fallback.get_agent_coordinates", lambda _: None)
    # Capture inbox call
    called = {}
    def fake_inbox(msg): called["ok"]=True; return True
    monkeypatch.setattr("src.services.messaging.delivery.fallback.send_message_inbox", fake_inbox)

    m = UnifiedMessage(content="hi", sender="t", recipient="Agent-1", message_type=UnifiedMessageType.TEXT)
    assert send_with_fallback(m) is True
    assert called.get("ok") is True
