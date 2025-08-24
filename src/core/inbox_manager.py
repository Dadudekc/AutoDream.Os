class InboxManager:
    """Minimal inbox manager used for testing."""

    def __init__(self):
        self.messages = []

    def get_messages(self, agent_id=None):
        return self.messages
