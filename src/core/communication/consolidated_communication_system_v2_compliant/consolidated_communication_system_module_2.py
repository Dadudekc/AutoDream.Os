    """HTTP-based communication implementation."""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = None
        self._connected = False
    
    async def connect(self) -> bool:
        """Establish HTTP connection."""
        try:
            import aiohttp
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
            self._connected = True
            return True
        except ImportError:
            logging.error("aiohttp not available for HTTP communication")
            return False
    
    async def disconnect(self) -> bool:
        """Close HTTP connection."""
        if self.session:
            await self.session.close()
            self._connected = False
        return True
    
    async def send(self, message: Message) -> bool:
        """Send HTTP message."""
        if not self._connected:
            return False
        try:
            async with self.session.post(
                f"{self.base_url}/message",
                json=message.__dict__
            ) as response:
                return response.status == 200
        except Exception as e:
            logging.error(f"HTTP send error: {e}")
            return False
    
    async def receive(self) -> Optional[Message]:
        """Receive HTTP message."""
        if not self._connected:
            return None
        try:
            async with self.session.get(f"{self.base_url}/message") as response:
                if response.status == 200:
                    data = await response.json()
                    return Message(**data)
        except Exception as e:
            logging.error(f"HTTP receive error: {e}")
        return None


class WebSocketCommunication(CommunicationInterface):