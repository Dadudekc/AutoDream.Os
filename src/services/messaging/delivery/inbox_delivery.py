from __future__ import annotations
from pathlib import Path
from datetime import datetime
import logging
from ..models import UnifiedMessage

logger = logging.getLogger(__name__)


def send_message_inbox(message: UnifiedMessage) -> bool:
    try:
        inbox = Path("agent_workspaces") / message.recipient / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = inbox / f"CONSOLIDATED_MESSAGE_{ts}.md"
        body = f"""# 🚨 CONSOLIDATED MESSAGE - {message.recipient}

**From**: {message.sender}
**To**: {message.recipient}
**Priority**: {message.priority}
**Message ID**: consolidated_{ts}
**Timestamp**: {datetime.now().isoformat()}

---

{message.content}

---

*Message delivered via Consolidated Messaging Service*
"""
        fn.write_text(body, encoding="utf-8")
        logger.info(f"[inbox] wrote {fn}")
        return True
    except Exception as e:
        logger.error(f"[inbox] failed: {e}")
        return False
