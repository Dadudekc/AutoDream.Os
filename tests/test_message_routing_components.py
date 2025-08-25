"""Tests for the refactored message routing components."""

import tempfile
import sys
from pathlib import Path

# Ensure src directory is on path
src_path = Path(__file__).resolve().parents[1] / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from core.message_router import (
    MessageRouter,
    MessageType,
    MessagePriority,
    MessageStatus,
)


def test_send_and_broadcast_messages():
    with tempfile.TemporaryDirectory() as tmp:
        router = MessageRouter(tmp)

        msg_id = router.send_message(
            "Agent-1", "Agent-2", MessageType.STATUS_UPDATE, {"status": "ok"}
        )
        assert msg_id
        assert router.get_message_status(msg_id) == MessageStatus.PENDING

        broadcast_ids = router.broadcast_message(
            "Agent-1", MessageType.COORDINATION, {"action": "sync"}
        )
        assert broadcast_ids
        router.shutdown()
